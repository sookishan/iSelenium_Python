#!/usr/bin/env python
# -*- coding:utf-8 -*-
import configparser
import os
import time
import unittest

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


@allure.feature('Test Baidu WebUI')
# 继承unittest.TestCase这个类,使用unittest里面一些功能
class ISelenium(unittest.TestCase):
    # 读取配置文件
    # HOME目录每个机器不一样,home/username
    # getcwd()读取当前目录下的配置文件
    def get_config(self):
        config = configparser.ConfigParser()
        # print(os.getcwd())
        # config.read(os.path.join(os.environ['HOME'], 'iselenium.ini'))
        config.read(os.path.join(os.getcwd(), 'iselenium.ini'))
        return config

    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        # 读取配置
        config = self.get_config()
        # 使用浏览器运行的时候，可以采用有界面运行还是无界面运行
        # 无界面运行是看不到浏览器的打开，无界面的执行的好处不会收到桌面干扰
        # 控制是否采用无界面形式运行自动化测试
        try:
            # using_headless就是一个控制变量
            using_headless = os.environ["using_headless"]
            # using_headless = 'True'
        except KeyError:
            using_headless = None
            print('没有配置环境变量 using_headless，按照有界面方式运行自动化测试')

        chrome_options = Options()
        if using_headless is not None and using_headless.lower() == 'true':
            print('使用无界面方式运行')
            # 添加浏览器参数，控制浏览器是无界面还是有界面
            chrome_options.add_argument("--headless")
            # 去掉提示受到自动软件控制提示，防止百度弹验证码
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(executable_path=config.get('driver', 'chrome_driver'), options=chrome_options)

    @allure.story('Test key word 今日头条')
    def test_webui_1(self):
        """
                测试用例2 验证‘今日头条’关键词在百度上的搜索结果
                :return:
                """
        self._test_baidu('今日头条', 'test_webui_1')

    @allure.story('Test key word 王者荣耀')
    def test_webui_2(self):
        """
        测试用例2 验证‘王者荣耀’关键词在百度上的搜索结果
        :return:
        """
        self._test_baidu('王者荣耀', 'test_webui_2')

    def _test_baidu(self, search_keyword, testcase_name):
        """
        测试百度搜索子函数
        :param search_keyword: 搜索关键词（str）
        :param testcase_name: 测试用例名（str）
        :return:
        """
        self.driver.get("https://www.baidu.com")
        print('打开浏览器，访问 www.baidu.com')
        time.sleep(5)
        assert f'百度一下' in self.driver.title

        elem = self.driver.find_element(By.ID, "kw")
        elem.send_keys(f'{search_keyword}')
        elem.send_keys(Keys.ENTER)
        time.sleep(5)
        print(f'搜索关键词~{search_keyword}')
        self.assertTrue(f'{search_keyword}' in self.driver.title, msg=f'{testcase_name}校验失败')





