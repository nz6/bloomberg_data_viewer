import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class BBGTable(QWidget):

    def __init__(self, datafile, owner):
        super().__init__()
        self.title = 'Bloomberg File Viewer'
        self.left = 200
        self.top = 200
        self.width = 1300
        self.height = 500
        self.datafile = datafile
        self.owner = owner
        self.items = {}
        self.tableInitOK = False
        self.tableWidget = QTableWidget()

    def display(self):
        # Show widget
        self.show()

    def initData(self, dataframe, currentPage, maxPages):
        self.dataframe = dataframe
        self.currentPage = currentPage
        self.maxPages = maxPages

    def initHeader(self, header):
        self.header = header

    def initTopText(self, text):
        self.topText = text

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.populateTable(self.dataframe)

        # table selection change
        #self.tableWidget.doubleClicked.connect(self.on_click)

        self.mainlayout = QVBoxLayout()
        self.toplayout = QHBoxLayout()

        self.topSection = QPlainTextEdit(self.topText, self)
        #self.textEdit = QPlainTextEdit(self.frame)
        self.topSection.setUndoRedoEnabled(False)
        self.topSection.setReadOnly(True)
        self.topSection.setFixedHeight(100)
        #self.topSection.setMaximumBlockCount(1)
        #self.topSection.setPlainText(_fromUtf8(""))
        #self.topSection.setObjectName(_fromUtf8("textEdit"))
        #self.topSection.resize(200, 200)

        self.pageLabel = QLabel("Page " + str(self.currentPage) + "/" + str(self.maxPages))
        self.topLeft = QHBoxLayout()
        self.upArrow = QPushButton('>>', self)
        self.downArrow = QPushButton('<<', self)
        self.topLeft.addWidget(self.pageLabel)
        self.topLeft.addWidget(self.downArrow)
        self.topLeft.addWidget(self.upArrow)

        self.criterion = QLineEdit(self)
        self.button = QPushButton('Filter', self)

        self.mainlayout.addWidget(self.topSection)
        self.toplayout.addLayout(self.topLeft)
        self.toplayout.addWidget(self.criterion)
        self.toplayout.addWidget(self.button)
        self.mainlayout.addLayout(self.toplayout)

        # Add box layout, add table to box layout and add box layout to widget
        #self.layout.addWidget(self.criterion)
        #self.layout.addWidget(self.button)

        self.bottomlayout = QHBoxLayout()
        self.bottomlayout.addWidget(self.tableWidget)


        self.mainlayout.addLayout(self.bottomlayout)
        self.setLayout(self.mainlayout)
        self.upArrow.clicked.connect(self.on_up)
        self.downArrow.clicked.connect(self.on_down)

    def populateTable(self, dataframe):
        self.tableWidget.setRowCount(self.dataframe.__len__())
        self.tableWidget.setColumnCount(self.header.__len__())
        self.tableWidget.setHorizontalHeaderLabels(self.header)
        rowCount = self.tableWidget.rowCount()
        rowcounter = 0

        for row in dataframe:
            columncounter = 0
            if (self.tableInitOK == False):
                for column in row:
                    newitem = QTableWidgetItem(column)
                    self.tableWidget.setItem(rowcounter, columncounter, newitem)
                    #k = str(rowcounter) + "," + str(columncounter)
                    #self.items[k]= newitem
                    columncounter = columncounter + 1
            else:
                for column in row:
                    #k = str(rowcounter) + "," + str(columncounter)
                    #item = self.items[k]
                    item = self.tableWidget.item(rowcounter, columncounter)
                    if(item != None):
                        item.setText(column)
                        columncounter = columncounter + 1
            rowcounter = rowcounter + 1
        #self.tableWidget.move(0,0)
        self.tableInitOK = True

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def on_up(self):
        self.currentPage = self.owner.nextPage()+1
        self.pageLabel.setText("Page " + str(self.currentPage) + "/" + str(self.maxPages))

    @pyqtSlot()
    def on_down(self):
        self.currentPage = self.owner.previousPage()+1
        self.pageLabel.setText("Page " + str(self.currentPage) + "/" + str(self.maxPages))