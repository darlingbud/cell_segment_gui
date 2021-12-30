from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from mainwindow import Ui_MainWindow
from picwin import Ui_picwin
from tablewin import Ui_Table
from PyQt5 import QtGui, QtCore, QtWidgets

import sys
import cv2
import numpy as np
from ST_segment import st_segmentation
from stardist.plot import render_label
import matplotlib.pyplot as plt


class Picwin(QMainWindow, Ui_picwin):
    close_sub = QtCore.pyqtSignal()

    def __init__(self, pic):
        super(Picwin, self).__init__()
        self.setupUi(self)
        self.img = pic.copy()
        self.show()

    def flush(self):
        # 将pic显示出来
        qimg = QtGui.QImage(self.img, self.img.shape[1], self.img.shape[0], \
                            self.img.shape[1] * 3, QtGui.QImage.Format_BGR888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(qimg))
        self.label.adjustSize()
        self.resize(self.img.shape[1], self.img.shape[0])
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_sub.emit()


class Tablewin(QMainWindow, Ui_Table):
    def __init__(self, data):
        # data : area, mean_gray, min_gray, max_gray, int_gray
        super(Tablewin, self).__init__()
        self.setupUi(self)
        self.tableWidget.setRowCount(data.shape[0]-1)#344
        self.tableWidget.setColumnCount(data.shape[1])#5
        for i in range(1, data.shape[0]):
            for j in range(0,data.shape[1]):
               item=QtWidgets.QTableWidgetItem(str(data[i][j]))
               #item.setCheckState(0)
               self.tableWidget.setItem(i-1, j, item)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        #self.tableWidget.cellClicked.connect(self.getPosContent)
        self.itemSelect = self.tableWidget.selectionModel()
        self.itemSelect.selectionChanged.connect(self.getPosContent)
        self.show()

    def getPosContent(self,row, col):
        items= self.itemSelect.selectedRows()
        for i in range(0, items.__len__()):
            introw=items[i].row()
            print(introw)



class Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwin, self).__init__()
        self.setupUi(self)
        self.move(150, 100)
        self.isCell = False
        self.isFlu = False
        self.isSegment = False

        # self.actionopen.triggered.connect(self.act_open)
        # self.actionopenFlu.triggered.connect(self.act_openFlu)
        # self.actionsegment.triggered.connect(self.act_segment)
        self.act_open()
        self.act_openFlu()
        self.act_segment()

    def pwCellClose(self):
        self.isCell = False

    def pwFluClose(self):
        self.isFlu = False

    def pwMaskClose(self):
        self.isSegment = False

    def act_open(self):
        # imgName, imgtype = QFileDialog.getOpenFileName(self, "打开细胞图片", "", "All Files(*);;*.jpg;;*.png")
        imgName = "./blue.tif"
        if imgName == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            # cv2_BGR
            self.imgCell = cv2.imread(imgName)
            self.pwCell = Picwin(self.imgCell)

            self.pwCell.flush()
            self.pwCell.move(self.x(), self.y() + self.height() * 1.5)
            self.isCell = True
            self.pwCell.close_sub.connect(self.pwCellClose)

    def act_openFlu(self):
        # imgName, imgtype = QFileDialog.getOpenFileName(self, "打开荧光图像", "", "All Files(*);;*.jpg;;*.png")
        imgName = "./green.tif"
        if imgName == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            # cv2_BGR
            self.imgFlu = cv2.imread(imgName)
            self.pwFlu = Picwin(self.imgFlu)
            self.pwFlu.flush()
            self.pwFlu.move(self.x() + self.imgCell.shape[1], self.y() + self.height() * 1.5)
            self.isFlu = True
            self.pwFlu.close_sub.connect(self.pwFluClose)

    def act_segment(self):
        # if(not self.isCell ):
        #     QtWidgets.QMessageBox.critical(self, "错误", "需要导入细胞图像")
        # elif(not self.isFlu):
        #     QtWidgets.QMessageBox.critical(self, "错误", "需要导入荧光图像")
        # elif(self.imgCell.shape[0]!=self.imgFlu.shape[0] or \
        #      self.imgCell.shape[1]!=self.imgFlu.shape[1]):
        #     QtWidgets.QMessageBox.critical(self, "错误", "需要保证图像大小一致")
        # else:
        ## imgMask 是 1，2，3，4 等mask值
        gray = cv2.cvtColor(self.imgCell, cv2.COLOR_BGR2GRAY)
        self.imgMask = st_segmentation(gray)
        pp = render_label(self.imgMask)
        pp = (pp * 255.0).astype(np.uint8)
        pp = cv2.cvtColor(pp, cv2.COLOR_RGBA2BGR)
        self.datacompute()
        # 创建窗口
        self.pwMask = Picwin(pp)
        self.pwMask.flush()
        self.pwMask.move(self.x() + self.imgCell.shape[1] * 2, self.y() + self.height() * 1.5)
        self.isSegment = True
        self.pwMask.close_sub.connect(self.pwMaskClose)
        self.pwTable = Tablewin(self.data)
        self.pwTable.move(self.x() + self.imgCell.shape[1] * 3, self.y() + self.height() * 1.5)

    #
    # if(self.isgray and self.ispic):
    #     self.mask = st_segmentation(self.img)
    #     self.issegment = True
    #     self.maskwin = Maskwin(self.mask)
    #     self.maskwin.move(self.x() + self.mask.shape[1], self.y() + self.height() * 1.5)
    #     print("segment success")
    #
    # else:
    #     QtWidgets.QMessageBox.critical(self, "错误", "需要导入灰度图")
    #
    def datacompute(self):
        nuc_num = 0
        for i in range(self.imgMask.shape[0]):
            for j in range(self.imgMask.shape[1]):
                nuc_num = max(nuc_num, self.imgMask[i][j])
        print(nuc_num)
        # area, mean_gray, min_gray, max_gray, int_gray
        imgGray = cv2.cvtColor(self.imgFlu, cv2.COLOR_BGR2GRAY)
        self.data = np.zeros((nuc_num + 1, 5), dtype=int)
        for i in range (self.data .shape[0]):
            self.data[i][2]=10000
        for i in range(self.imgMask.shape[0]):
            for j in range(self.imgMask.shape[1]):
                if (self.imgMask[i][j] != 0):
                    id = int(self.imgMask[i][j])
                    gray = int(imgGray[i][j])
                    self.data[id][0] += 1
                    self.data[id][2] = min(self.data[id][2], gray)
                    self.data[id][3] = max(self.data[id][3], gray)
                    self.data[id][4] += gray
        for i in range(1, self.data.shape[0]):
            self.data[i][1] = self.data[i][4] / self.data[i][0]


def qt_image_to_array(img, share_memory=False):
    """ Creates a numpy array from a QImage.

        If share_memory is True, the numpy array and the QImage is shared.
        Be careful: make sure the numpy array is destroyed before the image,
        otherwise the array will point to unreserved memory!!
    """
    assert isinstance(img, QtGui.QImage), "img must be a QtGui.QImage object"
    assert img.format() == QtGui.QImage.Format.Format_RGB32, \
        "img format must be QImage.Format.Format_RGB32, got: {}".format(img.format())

    img_size = img.size()
    buffer = img.constBits()

    # Sanity check
    n_bits_buffer = len(buffer) * 8
    n_bits_image = img_size.width() * img_size.height() * img.depth()
    assert n_bits_buffer == n_bits_image, \
        "size mismatch: {} != {}".format(n_bits_buffer, n_bits_image)

    assert img.depth() == 32, "unexpected image depth: {}".format(img.depth())

    # Note the different width height parameter order!
    arr = np.ndarray(shape=(img_size.height(), img_size.width(), img.depth() // 8),
                     buffer=buffer,
                     dtype=np.uint8)

    if share_memory:
        return arr
    else:
        return copy.deepcopy(arr)
