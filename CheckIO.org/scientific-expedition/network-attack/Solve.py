#     Nicola regularly inspects the local networks for security issues. He uses
# a smart and aggressive program which takes control of computers on the
# network.  This program attacks all connected computers simultaneously,
# then uses the captured computers for further attacks. Nicola started the
# virus program in the first computer and took note of the time it took to
# completely capture the network. We can help him improve his process by
# modeling and improving his inspections.  
#     We are given information about the connections in the network and the
# security level for each computer. Security level is the time (in minutes)
# that is required for the virus to capture a machine. Capture time is not
# related to the number of infected computers attacking the machine. Infection
# start from the 0th computer (which is already infected).  Connections in the
# network are undirected. Security levels are not equal to zero.  Information
# about a network is represented as a matrix NxN size, where N is a number of
# computers. If ith computer connected with jth computer, then matrix[i][j] ==
# matrix[j][i] == 1, else 0. Security levels are placed in the main matrix
# diagonal, so matrix[i][i] is the security level for the ith computer.
#
# Input: 
#    Network information as a list of lists with integers.
# Output: 
#    The total time of taken to capture the network as an integer.
# Precondition:
#    3 ? len(matrix) ? 10
#    matrix[0][0] == 0
#    all(len(row) == len(matrix) for row in matrix)
#    all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))
#    all(0 < matrix[i][i] < 10 for i in range(len(matrix)))
#    all(0 ? matrix[i][j] ? 1 for i in range(len(matrix)) for j in range(len(matrix)) if i != j)

# return index of list that found value in list
def SearchList(inList, SearchValue):
    baseInd = 0
    retInd = []
    for I in range(len(inList)):
        try:
            ind = inList.index(SearchValue, baseInd)
            retInd.append(ind)
            baseInd = ind + 1
        except ValueError:
            break
    return retInd

def CheckCracked(ConnectedComp, CrackingCompLevel, CrackedComp, NewCompId):
    # find cracked computer id
    CrackedCompId = SearchList(CrackingCompLevel, 0)
    # Add cracked computer id to New computer id
    [NewCompId.append(ind) for ind in CrackedCompId]
    # Remove cracked computer id from Connected computer id
    [ConnectedComp.remove(ind) for ind in CrackedCompId]
    # Add cracked computer to CrackedComp
    [CrackedComp.append(ind) for ind in CrackedCompId]

def AddConnection(maxtrix, NewCompId, ConnectedComp, CrackingCompLevel):
    for CompId in NewCompId:
        CompToConnectList = matrix[CompId]
        CompToConnectId = SearchList(CompToConnectList, 1)
        [ConnectedComp.append(ind) for ind in CompToConnectId]
        [CrackingCompLevel.append(matrix[ind][ind]) for ind in CompToConnectId]
    NewCompId = []

def capture(matrix):
    # New computer id to connect
    NewCompId         = [0]
    # Current connected computer
    ConnectedComp     = []
    # Store security level for connected but not cracked computer
    CrackingCompLevel = []
    # Store computer id to indecate cracked computer
    CrackedComp       = []

    # Loop for calculate time passed
    TimePassed = 0
    while TimePassed < 2:
        # Check Cracked

        # Add connection to computer
        AddConnection( ConnectedComp, CrackingComp )
        # Increase time passed count
        TimePassed += 1

    return TimePassed


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert capture([[0, 1, 0, 1, 0, 1],
                    [1, 8, 1, 0, 0, 0],
                    [0, 1, 2, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 3, 1],
                    [1, 0, 1, 0, 1, 2]]) == 8, "Base example"
    assert capture([[0, 1, 0, 1, 0, 1],
                    [1, 1, 1, 0, 0, 0],
                    [0, 1, 2, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 3, 1],
                    [1, 0, 1, 0, 1, 2]]) == 4, "Low security"
    assert capture([[0, 1, 1],
                    [1, 9, 1],
                    [1, 1, 9]]) == 9, "Small"

