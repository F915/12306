# -*- coding: utf-8 -*-


import sqlite3
import sys
import time

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QFile, QThread
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox

from Logging_UI import Ui_Logging


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.search_info = list()
        self.setupUi(self)

        self.refreshTrainInfo = RefreshTable()
        self.OrderState = RefreshOrderState()
        self.setSignalandSlot()

    def showAllTrainInfo(self):
        self.showAllHiddenRow()
        self.TrainInfoTableWidget.setSortingEnabled(False)
        self.TrainInfoTableWidget.clearContents()
        self.TrainInfoTableWidget.setRowCount(0)
        row_number = 0

        data_base = sqlite3.connect('Tickets.db')

        try:
            search_result = data_base.execute(
                '''SELECT * FROM '%s' ''' % self.search_info[0].strip())
            for row in search_result:
                self.TrainInfoTableWidget.setRowCount(row_number+1)
                column_current_number = 0
                for column in row:
                    # print(column)
                    current_item = QtWidgets.QTableWidgetItem(column)
                    current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.TrainInfoTableWidget.setItem(
                        row_number, column_current_number, current_item)
                    column_current_number = column_current_number + 1
                row_number = row_number+1
        except:
            pass
        data_base.close()
        self.TrainInfoTableWidget.setSortingEnabled(True)
        self.resetSelectTicket()

    def resetSelectTicket(self):
        row_number = self.TrainInfoTableWidget.rowCount()
        for i in range(row_number):
            self.TrainInfoTableWidget.setRowHidden(i, False)

        # 发车时间重置
        self.OneDepartTimeCheckBox.setChecked(True)
        self.TwoDepartTimeCheckBox.setChecked(True)
        self.ThreeDepartTimeCheckBox.setChecked(True)
        self.FourDepartTimeCheckBox.setChecked(True)

        # 到达时间重置
        self.OneArriveTimeCheckBox.setChecked(True)
        self.TwoArriveTimeCheckBox.setChecked(True)
        self.ThreeArriveTimeCheckBox.setChecked(True)
        self.FourArriveTimeCheckBox.setChecked(True)

        # 座席类型重置
        self.ShangwuzuoCheckBox.setChecked(True)
        self.YidengzuoCheckBox.setChecked(True)
        self.ErdengzuoCheckBox.setChecked(True)
        self.DongwoCheckBox.setChecked(True)
        self.WuzuoCheckBox.setChecked(True)
        self.GaojiruanwoCheckBox.setChecked(True)
        self.RuanwoCheckBox.setChecked(True)
        self.YingwoCheckBox.setChecked(True)
        self.RuanzuoCheckBox.setChecked(True)
        self.YingzuoCheckBox.setChecked(True)

        # 重置出发车站
        self.resetStartStationTable()

        # 重置到达车站
        self.resetEndStationTable()

        # 重置列车类型
        self.ExpressCheckBox.setChecked(True)
        self.OrdinaryCheckBox.setChecked(True)

        # 重置途经站点
        self.resetDepartTable()

        # 重置座席价格
        self.resetSeatPrice()

        # 重置选择座席
        self.resetChooseSeat()

    def resetDepartTable(self):

        self.DepartStationTableWidget.clearContents()
        self.DepartStationTableWidget.setRowCount(0)

    def resetSeatPrice(self):
        self.PriceTableWidget.clearContents()
        row_number = self.PriceTableWidget.rowCount()
        for row in range(row_number):
            self.PriceTableWidget.setRowHidden(row, False)

    def resetChooseSeat(self):
        self.SeatTableWidget.clearContents()
        self.SeatTableWidget.setRowCount(0)

    def resetStartStationTable(self):

        self.StartStationTableWidget.clearContents()
        self.StartStationTableWidget.setRowCount(0)

        data_base = sqlite3.connect('Tickets.db')
        row_number = 0
        start_station_info = data_base.execute(
            '''SELECT DISTINCT STARTSTATION FROM '%s' ''' % self.search_info[0].strip())
        for row in start_station_info:
            for column in row:
                self.StartStationTableWidget.setRowCount(row_number+1)
                current_item = QtWidgets.QTableWidgetItem(column)
                current_item.setCheckState(QtCore.Qt.Checked)
                current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.StartStationTableWidget.setItem(
                    row_number, 0, current_item)
                row_number = row_number+1
        data_base.close()

    def resetEndStationTable(self):
        self.EndStationTableWidget.clearContents()
        self.EndStationTableWidget.setRowCount(0)

        data_base = sqlite3.connect('Tickets.db')
        row_number = 0
        end_station_info = data_base.execute(
            '''SELECT DISTINCT ENDSTATION FROM '%s' ''' % self.search_info[0].strip())
        for row in end_station_info:
            for column in row:
                self.EndStationTableWidget.setRowCount(row_number+1)
                current_item = QtWidgets.QTableWidgetItem(column)
                current_item.setCheckState(QtCore.Qt.Checked)
                current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.EndStationTableWidget.setItem(
                    row_number, 0, current_item)
                row_number = row_number+1
        data_base.close()

    def clearStartStationTable(self):

        self.StartStationTableWidget.clearContents()
        self.StartStationTableWidget.setRowCount(0)

    def clearEndStationTable(self):
        self.EndStationTableWidget.clearContents()
        self.EndStationTableWidget.setRowCount(0)

    def clearSelectTicket(self):
        row_number = self.TrainInfoTableWidget.rowCount()
        for i in range(row_number):
            self.TrainInfoTableWidget.setRowHidden(i, False)

        # 发车时间重置
        self.OneDepartTimeCheckBox.setChecked(True)
        self.TwoDepartTimeCheckBox.setChecked(True)
        self.ThreeDepartTimeCheckBox.setChecked(True)
        self.FourDepartTimeCheckBox.setChecked(True)

        # 到达时间重置
        self.OneArriveTimeCheckBox.setChecked(True)
        self.TwoArriveTimeCheckBox.setChecked(True)
        self.ThreeArriveTimeCheckBox.setChecked(True)
        self.FourArriveTimeCheckBox.setChecked(True)

        # 座席类型重置
        self.ShangwuzuoCheckBox.setChecked(True)
        self.YidengzuoCheckBox.setChecked(True)
        self.ErdengzuoCheckBox.setChecked(True)
        self.DongwoCheckBox.setChecked(True)
        self.WuzuoCheckBox.setChecked(True)
        self.GaojiruanwoCheckBox.setChecked(True)
        self.RuanwoCheckBox.setChecked(True)
        self.YingwoCheckBox.setChecked(True)
        self.RuanzuoCheckBox.setChecked(True)
        self.YingzuoCheckBox.setChecked(True)

        # 重置出发车站
        self.clearStartStationTable()

        # 重置到达车站
        self.clearEndStationTable()

        # 重置列车类型
        self.ExpressCheckBox.setChecked(True)
        self.OrdinaryCheckBox.setChecked(True)

        # 重置途经站点
        self.resetDepartTable()

        # 重置座席价格
        self.resetSeatPrice()

        # 重置选择座席
        self.resetChooseSeat()

    def showSearchError(self):
        QMessageBox.information(self, '查询错误', '查询失败,请检查查询条件')
        self.showAllHiddenRow()
        self.TrainInfoTableWidget.setSortingEnabled(False)
        self.TrainInfoTableWidget.clearContents()
        self.TrainInfoTableWidget.setRowCount(0)
        self.TrainInfoTableWidget.setSortingEnabled(True)
        self.clearSelectTicket()
        # #print(dialog)

    def searchTicket(self):
        # ##print(int(time.time()))
        # ##print(self.StartStationEdit.text())
        # ##print(self.EndStationEdit.text())
        # ##print(self.DepartDateEdit.textFromDateTime(
            # self.DepartDateEdit.dateTime()))
        # ##print(int(self.StudentTicketRadioButton.isChecked()))

        self.refreshTrainInfo.start()

        self.search_info = [str(int(time.time()))+'\n', self.StartStationEdit.text()+'\n', self.EndStationEdit.text()+'\n',
                            self.DepartDateEdit.textFromDateTime(self.DepartDateEdit.dateTime())+'\n', str(int(self.StudentTicketRadioButton.isChecked()))+'\n']
        # ##print(self.search_info)

        ticket_info_file = open('TicketRequest.info', 'w')
        if ticket_info_file.writable():
            ticket_info_file.writelines(self.search_info)
            # print('openfile Error')

        ticket_info_file.close()

    def selectTicket(self):

        self.showAllHiddenRow()

        self.selectStartTime()
        self.selectEndTime()

        self.selectSeatType()

        self.selectStartStation()
        self.selectEndStation()

        self.selectTrainType()

    def showAllHiddenRow(self):
        for row in range(self.TrainInfoTableWidget.rowCount()):
            self.TrainInfoTableWidget.setRowHidden(row, False)

    def selectStartTime(self):
        row_number = self.TrainInfoTableWidget.rowCount()
        column_number = 3

        for row in range(row_number):
            if self.TrainInfoTableWidget.isRowHidden(row) == True:
                continue
            else:
                if self.OneDepartTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '00:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '06:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.TwoDepartTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '06:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '12:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.ThreeDepartTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '12:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '18:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.FourDepartTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '18:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '24:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

    def selectEndTime(self):
        row_number = self.TrainInfoTableWidget.rowCount()
        column_number = 4

        for row in range(row_number):
            if self.TrainInfoTableWidget.isRowHidden(row) == True:
                continue
            else:
                if self.OneArriveTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '00:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '06:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.TwoArriveTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '06:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '12:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.ThreeArriveTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '12:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '18:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

                if self.FourArriveTimeCheckBox.isChecked() == False:
                    if self.TrainInfoTableWidget.item(row, column_number).text() >= '18:00' and self.TrainInfoTableWidget.item(row, column_number).text() < '24:00':
                        self.TrainInfoTableWidget.setRowHidden(row, True)

    def selectSeatType(self):
        row_number = self.TrainInfoTableWidget.rowCount()

        for row in range(row_number):
            if self.TrainInfoTableWidget.isRowHidden(row) == True:
                continue
            else:
                try:
                    if self.ShangwuzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 6).text() != '' and self.TrainInfoTableWidget.item(row, 6).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 6).text())
                            continue
                    if self.YidengzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 7).text() != '' and self.TrainInfoTableWidget.item(row, 7).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 7).text())
                            continue
                    if self.ErdengzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 8).text() != '' and self.TrainInfoTableWidget.item(row, 8).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 8).text())
                            continue
                    if self.DongwoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 9).text() != '' and self.TrainInfoTableWidget.item(row, 9).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 9).text())
                            continue
                    if self.GaojiruanwoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 10).text() != '' and self.TrainInfoTableWidget.item(row, 10).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 10).text())
                            continue
                    if self.RuanwoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 11).text() != '' and self.TrainInfoTableWidget.item(row, 11).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 11).text())
                            continue
                    if self.YingwoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 12).text() != '' and self.TrainInfoTableWidget.item(row, 12).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 12).text())
                            continue
                    if self.RuanzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 13).text() != '' and self.TrainInfoTableWidget.item(row, 13).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 13).text())
                            continue
                    if self.YingzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 14).text() != '' and self.TrainInfoTableWidget.item(row, 14).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 14).text())
                            continue
                    if self.WuzuoCheckBox.isChecked() == True:
                        if self.TrainInfoTableWidget.item(row, 15).text() != '' and self.TrainInfoTableWidget.item(row, 15).text() != '无':
                            # print(row, self.TrainInfoTableWidget.item(row, 15).text())
                            continue
                    self.TrainInfoTableWidget.setRowHidden(row, True)
                except:
                    self.TrainInfoTableWidget.setRowHidden(row, True)
                # print('Hidden', row)

    def selectStartStation(self):
        train_row_number = self.TrainInfoTableWidget.rowCount()
        station_row_number = self.StartStationTableWidget.rowCount()

        for train_row in range(train_row_number):
            if self.TrainInfoTableWidget.isRowHidden(train_row) == True:
                continue
            else:
                for station_row in range(station_row_number):
                    if self.StartStationTableWidget.item(station_row, 0).checkState() != QtCore.Qt.Checked:
                        if self.StartStationTableWidget.item(station_row, 0).text() == self.TrainInfoTableWidget.item(train_row, 1).text():
                            self.TrainInfoTableWidget.setRowHidden(
                                train_row, True)

    def selectEndStation(self):
        train_row_number = self.TrainInfoTableWidget.rowCount()
        station_row_number = self.EndStationTableWidget.rowCount()

        for train_row in range(train_row_number):
            if self.TrainInfoTableWidget.isRowHidden(train_row) == True:
                continue
            else:
                for station_row in range(station_row_number):
                    if self.EndStationTableWidget.item(station_row, 0).checkState() != QtCore.Qt.Checked:
                        if self.EndStationTableWidget.item(station_row, 0).text() == self.TrainInfoTableWidget.item(train_row, 2).text():
                            self.TrainInfoTableWidget.setRowHidden(
                                train_row, True)

    def selectTrainType(self):
        row_number = self.TrainInfoTableWidget.rowCount()

        for row in range(row_number):
            if self.TrainInfoTableWidget.isRowHidden(row) == True:
                continue
            else:
                if self.TrainInfoTableWidget.item(row, 0).text()[0] == 'G' or self.TrainInfoTableWidget.item(row, 0).text()[0] == 'C' or self.TrainInfoTableWidget.item(row, 0).text()[0] == 'D':
                    if self.ExpressCheckBox.isChecked() == False:
                        self.TrainInfoTableWidget.setRowHidden(row, True)
                else:
                    if self.OrdinaryCheckBox.isChecked() == False:
                        self.TrainInfoTableWidget.setRowHidden(row, True)

    def bookTicket(self):
        # print('Book Ticket Function')
        order_passenger = list()

        if self.PassengerTableWidget.rowCount() == 0:
            QMessageBox().information(self, '未登陆', '请先登陆账号,以获得乘客信息')
            return -1
        # print('Login Check Correct')
        row_passenger_number = self.PassengerTableWidget.rowCount()
        row_seat_number = self.SeatTableWidget.rowCount()
        row_train_number = self.TrainInfoTableWidget.rowCount()
        passenger_number = 0
        seat_chosed = None

        for row_passenger_current_number in range(row_passenger_number):
            if self.PassengerTableWidget.item(row_passenger_current_number, 0).checkState() == QtCore.Qt.Checked:
                order_passenger.append(self.PassengerTableWidget.item(
                    row_passenger_current_number, 0).text()+'\n')
                order_passenger.append(self.PassengerTableWidget.item(
                    row_passenger_current_number, 3).text()+'\n')
                passenger_number += 1

        if passenger_number > 5:
            QMessageBox().information(self, '乘客过多', '最多同时选择5位乘客,请重新选择')
            return -1

        if passenger_number == 0:
            QMessageBox().information(self, '未选择乘客', '请选择购票乘客')
            return -1

        # print('Passenger Check Correct')

        for row_seat_current_number in range(row_seat_number):
            if self.SeatTableWidget.item(row_seat_current_number, 0).isSelected():
                seat_chosed = self.SeatTableWidget.item(
                    row_seat_current_number, 0).text()
                break

        if seat_chosed == None:
            QMessageBox().information(self, '未选择座席', '请选择计划购买的座席类型')
            return -1

        # print('Seat Check Correct')
        train_chosed = None

        for row_train_current_number in range(row_train_number):
            if self.TrainInfoTableWidget.item(row_train_current_number, 0).isSelected():
                train_chosed = self.TrainInfoTableWidget.item(
                    row_train_current_number, 0).text()
                break

        if train_chosed == None:
            QMessageBox().information(self, '未选择车次', '请选择计划购买的车次')
            return -1

        # print('Train Check Correct')

        book_request_field = [str(int(time.time()))+'\n',
                              self.user_account+'\n',
                              self.user_password+'\n',
                              self.StartStationEdit.text()+'\n',
                              self.EndStationEdit.text()+'\n',
                              self.DepartDateEdit.textFromDateTime(
                                  self.DepartDateEdit.dateTime())+'\n',
                              train_chosed+'\n',
                              seat_chosed+'\n']+order_passenger
        ticket_order_info = ('出发地:'+book_request_field[3]+'目的地:'+book_request_field[4] +
                             '出发时间:'+book_request_field[5]+'车次:'+book_request_field[6].strip())

        book_request_file = open('BookRequest.info', 'w')
        book_request_file.writelines(book_request_field)
        book_request_file.close()

        QMessageBox.information(self, '确认购票信息', ticket_order_info)

        self.OrderState.start()

        QMessageBox.information(self, '请稍等', '购票大约需要30秒\n请勿关闭此窗口')

    def setSignalandSlot(self):

        self.BookPushButton.clicked.connect(self.bookTicket)
        self.SearchButton.clicked.connect(self.searchTicket)
        self.SelectButton.clicked.connect(self.selectTicket)

        self.refreshTrainInfo.data_base_right.connect(self.showAllTrainInfo)
        self.refreshTrainInfo.data_base_wrong.connect(self.showSearchError)

        self.TrainInfoTableWidget.cellClicked.connect(
            self.showDepartStationAndPrice)
        self.about.triggered.connect(self.showAboutBox)
        self.logging.triggered.connect(self.logging_ui.show)
        self.logging_ui.OKButton.clicked.connect(self.setLogInfo)
        self.logging_ui.CancalButton.clicked.connect(self.logging_ui.close)

        self.OrderState.passenger_state_wrong.connect(
            self.showPassengerError)
        self.OrderState.passenger_state_right.connect(
            self.showPassengerInfo)

        self.OrderState.order_state_wrong.connect(
            self.showOrderError)
        self.OrderState.order_state_right.connect(
            self.showOrderInfo)

    def showOrderError(self):
        QMessageBox.information(self, '购票失败', '请检查购票信息及网络环境')

    def showOrderInfo(self):

        QMessageBox.information(self, '购票成功', '请在弹出窗口完成支付')

    def showPassengerError(self):
        QMessageBox.information(self, '登录失败', '请输入正确的账号或密码')

    def showPassengerInfo(self):

        self.resetPassengerTable()
        # print("I am Here")
        data_base = sqlite3.connect('Tickets.db')
        try:
            row_number = 0
            result = data_base.execute(
                '''SELECT * FROM '%s' ''' % ('L'+self.logging_time))
            for row in result:
                column_number = 0
                for column in row:
                    # #print(column)
                    current_item = QtWidgets.QTableWidgetItem(column)
                    if column_number == 0:
                        current_item.setCheckState(QtCore.Qt.Unchecked)
                    current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.PassengerTableWidget.setRowCount(row_number+1)
                    self.PassengerTableWidget.setItem(
                        row_number, column_number, current_item)
                    column_number = column_number + 1
                row_number = row_number+1

        except sqlite3.OperationalError:
            pass

    def resetPassengerTable(self):
        self.PassengerTableWidget.clearContents()
        self.PassengerTableWidget.setRowCount(0)

    def setLogInfo(self):
        self.user_account = self.logging_ui.AccountEdit.text()
        self.user_password = self.logging_ui.PasswordEdit.text()

        self.resetPassengerTable()

        if self.user_account == '' or self.user_password == '':
            QMessageBox.information(self, '登录失败', '请输入正确的账号或密码')
        else:
            self.getPassengers(self.user_account, self.user_password)
            self.OrderState.start()

        # #print(user_account,user_password)

        self.logging_ui.close()

    def getPassengers(self, user_account, user_password):

        self.logging_time = str(int(time.time()))

        self.OrderState.start()

        passenger_request_info = open('BookRequest.info', 'w')
        write_content = [self.logging_time+'\n',
                         user_account+'\n', user_password+'\n']
        passenger_request_info.writelines(write_content)
        passenger_request_info.close()

    def showAboutBox(self):
        QMessageBox.about(self, '关于', 'F915\nXidian University')

    def showDepartStationAndPrice(self, row, column):
        self.showDepartStation(row, column)
        self.showPriceInfo(row, column)
        self.showChooseSeat(row, column)

    def showChooseSeat(self, row, column):
        self.resetChooseSeat()
        ticket_info_column = 6
        seat_name = ['商务座', '一等座', '二等座',
                     '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        row_number = 0
        seat_row = 0
        for seat_row in range(len(seat_name)):
            if self.TrainInfoTableWidget.item(row, ticket_info_column).text() != '' and self.TrainInfoTableWidget.item(row, ticket_info_column).text() != '无':
                self.SeatTableWidget.setRowCount(row_number+1)
                current_item_name = QtWidgets.QTableWidgetItem(
                    seat_name[seat_row])
                current_item_name.setTextAlignment(QtCore.Qt.AlignCenter)
                self.SeatTableWidget.setItem(row_number, 0, current_item_name)
                row_number = row_number+1
            ticket_info_column = ticket_info_column+1

    def showDepartStation(self, row, column):
        self.resetDepartTable()
        # print(row, column)
        train_short_number = self.TrainInfoTableWidget.item(row, 0).text()
        row_number = 0
        # ##print(train_short_number)
        data_base = sqlite3.connect('Tickets.db')
        try:

            # ##print('D'+self.search_info[0].strip()+train_short_number)
            depart_result = data_base.execute(
                '''SELECT * FROM '%s' ''' % ('D'+self.search_info[0].strip()+train_short_number))
            for row in depart_result:
                self.DepartStationTableWidget.setRowCount(row_number+1)
                column_number = 0
                for column in row:
                    current_item = QtWidgets.QTableWidgetItem(column)
                    current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.DepartStationTableWidget.setItem(
                        row_number, column_number, current_item)
                    column_number = column_number+1
                row_number = row_number+1

        except sqlite3.OperationalError:
            pass
            # dialog = QMessageBox.information(self, '查询错误', '查询途经站点失败,请检查网络环境')
            # #print(dialog)
        data_base.close()

    def showPriceInfo(self, row, column):
        self.resetSeatPrice()
        # print(row, column)
        train_short_number = self.TrainInfoTableWidget.item(row, 0).text()
        row_number = self.PriceTableWidget.rowCount()
        # ##print(train_short_number)

        ticket_price_name = ['商务座', '一等座', '二等座',
                             '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        ticket_price = list()
        data_base = sqlite3.connect('Tickets.db')
        try:
            # ##print('P'+self.search_info[0].strip()+train_short_number)
            depart_result = data_base.execute(
                '''SELECT * FROM '%s' ''' % ('P'+self.search_info[0].strip()+train_short_number))
            for row in depart_result:
                for column in row:
                    ticket_price.append(column)
            # ##print(ticket_price)
            data_base.close()
            for row in range(row_number):
                current_item = QtWidgets.QTableWidgetItem(ticket_price[row])
                current_item_name = QtWidgets.QTableWidgetItem(
                    ticket_price_name[row])
                current_item.setTextAlignment(QtCore.Qt.AlignCenter)
                current_item_name.setTextAlignment(QtCore.Qt.AlignCenter)
                self.PriceTableWidget.setItem(
                    row, 0, current_item_name)
                self.PriceTableWidget.setItem(
                    row, 1, current_item)
                if ticket_price[row] == '':
                    self.PriceTableWidget.setRowHidden(row, True)

        except sqlite3.OperationalError:
            pass
            # QMessageBox.information(self, '查询错误', '查询席位票价失败,请检查网络环境')
            # #print(dialog)
            data_base.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 800)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1440, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1440, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SearchGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.SearchGroupBox.setGeometry(QtCore.QRect(10, 0, 391, 211))
        self.SearchGroupBox.setObjectName("SearchGroupBox")
        self.TicketTypeGroupBox = QtWidgets.QGroupBox(self.SearchGroupBox)
        self.TicketTypeGroupBox.setGeometry(QtCore.QRect(290, 30, 91, 101))
        self.TicketTypeGroupBox.setObjectName("TicketTypeGroupBox")
        self.layoutWidget = QtWidgets.QWidget(self.TicketTypeGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 72, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AdultTicketRadioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.AdultTicketRadioButton.setChecked(True)
        self.AdultTicketRadioButton.setObjectName("AdultTicketRadioButton")
        self.verticalLayout.addWidget(self.AdultTicketRadioButton)
        self.StudentTicketRadioButton = QtWidgets.QRadioButton(
            self.layoutWidget)
        self.StudentTicketRadioButton.setObjectName("StudentTicketRadioButton")
        self.verticalLayout.addWidget(self.StudentTicketRadioButton)
        self.SearchButton = QtWidgets.QPushButton(self.SearchGroupBox)
        self.SearchButton.setGeometry(QtCore.QRect(290, 140, 91, 61))
        self.SearchButton.setFlat(False)
        self.SearchButton.setObjectName("SearchButton")
        self.layoutWidget1 = QtWidgets.QWidget(self.SearchGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 271, 171))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.SearchLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.SearchLayout.setContentsMargins(0, 0, 0, 0)
        self.SearchLayout.setObjectName("SearchLayout")
        self.StartStationLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.StartStationLabel.setObjectName("StartStationLabel")
        self.SearchLayout.addWidget(self.StartStationLabel, 0, 0, 1, 1)
        self.StartStationEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.StartStationEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.StartStationEdit.setObjectName("StartStationEdit")
        self.SearchLayout.addWidget(self.StartStationEdit, 0, 1, 1, 1)
        self.EndStationLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.EndStationLabel.setObjectName("EndStationLabel")
        self.SearchLayout.addWidget(self.EndStationLabel, 1, 0, 1, 1)
        self.EndStationEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.EndStationEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.EndStationEdit.setObjectName("EndStationEdit")
        self.SearchLayout.addWidget(self.EndStationEdit, 1, 1, 1, 1)
        self.DepartDateLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.DepartDateLabel.setObjectName("DepartDateLabel")
        self.SearchLayout.addWidget(self.DepartDateLabel, 2, 0, 1, 1)
        self.DepartDateEdit = QtWidgets.QDateEdit(self.layoutWidget1)
        font = QtGui.QFont()
        self.DepartDateEdit.setFont(font)
        self.DepartDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.DepartDateEdit.setCalendarPopup(True)
        self.DepartDateEdit.setDate(QtCore.QDate.currentDate())
        self.DepartDateEdit.setObjectName("DepartDateEdit")
        self.DepartDateEdit.setDisplayFormat("yyyy-MM-dd")
        self.SearchLayout.addWidget(self.DepartDateEdit, 2, 1, 1, 1)
        self.ChooseGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ChooseGroupBox.setGeometry(QtCore.QRect(420, 0, 1011, 211))
        self.ChooseGroupBox.setObjectName("ChooseGroupBox")
        self.DepartGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.DepartGroupBox.setGeometry(QtCore.QRect(10, 30, 151, 171))
        self.DepartGroupBox.setObjectName("DepartGroupBox")
        self.layoutWidget2 = QtWidgets.QWidget(self.DepartGroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 30, 131, 141))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.DepartLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.DepartLayout.setContentsMargins(0, 0, 0, 0)
        self.DepartLayout.setObjectName("DepartLayout")
        self.OneDepartTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget2)
        self.OneDepartTimeCheckBox.setChecked(True)
        self.OneDepartTimeCheckBox.setObjectName("OneDepartTimeCheckBox")
        self.DepartLayout.addWidget(self.OneDepartTimeCheckBox)
        self.TwoDepartTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget2)
        self.TwoDepartTimeCheckBox.setAutoFillBackground(False)
        self.TwoDepartTimeCheckBox.setChecked(True)
        self.TwoDepartTimeCheckBox.setAutoExclusive(False)
        self.TwoDepartTimeCheckBox.setObjectName("TwoDepartTimeCheckBox")
        self.DepartLayout.addWidget(self.TwoDepartTimeCheckBox)
        self.ThreeDepartTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget2)
        self.ThreeDepartTimeCheckBox.setChecked(True)
        self.ThreeDepartTimeCheckBox.setObjectName("ThreeDepartTimeCheckBox")
        self.DepartLayout.addWidget(self.ThreeDepartTimeCheckBox)
        self.FourDepartTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget2)
        self.FourDepartTimeCheckBox.setChecked(True)
        self.FourDepartTimeCheckBox.setObjectName("FourDepartTimeCheckBox")
        self.DepartLayout.addWidget(self.FourDepartTimeCheckBox)
        self.SeatTypeGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.SeatTypeGroupBox.setGeometry(QtCore.QRect(330, 30, 231, 171))
        self.SeatTypeGroupBox.setObjectName("SeatTypeGroupBox")
        self.ShangwuzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.ShangwuzuoCheckBox.setGeometry(QtCore.QRect(12, 32, 102, 21))
        self.ShangwuzuoCheckBox.setChecked(True)
        self.ShangwuzuoCheckBox.setObjectName("ShangwuzuoCheckBox")
        self.GaojiruanwoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.GaojiruanwoCheckBox.setGeometry(QtCore.QRect(120, 32, 101, 21))
        self.GaojiruanwoCheckBox.setChecked(True)
        self.GaojiruanwoCheckBox.setObjectName("GaojiruanwoCheckBox")
        self.YidengzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.YidengzuoCheckBox.setGeometry(QtCore.QRect(12, 59, 102, 21))
        self.YidengzuoCheckBox.setChecked(True)
        self.YidengzuoCheckBox.setObjectName("YidengzuoCheckBox")
        self.RuanwoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.RuanwoCheckBox.setGeometry(QtCore.QRect(120, 59, 101, 21))
        self.RuanwoCheckBox.setChecked(True)
        self.RuanwoCheckBox.setObjectName("RuanwoCheckBox")
        self.ErdengzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.ErdengzuoCheckBox.setGeometry(QtCore.QRect(12, 86, 102, 21))
        self.ErdengzuoCheckBox.setChecked(True)
        self.ErdengzuoCheckBox.setObjectName("ErdengzuoCheckBox")
        self.YingwoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.YingwoCheckBox.setGeometry(QtCore.QRect(120, 86, 101, 21))
        self.YingwoCheckBox.setChecked(True)
        self.YingwoCheckBox.setObjectName("YingwoCheckBox")
        self.DongwoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.DongwoCheckBox.setGeometry(QtCore.QRect(12, 113, 102, 21))
        self.DongwoCheckBox.setChecked(True)
        self.DongwoCheckBox.setObjectName("DongwoCheckBox")
        self.RuanzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.RuanzuoCheckBox.setGeometry(QtCore.QRect(120, 113, 101, 21))
        self.RuanzuoCheckBox.setChecked(True)
        self.RuanzuoCheckBox.setObjectName("RuanzuoCheckBox")
        self.WuzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.WuzuoCheckBox.setGeometry(QtCore.QRect(12, 140, 102, 21))
        self.WuzuoCheckBox.setChecked(True)
        self.WuzuoCheckBox.setObjectName("WuzuoCheckBox")
        self.YingzuoCheckBox = QtWidgets.QCheckBox(self.SeatTypeGroupBox)
        self.YingzuoCheckBox.setGeometry(QtCore.QRect(120, 140, 101, 21))
        self.YingzuoCheckBox.setChecked(True)
        self.YingzuoCheckBox.setObjectName("YingzuoCheckBox")
        self.StartStationGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.StartStationGroupBox.setGeometry(QtCore.QRect(570, 30, 161, 171))
        self.StartStationGroupBox.setObjectName("StartStationGroupBox")

        self.StartStationTableWidget = QtWidgets.QTableWidget(
            self.StartStationGroupBox)
        self.StartStationTableWidget.setGeometry(
            QtCore.QRect(10, 30, 141, 131))
        self.StartStationTableWidget.setObjectName("StartStationTableWidget")
        self.StartStationTableWidget.setColumnCount(1)
        self.StartStationTableWidget.setRowCount(0)
        self.StartStationTableWidget.horizontalHeader().setVisible(False)
        self.StartStationTableWidget.verticalHeader().setVisible(False)
        self.StartStationTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.StartStationTableWidget.setAlternatingRowColors(True)
        self.StartStationTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        '''
        self.TrainInfoTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.TrainInfoTableWidget.setAlternatingRowColors(True)
        self.TrainInfoTableWidget.verticalHeader().setVisible(False)
        self.TrainInfoTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TrainInfoTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.TrainInfoTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.TrainInfoTableWidget.horizontalHeader().setStretchLastSection(False)
        self.TrainInfoTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        '''

        self.EndStationGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.EndStationGroupBox.setGeometry(QtCore.QRect(740, 30, 161, 171))
        self.EndStationGroupBox.setObjectName("EndStationGroupBox")

        self.EndStationTableWidget = QtWidgets.QTableWidget(
            self.EndStationGroupBox)
        self.EndStationTableWidget.setGeometry(QtCore.QRect(10, 30, 141, 131))
        self.EndStationTableWidget.setObjectName("EndStationTableWidget")
        self.EndStationTableWidget.setColumnCount(1)
        self.EndStationTableWidget.setRowCount(0)
        self.EndStationTableWidget.horizontalHeader().setVisible(False)
        self.EndStationTableWidget.verticalHeader().setVisible(False)
        self.EndStationTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.EndStationTableWidget.setAlternatingRowColors(True)
        self.EndStationTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ArriveGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.ArriveGroupBox.setGeometry(QtCore.QRect(170, 30, 151, 171))
        self.ArriveGroupBox.setObjectName("ArriveGroupBox")
        self.layoutWidget3 = QtWidgets.QWidget(self.ArriveGroupBox)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 30, 131, 141))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.ArriveLayout = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.ArriveLayout.setContentsMargins(0, 0, 0, 0)
        self.ArriveLayout.setObjectName("ArriveLayout")
        self.OneArriveTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.OneArriveTimeCheckBox.setChecked(True)
        self.OneArriveTimeCheckBox.setObjectName("OneArriveTimeCheckBox")
        self.ArriveLayout.addWidget(self.OneArriveTimeCheckBox)
        self.TwoArriveTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.TwoArriveTimeCheckBox.setAutoFillBackground(False)
        self.TwoArriveTimeCheckBox.setChecked(True)
        self.TwoArriveTimeCheckBox.setAutoExclusive(False)
        self.TwoArriveTimeCheckBox.setObjectName("TwoArriveTimeCheckBox")
        self.ArriveLayout.addWidget(self.TwoArriveTimeCheckBox)
        self.ThreeArriveTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.ThreeArriveTimeCheckBox.setChecked(True)
        self.ThreeArriveTimeCheckBox.setObjectName("ThreeArriveTimeCheckBox")
        self.ArriveLayout.addWidget(self.ThreeArriveTimeCheckBox)
        self.FourArriveTimeCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.FourArriveTimeCheckBox.setChecked(True)
        self.FourArriveTimeCheckBox.setObjectName("FourArriveTimeCheckBox")
        self.ArriveLayout.addWidget(self.FourArriveTimeCheckBox)
        self.TrainTypeGroupBox = QtWidgets.QGroupBox(self.ChooseGroupBox)
        self.TrainTypeGroupBox.setGeometry(QtCore.QRect(910, 30, 91, 101))
        self.TrainTypeGroupBox.setObjectName("TrainTypeGroupBox")
        self.layoutWidget4 = QtWidgets.QWidget(self.TrainTypeGroupBox)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 30, 71, 71))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.TrainTypeLayout = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.TrainTypeLayout.setContentsMargins(0, 0, 0, 0)
        self.TrainTypeLayout.setObjectName("TrainTypeLayout")
        self.ExpressCheckBox = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ExpressCheckBox.setChecked(True)
        self.ExpressCheckBox.setObjectName("ExpressCheckBox")
        self.TrainTypeLayout.addWidget(self.ExpressCheckBox)
        self.OrdinaryCheckBox = QtWidgets.QCheckBox(self.layoutWidget4)
        self.OrdinaryCheckBox.setChecked(True)
        self.OrdinaryCheckBox.setObjectName("OrdinaryCheckBox")
        self.TrainTypeLayout.addWidget(self.OrdinaryCheckBox)
        self.SelectButton = QtWidgets.QPushButton(self.ChooseGroupBox)
        self.SelectButton.setGeometry(QtCore.QRect(910, 140, 91, 61))
        self.SelectButton.setObjectName("SelectButton")
        self.TrainInfoGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TrainInfoGroupBox.setGeometry(QtCore.QRect(10, 220, 1421, 261))
        self.TrainInfoGroupBox.setObjectName("TrainInfoGroupBox")
        self.TrainInfoTableWidget = QtWidgets.QTableWidget(
            self.TrainInfoGroupBox)
        self.TrainInfoTableWidget.setGeometry(QtCore.QRect(10, 30, 1401, 221))
        self.TrainInfoTableWidget.setObjectName("TrainInfoTableWidget")
        self.TrainInfoTableWidget.setRowCount(0)
        ticket_info_horizontal_name = ['车次', '出发站', '到达站', '出发时间', '到达时间', '历时',
                                       '商务座', '一等座', '二等座', '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        self.TrainInfoTableWidget.setColumnCount(
            len(ticket_info_horizontal_name))
        self.TrainInfoTableWidget.setHorizontalHeaderLabels(
            ticket_info_horizontal_name)
        self.TrainInfoTableWidget.horizontalHeader().setHighlightSections(False)
        self.TrainInfoTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.TrainInfoTableWidget.setAlternatingRowColors(True)
        self.TrainInfoTableWidget.verticalHeader().setVisible(False)
        self.TrainInfoTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TrainInfoTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.TrainInfoTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.TrainInfoTableWidget.horizontalHeader().setStretchLastSection(False)
        self.TrainInfoTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.TicketInfoGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TicketInfoGroupBox.setGeometry(QtCore.QRect(10, 490, 711, 271))
        self.TicketInfoGroupBox.setObjectName("TicketInfoGroupBox")
        self.DepartStationGroupBox = QtWidgets.QGroupBox(
            self.TicketInfoGroupBox)
        self.DepartStationGroupBox.setGeometry(QtCore.QRect(9, 29, 521, 231))
        self.DepartStationGroupBox.setObjectName("DepartStationGroupBox")

        self.DepartStationTableWidget = QtWidgets.QTableWidget(
            self.DepartStationGroupBox)
        self.DepartStationTableWidget.setGeometry(
            QtCore.QRect(10, 30, 501, 191))
        self.DepartStationTableWidget.setObjectName("DepartStationTableWidget")
        self.DepartStationTableWidget.setRowCount(0)
        self.DepartStationTableWidget.setAlternatingRowColors(True)
        depart_horizontal_name = ['序号', '车站', '到达', '出发', '停留']
        self.DepartStationTableWidget.setColumnCount(
            len(depart_horizontal_name))
        self.DepartStationTableWidget.setHorizontalHeaderLabels(
            depart_horizontal_name)
        self.DepartStationTableWidget.horizontalHeader().setHighlightSections(False)
        self.DepartStationTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.DepartStationTableWidget.setAlternatingRowColors(True)
        self.DepartStationTableWidget.verticalHeader().setVisible(False)
        self.DepartStationTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.DepartStationTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.DepartStationTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.DepartStationTableWidget.horizontalHeader().setStretchLastSection(False)
        self.DepartStationTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        '''
          horizontal_name = ['车次', '出发站', '到达站', '出发时间', '到达时间', '历时',
                           '商务座', '一等座', '二等座', '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        self.TrainInfoTableWidget.setColumnCount(len(horizontal_name))
        self.TrainInfoTableWidget.setHorizontalHeaderLabels(horizontal_name)
        self.TrainInfoTableWidget.horizontalHeader().setHighlightSections(False)
        self.TrainInfoTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.TrainInfoTableWidget.setAlternatingRowColors(True)
        self.TrainInfoTableWidget.verticalHeader().setVisible(False)
        self.TrainInfoTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TrainInfoTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.TrainInfoTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.TrainInfoTableWidget.horizontalHeader().setStretchLastSection(False)
        self.TrainInfoTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
          
          '''

        self.PriceGroupBox = QtWidgets.QGroupBox(self.TicketInfoGroupBox)
        self.PriceGroupBox.setGeometry(QtCore.QRect(540, 30, 161, 231))
        self.PriceGroupBox.setObjectName("PriceGroupBox")

        self.PriceTableWidget = QtWidgets.QTableWidget(self.PriceGroupBox)
        self.PriceTableWidget.setGeometry(QtCore.QRect(10, 30, 141, 191))
        self.PriceTableWidget.setObjectName("PriceTableWidget")
        self.PriceTableWidget.setColumnCount(2)
        price_vertical_name = ['商务座', '一等座', '二等座',
                               '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        price_horizontial_name = ['座席', '价格']
        self.PriceTableWidget.setRowCount(len(price_vertical_name))
        self.PriceTableWidget.horizontalHeader().setHighlightSections(False)
        self.PriceTableWidget.setVerticalHeaderLabels(price_vertical_name)
        self.PriceTableWidget.setHorizontalHeaderLabels(price_horizontial_name)
        self.PriceTableWidget.verticalHeader().setHighlightSections(False)
        self.PriceTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.PriceTableWidget.setAlternatingRowColors(True)
        self.PriceTableWidget.horizontalHeader().setVisible(True)
        self.PriceTableWidget.verticalHeader().setVisible(False)
        self.PriceTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PriceTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.PriceTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.PriceTableWidget.horizontalHeader().setStretchLastSection(False)
        self.PriceTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.BookGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.BookGroupBox.setGeometry(QtCore.QRect(740, 490, 691, 271))
        self.BookGroupBox.setObjectName("BookGroupBox")
        self.PassengerGroupBox = QtWidgets.QGroupBox(self.BookGroupBox)
        self.PassengerGroupBox.setGeometry(QtCore.QRect(10, 30, 531, 231))
        self.PassengerGroupBox.setObjectName("PassengerGroupBox")

        self.PassengerTableWidget = QtWidgets.QTableWidget(
            self.PassengerGroupBox)
        self.PassengerTableWidget.setGeometry(QtCore.QRect(10, 30, 511, 191))
        self.PassengerTableWidget.setObjectName("PassengerTableWidget")
        self.PassengerTableWidget.setRowCount(0)
        Passenger_horizontal_name = ['姓名', '性别', '类别', '身份证号']
        self.PassengerTableWidget.setColumnCount(
            len(Passenger_horizontal_name))
        self.PassengerTableWidget.setHorizontalHeaderLabels(
            Passenger_horizontal_name)
        self.PassengerTableWidget.verticalHeader().setVisible(False)
        self.PassengerTableWidget.horizontalHeader().setVisible(True)
        self.PassengerTableWidget.horizontalHeader().setHighlightSections(False)
        self.PassengerTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.PassengerTableWidget.setAlternatingRowColors(True)
        self.PassengerTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PassengerTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.PassengerTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.PassengerTableWidget.horizontalHeader().setStretchLastSection(True)
        self.PassengerTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        '''
        price_vertical_name = ['商务座', '一等座', '二等座',
                               '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        self.PriceTableWidget.setRowCount(len(price_vertical_name))

        self.PriceTableWidget.setVerticalHeaderLabels(price_vertical_name)
        self.PriceTableWidget.verticalHeader().setHighlightSections(False)
        self.PriceTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.PriceTableWidget.setAlternatingRowColors(True)
        self.PriceTableWidget.horizontalHeader().setVisible(False)
        self.PriceTableWidget.verticalHeader().setVisible(False)
        self.PriceTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PriceTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.PriceTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.PriceTableWidget.horizontalHeader().setStretchLastSection(False)
        self.PriceTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        '''

        self.SeatGroupBox = QtWidgets.QGroupBox(self.BookGroupBox)
        self.SeatGroupBox.setGeometry(QtCore.QRect(550, 30, 131, 181))
        self.SeatGroupBox.setObjectName("SeatGroupBox")
        self.SeatTableWidget = QtWidgets.QTableWidget(self.SeatGroupBox)
        self.SeatTableWidget.setGeometry(QtCore.QRect(10, 30, 111, 141))
        self.SeatTableWidget.setObjectName("SeatTableWidget")

        self.SeatTableWidget.setColumnCount(1)
        self.SeatTableWidget.setRowCount(0)
        seat_horizontal_name = ['座席']
        self.SeatTableWidget.setColumnCount(len(seat_horizontal_name))
        self.SeatTableWidget.setHorizontalHeaderLabels(seat_horizontal_name)
        self.SeatTableWidget.verticalHeader().setVisible(False)
        self.SeatTableWidget.horizontalHeader().setVisible(False)
        self.SeatTableWidget.horizontalHeader().setHighlightSections(False)
        self.SeatTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.SeatTableWidget.setAlternatingRowColors(True)
        self.SeatTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.SeatTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.SeatTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.SeatTableWidget.horizontalHeader().setStretchLastSection(False)
        self.SeatTableWidget.horizontalHeader(
        ).setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.BookPushButton = QtWidgets.QPushButton(self.BookGroupBox)
        self.BookPushButton.setGeometry(QtCore.QRect(550, 220, 131, 41))
        self.BookPushButton.setObjectName("BookPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 28))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.logging = QtWidgets.QAction(MainWindow)
        self.logging.setObjectName("logging")
        self.about = QtWidgets.QAction(MainWindow)
        self.about.setObjectName("about")
        self.menu.addAction(self.logging)
        self.menu.addAction(self.about)
        self.menubar.addAction(self.menu.menuAction())
        self.StartStationLabel.setBuddy(self.StartStationEdit)
        self.EndStationLabel.setBuddy(self.EndStationEdit)
        self.DepartDateLabel.setBuddy(self.DepartDateEdit)

        self.logging_ui = Ui_Logging()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.StartStationEdit, self.EndStationEdit)
        MainWindow.setTabOrder(self.EndStationEdit, self.DepartDateEdit)
        MainWindow.setTabOrder(self.DepartDateEdit, self.ExpressCheckBox)
        MainWindow.setTabOrder(self.ExpressCheckBox, self.OrdinaryCheckBox)
        MainWindow.setTabOrder(self.OrdinaryCheckBox,
                               self.AdultTicketRadioButton)
        MainWindow.setTabOrder(self.AdultTicketRadioButton,
                               self.StudentTicketRadioButton)
        MainWindow.setTabOrder(
            self.StudentTicketRadioButton, self.SearchButton)
        MainWindow.setTabOrder(self.SearchButton, self.OneDepartTimeCheckBox)
        MainWindow.setTabOrder(self.OneDepartTimeCheckBox,
                               self.TwoDepartTimeCheckBox)
        MainWindow.setTabOrder(self.TwoDepartTimeCheckBox,
                               self.ThreeDepartTimeCheckBox)
        MainWindow.setTabOrder(self.ThreeDepartTimeCheckBox,
                               self.FourDepartTimeCheckBox)
        MainWindow.setTabOrder(self.FourDepartTimeCheckBox,
                               self.OneArriveTimeCheckBox)
        MainWindow.setTabOrder(self.OneArriveTimeCheckBox,
                               self.TwoArriveTimeCheckBox)
        MainWindow.setTabOrder(self.TwoArriveTimeCheckBox,
                               self.ThreeArriveTimeCheckBox)
        MainWindow.setTabOrder(self.ThreeArriveTimeCheckBox,
                               self.FourArriveTimeCheckBox)
        MainWindow.setTabOrder(
            self.FourArriveTimeCheckBox, self.ShangwuzuoCheckBox)
        MainWindow.setTabOrder(self.ShangwuzuoCheckBox, self.YidengzuoCheckBox)
        MainWindow.setTabOrder(self.YidengzuoCheckBox, self.ErdengzuoCheckBox)
        MainWindow.setTabOrder(self.ErdengzuoCheckBox, self.DongwoCheckBox)
        MainWindow.setTabOrder(self.DongwoCheckBox, self.WuzuoCheckBox)
        MainWindow.setTabOrder(self.WuzuoCheckBox, self.GaojiruanwoCheckBox)
        MainWindow.setTabOrder(self.GaojiruanwoCheckBox, self.RuanwoCheckBox)
        MainWindow.setTabOrder(self.RuanwoCheckBox, self.YingwoCheckBox)
        MainWindow.setTabOrder(self.YingwoCheckBox, self.RuanzuoCheckBox)
        MainWindow.setTabOrder(self.RuanzuoCheckBox, self.YingzuoCheckBox)
        MainWindow.setTabOrder(self.YingzuoCheckBox,
                               self.StartStationTableWidget)
        MainWindow.setTabOrder(
            self.StartStationTableWidget, self.EndStationTableWidget)
        MainWindow.setTabOrder(self.EndStationTableWidget,
                               self.TrainInfoTableWidget)
        MainWindow.setTabOrder(self.TrainInfoTableWidget,
                               self.DepartStationTableWidget)
        MainWindow.setTabOrder(
            self.DepartStationTableWidget, self.PriceTableWidget)
        MainWindow.setTabOrder(self.PriceTableWidget,
                               self.PassengerTableWidget)
        MainWindow.setTabOrder(self.PassengerTableWidget, self.SeatTableWidget)
        MainWindow.setTabOrder(self.SeatTableWidget,
                               self.BookPushButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "MainWindow", "基于Python3的火车票查询系统", None, -1))
        self.SearchGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "车票查询", None, -1))
        self.TicketTypeGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "车票类型", None, -1))
        self.AdultTicketRadioButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "成人票", None, -1))
        self.StudentTicketRadioButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "学生票", None, -1))
        self.SearchButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "点我查询", None, -1))
        self.StartStationLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "出发车站：", None, -1))
        self.StartStationEdit.setText(
            QtWidgets.QApplication.translate("MainWindow", "北京", None, -1))
        self.EndStationLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "目的车站：", None, -1))
        self.EndStationEdit.setText(
            QtWidgets.QApplication.translate("MainWindow", "上海", None, -1))
        self.DepartDateLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "出发日期：", None, -1))
        self.ChooseGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "车票筛选", None, -1))
        self.DepartGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "发车时间", None, -1))
        self.OneDepartTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "00:00 - 06:00", None, -1))
        self.TwoDepartTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "06:00 - 12:00", None, -1))
        self.ThreeDepartTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "12:00 - 18:00", None, -1))
        self.FourDepartTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "18:00 - 24:00", None, -1))
        self.SeatTypeGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "座席类型", None, -1))
        self.ShangwuzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "商务座", None, -1))
        self.GaojiruanwoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "高级软卧", None, -1))
        self.YidengzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "一等座", None, -1))
        self.RuanwoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "软卧", None, -1))
        self.ErdengzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "二等座", None, -1))
        self.YingwoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "硬卧", None, -1))
        self.DongwoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "动卧", None, -1))
        self.RuanzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "软座", None, -1))
        self.WuzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "无座", None, -1))
        self.YingzuoCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "硬座", None, -1))
        self.StartStationGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "出发车站", None, -1))
        self.EndStationGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "到达车站", None, -1))
        self.ArriveGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "到达时间", None, -1))
        self.OneArriveTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "00:00 - 06:00", None, -1))
        self.TwoArriveTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "06:00 - 12:00", None, -1))
        self.ThreeArriveTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "12:00 - 18:00", None, -1))
        self.FourArriveTimeCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "18:00 - 24:00", None, -1))
        self.TrainTypeGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "列车类型", None, -1))
        self.ExpressCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "动车", None, -1))
        self.OrdinaryCheckBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "普速", None, -1))
        self.SelectButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "点我筛选", None, -1))
        self.TrainInfoGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "车次信息", None, -1))
        self.TrainInfoTableWidget.setSortingEnabled(True)
        self.TicketInfoGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "车票信息", None, -1))
        self.DepartStationGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "途径站点", None, -1))
        self.PriceGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "座席价格", None, -1))
        self.BookGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "购票设置", None, -1))
        self.PassengerGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "选择乘客", None, -1))
        self.SeatGroupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "选择座席", None, -1))
        self.BookPushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "点我购票", None, -1))
        self.menu.setTitle(QtWidgets.QApplication.translate(
            "MainWindow", "选项", None, -1))
        self.logging.setText(QtWidgets.QApplication.translate(
            "MainWindow", "登录", None, -1))
        self.about.setText(QtWidgets.QApplication.translate(
            "MainWindow", "关于", None, -1))


