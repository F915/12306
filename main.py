# -*- coding: utf-8 -*-

import base64
import datetime
import io
import json
import random
import re
import smtplib
import sqlite3
import sys
import threading
import time
import urllib
import urllib.parse
import urllib.request
from threading import Thread

import requests
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QFile, QThread
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from splinter import Browser

import MainWindow_UI
import Ordering
import Tickets
import UrlConfig
from Logging_UI import Ui_Logging
from UrlConfig import Urlconf


class MainUI(threading.Thread):
    def __init__(self):
        super(MainUI, self).__init__()

    def run(self):
        app = QApplication(sys.argv)

        window = MainWindow_UI.Ui_MainWindow()
        window.show()

        sys.exit(app.exec_())


class SearchTicket(threading.Thread):
    def __init__(self):
        super(SearchTicket, self).__init__()

    def run(self):
        Tickets.Search()


class CheckOrder(threading.Thread):
    def __init__(self):
        super(CheckOrder, self).__init__()

    def run(self):
        Ordering.Checking()


if __name__ == '__main__':
    ui = MainUI()
    search = SearchTicket()
    check = CheckOrder()

    book_result = open('BookResult.info', 'w')
    book_result.write('0')
    book_result.close()

    check_result = open('CheckResult.info', 'w')
    check_result.write('0')
    check_result.close()

    book_request = open('BookRequest.info', 'w')
    book_request.write('0')
    book_request.close()

    ticket_result = open('TicketRequest.info', 'w')
    ticket_result.write('0')
    ticket_result.close()

    ui.start()
    search.start()
    check.start()
