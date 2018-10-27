import sys
import random
import BFS
import DFS
import UCS
import IDS
import Astar
import Utilities
import time
import re
from beautifultable import BeautifulTable
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QWidget,QErrorMessage
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
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from time import sleep

perfectState =  [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
costs = []
times = []
nodes_number = []
depth = []
search_methods = ["A* Manhattan Distance", "A* Euclidean Distance", "A* Misplaced Tiles", "BFS", "DFS", "UCS", "IDS"]


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.costPushButtonPlot = QPushButton(self)
        self.costPushButtonPlot.setText("Plot Costs")
        self.costPushButtonPlot.clicked.connect(self.costPushButtonPlot_action)

        self.timesPushButtonPlot = QPushButton(self)
        self.timesPushButtonPlot.setText("Plot Consumed Time")
        self.timesPushButtonPlot.clicked.connect(self.timesPushButtonPlot_action)

        self.nodesPushButtonPlot = QPushButton(self)
        self.nodesPushButtonPlot.setText("Plot Visited Nodes")
        self.nodesPushButtonPlot.clicked.connect(self.nodesPushButtonPlot_action)

        self.depthPushButtonPlot = QPushButton(self)
        self.depthPushButtonPlot.setText("Plot Maximum depth")
        self.depthPushButtonPlot.clicked.connect(self.depthPushButtonPlot_action)

        self.matplotlibWidget = MatplotlibWidget(self)

        self.GUIObject = None
        self.mainLabel = QLabel("Plot the search results.")

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.mainLabel)
        self.layoutVertical.addWidget(self.costPushButtonPlot)
        self.layoutVertical.addWidget(self.timesPushButtonPlot)
        self.layoutVertical.addWidget(self.nodesPushButtonPlot)
        self.layoutVertical.addWidget(self.depthPushButtonPlot)
        self.layoutVertical.addWidget(self.matplotlibWidget)


        #self.threadSample = ThreadSample(self)
        # self.threadSample.newSample.connect(self.on_threadSample_newSample)


    def setGUI(self, _GUIObject):
        self.GUIObject = _GUIObject;

    def display(self, sample):
        
        if self.GUIObject.serachStatus:
            self.mainLabel.setText("Can't plot in middle of searching.")
            return

        if self.GUIObject.numOfSearchs == 0:
            self.mainLabel.setText("No search was done to be plotted.")
            return

        self.mainLabel.setText("Plot the search results.")
        self.matplotlibWidget.axis.clear()
        self.matplotlibWidget.axis.plot(search_methods, sample)
        self.matplotlibWidget.canvas.draw()

    def costPushButtonPlot_action(self):
        self.display(costs)

    def timesPushButtonPlot_action(self):
        self.display(times)

    def nodesPushButtonPlot_action(self):
        self.display(nodes_number)

    def depthPushButtonPlot_action(self):
        self.display(depth)


class ProgressBar(QProgressBar):

    def __init__(self):
        super().__init__()
        self.setRange(0, 1)
        self.setMaximum(1)
        self.setMinimum(0)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._text = None
        self.style = ''' 
                        QProgressBar
                        {
                        border: 2px solid grey;
                        border - radius: 5 px;
                        text - align: center;
                        }
                        '''
        self.setStyleSheet(self.style)

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text


