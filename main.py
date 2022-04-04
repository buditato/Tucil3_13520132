import numpy as np
from queue import PriorityQueue
import os.path
import time

class Node:
    def __init__(self, move, cost):
        self.move = move
        self.matrix = np.arange(16).reshape(4,4)
        self.cost = cost

    def readFile(self):
        numList = []
        while True: 
            filename = input("Masukan nama file dengan ekstensinya (ex: test1.txt): ")
            path = "puzzle/" + filename
            if (os.path.isfile(path)):
                break
            else :
                print("File tidak ditemukan! silahkan input ulang")
        file = open(path)
        for i in range(4) :
            numList.extend([int(number) for number in file.readline().split()]) 
        for i in range(len(numList)):
            if numList[i] == 16: # Input blank boleh 0 atau 16, nanti akan diubah menjadi 0
                numList[i] = 0
        self.matrix = np.array(numList).reshape((4,4))

    def locateZero(self):
        result = np.where(self.matrix == 0)
        row = result[0][0]
        col = result[1][0]
        return row, col
        
    def printMatrix(self):
        print("---------------------")
        for arr in self.matrix :
            for angka in arr :
                print("|",end="")
                if angka == 0 :
                    print("   ",end=" ")
                elif angka < 10 :
                    print(" ",angka,end=" ")
                else :
                    print("",angka,end=" ")
            print("|")
            print("---------------------")

    def oneOrZero(self):
        row, col = self.locateZero()
        return (row + col)% 2

    def kurangI(self):
        r, c = self.locateZero()
        tempMatrix = self.matrix.copy()
        tempMatrix[r][c] = 16
        tempMatrix = tempMatrix.flatten()
        total = 0
        arr = [0 for i in range(16)]
        for i in range (16):
            curNumber = tempMatrix[i]
            count = 0
            for j in range(i + 1, len(tempMatrix)):
                if tempMatrix[j] < curNumber:
                    count += 1
            arr[tempMatrix[i] - 1] = count
        return arr

    def syarat(self):
        total = sum(self.kurangI())
        return int(total + self.oneOrZero())
    
    def isSolvable(self):
        if (self.syarat())%2 == 0:
            return True
        else:
            return False

    def countSame(self):
        temp = self.matrix.flatten()
        count = 0
        for i in range(16) :
            if (temp[i] != (i+1) and temp[i] != 0):
                count += 1
        return count

    #MOVEMENT

    def moveUp(self):
        row, col = self.locateZero()
        after = self.matrix.copy()
        after[row-1,col] = self.matrix[row,col]
        after[row,col] = self.matrix[row-1,col]
        return after
    
    def moveDown(self):
        row, col = self.locateZero()
        after = self.matrix.copy()
        after[row+1,col] = self.matrix[row,col]
        after[row,col] = self.matrix[row+1,col]
        return after
    
    def moveLeft(self):
        row, col = self.locateZero()
        after = self.matrix.copy()
        after[row,col-1] = self.matrix[row,col]
        after[row,col] = self.matrix[row,col-1]
        return after
    
    def moveRight(self):
        row, col = self.locateZero()
        after = self.matrix.copy()
        after[row,col+1] = self.matrix[row,col]
        after[row,col] = self.matrix[row,col+1]
        return after

    def __lt__(self, other):
        return False

class BranchAndBound:
    def __init__(self):
        self.checked = []
        self.queue = PriorityQueue()
        self.mapMatrix = {}
        self.root = Node(["-"], 0)
        self.finalState = Node(["-"], 0)
        self.target = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])

    def bAndB(self):
        while True:
            curNode = self.queue.get()[1]
            self.checked.append(curNode)
            row, col = curNode.locateZero()
            curMove = curNode.move
            if np.array_equal(curNode.matrix, self.target):
                self.finalState = curNode
                break

            #MOVE RIGHT
            if(col != 3 and curNode.move[-1] != "left"):
                newNode = Node(curMove + ["right"], len(curNode.move))
                newNode.matrix = curNode.moveRight()
                newNode.cost += newNode.countSame()
                if newNode.matrix.tobytes() not in self.mapMatrix.keys():
                    self.mapMatrix[newNode.matrix.tobytes()] = True
                    self.queue.put((newNode.cost, newNode))
                    if np.array_equal(newNode.matrix, self.target):
                        self.finalState = newNode
                        break
            
            #MOVE DOWN
            if(row != 3 and curNode.move[-1] != "up"):
                newNode = Node(curMove + ["down"], len(curNode.move))
                newNode.matrix = curNode.moveDown()
                newNode.cost += newNode.countSame()
                if newNode.matrix.tobytes() not in self.mapMatrix.keys():
                    self.mapMatrix[newNode.matrix.tobytes()] = True
                    self.queue.put((newNode.cost, newNode))
                    if np.array_equal(newNode.matrix, self.target):
                        self.finalState = newNode
                        break
            
            #MOVE LEFT
            if(col != 0 and curNode.move[-1] != "right"):
                newNode = Node(curMove + ["left"], len(curNode.move))
                newNode.matrix = curNode.moveLeft()
                newNode.cost += newNode.countSame()
                if newNode.matrix.tobytes() not in self.mapMatrix.keys():
                    self.mapMatrix[newNode.matrix.tobytes()] = True
                    self.queue.put((newNode.cost, newNode))
                    if np.array_equal(newNode.matrix, self.target):
                        self.finalState = newNode
                        break
                
            #MOVE UP
            if(row != 0 and curNode.move[-1] != "down"):
                newNode = Node(curMove + ["up"], len(curNode.move))
                newNode.matrix = curNode.moveUp()
                newNode.cost += newNode.countSame()
                if newNode.matrix.tobytes() not in self.mapMatrix.keys():
                    self.mapMatrix[newNode.matrix.tobytes()] = True
                    self.queue.put((newNode.cost, newNode))
                    if np.array_equal(newNode.matrix, self.target):
                        self.finalState = newNode
                        break

    def printPath(self):
        print("Banyaknya simpul yang dibangkitkan   : ", self.queue.qsize() + len(self.checked))
        print("Banyaknya step yang ditempuh         : ", len(self.finalState.move) - 1)
        print()
        temp = self.root
        for i in range(1,len(self.finalState.move)):
            if self.finalState.move[i] == "up":
                print("Up")
                temp.matrix = temp.moveUp()
            elif self.finalState.move[i] == "down":
                print("Down")
                temp.matrix = temp.moveDown()
            elif self.finalState.move[i] == "left":
                print("Left")
                temp.matrix = temp.moveLeft()
            elif self.finalState.move[i] == "right":
                print("Right")
                temp.matrix = temp.moveRight()
            temp.printMatrix()
            print()

    def solver(self):
        self.root.printMatrix()
        kurangi = self.root.kurangI()
        for i in range(16):
            print("Kurang(" + str(i+1)+ ")"+ " = " + str(kurangi[i]))
        print("syarat = ", str(self.root.syarat()))
        if (self.root.isSolvable()):
            self.root.cost = self.root.countSame()
            self.queue.put((self.root.cost, self.root))
            self.mapMatrix[self.root.matrix.tobytes()] = True
            self.bAndB()
        else:
            print("Puzzle tidak solvable")

puzzle = BranchAndBound()
puzzle.root.readFile()
waktuawal = time.time()
puzzle.solver()
waktuakhir = time.time()
if puzzle.root.isSolvable():
    puzzle.printPath()
print("Waktu eksekusi   :", "%.4f" %(waktuakhir-waktuawal), "sekon")