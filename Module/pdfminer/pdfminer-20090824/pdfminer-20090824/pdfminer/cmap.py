#!/usr/bin/env python
import sys, re, os, os.path
stderr = sys.stderr
from struct import pack, unpack
from pdfminer.utils import choplist, nunpack
from pdfminer.fontmetrics import FONT_METRICS
from pdfminer.latin_enc import ENCODING
from pdfminer.glyphlist import charname2unicode
from pdfminer.psparser import PSException, PSSyntaxError, PSTypeError, PSEOF, \
     PSLiteral, PSKeyword, literal_name, keyword_name, \
     PSStackParser
try:
  import cdb
except ImportError:
  import pdfminer.pycdb as cdb


class CMapError(Exception): pass


##  find_cmap_path
##
def find_cmap_path():
  try:
    return os.environ['CMAP_PATH']
  except KeyError:
    pass
  basedir = os.path.dirname(__file__)
  return os.path.join(basedir, 'CMap')


STRIP_NAME = re.compile(r'[0-9]+')
def name2unicode(name):
  if name in charname2unicode:
    return charname2unicode[name]
  m = STRIP_NAME.search(name)
  if not m: raise KeyError(name)
  return int(m.group(0))


##  CMap
##
class CMap(object):

  debug = 0
  
  def __init__(self):
    self.code2cid = {}
    self.cid2code = {}
    self.attrs = {}
    return

  def __repr__(self):
    return '<CMap: %s>' % self.attrs.get('CMapName')

  def update(self, code2cid=None, cid2code=None):
    if code2cid:
      self.code2cid.update(code2cid)
    if cid2code:
      self.cid2code.update(cid2code)
    return self
    
  def copycmap(self, cmap):
    self.code2cid.update(cmap.getall_code2cid())
    self.cid2code.update(cmap.getall_cid2code())
    return self

  def register_code2cid(self, code, cid):
    if isinstance(code, str) and isinstance(cid, int):
      self.code2cid[code] = cid
    return self

  def register_cid2code(self, cid, code):
    if isinstance(cid, int):
      if isinstance(code, PSLiteral):
        self.cid2code[cid] = pack('>H', name2unicode(code.name))
      elif isinstance(code, str):
        self.cid2code[cid] = code
    return self

  def decode(self, bytes):
    if self.debug:
      print >>stderr, 'decode: %r, %r' % (self, bytes)
    x = ''
    for c in bytes:
      if x:
        if x+c in self.code2cid:
          yield self.code2cid[x+c]
        x = ''
      elif c in self.code2cid:
        yield self.code2cid[c]
      else:
        x = c
    return
  
  def is_vertical(self):
    return self.attrs.get('WMode', 0)

  def tocid(self, code):
    return self.code2cid.get(code)
  def tocode(self, cid):
    return self.cid2code.get(cid)

  def getall_attrs(self):
    return self.attrs.iteritems()
  def getall_code2cid(self):
    return self.code2cid.iteritems()
  def getall_cid2code(self):
    return self.cid2code.iteritems()

  
##  CDBCMap
##
class CDBCMap(CMap):
  
  def __init__(self, cdbname):
    CMap.__init__(self)
    self.cdbname = cdbname
    self.db = cdb.init(cdbname)
    return

  def __repr__(self):
    return '<CDBCMap: %s (%r)>' % (self.db['/CMapName'], self.cdbname)

  def tocid(self, code):
    k = 'c'+code
    if not self.db.has_key(k):
      return None
    return unpack('>L', self.db[k])
  def tocode(self, cid):
    k = 'i'+pack('>L', cid)
    if not self.db.has_key(k):
      return None
    return self.db[k]
  
  def is_vertical(self):
    return (self.db.has_key('/WMode') and
            self.db['/WMode'] == '1')

  def getall(self, c):
    while 1:
      x = self.db.each()
      if not x: break
      (k,v) = x
      if k.startswith(c):
        yield (k[1:], unpack('>L', v)[0])
    return

  def getall_attrs(self):
    while 1:
      x = self.db.each()
      if not x: break
      (k,v) = x
      if k.startswith('/'):
        yield (k[1:], eval(v)[0])
    return
  
  def getall_cid2code(self):
    return self.getall('i')
  def getall_code2cid(self):
    return self.getall('c')

  def decode(self, bytes):
    if self.debug:
      print >>stderr, 'decode: %r, %r' % (self, bytes)
    x = ''
    for c in bytes:
      if x:
        if x+c in self.code2cid:
          yield self.code2cid[x+c]
        elif self.db.has_key('c'+x+c):
          (dest,) = unpack('>L', self.db['c'+x+c])
          self.code2cid[x+c] = dest
          yield dest
        x = ''
      elif c in self.code2cid:
        yield self.code2cid[c]
      elif self.db.has_key('c'+c):
        (dest,) = unpack('>L', self.db['c'+c])
        self.code2cid[c] = dest
        yield dest
      else:
        x = c
    return


