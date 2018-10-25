import sys
import random
import BFS
import DFS
import UCS
import Astar
import Utilities
import time
import re
from beautifultable import BeautifulTable
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QProgressBar
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
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from time import sleep

perfectState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
costs = []
times = []
nodes_number = []
depth = []
search_methods = ["A* Manhattan Distance", "A* Euclidean Distance", "A* Misplaced Tiles", "BFS", "DFS", "UCS"]


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class ThreadSample(QtCore.QThread):
    newSample = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)

    def run(self):
        randomSample = random.sample(range(0, 10), 10)
        self.newSample.emit(randomSample)

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.pushButtonPlot = QPushButton(self)
        self.pushButtonPlot.setText("Plot")
        self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)

        self.matplotlibWidget = MatplotlibWidget(self)

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonPlot)
        self.layoutVertical.addWidget(self.matplotlibWidget)

        self.threadSample = ThreadSample(self)
        self.threadSample.newSample.connect(self.on_threadSample_newSample)
        self.threadSample.finished.connect(self.on_threadSample_finished)

    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        self.samples = 0
        self.matplotlibWidget.axis.clear()
        self.threadSample.start()

    @QtCore.pyqtSlot(list)
    def on_threadSample_newSample(self, sample):
        self.matplotlibWidget.axis.plot(sample)
        self.matplotlibWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def on_threadSample_finished(self):
        self.samples += 1
        if self.samples <= 2:
            self.threadSample.start()


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
                        border - radius: 5
                        px;
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
        self.cellsInput = [QLineEdit(str(e % 9)) for e in range(1, 10)]
        self.solveButton = QPushButton("Solve")
        self.randomButton = QPushButton("Random")
        self.plotButton = QPushButton("Plot")
        self.mainLabel = QLabel("Welcome ....")
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

    def constructGrid(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.cellsGrid.addWidget(self.cellsInput[i * 3 + j], i + 1, j + 1)
        self.cellsGrid.addWidget(self.solveButton, 5, 2)
        self.cellsGrid.addWidget(self.randomButton, 5, 1)
        self.cellsGrid.addWidget(self.plotButton, 5, 3)

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
        self.solveButton.clicked.connect(self.solveButtonAction)
        self.plotButton.clicked.connect(self.plotButtonAction)

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
                self.setMainLabel("Can't insert duplicated entries.")
                return False
            if Utilities.represents_int(cell.text()) == False:
                self.setMainLabel("Entries must be integers.")
                return False
            nums.add(cell.text())
        if Utilities.is_solvable_puzzle(self.cellsInputToState()) == False:
            self.setMainLabel("This board is un-solvable.")
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
        self.plot.resize(666,333)
        self.plot.show()

    def solveButtonAction(self):

        self.progressBar.setRange(0, 0)
        if not self.validInput:
            return

        # show the result tabs if not shown
        if self.solutionTabActive == False:
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
        self.timers[6].timeout.connect(self.doneSearch)

        # start the sequence of searches
        self.timers[self.currentTimer].start(0)

    def doneSearch(self):
        self.timers[self.currentTimer].stop()
        self.progressBar.setText("Searching Done")
        self.progressBar.setRange(0, 1)

    def startBFS(self):
        self.progressBar.setText("BFS searching")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(BFS.search, {'state': self.cellsInputToState(), 'goal_state': perfectState}, "BFS")

    def startDFS(self):
        self.progressBar.setText("DFS searching")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(DFS.search, {'state': self.cellsInputToState(), 'goal_state': perfectState}, "DFS")

    def startUCS(self):
        self.progressBar.setText("UCS searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(UCS.search, {'initial_state': self.cellsInputToState(), 'goal_state': perfectState}, "UCS")

    # def startIDS(self):
    #     self.setMainLabel("IDS searching .....")
    #     self.assignListOfCells(self.cellsInput, self.savedCellsInput)
    #     self.timers[self.currentTimer].stop()
    #     self.startTime = time.time()
    #     self.startSearch(IDS.search, {'initial_state': self.cellsInputToState(), 'goal_state': perfectState}, "IDS")

    def startAStarManh(self):
        # self.setMainLabel("A* Manhattan searching .....")
        self.progressBar.setText("A* Manhattan searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search,
                         {'state': self.cellsInputToState(), 'goal_state': perfectState,
                          'heuristic_type': 'Manhattan Distance'},
                         "A* Manhattan Distance")

    def startAStarEuc(self):
        # self.setMainLabel("A* Euclidean Distance searching .....")
        self.progressBar.setText("A* Euclidean Distance searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search, {'state': self.cellsInputToState(), 'goal_state': perfectState,
                                        'heuristic_type': 'Euclidean Distance'}, "A* Euclidean Distance")

    def startAStarMisPlacedTiles(self):
        # self.setMainLabel("A* Euclidean Distance searching .....")
        self.progressBar.setText("A* Euclidean Distance searching .....")
        self.assignListOfCells(self.cellsInput, self.savedCellsInput)
        self.timers[self.currentTimer].stop()
        self.startTime = time.time()
        self.startSearch(Astar.search, {'state': self.cellsInputToState(), 'goal_state': perfectState,
                                        'heuristic_type': 'Misplaced Tiles'}, "A* Misplaced Tiles")

    def startSearch(self, searchFunction, functionParameters, searchName):

        self.currentSearch = searchName
        self.addTabInResults(searchName)
        self.steps = searchFunction(**functionParameters)
        # start the search
        self.timer = QTimer()
        self.timer.timeout.connect(self.change)
        self.timer.start(0)

    def addTabInResults(self, title):
        scrollArea = QScrollArea()
        label = QLabel("")
        newfont = QFont("Times", 10, QFont.Bold)
        label.setFont(newfont)
        scrollArea.setWidget(label)
        self.solutionTabsDict[title] = label
        self.solutionTabs.addTab(scrollArea, title)

    def addLineInTab(self, tabTitle, data):
        self.solutionTabsDict[tabTitle].setText(self.solutionTabsDict[tabTitle].text() + "\n " + data)
        self.solutionTabsDict[tabTitle].adjustSize()

    def stateToAscii(self, state):
        rows = []
        table = BeautifulTable()
        for row in state:
            for cell in row:
                if cell != 0:
                    rows.append(" " + str(cell) + " ")
                else:
                    rows.append("   ")
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
                self.addLineInTab(self.currentSearch, "Total cost is : \t\t" + str(len(step[2])) + " move.\n")
                self.addLineInTab(self.currentSearch, "Total visited nodes is : \t" + str(step[3]) + " nodes.\n")
                self.addLineInTab(self.currentSearch,
                                  "Consumed Time is : \t" + str(
                                      round((time.time() - self.startTime), 3)) + " seconds.\n")
                self.addLineInTab(self.currentSearch, "Taken Path is : \n")
                costs.append(len(step[2]))
                nodes_number.append(step[3])
                times.append(round((time.time() - self.startTime), 3))
                counter = 0
                flag = 0
                path = ""
                for state in step[2]:
                    if counter == 100: break
                    counter += 1
                    string = self.stateToAscii(state)
                    pat = re.compile(r"([|])")

                    if flag == 1:
                        right = re.sub("\n", "\n\t\t\t\t", string)
                        path += pat.sub(" \\1 ", right)
                        path += str("\n\t\t\t<---\n")
                        flag = 0
                    else:
                        path += pat.sub(" \\1 ", string)
                        path += str("\t\t--->\t")
                        flag = 1
                self.addLineInTab(self.currentSearch, path)

                # run the next timer
                self.currentTimer += 1
                self.timers[self.currentTimer].start(0)
            break
        self.window.repaint()
        costs.clear()
        nodes_number.clear()
        times.clear()
        depth.clear()


if __name__ == '__main__':
    gui = GUI()
    gui.displayWindow()
