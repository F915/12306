# -*- coding: utf-8 -*-

import base64
import datetime
import io
import json
import re
import smtplib
import sqlite3
import sys
import time
import urllib

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from splinter import Browser

import UrlConfig


class Passengers(object):
    def __init__(self, state):
        self.session = requests.Session()
        self.time_stamp = state[0].strip()
        self.user_account = state[1].strip()
        self.user_password = state[2].strip()
        self.headers = {
            'Origin': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
        self.answer = str()

        self.login()

    def login(self):
        while(True):
            if self.checkCaptcha() == -1:
                continue
            break
        if self.loginAccount() == -1:
            self.loginError()
            return -1
        self.getPassengers()
        self.loginCorrect()

    def loginCorrect(self):
        file_state = open('BookResult.info', 'w')
        file_state.write('1')
        file_state.close()

    def setCookies(self):
        for i in range(5):
            try:

                self.session.get('https://kyfw.12306.cn/otn/index12306/getLoginBanner',
                                 headers=self.headers, verify=False, timeout=5)
                self.session.get('https://kyfw.12306.cn/otn/HttpZF/GetJS',
                                 headers=self.headers, verify=False, timeout=5)
                break
            except:
                continue
        #rail_id = self.session.get(UrlConfig.Urlconf().getRailIdUrl(),headers = self.headers,verify = False).content.replace("callbackFunction('",'').replace("')",'')
        # #print(rail_id)
        #rail_id = json.loads(rail_id)
        # self.session.cookies.set('RAIL_EXPIRATION',rail_id['exp'])
        # self.session.cookies.set('RAIL_DEVICEID',rail_id['dfp'])
        browser = Browser(headless=True)
        browser.visit('https://www.12306.cn')
        for i in range(10):
            try:
                print(browser.cookies['RAIL_DEVICEID'])
                print(browser.cookies['RAIL_EXPIRATION'])
                self.session.cookies.set(
                    'RAIL_EXPIRATION', browser.cookies['RAIL_EXPIRATION'])
                self.session.cookies.set(
                    'RAIL_DEVICEID', browser.cookies['RAIL_DEVICEID'])
                browser.quit()
                break
            except:
                time.sleep(1)

        return 0

    def loginError(self):
        file_state = open('BookResult.info', 'w')
        file_state.write('-1')
        file_state.close()
        return -1

    def getPassengers(self):
        for i in range(5):
            try:
                passenger_result = self.session.get(
                    UrlConfig.Urlconf().passengers_gate, headers=self.headers, verify=False, timeout=5)
                break
            except:
                continue

        # print(passenger_result.json())
        passenger_list = passenger_result.json()['data']['normal_passengers']
        data_base = sqlite3.connect('Tickets.db')
        data_base.execute('''CREATE TABLE '%s' (
                                    NAME TEXT,
                                    SEX TEXT,
                                    TYPE TEXT,
                                    IDNUMBER TEXT); ''' % ('L'+self.time_stamp))

        for passenger_single in passenger_list:
            print(passenger_single['passenger_name'], passenger_single['sex_name'],
                  passenger_single['passenger_type_name'], passenger_single['passenger_id_no'])
            data_base.execute('''INSERT INTO '%s' VALUES ('%s','%s','%s','%s'); ''' % (('L'+self.time_stamp),
                                                                                       passenger_single['passenger_name'],
                                                                                       passenger_single['sex_name'],
                                                                                       passenger_single['passenger_type_name'],
                                                                                       passenger_single['passenger_id_no']))

        data_base.commit()
        data_base.close()
        return 0

    def loginAccount(self):
        # self.session.cookies.set('RAIL_DEVICEID','MIsdPaqppYzfn0waUm7Uupzx-7M87oasExLubP4Q-6vgaDfcFXzLz_Z3a-g5uKDutx1xTVUx7hw9k-AJJtdSr7La1Cl_dBJLl-SOt0VyaoELljOw8SUqWeu-I9Lt4qsvLB7Ai1gcESbmqegLAqezZM6wivw9l8Us')
        # self.session.cookies.set('RAIL_EXPIRATION','1553840695363')
        #rail_id = self.session.get(UrlConfig.Urlconf().getRailIdUrl(),headers = self.headers,verify = False).text.replace("callbackFunction('",'').replace("')",'')
        # #print(rail_id)
        #rail_id = json.loads(rail_id)
        # self.session.cookies.set('RAIL_DEVICEID',rail_id['dfp'].strip())
        # self.session.cookies.set('RAIL_EXPIRATION',rail_id['exp'].strip())

        self.setCookies()
        #cookies = self.session.cookies.get_dict()
        # #print(cookies)

        login_field = {
            'username': self.user_account.strip(),
            'password': self.user_password.strip(),
            'appid': 'otn',
            'answer': self.answer.strip()
        }
        # #print(login_field)
        for i in range(5):
            try:
                login_result = self.session.post(UrlConfig.Urlconf(
                ).user_login_gate, data=login_field, headers=self.headers, verify=False, timeout=5)
                break
            except:
                continue
        # #print(login_result.text)
        # open('hahaha.html','wb').write(login_result.content)
        try:
            if login_result.json()['result_code'] == 0:
                print('恭喜您,登录成功!')
                self.setuamtk()
                return 0
            else:
                print('账号密码错误,登录失败!')
                return -1
        except:
            print('账号密码错误,登录失败!')
            ##print(self.session.post('https://kyfw.12306.cn/otn/login/conf',headers= self.headers,verify = False).text)

            return -1

    def setuamtk(self):
        for i in range(5):
            try:

                uamtk_field = {'appid': 'otn'}
                uamtk_result = self.session.post(UrlConfig.Urlconf(
                ).uamtk_gate, uamtk_field, headers=self.headers, verify=False, timeout=5)
                uamtk = uamtk_result.json()['newapptk']
                uam_client_field = {'tk': uamtk}
                uam_client_result = self.session.post(UrlConfig.Urlconf(
                ).uam_client, uam_client_field, headers=self.headers, verify=False, timeout=5)
                break
            except:
                continue
        # print(uam_client_result.json())
        return 0

    def checkCaptcha(self):
        captcha_position = self.getCaptchaImage()
        if captcha_position == -1:
            return -1
        else:
            return self.checkCaptchaAnswer(captcha_position)

    def checkCaptchaAnswer(self, captcha_position):
        post_field = {
            'answer': captcha_position,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        for i in range(5):
            try:
                check_result = self.session.post(UrlConfig.Urlconf(
                ).captcha_check_gate, data=post_field, headers=self.headers, verify=False, timeout=5)
                break
            except:
                continue

        # print(check_result.text)
        try:
            if check_result.json()['result_code'] == '4':
                print('验证码校验成功!')
                self.answer = captcha_position
                return 0
            else:
                print('验证码校验失败!')
                return -1
        except:
            print('验证码校验失败!')
            return -1

    def getCaptchaImage(self):
        while(True):
            try:
                captcha_get_url = UrlConfig.Urlconf().getCaptchaUrl()
                # print(captcha_get_url)
                captcha_image_file = self.session.get(
                    captcha_get_url, headers=self.headers, verify=False, timeout=5).content
                # #print(captcha_image_file)
                picture = open('pic.jpg', 'wb')
                picture.write(captcha_image_file)
                picture.close()
                #captcha_image = base64.b64encode(captcha_image_file)
                # #print(captcha_image)
                break
            except:
                continue
        captcha_position = self.getCaptchaAnswer(captcha_image_file)
        return captcha_position

    def getCaptchaAnswer(self, captcha_image):
        # #print(captcha_image)
        for times in range(10):
            try:

                # AutoChooseOne
                files = {'pic_xxfile': captcha_image}
                result_origin = self.session.post(
                    UrlConfig.Urlconf().auto_choose_captcha_one, files=files, timeout=5).text
                # #print(result_origin)
                result = re.search(
                    '<B>(.*?)</B>', result_origin).group(1).replace(' ', ',')
                # print(result)
                result_single = result.split(',')
                result_list = []
                captcha_image_position = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (
                    243, 50), '5': (22, 114), '6': (117, 94), '7': (167, 120), '8': (251, 105)}
                for i in result_single:
                    for j in captcha_image_position.keys():
                        if i == j:
                            result_list.append(captcha_image_position[j][0])
                            result_list.append(',')
                            result_list.append(captcha_image_position[j][1])
                            result_list.append(',')
                answer_reverse = ''
                for current_item in result_list:
                    answer_reverse += str(current_item)
                answer = answer_reverse[:-1]
                # print(answer)
                return answer
            except:
                try:
                    # AutoChooseTwo
                    post_field = {'base64': base64.b64encode(captcha_image)}
                    result = self.session.post(
                        UrlConfig.Urlconf().auto_choose_captcha_two, post_field).json()['res']
                    # #print(result)
                    answer = str()
                    for single_letter in result:
                        if single_letter != '(' and single_letter != ')':
                            answer += str(single_letter)
                    # print(answer)
                    return answer
                except:
                    continue
        if times == 10:
            return -1

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################


class Ordering(object):
    def __init__(self, interface, state):
        self.interface = interface  # 浏览器运行的方式：0 后台运行 1 前台运行
        self.totalFlush = 0
        self.startTime = time.time()
        self.seat_list = {'商务座': 'SWZ_', '一等座': 'ZY_', '二等座': 'ZE_', '高级软卧':'GR_' , '软卧': 'RW_', '动卧': 'SRRB_',
                          '硬卧': 'YW_', '软座': 'RZ_', '硬座': 'YZ_', '无座': 'WZ_', '其他': 'QT_'}
        self.seat_codes = {'商务座': '9', '一等座': 'M', '二等座': 'O',  '高级软卧':'6', '软卧': '4', '动卧': 'F',
                          '硬卧': '3', '软座': '2', '硬座': '1', '无座': '1'}
        self.state = state

        self.time_stamp = self.state[0].strip()
        self.user_account = self.state[1].strip()
        self.user_password = self.state[2].strip()
        self.start_station = self.state[3].strip()
        self.end_station = self.state[4].strip()
        self.depart_time = self.state[5].strip()
        self.train_number = self.state[6].strip()
        self.seat_chosed = self.state[7].strip()
        self.answer = None
        self.passenger_list = list()

        for i in range(8, len(self.state), 2):
            self.passenger_list.append(self.state[i].strip())

        if self.interface == 0:
            print('运行无界面chrome')
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            # self.driver = '' #驱动chrome浏览器进行操作
            print('运行有界面chrome')
            driver = webdriver.Chrome()
            #driver  =  webdriver.Firefox()
            driver.set_window_size(1200, 800)
            self.driver = driver  # 驱动chrome浏览器进行

        while(True):
            if self.startLogin() == -1:
                continue
            if self.getLoginStatus() == 0:
                break
        if self.addOrder() == -1:
            self.orderError()
            return
        self.orderCorrect()

    def startLogin(self):

        if self.getLoginStatus() != -1:
            return 0

        self.driver.get(UrlConfig.Urlconf().official_website)
        time.sleep(3)
        self.driver.get(UrlConfig.Urlconf().login_url)
        time.sleep(1)

        for i in range(5):
            try:
                self.driver.find_element_by_class_name("login-hd-account")
                break
            except:
                time.sleep(1)
                continue

        if i == 5:
            return -1

        account = self.driver.find_element_by_class_name("login-hd-account")
        account.click()
        userName = self.driver.find_element_by_id("J-userName")
        userName.send_keys(self.user_account)  # 12306账号
        passWord = self.driver.find_element_by_id("J-password")
        passWord.send_keys(self.user_password)  # 12306密码
        time.sleep(0.1)

        try:
            if self.getVerifyImage() == -1:
                return -1

            if self.getVerifyResult() == -1:
                return -1

            if self.clickVerification() == -1:
                return -1

        except Exception:
            return -1

        self.submit()

        # 判断登陆是否成功
        return self.getLoginStatus()

    def clickVerification(self):
        captcha_result = self.answer.split(',')
        try:
            Action = ActionChains(self.driver)
            for i in range(0, len(captcha_result), 2):
                Action.move_to_element(self.img_element).move_by_offset(
                    int(captcha_result[i])-146, int(captcha_result[i+1])-80).click()
                print(int(captcha_result[i]), int(captcha_result[i+1]))
                # move_to_element 将鼠标移动到指定的某个元素的位置
                # move_by_offset  指定鼠标移动到某一个位置，需要给出两个坐标为位置
            Action.perform()  # 执行之前的一系列动作
        except Exception as e:
            print(e)
            return -1

    def getVerifyImage(self):
        try:
            img_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "J-loginImg")))
        except Exception:
            print("网络开小差,请稍后尝试")
            return -1
        self.img_base64_str = img_element.get_attribute("src").split(",")[-1]
        self.img_data = base64.b64decode(self.img_base64_str)
        with open('verify.jpg', 'wb') as file:
            file.write(self.img_data)
            file.close()
        self.img_element = img_element
        return 0

    def getVerifyResult(self):
        '''
        files = {"pic_xxfile": ('verify.jpg', open('verify.jpg', 'rb'), 'image/jpeg')}
        response = requests.request("POST", url, data={"Content-Disposition": "form-data"}, files=files)
        result = []
        time.sleep(2)
        # print(response.text)
        # print(len(response.text))
        n = 0
        while len(response.text) <= 400:  # error_len: 278
            response = requests.request("POST", url, data={"Content-Disposition": "form-data"}, files=files)
            print(response.text)
            n += 1
            if n > 5:
                break

        for i in re.findall("<B>(.*)</B>", response.text)[0].split(" "):
            result.append(int(i) - 1)
        self.result = result
        print('从左到右从上到下编号依次为:0 1 2 3 4 5 6 7, 经过仔细揣摩-图片貌似选择第{}个，正在尝试登录～'.format(result))
        '''

        for times in range(5):
            try:
                print('I am in Method 1')
                # AutoChooseOne
                files = {'pic_xxfile': open('verify.jpg', 'rb')}
                result_origin = requests.post(
                    UrlConfig.Urlconf().auto_choose_captcha_one, files=files).text
                # #print(result_origin)
                result = re.search(
                    '<B>(.*?)</B>', result_origin).group(1).replace(' ', ',')
                print(result)
                result_single = result.split(',')
                result_list = []
                captcha_image_position = {'1': (30, 70), '2': (110, 70), '3': (190, 70), '4': (
                    250, 70), '5': (30, 130), '6': (110, 130), '7': (190, 130), '8': (250, 130)}
                for i in result_single:
                    for j in captcha_image_position.keys():
                        if i == j:
                            result_list.append(captcha_image_position[j][0])
                            result_list.append(',')
                            result_list.append(captcha_image_position[j][1])
                            result_list.append(',')
                answer_reverse = ''
                for current_item in result_list:
                    answer_reverse += str(current_item)
                answer = answer_reverse[:-1]
                print(answer)
                self.answer = answer
                return 0
            except:
                try:
                    print('I am in Method 2')
                    # AutoChooseTwo
                    post_field = {'base64': self.img_base64_str}
                    result = requests.post(
                        UrlConfig.Urlconf().auto_choose_captcha_two, post_field).json()['res']
                    print(result)
                    answer = str()
                    for single_letter in result:
                        if single_letter != '(' and single_letter != ')':
                            answer += str(single_letter)
                    print(answer)
                    self.answer = answer
                    return 0
                except:
                    continue
        if times == 5:
            return -1

    def submit(self):
        self.driver.find_element_by_id("J-login").click()
        print('Submit Answer')
        time.sleep(1)

    def getLoginStatus(self):
        time.sleep(0.5)
        user = None
        # self.driver.get('https://kyfw.12306.cn/otn/view/index.html')
        for i in range(5):
            try:
                self.driver.find_element_by_id('J-header-logout')
                user = self.driver.find_elements_by_xpath(
                    '//*[@id="J-header-logout"]/a[1]')[0].text
                break
            except:
                time.sleep(0.2)
                continue
        if i == 5:
            print('登录失败')
            return -1

        if user:
            if user == '登录':
                print('Login Error')
                return -1
            else:
                print('Login Correct')
                return 0
        else:
            print('Login Error')
            return -1

    def addOrder(self):
        for i in range(5):
            try:
                self.driver.get(UrlConfig.Urlconf().search_url)
                if self.driver.find_element_by_id("fromStationText") != None:
                    break
            except:
                time.sleep(1)
                continue
        # self.driver.navigate().to(self.search_url)
        self.driver.find_element_by_id("fromStationText").click()
        self.driver.find_element_by_id(
            "fromStationText").send_keys(self.start_station)
        o_InputSelect = self.driver.find_elements_by_class_name(
            "ralign")  # 获取局部刷新的数据，然后循环比对文字
        for i in o_InputSelect:  # 注意：如果不用这种方法，用输入回车来选择会出现  要选北京结果选到北京西  这类的
            if i.text == self.start_station:
                i.click()
                break
        self.driver.find_element_by_id("toStationText").click()
        self.driver.find_element_by_id(
            "toStationText").send_keys(self.end_station)
        o_InputSelect = self.driver.find_elements_by_class_name(
            "ralign")  # 获取局部刷新的数据，然后循环比对文字
        for i in o_InputSelect:  # 注意：如果不用这种方法，用输入回车来选择会出现  要选北京结果选到北京西  这类的
            if i.text == self.end_station:
                i.click()
                break

        # 出发日
        year = self.depart_time.split('-')[0]
        month = self.depart_time.split('-')[1]
        day = self.depart_time.split('-')[2]
        y = 4 if year == "2017" else 5 if year == "2018" else 6
        # m = int(month) - 1
        # d = int(day)-1
        m = int(month)
        d = int(day)
        for i in range(10):
            try:
                self.driver.find_element_by_id('date_icon_1')
                break
            except:
                time.sleep(1)
                continue

        WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable((By.ID, 'date_icon_1'))).click()
        self.driver.find_element_by_xpath("//div[@class='year']/input").click()
        self.driver.find_element_by_xpath(
            "//div[@class='year']/div/ul/li[%s]" % y).click()
        self.driver.find_element_by_xpath(
            "//div[@class='month']/input").click()
        self.driver.find_element_by_xpath(
            "//div[@class='month']/ul/li[%s]" % m).click()
        self.driver.find_element_by_xpath(
            "//div[@class='cal']/div[@class='cal-cm']/div[%s]/div" % d).click()
        try:
            for i in range(5):
                for j in range(5):
                    try:
                        self.driver.find_element_by_id("query_ticket").click()
                        time.sleep(0.5)
                        break
                    except Exception as e:
                        time.sleep(1)
                        continue
                time.sleep(1)
                # 找到相应的火车信息datatrain属性的tr标签
                element = self.driver.find_elements_by_xpath(
                    ".//tbody[@id = 'queryLeftTable']/tr")
                if element:
                    current_tr = self.driver.find_elements_by_xpath(
                        '//*[@datatran="' + self.train_number + '"]')
                    current_ge = self.driver.find_elements_by_xpath(
                        '//*[@datatran="' + self.train_number + '"]/preceding-sibling::tr[1]')
                    current_id = current_tr[0].get_attribute("id").split('_')[1]

                    id = self.seat_list[self.seat_chosed] + current_id
                    current_td = self.driver.find_element_by_id(
                        id).text
                    print(self.start_station, '至', self.end_station,
                          self.depart_time, self.train_number, self.seat_chosed, current_td)
                    if current_td != '无' and current_td != '--':
                        print('发现有余票啦！')
                        orderBotton = current_ge[0].find_element_by_class_name(
                            'btn72')
                        orderBotton.click()
                        # 等待所有的乘客信息被加载完毕
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, ".//ul[@id = 'normal_passenger_id']/li")))
                        # 获取所有的乘客信息
                        passanger_labels = self.driver.find_elements_by_xpath(
                            ".//ul[@id = 'normal_passenger_id']/li/label")
                        for passanger_label in passanger_labels:  # 遍历所有的label标签
                            name = passanger_label.text
                            if name in self.passenger_list:  # 判断名字是否与之前输入的名字重合
                                passanger_label.click()  # 执行点击选中操作
                        # 选择所需要的座席
                        seat_labels = self.driver.find_elements_by_xpath(".//tbody[@id = 'ticketInfo_id']/tr/td[3]/select/option[@value = '%s']" % self.seat_codes[self.seat_chosed])
                        for seat_label in seat_labels:  # 遍历所有的label标签
                            seat_label.click()
                        # 获取提交订单的按钮
                        submitBotton = self.driver.find_element_by_id(
                            'submitOrder_id')
                        submitBotton.click()
                        # 显示等待确人订单对话框是否出现
                        for k in range(10):
                            try:
                                self.driver.find_element_by_class_name(
                                    'dhtmlx_wins_body_outer')
                                break
                            except:
                                time.sleep(1)
                        # 显示等待确认按钮是否加载出现，出现后执行点击操作
                        for k in range(10):
                            try:
                                self.driver.find_element_by_id('qr_submit_id')
                                break
                            except:
                                time.sleep(1)
                                continue
                        ConBotton = self.driver.find_element_by_id(
                            'qr_submit_id')
                        ConBotton.click()
                        try:
                            while ConBotton:
                                ConBotton.click()
                                ConBotton = self.driver.find_element_by_id(
                                    'qr_submit_id')
                        except Exception as e:
                            pass
                        # 发送抢票成功邮件
                        return 0
                else:
                    print('网络好像开了小差，正在努力刷新～')
                    self.driver.refresh()  # 刷新页面
                    time.sleep(1)
                    continue
                return -1
        except Exception as e:
            # self.driver.quit()
            print('程序异常停止：')
            print(e)
            return -1

    def orderError(self):
        file_state = open('BookResult.info', 'w')
        file_state.write('-2')
        file_state.close()
        self.driver.quit()
        return -1

    def orderCorrect(self):

        file_state = open('BookResult.info', 'w')
        file_state.write('2')
        file_state.close()
        cookies = self.driver.get_cookies()
        print(cookies)
        print('运行有界面chrome')
        driver_payment = webdriver.Chrome()
        driver_payment.set_window_size(1200, 800)
        driver_payment.get(UrlConfig.Urlconf().ticket_order_url)
        driver_payment.delete_all_cookies()
        for cookie in cookies:
            driver_payment.add_cookie(cookie)

        # driver_payment.add_cookie(cookies)
        driver_payment.get(UrlConfig.Urlconf().ticket_order_url)
        self.driver.quit()
        return 0


#################################################################################################################################
#################################################################################################################################
#################################################################################################################################


class Checking(object):
    def __init__(self):
        self.time_stamp = str()
        self.check_method = 0

        while(True):
            if self.getNewState() == -1:
                continue
            if self.check_method == 3:
                self.getPassenger()
            else:
                self.orderTickets()

    def orderTickets(self):
        Ordering(0, self.state)

    def getPassenger(self):
        Passengers(self.state)

    def getNewState(self):
        try:
            file_state = open('BookRequest.info')
            state = file_state.readlines()
            file_state.close()
            if state[0].strip() == self.time_stamp:
                #print('No New Order')
                return -1
            else:
                self.check_method = len(state)
                self.time_stamp = state[0].strip()
                # print(state)
                # print(self.check_method)
                if self.check_method == 1:
                    return -1
                else:
                    self.state = state
                return 0
        except:
            return -1


if __name__ == '__main__':
    Checking()
