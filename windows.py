from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog
from mainwindow import Ui_MainWindow
from PyQt5 import QtGui ,QtCore,QtWidgets
from picwin import  Ui_picwin
import sys
import cv2
import numpy as np
from ST_segment import st_segmentation
from stardist.plot import render_label
import matplotlib.pyplot as plt

class Picwin(QMainWindow,Ui_picwin):
    submitted = QtCore.pyqtSignal(np.ndarray)
    close_sub =QtCore.pyqtSignal()
    def __init__(self):
        super(Picwin, self).__init__()
        self.setupUi(self)
    def open(self):
        #imgname 是图片的路径
        imgName,imgtype = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*);;*.jpg;;*.png")
        if imgName == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            print("open success")
            self.jpg = cv2.imread(imgName)
            self.submitted.emit(self.jpg)
            #输出到label ndarry-> qimage -> qpixmap
            self.label.setPixmap(np2qpixmap(self.jpg))
            self.label.adjustSize()
            self.resize(self.jpg.shape[1],self.jpg.shape[0])
            self.show()
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_sub.emit()


class Maskwin(QMainWindow,Ui_picwin):
    def __init__(self ,img):
        super(Maskwin, self).__init__()
        self.setupUi(self)
        self.printimg = img.copy()
        #self.pp=cv2.cvtColor(render_label(self.printimg), cv2.COLOR_RGBA2RGB)
        self.pp = render_label(self.printimg)
        self.pp=(self.pp*255.0).astype(np.uint8)
        self.qimg=QtGui.QImage(self.pp, self.pp.shape[1], self.pp.shape[0], self.pp.shape[1]*4, QtGui.QImage.Format_RGBA8888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.qimg))
        self.label.adjustSize()
        self.resize(self.printimg.shape[1], self.printimg.shape[0])
        self.show()


class Mainwin(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Mainwin, self).__init__()
        self.setupUi(self)
        self.move(300,100)
        self.ispic=False
        self.isgray =False
        self.issegment = False

        self.actionopen.triggered.connect(self.act_open)
        self.actiongray.triggered.connect(self.act_gray)
        self.actionsegment.triggered.connect(self.act_segment)
    def update_img(self,img):
        self.img=img
        self.ispic=True
        self.isgray=False
    def picclose(self):
        self.ispic=False
        self.isgray=False

    def act_open(self):
        self.pw =Picwin()
        self.pw.submitted.connect(self.update_img)
        self.pw.open()
        self.pw.move(self.x(),self.y()+self.height()*1.5)
        self.pw.close_sub.connect(self.picclose)

    def act_gray(self):
        if(self.isgray):
            pass
        elif(not self.ispic):
            QtWidgets.QMessageBox.critical(self, "错误", "请先在 文件->open 导入图片")
        else:
            self.img= cv2.cvtColor(self.img , cv2.COLOR_BGR2GRAY)
            self.pw.label.setPixmap(np2qpixmap(cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)))
           # self.gray_pw.show()
            self.isgray=True

    def act_segment(self):
        if(self.isgray and self.ispic):
            self.mask = st_segmentation(self.img)
            self.issegment = True
            self.maskwin = Maskwin(self.mask)
            self.maskwin.move(self.x() + self.mask.shape[1], self.y() + self.height() * 1.5)
            print("segment success")

        else:
            QtWidgets.QMessageBox.critical(self, "错误", "需要导入灰度图")







#function
def np2qpixmap(frame):
    # rgb ndarry 2 qpixmap
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(frame.dtype)
    img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1]*3 ,QtGui.QImage.Format_BGR888)
    return QtGui.QPixmap.fromImage(img)

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
    n_bits_image  = img_size.width() * img_size.height() * img.depth()
    assert n_bits_buffer == n_bits_image, \
        "size mismatch: {} != {}".format(n_bits_buffer, n_bits_image)

    assert img.depth() == 32, "unexpected image depth: {}".format(img.depth())

    # Note the different width height parameter order!
    arr = np.ndarray(shape  = (img_size.height(), img_size.width(), img.depth()//8),
                     buffer = buffer,
                     dtype  = np.uint8)

    if share_memory:
        return arr
    else:
        return copy.deepcopy(arr)