class RefreshTable(QThread):

    data_base_right = QtCore.Signal()
    data_base_wrong = QtCore.Signal()

    def __init__(self):
        super(RefreshTable, self).__init__()

    def run(self):
        while(1):
            file_state = open('CheckResult.info')
            state = file_state.read()
            file_state.close()
            if state == '-1':
                # print('Search Error.(RefreshTable)')
                file_state = open('CheckResult.info', 'w')
                state = file_state.write('0')
                file_state.close()
                self.data_base_wrong.emit()
                break
            elif state == '1':
                # print('Search Correct.(RefreshTable)')
                file_state = open('CheckResult.info', 'w')
                state = file_state.write('0')
                file_state.close()
                self.data_base_right.emit()
                break
        return 0


class RefreshOrderState(QThread):

    passenger_state_right = QtCore.Signal()
    passenger_state_wrong = QtCore.Signal()
    order_state_right = QtCore.Signal()
    order_state_wrong = QtCore.Signal()

    def __init__(self):
        super(RefreshOrderState, self).__init__()

    def run(self):
        while(1):

            file_state = open('BookResult.info')
            state = file_state.readlines()
            file_state.close()
            try:
                if state[0] == '-1':
                    # print('Search Error.(RefreshTable)')
                    file_state = open('BookResult.info', 'w')
                    state = file_state.write('0')
                    file_state.close()
                    # print('-1')
                    file_state = open('BookRequest.info', 'w')
                    state = file_state.write('0')
                    file_state.close()

                    self.passenger_state_wrong.emit()
                    break
                elif state[0] == '1':
                    # print('Search Correct.(RefreshTable)')
                    file_state = open('BookResult.info', 'w')
                    state = file_state.write('0')
                    file_state.close()
                    # print('1')
                    file_state = open('BookRequest.info', 'w')
                    state = file_state.write('0')
                    file_state.close()

                    self.passenger_state_right.emit()
                    break

                elif state[0] == '-2':
                    # print('Search Error.(RefreshTable)')
                    file_state = open('BookResult.info', 'w')
                    state = file_state.write('0')
                    file_state.close()
                    # print('-2')
                    file_state = open('BookRequest.info', 'w')
                    state = file_state.write('0')
                    file_state.close()

                    self.order_state_wrong.emit()
                    break
                elif state[0] == '2':
                    # print('Search Correct.(RefreshTable)')

                    file_state = open('BookResult.info', 'w')
                    state = file_state.write('0')
                    file_state.close()
                    # print('2')
                    file_state = open('BookRequest.info', 'w')
                    state = file_state.write('0')
                    file_state.close()

                    self.order_state_right.emit()
                    break
            except:
                continue
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_MainWindow()
    window.show()

    sys.exit(app.exec_())
