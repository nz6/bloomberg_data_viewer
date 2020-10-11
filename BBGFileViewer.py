import sys
import math
from PyQt5.QtWidgets import QApplication
from BOFIleFunctions import  BBGFileReader
from BBGViewerTable import BBGTable

class BBGFileViewer:

    def __init__(self, datafile, nbLines=50):
        self.datafile = datafile
        self.maxLines = nbLines
        self.bbgreader = BBGFileReader(datafile)
        self.viewer = BBGTable(datafile, self)
        self.currentPage = 0

    def loadData(self):
        self.dataframe = self.bbgreader.getDataRows(0, self.maxLines)
        self.headerFields = self.bbgreader.getFieldsList()

    def initUI(self):
        self.viewer.initHeader(self.headerFields)
        self.viewer.initTopText(self.bbgreader.topSection)
        nbPages = math.ceil(self.bbgreader.nbLines/self.maxLines)
        self.viewer.initData(self.dataframe, self.currentPage+1, nbPages)

        self.viewer.initUI()

    def show(self):
        self.viewer.display()

    def previousPage(self):
        if(self.currentPage>=1):
            self.currentPage = self.currentPage -1
            min = self.currentPage * self.maxLines
            max = (self.currentPage + 1) * self.maxLines
            self.dataframe = self.bbgreader.getDataRows(min, max)
            self.viewer.populateTable(self.dataframe)
        return self.currentPage

    def nextPage(self):
        self.currentPage = self.currentPage + 1
        min = self.currentPage * self.maxLines
        max = (self.currentPage + 1) * self.maxLines
        self.dataframe = self.bbgreader.getDataRows(min, max)
        self.viewer.populateTable(self.dataframe)
        return self.currentPage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = BBGFileViewer('D:/NeoXam DataHub/Data/import/bloomberg/datafiles/bulk/credit_risk_ext_corp_struc.out')
    #view = BBGFileViewer('D:/Shared Services/NBC - CIB Data Integration/Data/BBG_SYNDLOAN_20180924_dec.out')
    view.loadData()
    view.initUI()
    view.show()
    sys.exit(app.exec_())