#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/8 18:00
# @Author  : Jacob
# @File    : use_opening_chrome2



# os.popen() 方法在 Python 3.3 版本中被废弃，并在 Python 3.6 版本中移除

#命令行启动浏览器
# 接下来，在 CMD 终端中通过命令行启动 Chrome 浏览器
# 启动浏览器
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile" --window-size=1200,720

# 其中--remote-debugging-port指定浏览器调试端口号   PS：这里可以随机指定一个端口号，不要指定为已经被占用的端口号
# --user-data-dir指定用户配置文件目录，这里需要单独指定一个文件夹目录（不存在会新建），如果不显式指定该参数，运行会污染浏览器默认的配置文件


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os, re, time, random
import selenium
import subprocess


###***  先指定浏览器配置文件Chrome_file位置  ***###
CHROME_FILE_PATH = r'../Chrome/AutomationProfile'

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)





class ChromeWindows:
    def __init__(self, port, config_file=CHROME_FILE_PATH):
        self.port = port
        self.config_file = config_file

        self.is_runing = self.start()
        self.driver = self.use_opening_chrome()

    @property
    def windows(self):
        """
        获取当前所有窗口的句柄和默认名称
        :return: 包含窗口句柄和名称的列表
        """
        windows_info = []
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            windows_info.append({
                "handle": handle,
                "name": self.driver.title or "Unnamed Window",
                "url": self.driver.current_url or "No URL"
            })

        return windows_info


    def start(self, window_size={'width': 1200, 'height': 720}):
        """
        用CMD打开chrome浏览器
        :param port: 使用的端口号
        window_size:{'width':1200, 'height':720} 初始尺寸 宽度 默认1200 高度 默认720
        """
        width, height = window_size['width'], window_size['height']

        if selenium.webdriver.common.utils.is_connectable(self.port):
            print(f'\033[32m端口号为\033[90m {self.port} \033[32m的Chrome Brower正在运行\033[0m')
        else:
            cmd = f'start chrome --remote-debugging-port={self.port} --user-data-dir={self.config_file} --window-size={width},{height}'
            # os.popen(f'start chrome --remote-debugging-port={port} --user-data-dir={chrome_file} --window-size={width},{height}')

            subprocess.Popen(cmd, shell=True)
            print(f'\033[32m成功开启端口号为 \033[90m{self.port}\033[32m 的Chrome Brower \033[0m')
            print(f'\033[32m分辨率：\033[90m{width}*{height}\033[0m')


        driver = self.use_opening_chrome()

        return driver

    def use_opening_chrome(self):
        '''
        使用已经在运行的chrome浏览器
        :param port: 使用的端口号
        '''
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")
        driver = webdriver.Chrome(options=options)
        return driver


    def get_url(self, url, new_window=True):
        """
        打开一个网页，如果 new_window=True 则在新窗口中打开
        :param url: 要打开的网页的URL
        :param new_window: 是否在新窗口中打开URL，默认为True
        """
        if new_window:
            # 使用 JavaScript 打开一个新窗口
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            # 切换到最新打开的窗口
            self.driver.switch_to.window(self.driver.window_handles[-1])
        else:
            # 在当前窗口中打开 URL
            self.driver.get(url)

        print(f"\033[33m已打开 URL：\033[90m{url}\033[0m")


    def switch_to_window(self, handle=None, name=None, url=None):
        """
        根据 handle, name 或 url 切换到指定窗口
        :param handle: 窗口句柄
        :param name: 窗口名称
        :param url: 窗口 URL
        :return: 是否成功切换
        """
        for window in self.windows:
            if (handle and window["handle"] == handle) or \
                    (name and window["name"] == name) or \
                    (url and window["url"] == url):
                self.driver.switch_to.window(window["handle"])
                print(
                    f"\033[33m已切换到窗口 - Handle: \033[90m{window['handle']}\033[32m, Name: \033[90m{window['name']}\033[33m, URL: \033[90m{window['url']}\033[0m")
                return True
        print("\033[31m未找到符合条件的窗口\033[0m")
        return False

    def close_window(self):
        """
        关闭当前窗口，并切换到下一个窗口（如果有的话）
        """
        current_handle = self.driver.current_window_handle  # 获取当前窗口的句柄
        self.driver.close()  # 关闭当前窗口

        # 获取剩余窗口的句柄，切换到下一个窗口
        remaining_handles = self.driver.window_handles
        if len(remaining_handles) > 0:
            # 如果还有其他窗口，切换到第一个窗口
            next_handle = [handle for handle in remaining_handles if handle != current_handle][0]
            self.driver.switch_to.window(next_handle)
            print(f"\033[33m已关闭当前窗口，切换到窗口：{next_handle}\033[0m")
        else:
            print("\033[31m没有剩余窗口，当前窗口已关闭\033[0m")


    def execute_cdp_cmd(self):
        '''
        移除seLenium当中爬虫的特征,start后使用
        '''
        f = open('../Scripts/stealth.min.js', mode='r', encoding='utf-8').read()
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': f})


    def scroll(self, speed = 400, distance = 4000):
        '''
        滚动速度和滚动总距离
        '''
        for _ in range(distance // speed):
            self.driver.execute_script(f"window.scrollBy(0, {speed});")
            time.sleep(0.2)  # 等待一小段时间以控制滚动速度








def text_write(text,file_path,mode="a"):
    '''
    写入文件
    :param text:
    :param file_path:
    :param mode:
        "r": 读取模式，打开文件用于读取。
        "w": 写入模式，打开文件用于写入。如果文件已存在，则截断文件（即删除文件中的所有内容）。如果文件不存在，则创建新文件。
        "a": 追加模式，打开文件用于写入。如果文件已存在，则将数据写入文件末尾，而不是覆盖文件内容。如果文件不存在，则创建新文件。
        "b": 二进制模式，用于处理二进制文件（例如图片、音频等）。
        "x": 专门用于创建新文件的独占写入模式。如果文件已存在，则 FileExistsError 异常将被引发。
        这些模式可以组合使用，例如 "rb" 表示以二进制模式读取文件，"w+" 表示读写模式，如果文件不存在则创建。你可以根据具体的需求选择适当的模式。
    :param encoding:
        "UTF-8"
        "GBK"
    :return:
    '''
    # os.makedirs(file_path, exist_ok=True)

    with open(file_path, mode, encoding='utf-8') as file:
        if text is not None:
            file.write(text)
        else:
            file.write("")
# def text_write(text,file_path,mode="a",encoding='utf-8'):
#     '''
#     写入文件
#     :param text:
#     :param file_path:
#     :param mode:
#         "r": 读取模式，打开文件用于读取。
#         "w": 写入模式，打开文件用于写入。如果文件已存在，则截断文件（即删除文件中的所有内容）。如果文件不存在，则创建新文件。
#         "a": 追加模式，打开文件用于写入。如果文件已存在，则将数据写入文件末尾，而不是覆盖文件内容。如果文件不存在，则创建新文件。
#         "b": 二进制模式，用于处理二进制文件（例如图片、音频等）。
#         "x": 专门用于创建新文件的独占写入模式。如果文件已存在，则 FileExistsError 异常将被引发。
#         这些模式可以组合使用，例如 "rb" 表示以二进制模式读取文件，"w+" 表示读写模式，如果文件不存在则创建。你可以根据具体的需求选择适当的模式。
#     :param encoding:
#         "UTF-8"
#         "GBK"
#     :return:
#     '''
#     # os.makedirs(file_path, exist_ok=True)
#
#     with open(file_path, mode, encoding) as file:
#         if text is not None:
#             file.write(text)
#         else:
#             file.write("")



'''登录相关'''

def login_Manual(login_elements_tag):
    '''
    用于手动登录阻塞,需要提前获取登录元素
    '''
    if login_elements_tag:
        input('可能需要登录，登录后按‘ENTER’继续！')



if __name__ == "__main__":
    win = ChromeWindows(port=1001)
    # print('window_handles',win.window_handles)
    print('windows',win.windows)
    driver = win.driver
    print(driver)
    # win.get_url('https://www.google.com')
    # # time.sleep(2)
    # print('windows',win.windows)
    # win.get_url("https://www.taobao.com")
    # print('windows',win.windows)

