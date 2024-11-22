import json
import time
import requests
import os
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from seleniumbase import Driver

from webdriver_manager.chrome import ChromeDriverManager

driver = Driver(uc=True, user_data_dir='C:\\selenium_data\\Chrome', port=54806)
driver.get("https://www.google.com")