##  CMapDB
##
class CMapDB(object):

  class CMapNotFound(CMapError): pass
  
  CMAP_ALIAS = {
    }
  
  debug = 0
  dirname = None
  cdbdirname = None
  cmapdb = {}

  @classmethod
  def initialize(klass, dirname=None, cdbdirname=None):
    if not dirname:
      dirname = find_cmap_path()
    klass.dirname = dirname
    klass.cdbdirname = cdbdirname or dirname
    return

  @classmethod
  def get_cmap(klass, cmapname, strict=True):
    cmapname = klass.CMAP_ALIAS.get(cmapname, cmapname)
    if cmapname in klass.cmapdb:
      cmap = klass.cmapdb[cmapname]
    else:
      fname = os.path.join(klass.dirname, cmapname)
      cdbname = os.path.join(klass.cdbdirname, cmapname+'.cmap.cdb')
      if os.path.exists(cdbname):
        if 1 <= klass.debug:
          print >>stderr, 'Opening: CDBCMap %r...' % cdbname
        cmap = CDBCMap(cdbname)
      elif os.path.exists(fname):
        if 1 <= klass.debug:
          print >>stderr, 'Reading: CMap %r...' % fname
        cmap = CMap()
        fp = file(fname, 'rb')
        CMapParser(cmap, fp).run()
        fp.close()
      elif not strict:
        cmap = CMap() # just create empty cmap
      else:
        raise CMapDB.CMapNotFound(cmapname)
      klass.cmapdb[cmapname] = cmap
    return cmap


##  CMapParser
##
class CMapParser(PSStackParser):

  def __init__(self, cmap, fp):
    PSStackParser.__init__(self, fp)
    self.cmap = cmap
    self.in_cmap = False
    return

  def run(self):
    try:
      self.nextobject()
    except PSEOF:
      pass
    return

  def do_keyword(self, pos, token):
    name = token.name
    if name == 'begincmap':
      self.in_cmap = True
      self.popall()
      return
    elif name == 'endcmap':
      self.in_cmap = False
      return
    if not self.in_cmap: return
    #
    if name == 'def':
      try:
        ((_,k),(_,v)) = self.pop(2)
        self.cmap.attrs[literal_name(k)] = v
      except PSSyntaxError:
        pass
      return
    
    if name == 'usecmap':
      try:
        ((_,cmapname),) = self.pop(1)
        self.cmap.copycmap(CMapDB.get_cmap(literal_name(cmapname)))
      except PSSyntaxError:
        pass
      return
      
    if name == 'begincodespacerange':
      self.popall()
      return
    if name == 'endcodespacerange':
      self.popall()
      return
    
    if name == 'begincidrange':
      self.popall()
      return
    if name == 'endcidrange':
      objs = [ obj for (_,obj) in self.popall() ]
      for (s,e,cid) in choplist(3, objs):
        if (not isinstance(s, str) or not isinstance(e, str) or
            not isinstance(cid, int) or len(s) != len(e)): continue
        sprefix = s[:-4]
        eprefix = e[:-4]
        if sprefix != eprefix: continue
        svar = s[-4:]
        evar = e[-4:]
        s1 = nunpack(svar)
        e1 = nunpack(evar)
        vlen = len(svar)
        #assert s1 <= e1
        for i in xrange(e1-s1+1):
          x = sprefix+pack('>L',s1+i)[-vlen:]
          self.cmap.register_code2cid(x, cid+i)
      return
    
    if name == 'begincidchar':
      self.popall()
      return
    if name == 'endcidchar':
      objs = [ obj for (_,obj) in self.popall() ]
      for (cid,code) in choplist(2, objs):
        if isinstance(code, str) and isinstance(cid, str):
          self.cmap.register_code2cid(code, nunpack(cid))
      return
        
    if name == 'beginbfrange':
      self.popall()
      return
    if name == 'endbfrange':
      objs = [ obj for (_,obj) in self.popall() ]
      for (s,e,code) in choplist(3, objs):
        if (not isinstance(s, str) or not isinstance(e, str) or
            len(s) != len(e)): continue
        s1 = nunpack(s)
        e1 = nunpack(e)
        #assert s1 <= e1
        if isinstance(code, list):
          for i in xrange(e1-s1+1):
            self.cmap.register_cid2code(s1+i, code[i])
        else:
          var = code[-4:]
          base = nunpack(var)
          prefix = code[:-4]
          vlen = len(var)
          for i in xrange(e1-s1+1):
            x = prefix+pack('>L',base+i)[-vlen:]
            self.cmap.register_cid2code(s1+i, x)
      return
        
    if name == 'beginbfchar':
      self.popall()
      return
    if name == 'endbfchar':
      objs = [ obj for (_,obj) in self.popall() ]
      for (cid,code) in choplist(2, objs):
        if isinstance(cid, str) and isinstance(code, str):
          self.cmap.register_cid2code(nunpack(cid), code)
      return
        
    if name == 'beginnotdefrange':
      self.popall()
      return
    if name == 'endnotdefrange':
      self.popall()
      return

    self.push((pos, token))
    return


