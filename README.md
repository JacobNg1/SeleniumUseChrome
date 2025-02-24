## 方便使用chrome自动化脚本

### pip安装

```commandline
pip install git+https://github.com/JacobNg1/SeleniumUseChrome.git #以包的形式安装
```

###示例代码

```python
from SeleniumUseChrome.actions import ChromeWindows, CHROME_FILE_PATH, CHROMEDRIVER

#有三种方式指定配置文件和webdriver 全局环境、放到包里的正确位置，在代码路径写死，此处用写死

CHROME_FILE_PATH = r'D:\PythonProject\ISDP\Chrome\AutomationProfile' #指定Chrome配置文件路径
CHROMEDRIVER = r'D:\PythonProject\ISDP\webdriver\chromedriver-win64\chromedriver.exe'

C = ChromeWindows(port=1234, chromedriver=CHROMEDRIVER, config_file=CHROME_FILE_PATH)
driver = C.driver


C.get_url('https://www.baidu.com')
```


#### webdriver下载地址
```commandline
#旧版本
http://chromedriver.storage.googleapis.com/index.html 

#开发版
https://googlechromelabs.github.io/chrome-for-testing/#stable

```
下载完成后放到webdriver路径或者放到python的script目录
