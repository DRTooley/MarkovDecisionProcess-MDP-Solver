
import sys
import copy
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class mdpSolution(QWidget):
    def __init__(self, mazeValues, hrzn, gam):
        super(mdpSolution, self).__init__()
        self.setMinimumSize(300,300)
        self.solArr = [[[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]]
        self.maze = mazeValues #Sanatize into int values
        self.horizon = hrzn
        self.gamma = gam
        if self.horizon == -1:
            self.horizon = 1000

        self.solver()

        windowLayout = QVBoxLayout()

        self.mazeValues = QGridLayout()
        self.MazeValueLabels()

        self.Actions = QGridLayout()
        self.valFunc = QGridLayout()
        self.CreateActionAndValGrid()

        lineOne = QFrame()
        lineOne.setFrameShape(QFrame.HLine)
        lineOne.setFrameShadow(QFrame.Raised)
        lineOne.setFrameStyle(4)

        lineTwo = QFrame()
        lineTwo.setFrameShape(QFrame.HLine)
        lineTwo.setFrameShadow(QFrame.Sunken)
        lineTwo.setFrameStyle(4)

        windowLayout.addLayout(self.mazeValues)
        windowLayout.addWidget(lineOne)
        windowLayout.addLayout(self.Actions)
        windowLayout.addWidget(lineTwo)
        windowLayout.addLayout(self.valFunc)

        self.setLayout(windowLayout)
        self.setWindowTitle("Maze Solution")

    def solver(self):
        compass = ['N', 'E', 'S', 'W']
        tempArr = copy.deepcopy(self.solArr[0])
        for iteration in range(self.horizon):

            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    for direction in range(4):
                        x = j
                        y = i
                        xFail = j
                        yFail = i
                        if compass[direction] == 'N':
                            x = j - 1  # Move West
                            xFail = j + 1  # Move East
                        elif compass[direction] == 'E':
                            y = i + 1  # Move South
                            yFail = i - 1  # Move North
                        elif compass[direction] == 'S':
                            x = j + 1  # Move East
                            xFail = j - 1  # Move West
                        elif compass[direction] == 'W':
                            y = i - 1  # Move North
                            yFail = i + 1  # Move South

                        #Check for out of bounds
                        x, y = self.checkBounds(x,y)
                        xFail, yFail = self.checkBounds(xFail, yFail)

                        tempArr[i][j][direction] = 0.7 * (self.maze[y][x] + self.gamma*max(self.solArr[iteration][y][x])) \
                                                           + 0.2 * (self.maze[yFail][xFail] + self.gamma*max(self.solArr[iteration][yFail][xFail])) \
                                                           + 0.1 * (self.maze[i][j] + self.gamma*max(self.solArr[iteration][i][j]))

            self.solArr.append(copy.deepcopy(tempArr))

    def checkBounds(self, x, y):
        if x >= 4:
            x = 3
        elif x <= -1:
            x = 0

        if y >= 4:
            y = 3
        elif y <= -1:
            y = 0

        return x, y



    def MazeValueLabels(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                lb_temp = QLabel(str(self.maze[i][j]))
                lb_temp.setAlignment(Qt.AlignCenter)
                self.mazeValues.addWidget(lb_temp, i, j)



    def CreateActionAndValGrid(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                stepsleft = self.horizon - (i + j)
                if stepsleft < 0:
                    stepsleft = 0
                localMax = max(self.solArr[stepsleft][i][j])

                direction = self.solArr[stepsleft][i][j].index(localMax)
                arrow = '-'
                if self.solArr[stepsleft][i][j][direction] != 0:
                    if direction == 0:
                        arrow = 'West'
                    elif direction == 1:
                        arrow = 'South'
                    elif direction == 2:
                        arrow = 'East'
                    elif direction == 3:
                        arrow = 'North'

                lb_tempDirection= QLabel(arrow)
                lb_tempDirection.setAlignment(Qt.AlignCenter)
                self.Actions.addWidget(lb_tempDirection, i, j)

                lb_tempValue = QLabel(str('%.2f'%(localMax)))
                lb_tempValue.setAlignment(Qt.AlignCenter)
                self.valFunc.addWidget(lb_tempValue, i, j)









class mdpGUI(QWidget):
    def __init__(self):
        super(mdpGUI, self).__init__()

        self.maze = [[0, 50, 0, 50], [0, 50, 0, 100],[0, 50, 0, 50],[0, 50, 200, 50]]

        self.maze_values = [] #Filled in by the QLineTexts inside createMazeWidget

        windowLayout = QHBoxLayout()
        self.inputWidgets = QGridLayout()
        self.createInputWidgets()
        windowLayout.addLayout(self.inputWidgets)
        self.mazeWidget = QGridLayout()
        self.createMazeWidget()
        windowLayout.addLayout(self.mazeWidget)
        self.btn_solve.clicked.connect(self.solve)

        self.setLayout(windowLayout)
        self.setWindowTitle("Markov Decision Process Maze")

    def solve(self):
        #Check for updates made to the maze values
        self.updateMaze()
        self.mySol = mdpSolution(self.maze, self.sb_horizon.value(),self.sb_gamma.value())
        self.mySol.show()

    def updateMaze(self):
        for i in range(len(self.maze_values)):
            for j in range(len(self.maze_values[i])):
                try:
                    self.maze[i][j] = int(self.maze_values[i][j].text())
                except ValueError:
                    print("There is a problem with the input values!!\nThese will be ignored and previous values will be used in their place.")

    def createMazeWidget(self):

        for i in range(len(self.maze)):
            temp_arr = []
            for j in range(len(self.maze[i])):
                te_temp = QLineEdit(str(self.maze[i][j]))
                te_temp.setAlignment(Qt.AlignCenter)
                te_temp.setFixedSize(40, 40)
                self.mazeWidget.addWidget(te_temp, i, j)
                temp_arr.append(te_temp)
            self.maze_values.append(temp_arr)

    def createInputWidgets(self):
        #Add spinbox horizon (num iterations) -1 = infinite, gamma != 1
        lb_horizon = QLabel("Horizon")
        lb_horizon.setAlignment(Qt.AlignRight)
        self.sb_horizon = QSpinBox()
        self.sb_horizon.setRange(-1, 1000)
        self.sb_horizon.setValue(7)
        self.sb_horizon.setSingleStep(1)
        #Add gamma value 0 to 1 (also spinbox?)
        lb_gamma = QLabel("Gamma")
        lb_gamma.setAlignment(Qt.AlignRight)
        self.sb_gamma = QDoubleSpinBox()
        self.sb_gamma.setRange(0, 1)
        self.sb_gamma.setValue(1)
        self.sb_gamma.setSingleStep(0.01)
        #Solve Button
        self.btn_solve = QPushButton("Solve Current Puzzle")


        self.inputWidgets.addWidget(lb_horizon, 0, 0)
        self.inputWidgets.addWidget(self.sb_horizon, 0, 1)
        self.inputWidgets.addWidget(lb_gamma, 1, 0)
        self.inputWidgets.addWidget(self.sb_gamma, 1, 1)
        self.inputWidgets.addWidget(self.btn_solve, 2, 0, 1, 2)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = mdpGUI()
    myWin.show()
    sys.exit(app.exec_())
