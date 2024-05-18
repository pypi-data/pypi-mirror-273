from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import sys  # We need sys so that we can pass argv to QApplication
import json

__version__ = "1.000"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.filename = QFileDialog.getOpenFileName(self, 'Open Requester File', './logfiles', 'Logs (*.log *.json)')
        print("FileName:", self.filename[0])
        self.graphSizeX = 600
        self.graphSizeY = 600
        logfile = open(self.filename[0],"r")
        dataLines = logfile.readlines()
        dataLines = dataLines[4:]
        data = []
        for dataLine in dataLines:
            print(dataLine)
            data.append(json.loads(dataLine))
        logfile.close()
        self.setGeometry(10,10,self.graphSizeX,self.graphSizeY)
        self.initGUI()
        self.show()
        self.processData(data)

    def processData(self, data):
        self.plotX = []
        self.plotY = []
        for k in range(len(data)):
            if "RANGE_INFO" in data[k]:
                self.plotX.append(k)
                self.plotY.append(data[k]['RANGE_INFO']['precisionRangeM'])
                # self.plotY.append(data[k]['RANGE_INFO']['msgId'])
            self.rangeData.setData(self.plotX, self.plotY)
        self.dataWindow.enableAutoRange(axis = 'y', enable = True)
        self.dataWindow.enableAutoRange(axis = 'x', enable = True)
        print("\nExample JSON message:\n", data[100])
        print("\nRecords in logfile:", len(data))

    def closeItDown(self):
        print("\nLater!\n")

    def initGUI(self):
        # Range Chart
        rPen = pg.mkPen(width = 4, color=(255,0,0))
        self.dataWindow = pg.PlotWidget(self)
        self.dataWindow.setBackground('w')
        self.dataWindow.setGeometry(5,5,self.graphSizeX-5,self.graphSizeY-5)
        self.dataWindow.showGrid(x=True, y=True)
        self.plotX = []
        self.plotY = []
        self.rangeData = self.dataWindow.plot(self.plotX, self.plotY, pen=rPen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
