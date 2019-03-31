# -*- coding: utf-8 -*-


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Logging(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Logging, self).__init__()
        self.setupUi(self)

    def setupUi(self, Logging):
        Logging.setObjectName("Logging")
        Logging.resize(300, 200)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Logging.sizePolicy().hasHeightForWidth())
        Logging.setSizePolicy(sizePolicy)
        Logging.setMinimumSize(QtCore.QSize(300, 200))
        Logging.setMaximumSize(QtCore.QSize(300, 200))
        self.layoutWidget = QtWidgets.QWidget(Logging)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 261, 111))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.AccountLabel = QtWidgets.QLabel(self.layoutWidget)
        self.AccountLabel.setObjectName("AccountLabel")
        self.gridLayout.addWidget(self.AccountLabel, 0, 0, 1, 1)
        self.AccountEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.AccountEdit.setObjectName("AccountEdit")
        self.gridLayout.addWidget(self.AccountEdit, 0, 1, 1, 1)
        self.PasswordLabel = QtWidgets.QLabel(self.layoutWidget)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.gridLayout.addWidget(self.PasswordLabel, 1, 0, 1, 1)
        self.PasswordEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.PasswordEdit.setText("")
        self.PasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.PasswordEdit.setObjectName("PasswordEdit")
        self.gridLayout.addWidget(self.PasswordEdit, 1, 1, 1, 1)
        self.OKButton = QtWidgets.QPushButton(Logging)
        self.OKButton.setGeometry(QtCore.QRect(50, 160, 89, 25))
        self.OKButton.setObjectName("OKButton")
        self.CancalButton = QtWidgets.QPushButton(Logging)
        self.CancalButton.setGeometry(QtCore.QRect(160, 160, 89, 25))
        self.CancalButton.setObjectName("CancalButton")

        self.retranslateUi(Logging)
        QtCore.QMetaObject.connectSlotsByName(Logging)
        Logging.setTabOrder(self.AccountEdit, self.PasswordEdit)

    def retranslateUi(self, Logging):
        Logging.setWindowTitle(
            QtWidgets.QApplication.translate("Logging", "登录", None, -1))
        self.AccountLabel.setText(
            QtWidgets.QApplication.translate("Logging", "12306账号", None, -1))
        self.PasswordLabel.setText(
            QtWidgets.QApplication.translate("Logging", "12306密码", None, -1))
        self.OKButton.setText(
            QtWidgets.QApplication.translate("Logging", "确定", None, -1))
        self.CancalButton.setText(
            QtWidgets.QApplication.translate("Logging", "取消", None, -1))
