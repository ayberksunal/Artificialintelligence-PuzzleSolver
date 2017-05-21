import heapq
from heapq import heappush, heappop
import time
import random




####################
#   GOAL STATE     #
#                  #
#  -------------   #
#  | 1 | 2 | 3 |   #
#  -------------   #
#  | 4 | 5 | 6 |   #
#  -------------   #
#  | 7 | 8 |   |   #
#  -------------   #
####################

goalState=[1, 2, 3,
           4, 5, 6,
           7, 8, 0]

initialState1=[1, 7, 4,
               6, 8, 3,
               2, 5, 0]

initialState2=[0, 1, 3,
               4, 2, 5,
               7, 8, 6,
               ]

initialState3=[8, 1, 3,
               4, 0, 2,
               7, 6, 5]

initialState4=[0, 2, 3,
               1, 4, 5,
               7, 8, 6]

goDown=[0, 1, 2, 3, 4, 5]
goUp = [3, 4, 5, 6, 7, 8]
goLeft = [1, 2, 4, 5, 7, 8]
goRight = [0, 1, 3, 4, 6, 7]



class Solver:
    def __init__(self, initial_state=None):
        self.initial_state = State(initial_state)
        self.goal = range(1, 9)

    '''
    reCreatePath Function
    Input = an object and goal state
    Purpose = Creating an array and takes all valid steps from tail to head.
    '''
    def reCreatePath(self, end):
        path = [end]
        state = end.parent
        while state.parent:
            path.append(state)
            state = state.parent
        return path



    '''
    A* pseudocode
1	Create a node containing the goal state node_goal
2	Create a node containing the start state node_start
3	Put node_start on the open list
4	while the OPEN list is not empty
5	{
6	Get the node off the open list with the lowest f and call it node_current
7	if node_current is the same state as node_goal we have found the solution; break from the while loop
8	    Generate each state node_successor that can come after node_current
9	    for each node_successor of node_current
10	    {
11	        Set the cost of node_successor to be the cost of node_current plus the cost to get to node_successor from node_current
12	        find node_successor on the OPEN list
13	        if node_successor is on the OPEN list but the existing one is as good or better then discard this successor and continue
14	        if node_successor is on the CLOSED list but the existing one is as good or better then discard this successor and continue
15	        Remove occurences of node_successor from OPEN and CLOSED
16	        Set the parent of node_successor to node_current
17	        Set h to be the estimated distance to node_goal (Using the heuristic function)
18	         Add node_successor to the OPEN list
19	    }
20	    Add node_current to the CLOSED list
21	}

kok kuyruga atilir
toplam uzakligi en az olan dugum bulunur ve kuyruktan cikartilir ve dongu olusturmayan alt dugumler kugruga eklenir
hedefe ulasana kadar toplam uzakligi en az olan dugumun secilmesi ve alt dugumlerini olusturulmasina devam edilir

'''

    '''
       astar function
       Input = An object
       Purpose = Search Algorithm
       '''
    def astar(self):
        stepCounter=1
        # The open and closed sets
        moves = 0
        open = PriorityQueue()
        closed = set()
        # Add the starting point to the open set
        open.add(self.initial_state)
        print '--------------------\n'
        print 'Trying to solve... '
        print open.firstElement()
        print '--------------------\n'
        startTime = time.time()
        while open:
            # Current point is the starting point
            current = open.pop()
            #check the arrays equal or not
            if current.values[:-1] == self.goal:
                #starts to calc. the time
                endTime = time.time()
                print u'\u2713' + ' There Is A Solution'
                path = self.reCreatePath(current)
                for state in reversed(path):
                    print 'step: %i'%(stepCounter)
                    #count 1 to show the steps
                    stepCounter+=1
                    print state
                    print
                print 'Solved with %d moves' % len(path)
                print 'Found solution within %2.f seconds' % float(endTime - startTime)
                break
            moves += 1
            #finds the possible moves of blank tile
            for state in current.possibleMoves(moves):
                if state not in closed:
                    open.add(state)
            # Add it to the closed set
            closed.add(current)
        else:
            print ' X There Is No Solution!!'


