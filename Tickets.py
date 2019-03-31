# -*- coding: utf-8 -*-
import datetime
import json
import random
import sqlite3
import time
import urllib
from threading import Thread

from UrlConfig import Urlconf


class Search(object):

    def __init__(self):
        self.file_state_result = list()
        self.ticket_info_result = list()
        self.time_stamp = str()
        self.start_station = str()
        self.end_station = str()
        self.start_date = str()
        self.student_ticket = str()
        self.ticket_info = str()
        self.ticket_info_result_DP = list()

        while(True):
            if self.getState() == -1:
                continue

            self.setState()

            if self.requestTicket() == -1:
                continue

            self.addDataBase()

    def getState(self):
        file_state = open("TicketRequest.info")
        self.file_state_result = file_state.readlines()
        file_state.close()
        try:
            ##print("Open %s Request." % self.file_state_result[0].strip())
            if self.time_stamp == self.file_state_result[0].strip():
                ##print("Have No New Request.")
                return -1
            else:
                if self.file_state_result[0].strip() == '0':
                    return -1
                return 0
        except:
            ##print('Read TicketRequest.info Error, Retry.')
            return -1

    def setState(self):
        self.time_stamp = self.file_state_result[0].strip()
        self.start_station = self.file_state_result[1].strip()
        self.end_station = self.file_state_result[2].strip()
        self.start_date = self.file_state_result[3].strip()
        self.student_ticket = self.file_state_result[4].strip()
        if self.file_state_result[4].strip() == '0':
            self.student_ticket = 'ADULT'
        else:
            self.student_ticket = '0X00'
        #print("时间戳:", self.time_stamp)
        #print("出发车站:", self.start_station)
        #print("到达车站:", self.end_station)
        #print("出发时间:", self.start_date)
        #print("学生票:", self.student_ticket)
        return 0

    def requestTicket(self):
        search_ticket_field = {'leftTicketDTO.train_date': self.start_date,
                               'leftTicketDTO.from_station': Urlconf().getStationCode(self.start_station),
                               'leftTicketDTO.to_station': Urlconf().getStationCode(self.end_station),
                               'purpose_codes': self.student_ticket
                               }
        search_ticket_url = Urlconf().getSearchUrl(search_ticket_field)
        try:
            ticket_info_origin = urllib.request.urlopen(
                search_ticket_url)
        except:
            pass
        if ticket_info_origin.getcode() == 200:
            self.ticket_info = ticket_info_origin.read().decode('utf-8')
            return 0
        else:
            #print('Network Error.')
            return -1

    def addDataBase(self):

        data_base = sqlite3.connect('Tickets.db')
        data_cursor = data_base.cursor()
        try:
            data_cursor.execute('''CREATE TABLE '%s'
                                (SHORTNAME TEXT,
                                STARTSTATION TEXT,
                                ENDSTATION TEXT,
                                STARTTIME TEXT,
                                ENDTIME TEXT,
                                DURINGTIME TEXT,
                                SHANGWUZUOSEAT TEXT,
                                YIDENGZUOSEAT TEXT,
                                ERDENGZUOSEAT TEXT,
                                DONGWOSEAT TEXT,
                                GAOJIRUANWOSEAT TEXT,
                                RUANWOSEAT TEXT,
                                YINGWOSEAT TEXT,
                                RUANZUOSEAT TEXT,
                                YINGZUOSEAT TEXT,
                                WUZUOSEAT TEXT);''' % self.time_stamp)
        except:
            #print('Table Create Error.')
            return -1
        data_base.commit()
        data_base.close()

        try:
            ticket_info_current_all = json.loads(self.ticket_info)[
                'data']['result']
            for ticket_info_current in ticket_info_current_all:
                ticket_info_current_divide = ticket_info_current.split('|')
                if ticket_info_current_divide[1] != '预订':
                    continue
                else:
                    # print(ticket_info_current_divide)
                    self.ticket_info_result.append(
                        Ticket(ticket_info_current, self.time_stamp))

            state_file = open('CheckResult.info', 'w')
            state_file.write('1')
            state_file.close()

            self.ticket_info_result_DP.clear()

            for ticket_info_current in ticket_info_current_all:
                ticket_info_current_divide = ticket_info_current.split('|')
                if ticket_info_current_divide[1] != '预订':
                    continue
                else:
                    if self.getState() == 0:
                        return -1
                    # print(ticket_info_current_divide)
                    self.ticket_info_result_DP.append(
                        TicketDP(ticket_info_current, self.time_stamp))
            for ticketDP_single in self.ticket_info_result_DP:
                ticketDP_single.start()

        except:
            # 发送信号给GUI显示
            #print('No Valid Result')
            state_file = open('CheckResult.info', 'w')
            state_file.write('-1')
            state_file.close()
            return -1