class GUI:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.mainGrid = QVBoxLayout()
        self.cellsGrid = QGridLayout()
        self.cellsInput = [QLineEdit(str(e)) for e in range(0, 9)]
        self.solveButton = QPushButton("Solve")
        self.randomButton = QPushButton("Random")
        self.plotButton = QPushButton("Plot")
        self.slowMotionButton = QPushButton("Slow Motion")
        self.mainLabel = QLabel("Welcome ....")
        self.scroll_style = '''
                       QAbstractScrollArea
                       {
                        background-color: black;
                        color: black;
                        }
                       QWidget#scrollAreaWidgetContents{
                         background-color: black; /*or a colour*/
                         color: black;
                        }
                       '''

        self.solutionTabs = QTabWidget()
        self.progressBar = ProgressBar()
        self.solutionTabsDict = {}
        self.currentSearch = None
        self.solutionTabActive = False
        self.timer = QTimer()
        self.timers = [QTimer() for e in range(100)]
        self.currentTimer = 0
        self.savedCellsInput = []
        self.startTime = None

        # keep track of number of searches performed and if we are currently in one or not
        self.serachStatus = False
        self.numOfSearchs = 0

        # how fast should the search go?
        self.timerInterval = 0
        self.searchYield = 100

    def constructGrid(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.cellsGrid.addWidget(self.cellsInput[i * 3 + j], i + 1, j + 1)
        self.cellsGrid.addWidget(self.solveButton, 5, 2)
        self.cellsGrid.addWidget(self.randomButton, 5, 1)
        self.cellsGrid.addWidget(self.plotButton, 5, 3)
        self.cellsGrid.addWidget(self.slowMotionButton, 6, 2)

    def displayWindow(self):

        self.window.setGeometry(300, 150, 400, 200)
        self.window.setWindowTitle("Solve 8-puzzle")

        # add the header label
        self.mainGrid.addWidget(self.mainLabel)

        # construct the input cells
        self.constructGrid()
        self.mainGrid.addLayout(self.cellsGrid)
        self.mainGrid.addWidget(self.progressBar)

        # add the cells and show the window
        self.window.setLayout(self.mainGrid)
        self.window.show()

        # signals connections
        self.randomButton.clicked.connect(self.randomButtonAction)
        self.solveButton.clicked.connect(self.solveButtonActionFast)
        self.plotButton.clicked.connect(self.plotButtonAction)
        self.slowMotionButton.clicked.connect(self.solveButtonActionSlow)

        sys.exit(self.app.exec_())

    def cellsInputToState(self):
        counter = 0
        state = []
        row = []
        for cell in self.cellsInput:
            row.append(int(cell.text()))
            counter += 1
            if counter == 3:
                state.append(row)
                row = []
                counter = 0
        return state

    def stateToCellsInput(self, state):
        for i in range(3):
            for j in range(3):
                self.cellsInput[i * 3 + j].setText(str(state[i][j]))

    def randomButtonAction(self):
        nums = set()
        for cell in self.cellsInput:
            num = random.randint(0, 8)
            while num in nums:
                num = random.randint(0, 8)
            nums.add(num)
            cell.setText(str(num))
        if Utilities.is_solvable_puzzle(self.cellsInputToState()) == False:
            self.randomButtonAction()

    def setMainLabel(self, message):
        self.mainLabel.setText(message)

    def validInput(self):
        nums = set()
        for cell in self.cellsInput:
            if cell.text() in nums:
                self.error_msg = QErrorMessage()
                self.error_msg.showMessage("Can't insert duplicated entries.")
               # self.setMainLabel("Can't insert duplicated entries.")
                return False
            if not Utilities.represents_int(cell.text()):
                self.error_msg = QErrorMessage()
                self.error_msg.showMessage("Entries must be integers.")
                # self.setMainLabel("Entries must be integers.")
                return False
            nums.add(cell.text())
        if not Utilities.is_solvable_puzzle(self.cellsInputToState()):
            self.error_msg = QErrorMessage()
            self.error_msg.showMessage("This board is un-solvable.")
            # self.setMainLabel("This board is un-solvable.")
            return False
        return True

    def deepCopyListOfCells(self, listOfCells):
        newList = []
        for cell in listOfCells:
            newList.append(QLineEdit(cell.text()))
        return newList

    def assignListOfCells(self, toList, fromList):
        for i in range(len(toList)):
            toList[i].setText(fromList[i].text())

    def plotButtonAction(self):
        self.plot = MyWindow()
        self.plot.setGUI(self)
        self.plot.resize(666,600)
        self.plot.show()

    def solveButtonActionFast(self):
        if self.serachStatus:
            return
        self.timerInterval = 0
        self.searchYield = 100
        return self.solveButtonAction()

    def solveButtonActionSlow(self):
        if self.serachStatus:
            return
        self.timerInterval = 1000
        self.searchYield = 1
        return self.solveButtonAction()

    def solveButtonAction(self):

        self.progressBar.setRange(0, 0)
        if not self.validInput():
            return

        # mark the start of a new search
        self.serachStatus = True

        # show the result tabs if not shown
        if not self.solutionTabActive:
            self.window.setGeometry(300, 150, 400, 600)
            self.mainGrid.addWidget(self.solutionTabs)
            self.solutionTabActive = True

        # clear old data
        self.solutionTabs.clear()
        self.solutionTabsDict = {}

        # set timers
        self.timers = [QTimer() for e in range(100)]
        self.currentTimer = 0

        # save the cell
        self.savedCellsInput = self.deepCopyListOfCells(self.cellsInput)

        self.timers[0].timeout.connect(self.startAStarManh)
        self.timers[1].timeout.connect(self.startAStarEuc)
        self.timers[2].timeout.connect(self.startAStarMisPlacedTiles)
        self.timers[3].timeout.connect(self.startBFS)
        self.timers[4].timeout.connect(self.startDFS)
        self.timers[5].timeout.connect(self.startUCS)
        self.timers[6].timeout.connect(self.startIDS)
        self.timers[7].timeout.connect(self.doneSearch)

        # clear prev search
        costs.clear()
        nodes_number.clear()
        times.clear()
        depth.clear()

        # start the sequence of searches
        self.timers[self.currentTimer].start(0)

    def doneSearch(self):
        self.timers[self.currentTimer].stop()
        self.progressBar.setText("Searching Done")
        self.progressBar.setRange(0, 1)
        self.serachStatus = False
        self.numOfSearchs += 1

    def startBFS(self):
        self.progressBar.setText("BFS searching")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(BFS.search, {'yield_after' : self.searchYield, 'state': self.cellsInputToState(), 'goal_state': perfectState}, "BFS")

    def startDFS(self):
        self.progressBar.setText("DFS searching")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(DFS.search, {'yield_after' : self.searchYield, 'state': self.cellsInputToState(), 'goal_state': perfectState}, "DFS")

    def startUCS(self):
        self.progressBar.setText("UCS searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(UCS.search, {'yield_after' : self.searchYield, 'initial_state': self.cellsInputToState(), 'goal_state': perfectState}, "UCS")

    def startIDS(self):
        self.progressBar.setText("IDS searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(IDS.search, {'yield_after' : self.searchYield,'initial_state': self.cellsInputToState(), 'goal_state': perfectState}, "IDS")

    def startAStarManh(self):
        self.progressBar.setText("A* Manhattan searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search,
                         {'yield_after' : self.searchYield, 'state': self.cellsInputToState(), 'goal_state': perfectState,
                          'heuristic_type': 'Manhattan Distance'},
                         "A* Manhattan Distance")

    def startAStarEuc(self):
        self.progressBar.setText("A* Euclidean Distance searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search, {'yield_after' : self.searchYield, 'state': self.cellsInputToState(), 'goal_state': perfectState,
                                        'heuristic_type': 'Euclidean Distance'}, "A* Euclidean Distance")

    def startAStarMisPlacedTiles(self):
        self.progressBar.setText("A* Euclidean Distance searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search, {'yield_after' : self.searchYield, 'state': self.cellsInputToState(), 'goal_state': perfectState,
                                        'heuristic_type': 'Misplaced Tiles'}, "A* Misplaced Tiles")

    def startSearch(self, searchFunction, functionParameters, searchName):

        self.currentSearch = searchName
        self.addTabInResults(searchName)
        self.steps = searchFunction(**functionParameters)
        # start the search
        self.timer = QTimer()
        self.timer.timeout.connect(self.change)
        self.timer.start(self.timerInterval)

    def addTabInResults(self, title):
        scrollArea = QScrollArea()
        label = QLabel("")
        newfont = QFont("Georgian",10,QFont.Bold)
        label.setFont(newfont)
        scrollArea.setWidget(label)
        self.solutionTabsDict[title] = label
        self.solutionTabs.addTab(scrollArea, title)

    def addLineInTab(self, tabTitle, data):
        self.solutionTabsDict[tabTitle].setText(self.solutionTabsDict[tabTitle].text() + "\n" + data)
        self.solutionTabsDict[tabTitle].adjustSize()

    def stateToAscii(self, state):
        rows = []
        table = BeautifulTable()
        for row in state:
            for cell in row:
                rows.append(str(cell))
            table.append_row(rows)
            rows.clear()

        return table.__str__()

    def change(self):
        step = 1
        for step in self.steps:
            self.stateToCellsInput(step[1])
            # search stop and ready to display info
            if step[0] == 1:
                # finish and stop the timer
                self.timer.stop()

                # print data to GUI
                self.addLineInTab(self.currentSearch, "Total cost is : \t\t" + str(len(step[2])-1) + " moves.\n")
                self.addLineInTab(self.currentSearch, "Total visited nodes is : \t" + str(step[3]+1) + " nodes.\n")
                self.addLineInTab(self.currentSearch, "Max Depth is : \t\t" + str(step[4]) + " levels.\n")
                self.addLineInTab(self.currentSearch,
                                  "Consumed Time is : \t" + str(
                                      round((time.time() - self.startTime), 3)) + " seconds.\n")
                self.addLineInTab(self.currentSearch, "Taken Path is : \n")
                costs.append(len(step[2]))
                nodes_number.append(step[3])
                times.append(round((time.time() - self.startTime), 3))
                depth.append(step[4])
                counter = 0
                flag = 0
                path = ""
                for state in step[2]:
                    if counter == 100: break
                    counter += 1
                    string = self.stateToAscii(state).strip()
                    pat = re.compile(r"([+|123456780])")

                    if flag == 1:
                        right = re.sub("\n", "\n\t\t\t\t", string)
                        temp = re.sub("0", "    ", right)
                        path += pat.sub(" \\1 ",temp)
                        path += str("\n\t\t\t<---\n")
                        flag = 0
                    else:
                        temp = re.sub("0", "    ", string)
                        path += pat.sub(" \\1 ", temp)
                        path += str("\t--->\t")
                        flag = 1
                self.addLineInTab(self.currentSearch, path+"  SOLVED !\n")

                # run the next timer
                self.currentTimer += 1
                self.timers[self.currentTimer].start(0)
            break
        self.window.repaint()


if __name__ == '__main__':
    gui = GUI()
    gui.displayWindow()