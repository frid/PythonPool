# GNUMakefile for test

PYTHON=python
PDF2TXT=PYTHONPATH=.. $(PYTHON) ../tools/pdf2txt.py

HTMLS= \
	simple1.html \
	simple2.html \
	dmca.html \
	f1040nr.html \
	i1040nr.html \
	jo.html \
	kampo.html \
	naacl06-shinyama.html \
	nlp2004slides.html

TEXTS= \
	simple1.txt \
	simple2.txt \
	dmca.txt \
	f1040nr.txt \
	i1040nr.txt \
	jo.txt \
	kampo.txt \
	naacl06-shinyama.txt \
	nlp2004slides.txt

SGMLS= \
	simple1.sgml \
	simple2.sgml \
	dmca.sgml \
	f1040nr.sgml \
	i1040nr.sgml \
	jo.sgml \
	kampo.sgml \
	naacl06-shinyama.sgml \
	nlp2004slides.sgml

all:

clean:
	-rm $(HTMLS)
	-rm $(TEXTS)
	-rm $(SGMLS)

test: $(HTMLS) $(TEXTS) $(SGMLS)

.SUFFIXES: .pdf .html .sgml .txt
.pdf.html:
	$(PDF2TXT) -t html $< > $@
.pdf.sgml:
	$(PDF2TXT) -t sgml $< > $@
.pdf.txt:
	$(PDF2TXT) -t text $< > $@