class Ticket(object):

    def __init__(self, ticket_info, time_stamp):

        self.start_time = str()
        self.end_time = str()
        self.start_station = str()
        self.end_station = str()
        self.start_station_chinese = str()
        self.end_station_chinese = str()

        self.first_station_chinese = str()
        self.last_station_chinese = str()
        self.during_time = str()

        self.train_short_number = str()
        self.train_long_number = str()

        self.train_state = str()
        self.seat_type = str()

        self.depart_date = str()
        self.depart_station = list()

        self.start_station_number = str()
        self.end_station_number = str()

        self.time_stamp = time_stamp
        self.seat_price = dict()

        self.left_tickets = dict()

        self.ticket_info_current_divide = ticket_info.split('|')
        # print(self.ticket_info_current_divide)

        self.setTicketProporty()
        self.addTicketDatabase()

    def setTicketProporty(self):
        seat_name = ['商务座', '一等座', '二等座', '动卧',
                     '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        seat_number = [32, 31, 30, 33, 21, 23, 28, 24, 29, 28]
        for i in range(len(seat_name)):
            self.left_tickets[seat_name[i]
                              ] = self.ticket_info_current_divide[seat_number[i]]

        self.start_time = self.ticket_info_current_divide[8]
        self.end_time = self.ticket_info_current_divide[9]
        self.start_station = self.ticket_info_current_divide[6]
        self.end_station = self.ticket_info_current_divide[7]

        self.first_station = self.ticket_info_current_divide[4]
        self.last_station = self.ticket_info_current_divide[5]

        self.during_time = self.ticket_info_current_divide[10]

        self.train_short_number = self.ticket_info_current_divide[3]
        self.train_long_number = self.ticket_info_current_divide[2]

        self.train_state = self.ticket_info_current_divide[1]
        self.seat_type = self.ticket_info_current_divide[35]

        self.depart_date = self.ticket_info_current_divide[13]
        self.depart_date = self.depart_date[0:4] + '-' + \
            self.depart_date[4:6] + '-' + self.depart_date[6:]

        self.start_station_chinese = Urlconf().getStationName(
            self.start_station)
        self.end_station_chinese = Urlconf().getStationName(
            self.end_station)
        self.first_station_chinese = Urlconf().getStationName(
            self.first_station)
        self.last_station_chinese = Urlconf().getStationName(
            self.last_station)

        # print(self.start_time, self.end_time,
        # Urlconf().getStationName(self.start_station),
        # Urlconf().getStationName(self.end_station),
        # Urlconf().getStationName(self.first_station),
        # Urlconf().getStationName(self.last_station),
        # self.during_time,
        # self.train_short_number,
        # self.train_long_number, self.seat_type)
        # print(self.left_tickets)

    def addTicketDatabase(self):

        # 防止重复，子表采用短号+时间戳的方式对表进行命名
        data_base = sqlite3.connect('Tickets.db')
        data_cursor = data_base.cursor()
        try:
            data_cursor.execute('''INSERT INTO '%s' (
                                SHORTNAME,
                                STARTSTATION,
                                ENDSTATION,
                                STARTTIME,
                                ENDTIME,
                                DURINGTIME,
                                SHANGWUZUOSEAT,
                                YIDENGZUOSEAT,
                                ERDENGZUOSEAT,
                                DONGWOSEAT,
                                GAOJIRUANWOSEAT,
                                RUANWOSEAT,
                                YINGWOSEAT,
                                RUANZUOSEAT,
                                YINGZUOSEAT,
                                WUZUOSEAT
                                ) VALUES(
                                '%s','%s','%s','%s','%s',
                                '%s','%s','%s','%s','%s',
                                '%s','%s','%s','%s','%s',
                                '%s');''' % (self.time_stamp,
                                             self.train_short_number,
                                             self.start_station_chinese,
                                             self.end_station_chinese,
                                             self.start_time,
                                             self.end_time,
                                             self.during_time,
                                             self.left_tickets['商务座'],
                                             self.left_tickets['一等座'],
                                             self.left_tickets['二等座'],
                                             self.left_tickets['动卧'],
                                             self.left_tickets['高级软卧'],
                                             self.left_tickets['软卧'],
                                             self.left_tickets['硬卧'],
                                             self.left_tickets['软座'],
                                             self.left_tickets['硬座'],
                                             self.left_tickets['无座']))
            #print('Table Operation Correct.')
        except:
            #print("Table Operation Error.")
            pass
        data_base.commit()
        data_base.close()

        return 0


class TicketDP(Thread):

    def __init__(self, ticket_info, time_stamp):
        super(TicketDP, self).__init__()
        self.start_time = str()
        self.end_time = str()
        self.start_station = str()
        self.end_station = str()
        self.start_station_chinese = str()
        self.end_station_chinese = str()

        self.first_station_chinese = str()
        self.last_station_chinese = str()
        self.during_time = str()

        self.train_short_number = str()
        self.train_long_number = str()

        self.train_state = str()
        self.seat_type = str()

        self.depart_date = str()
        self.depart_station = list()

        self.start_station_number = str()
        self.end_station_number = str()

        self.time_stamp = time_stamp
        self.seat_price = dict()

        self.left_tickets = dict()

        self.ticket_info_current_divide = ticket_info.split('|')
        # print(self.ticket_info_current_divide)

    def run(self):
        self.setTicketProporty()

        if self.getDepatrStation() != -1:
            self.addDepartDatabase()

            if self.getTicketPrice() != -1:
                self.addPriceDatabase()

    def setTicketProporty(self):
        seat_name = ['商务座', '一等座', '二等座', '动卧',
                     '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座']
        seat_number = [32, 31, 30, 33, 21, 23, 28, 24, 29, 28]
        for i in range(len(seat_name)):
            self.left_tickets[seat_name[i]
                              ] = self.ticket_info_current_divide[seat_number[i]]

        self.start_time = self.ticket_info_current_divide[8]
        self.end_time = self.ticket_info_current_divide[9]
        self.start_station = self.ticket_info_current_divide[6]
        self.end_station = self.ticket_info_current_divide[7]

        self.first_station = self.ticket_info_current_divide[4]
        self.last_station = self.ticket_info_current_divide[5]

        self.during_time = self.ticket_info_current_divide[10]

        self.train_short_number = self.ticket_info_current_divide[3]
        self.train_long_number = self.ticket_info_current_divide[2]

        self.train_state = self.ticket_info_current_divide[1]
        self.seat_type = self.ticket_info_current_divide[35]

        self.depart_date = self.ticket_info_current_divide[13]
        self.depart_date = self.depart_date[0:4] + '-' + \
            self.depart_date[4:6] + '-' + self.depart_date[6:]

        self.start_station_chinese = Urlconf().getStationName(
            self.start_station)
        self.end_station_chinese = Urlconf().getStationName(
            self.end_station)
        self.first_station_chinese = Urlconf().getStationName(
            self.first_station)
        self.last_station_chinese = Urlconf().getStationName(
            self.last_station)

        '''
        #print(self.start_time, self.end_time,
              Urlconf().getStationName(self.start_station),
              Urlconf().getStationName(self.end_station),
              Urlconf().getStationName(self.first_station),
              Urlconf().getStationName(self.last_station),
              self.during_time,
              self.train_short_number,
              self.train_long_number, self.seat_type)
        #print(self.left_tickets)
        '''

    def getDepatrStation(self):
        depart_train_field = {'train_no': self.train_long_number,
                              'from_station_telecode': self.start_station,
                              'to_station_telecode': self.end_station,
                              'depart_date': self.depart_date
                              }
        depart_url = Urlconf().getDepartUrl(depart_train_field)

        # HTTP200状态响应检测
        for i in range(5):
            try:
                depart_info = urllib.request.urlopen(
                    depart_url, timeout=5).read().decode('utf-8')
                break
            except:
                continue
        try:
            depart_info_json = json.loads(depart_info)['data']['data']
        except:
            #print('Decode Depart Info Error.')
            return -1
        # #print(depart_info_json)

        for depart_station_single in depart_info_json:
            # print(depart_station_single)
            self.depart_station.append([depart_station_single['station_no'],
                                        depart_station_single['station_name'],
                                        depart_station_single['arrive_time'],
                                        depart_station_single['start_time'],
                                        depart_station_single['stopover_time']])

            if depart_station_single['station_name'] == Urlconf().getStationName(self.start_station):
                self.start_station_number = depart_station_single['station_no']
                # #print(self.start_station_number)
                continue

            if depart_station_single['station_name'] == Urlconf().getStationName(self.end_station):
                self.end_station_number = depart_station_single['station_no']
                # #print(self.end_station_number)
                continue
        return 0

    def addDepartDatabase(self):
        data_base = sqlite3.connect('Tickets.db')
        data_cursor = data_base.cursor()
        for i in range(5):
            try:
                data_cursor.execute('''CREATE TABLE '%s' (
                                    STATIONNUMBER TEXT,
                                    STATIONNAME TEXT,
                                    ARRIVETIME TEXT,
                                    STARTTIME TEXT,
                                    STOPOVERTIME TEXT)''' % ('D' + self.time_stamp + self.train_short_number))
                for depart in self.depart_station:
                    data_cursor.execute('''INSERT INTO '%s' VALUES( '%s' , '%s' , '%s' , '%s' , '%s'
                                        )''' % ('D' + self.time_stamp + self.train_short_number,
                                                depart[0], depart[1], depart[2], depart[3], depart[4]))
                #print('Table Operation Correct.')
                # 增加数据库处理完成信号
                break
            except:
                #print("Table Operation Error.")
                time.sleep(2)
                continue

        data_base.commit()
        data_base.close()
        return 0

    def getTicketPrice(self):

        price_field = {'train_no': self.train_long_number,
                       'from_station_no': self.start_station_number,
                       'to_station_no': self.end_station_number,
                       'seat_types': self.seat_type,
                       'train_date': self.depart_date}
        price_url = Urlconf().getPriceUrl(price_field)

        for i in range(5):
            try:
                price_info = urllib.request.urlopen(
                    price_url, timeout=5).read().decode('utf-8')
                break
            except:
                continue

        try:
            price_info_seat = json.loads(price_info)['data']
        except:
            #print('Get Price Error.')
            return -1

        seat_code = dict(zip(['商务座', '一等座', '二等座', '动卧', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座'],
                             ['A9', 'M', 'O', 'F', 'A6', 'A4', 'A3', 'A2', 'A1', 'WZ']))

        for seat_name in seat_code:
            self.seat_price[seat_name] = price_info_seat.get(
                seat_code[seat_name], '')
            #print(seat_name, self.seat_price[seat_name])

        return 0

    def addPriceDatabase(self):
        data_base = sqlite3.connect('Tickets.db')
        data_cursor = data_base.cursor()
        for i in range(5):
            try:
                data_cursor.execute('''CREATE TABLE '%s' (
                                    SHANGWUZUOPRICE TEXT,
                                    YIDENGZUOPRICE TEXT,
                                    ERDENGZUOPRICE TEXT,
                                    DONGWUPRICE TEXT,
                                    GAOJIRUANWOPRICE TEXT,
                                    RUANWOPRICE TEXT,
                                    YINGWOPRICE TEXT,
                                    RUANZUOPRICE TEXT,
                                    YINGZUOPRICE TEXT,
                                    WUZUOPRICE TEXT)''' % ('P' + self.time_stamp + self.train_short_number))

                data_cursor.execute('''INSERT INTO '%s' VALUES( '%s' , '%s' , '%s' , '%s' , '%s', '%s', '%s', '%s', '%s', '%s'
                                        )''' % ('P' + self.time_stamp + self.train_short_number,
                                                self.seat_price['商务座'], self.seat_price['一等座'], self.seat_price[
                                                    '二等座'], self.seat_price['动卧'], self.seat_price['高级软卧'],
                                                self.seat_price['软卧'], self.seat_price['硬卧'], self.seat_price['软座'], self.seat_price['硬座'], self.seat_price['无座']))
                #print('Table Operation Correct.')
                # 增加数据库处理完成信号
                break
            except:
                #print("Table Operation Error.")
                time.sleep(2)
                continue

        data_base.commit()
        data_base.close()
        return 0


if __name__ == "__main__":
    #print("Just run ticket.py")
    Search()