##  FontMetricsDB
##
class FontMetricsDB(object):
  
  @classmethod
  def get_metrics(klass, fontname):
    return FONT_METRICS[fontname]


##  EncodingDB
##
class EncodingDB(object):
      
  std2unicode = {}
  mac2unicode = {}
  win2unicode = {}
  pdf2unicode = {}
  for (name,std,mac,win,pdf) in ENCODING:
    c = unichr(name2unicode(name))
    if std: std2unicode[std] = c
    if mac: mac2unicode[mac] = c
    if win: win2unicode[win] = c
    if pdf: pdf2unicode[pdf] = c
  
  encodings = {
    'StandardEncoding': std2unicode,
    'MacRomanEncoding': mac2unicode,
    'WinAnsiEncoding': win2unicode,
    'PDFDocEncoding': pdf2unicode,
    }
  
  @classmethod
  def get_encoding(klass, name, diff=None):
    cid2unicode = klass.encodings.get(name, klass.std2unicode)
    if diff:
      cid2unicode = cid2unicode.copy()
      cid = 0
      for x in diff:
        if isinstance(x, int):
          cid = x
        elif isinstance(x, PSLiteral):
          try:
            cid2unicode[cid] = unichr(name2unicode(x.name))
          except KeyError:
            pass
          cid += 1
    return cid2unicode


##  CMap -> CMapCDB conversion
##
def dumpcdb(cmap, cdbfile, verbose=1):
  m = cdb.cdbmake(cdbfile, cdbfile+'.tmp')
  if verbose:
    print >>stderr, 'Writing: %r...' % cdbfile
  for (k,v) in cmap.getall_attrs():
    m.add('/'+k, repr(v))
  for (code,cid) in cmap.getall_code2cid():
    m.add('c'+code, pack('>L',cid))
  for (cid,code) in cmap.getall_cid2code():
    m.add('i'+pack('>L',cid), code)
  m.finish()
  return

def convert_cmap(cmapdir, outputdir, force=False):
  CMapDB.initialize(cmapdir)
  for fname in os.listdir(cmapdir):
    if '.' in fname: continue
    cmapname = os.path.basename(fname)
    cdbname = os.path.join(outputdir, cmapname+'.cmap.cdb')
    if not force and os.path.exists(cdbname):
      print >>stderr, 'Skipping: %r' % cmapname
      continue
    print >>stderr, 'Reading: %r...' % cmapname
    cmap = CMapDB.get_cmap(cmapname)
    dumpcdb(cmap, cdbname)
  return

def main(argv):
  import getopt
  def usage():
    print 'usage: %s [-D outputdir] [-f] cmap_dir' % argv[0]
    return 100
  try:
    (opts, args) = getopt.getopt(argv[1:], 'C:D:f')
  except getopt.GetoptError:
    return usage()
  if args:
    cmapdir = args.pop(0)
  else:
    cmapdir = find_cmap_path()
  outputdir = cmapdir
  force = False
  for (k, v) in opts:
    if k == '-f': force = True
    elif k == '-C': cmapdir = v
    elif k == '-D': outputdir = v
  if not os.path.isdir(cmapdir):
    print >>stderr, 'directory does not exist: %r' % cmapdir
    return 111
  if not os.path.isdir(outputdir):
    print >>stderr, 'directory does not exist: %r' % outputdir
    return 111
  return convert_cmap(cmapdir, outputdir, force=force)

if __name__ == '__main__': sys.exit(main(sys.argv))
