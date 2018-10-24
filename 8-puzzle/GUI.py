import sys
import random
import BFS
import DFS
import Astar
import Utilities
import copy 
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
from time import sleep

perfectState = [[1,2,3],[4,5,6],[7,8,0]]

class GUI:
   
   def __init__(self):
      self.app = QApplication(sys.argv)
      self.window = QWidget()
      self.mainGrid = QVBoxLayout()
      self.cellsGrid = QGridLayout()
      self.cellsInput = [QLineEdit(str(e%9)) for e in range(1,10)]
      self.solveButton = QPushButton("Solve")
      self.randomButton = QPushButton("Random")
      self.mainLabel = QLabel("Welcome ....")
      self.solutionTabs = QTabWidget()

      self.solutionTabsDict = {}
      self.currentSearch = None
      self.solutionTabActive = False

      self.timer = QTimer()
      self.timers = [QTimer() for e in range(100)]
      self.currentTimer = 0

      self.savedCellsInput = []
      self.startTime = None

   def constructGrid(self):
      for i in range(0,3):
         for j in range(0,3):
            self.cellsGrid.addWidget(self.cellsInput[i*3+j],i+1,j+1)
      self.cellsGrid.addWidget(self.solveButton,5,3)
      self.cellsGrid.addWidget(self.randomButton,5,1)

   def displayWindow(self):
      
      self.window.setGeometry(300,150,400,200)
      self.window.setWindowTitle("Solve 8-puzzle")

      #add the header label
      self.mainGrid.addWidget(self.mainLabel)

      #construct the input cells
      self.constructGrid()
      self.mainGrid.addLayout(self.cellsGrid)

      #add the cells and show the window
      self.window.setLayout(self.mainGrid)
      self.window.show()

      #signals connections
      self.randomButton.clicked.connect(self.randomButtonAction)
      self.solveButton.clicked.connect(self.solveButtonAction)

      sys.exit(self.app.exec_())
	
   def cellsInputToState(self):
      counter = 0;
      state = []
      row = []
      for cell in self.cellsInput:
         row.append(int(cell.text()))
         counter += 1
         if counter == 3:
            state.append(row)
            row = []
            counter = 0;
      return state

   def stateToCellsInput(self, state):
      for i in range (3):
         for j in range (3):
            self.cellsInput[i*3+j].setText(str(state[i][j]))   

   def randomButtonAction(self):
      nums = set()
      for cell in self.cellsInput:
         num = random.randint(0, 8)
         while num in nums:
            num = random.randint(0, 8)
         nums.add(num)
         cell.setText(str(num))
      if Utilities.is_solvable_puzzle(self.cellsInputToState()) == False:
         self.randomButtonAction();

   def setMainLabel(self, message):
      self.mainLabel.setText(message)

   def validInput(self):
      nums = set()
      for cell in self.cellsInput:
         if cell.text() in nums:
            self.setMainLabel("Can't insert duplicated entries.")
            return False
         if Utilities.represents_int(cell.text()) == False:
            self.setMainLabel("Entries must be integers.")
            return False
         nums.add(cell.text())
      if Utilities.is_solvable_puzzle(self.cellsInputToState()) == False:
         self.setMainLabel("This board is un-solvable.")
         return False;
      return True

   def deepCopyListOfCells(self, listOfCells):
      newList = []
      for cell in listOfCells:
         newList.append(QLineEdit(cell.text()))
      return newList

   def assignListOfCells(self, toList, fromList):
      for i in range(len(toList)):
         toList[i].setText(fromList[i].text())

   def solveButtonAction(self):
      
      if not self.validInput():
         return

      #show the result tabs if not shown
      if self.solutionTabActive == False:
         self.window.setGeometry(300,150,400,600)
         self.mainGrid.addWidget(self.solutionTabs)
         self.solutionTabActive = True

      #clear old data
      self.solutionTabs.clear()
      self.solutionTabsDict = {}

      #set timers
      self.timers = [QTimer() for e in range(100)]
      self.currentTimer = 0

      #save the cell
      self.savedCellsInput = self.deepCopyListOfCells(self.cellsInput)

      self.timers[0].timeout.connect(self.startAStarManh)
      self.timers[1].timeout.connect(self.startAStarEuc)
      self.timers[2].timeout.connect(self.startBFS)
      self.timers[3].timeout.connect(self.startDFS)
      self.timers[4].timeout.connect(self.doneSearch)

      #start the sequence of searchs
      self.timers[self.currentTimer].start(0)

   def doneSearch(self):
      self.timers[self.currentTimer].stop()
      self.setMainLabel("Searching done.")

   def startBFS(self):
      self.setMainLabel("BFS searching .....")
      self.assignListOfCells(self.cellsInput, self.savedCellsInput)
      self.timers[self.currentTimer].stop()
      self.startTime = time.time()
      self.startSearch(BFS.search, {'state' : self.cellsInputToState(),'goal_state': perfectState}, "BFS")

   def startDFS(self):
      self.setMainLabel("DFS searching .....")
      self.assignListOfCells(self.cellsInput, self.savedCellsInput)
      self.timers[self.currentTimer].stop()
      self.startTime = time.time()
      self.startSearch(DFS.search, {'state' : self.cellsInputToState(),'goal_state': perfectState}, "DFS")

   def startAStarManh(self):
      self.setMainLabel("A* Manhattan searching .....")
      self.assignListOfCells(self.cellsInput, self.savedCellsInput)
      self.timers[self.currentTimer].stop()
      self.startTime = time.time()
      self.startSearch(Astar.search, {'state' : self.cellsInputToState(),'goal_state': perfectState, 'heuristic_type' : 'Manhattan'}, "A* Manhattan")

   def startAStarEuc(self):
      self.setMainLabel("A* Euclidean Distance searching .....")
      self.assignListOfCells(self.cellsInput, self.savedCellsInput)
      self.timers[self.currentTimer].stop()
      self.startTime = time.time()
      self.startSearch(Astar.search, {'state' : self.cellsInputToState(),'goal_state': perfectState, 'heuristic_type' : 'Euclidean Distance'}, "A* Euclidean Distance")

   def startSearch(self, searchFunction, functionParameters, searchName):

      self.currentSearch = searchName
      self.addTabInResults(searchName)
      self.steps = searchFunction(**functionParameters)
      #start the search
      self.timer = QTimer()
      self.timer.timeout.connect(self.change)
      self.timer.start(0)

   def addTabInResults(self, title):
      scrollArea = QScrollArea()
      label = QLabel("")
      newfont = QFont("Times", 14, QFont.Bold) 
      label.setFont(newfont)
      scrollArea.setWidget(label)
      self.solutionTabsDict[title] = label
      self.solutionTabs.addTab(scrollArea, title)

   def addLineInTab(self, tabTitle, data):
      self.solutionTabsDict[tabTitle].setText(self.solutionTabsDict[tabTitle].text() + "\n " + data)
      self.solutionTabsDict[tabTitle].adjustSize()

   def stateToAscii(self, state):
      lines = []
      for row in state:
         lines.append("----------------")
         textRow = "|"
         for cell in row:
            if cell != 0:
               textRow += "  " + str(cell) + "  |"
            else:
               textRow += "  " + "  " + "  |"
         lines.append(textRow)
      lines.append("----------------")
      textState = ""
      for line in lines:
         textState += "\t" + line + "\n"
      return textState

   def change(self):
      step = 1
      for step in self.steps:
         self.stateToCellsInput(step[1])
         #search stop and ready to diplay info
         if step[0] == 1:
            #finsh and stop the timer
            self.timer.stop()

            #print data to GUI
            self.addLineInTab(self.currentSearch, "Total cost is\t\t:" + str(len(step[2])) + " move.")
            self.addLineInTab(self.currentSearch, "Total visited nodes is\t:" + str(step[3]) + " nodes.")
            self.addLineInTab(self.currentSearch, "Consumed Time is\t:" + str(round((time.time() - self.startTime), 3)) + " seconds.")
            self.addLineInTab(self.currentSearch, "Taken Path is:")

            counter = 0
            path = ""
            for state in step[2]:
               if counter == 100: break
               counter += 1
               path += self.stateToAscii(state)
               path += str("\t         v\n")

            self.addLineInTab(self.currentSearch, path)

            #run the next timer
            self.currentTimer += 1
            self.timers[self.currentTimer].start(0)
         break;
      self.window.repaint()

if __name__ == '__main__':
   gui = GUI()
   gui.displayWindow()
