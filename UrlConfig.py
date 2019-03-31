# -*- coding: utf-8 -*-

import random
import urllib
import urllib.parse
import urllib.request


class Urlconf(object):
        # https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=2019-03-12&leftTicketDTO.from_station=XAY&leftTicketDTO.to_station=BJP&purpose_codes=ADULT
    search_gate = "https://kyfw.12306.cn/otn/leftTicket/query?"

    # https://kyfw.12306.cn/otn/leftTicket/queryTicketPriceFL?train_no=4g0000G6720D&from_station_no=05&to_station_no=17&seat_types=OM9&train_date=2019-03-12
    # https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=4g0000G6720D&from_station_no=05&to_station_no=17&seat_types=OM9&train_date=2019-03-12
    price_gate = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?"
    price_gate_pre = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPriceFL?"

    # https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=4g0000G6720D&from_station_telecode=EAY&to_station_telecode=BXP&depart_date=2019-03-12
    depart_gate = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"

    station_gate = "station_name.js"
    station_name_to_code = dict()
    station_code_to_name = dict()

    # captcha_get_gate = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.15905700266966694'
    captcha_get_gate = 'https://kyfw.12306.cn/passport/captcha/captcha-image?'
    captcha_check_gate = 'https://kyfw.12306.cn/passport/captcha/captcha-check'

    user_login_gate = 'https://kyfw.12306.cn/passport/web/login'

    passengers_gate = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

    uamtk_gate = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
    uam_client = 'https://kyfw.12306.cn/otn/uamauthclient'

    official_website = 'https://www.12306.cn/'

    auto_choose_captcha_one = 'http://littlebigluo.qicp.net:47720'
    auto_choose_captcha_two = 'https://12306.jiedanba.cn/api/v2/img_vcode/'

    rail_id_gate = 'https://kyfw.12306.cn/otn/HttpZF/logdevice?'

    submit_order_request = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'

    confirm_DC = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

    check_order_info_gate = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'

    queue_count_gate = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

    check_user_gate = 'https://kyfw.12306.cn/otn/login/checkUser'

    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'

    initmy_url = 'https://kyfw.12306.cn/otn/view/index.html'

    search_url = 'https://kyfw.12306.cn/otn/leftTicket/init'

    ticket_order_url = 'https://kyfw.12306.cn/otn/view/train_order.html'

    def getRailIdUrl(self):
        rail_id_field = {
            'timestamp': str(random.random())
        }
        rail_id_url = self.rail_id_gate + urllib.parse.urlencode(rail_id_field)
        return rail_id_url

    def getCaptchaUrl(self):
        captcha_field = {'login_site': 'E',
                         'module': 'login',
                         'rand': 'sjrand',
                         '': str(random.random())
                         }
        captcha_url = self.captcha_get_gate + \
            urllib.parse.urlencode(captcha_field)
        return captcha_url

    def getStationNameInfo(self):

        station_name_to_code = open(self.station_gate).read()
        station_name_divide = station_name_to_code.split('@')
        for station_name_origin in station_name_divide:
            # #print(station_name_origin)
            station_name_divide_single = station_name_origin.split('|')
            if len(station_name_divide_single) != 6:
                continue
            self.station_name_to_code[station_name_divide_single[1]
                                      ] = station_name_divide_single[2]
            self.station_code_to_name[station_name_divide_single[2]
                                      ] = station_name_divide_single[1]

    def getStationCode(self, station_name_chinese):
        self.getStationNameInfo()
        if station_name_chinese in self.station_name_to_code:
            return self.station_name_to_code[station_name_chinese]
        else:
            # print("No station name")
            return -1

    def getStationName(self, station_code):
        self.getStationNameInfo()
        if station_code in self.station_code_to_name:
            return self.station_code_to_name[station_code]
        else:
            # print("No station code")
            return -1

    def getSearchUrl(self, search_field):
        search_url = self.search_gate + urllib.parse.urlencode(search_field)
        return search_url

    def getDepartUrl(self, depart_field):
        depart_url = self.depart_gate + urllib.parse.urlencode(depart_field)
        return depart_url

    def getPriceUrl(self, price_field):
        price_url = self.price_gate + urllib.parse.urlencode(price_field)
        price_url_pre = self.price_gate_pre + \
            urllib.parse.urlencode(price_field)
        # 查询票价前要访问另一个虚假网关(不知道12306为什么要这样设计)
        try:
            urllib.request.urlopen(price_url_pre)
        except:
            pass
        return price_url


if __name__ == '__main__':
    # print("just run urlconfig")
    city_name = input("Input city name:")

    city = Urlconf()
    # print(city.getStationCode(city_name))