class State:
    def __init__(self, values, moves=0, parent=None):
        self.goal = [0,1,2,3,4,5,6,7,8]
        self.values = values
        self.moves = moves
        self.parent = parent


    '''
    PossibleMoves Function
    Initial = An object and moves
    Purpose = finding the blank tile and reach possible swapping
    '''
    def possibleMoves(self, moves):
        locOfBlank = self.values.index(0)
        #goDown
        if locOfBlank in goDown:
            array = self.values[:]
            temp4=array[locOfBlank]
            array[locOfBlank]=array[locOfBlank+3]
            array[locOfBlank+3]=temp4
            yield State(array, moves, self)
        #goUp
        if locOfBlank in goUp:
            array = self.values[:]
            temp=array[locOfBlank]
            array[locOfBlank]=array[locOfBlank-3]
            array[locOfBlank-3]=temp
            yield State(array, moves, self)
        #goRight
        if locOfBlank in goRight:
            array = self.values[:]
            temp3=array[locOfBlank]
            array[locOfBlank]=array[locOfBlank+1]
            array[locOfBlank+1]=temp3
            yield State(array, moves, self)
        #goLeft
        if locOfBlank in goLeft:
            array = self.values[:]
            temp2=array[locOfBlank]
            array[locOfBlank]=array[locOfBlank-1]
            array[locOfBlank-1]=temp2
            yield State(array, moves, self)


    def score(self):
        #heuristic function + cost
        return self.h() + self.g()
    '''
    H Function
    Input = An object
    Purpose = Using the f, g and h values the A* algorithm will
    be directed, subject to conditions we will look at further on,
    towards the goal and will find it in the shortest route possible.

    g= baslancica olan uzakligi
    h= hedefe olan tahmini uzaklik

    '''
    def h(self):
        sum=0
        for i in xrange(8):
            if self.values[i] != self.goal[i]:
                sum = sum + 1
            else:
                sum = sum + 0
        return sum


    '''
    G function
    Input = An object
    Purpose = is the sum of all the costs it took to get here
    '''
    def g(self):
        return self.moves
    #tum carsilastirma operatorlari
    def __cmp__(self, other):
        return self.values == other.values

    def __eq__(self, other):
        return self.__cmp__(other)

    def __hash__(self):
        return hash(str(self.values))

    #Kucuk operatorunun davranisini belirler
    def __lt__(self, other):
        return self.score() < other.score()

    def __str__(self):
        return ('\n' \
           '+---+---+---+\n' \
           '| %s | %s | %s |\n' \
           '+---+---+---+\n' \
           '| %s | %s | %s |\n' \
           '+---+---+---+\n' \
           '| %s | %s | %s |\n' \
           '+---+---+---+\n' \
               % (str(self.values[:1]), str(self.values[1:2]), str(self.values[2:3]), str(self.values[3:4]), str(self.values[4:5]), str(self.values[5:6]),
                  str(self.values[6:7]),str(self.values[7:8]),str(self.values[8:9]))).replace('0',' ').replace('[','').replace(']','')



class PriorityQueue:
    def __init__(self):
        self.pq = []


    def __len__(self):
        return len(self.pq)

    def pop(self):
        return heappop(self.pq)

    def add(self, item):
        heappush(self.pq, item)

    def firstElement(self):
        return self.pq[0]

    # Remove the item from the open set
    def remove(self, item):
        value = self.pq.remove(item)
        heapq.heapify(self.pq)
        return value is not None



'''
TwoDimensionalToOneDimensional funtion
Input = A two dimensional array
Purpose = Converting a two

'''

def TwoDimensionalToOneDimensional(TwoDimensional):
    OneDimensional = list()
    for row in range(len(TwoDimensional)):
        for col in range(len(TwoDimensional)):
            OneDimensional.append(TwoDimensional[row][col])
    return OneDimensional

'''
IsItSolvable function
Input = Array of 8 puzzle problem
Purpose = Controlling the sum of the numbers to check whether it is acceptable or not.
'''
def IsItSolvable(listOfNumber):
    sum = 0
    for row in range(len(listOfNumber)):
        sum = sum + listOfNumber[row]
    if sum == 36:
        return True
    else:
        return False



'''
autoArrayCreator Function
Input=None
Purpose=Creating a new array with wanted number series.
'''
def autoArrayCreator():
    list=[1,2,3,4,5,6,7,8,0]
    newList=[]
    for i in range(len(list)):
        selectedItem=random.choice(list)
        newList.append(selectedItem)
        list.remove(selectedItem)
    return newList


print "Enter \"1\" to use a default puzzle, enter \"2\" to write your own puzzle or enter \"3\" to use a random puzzle"

wanted = int(raw_input())
if wanted == 1:
    solver = Solver(initialState4)
    solver.astar()


elif wanted == 2:
    print "Enter elements for Puzzle."
    print "!!! Use \"0\" for blank.\n"
    listOfAllNumber = []
    for i in range(3):
        listOfARow = []
        for j in range(3):
            print "Enter elements for row %d" % (i + 1)
            listOfARow.append(input("Element {0}:{1}: ".format(i, j)))
        listOfAllNumber.append(listOfARow)
    listOfAllNumber=TwoDimensionalToOneDimensional(listOfAllNumber)

    if IsItSolvable(listOfAllNumber)==True and listOfAllNumber!=goalState:
        solver2 = Solver(listOfAllNumber)
        solver2.astar()
    else:
        print '\nWrong number set for 8puzzle Game.'

elif wanted==3:
    createdArray=autoArrayCreator()
    solver3 = Solver(createdArray)
    solver3.astar()

else:
    print 'Not determined number. Please try again...'
