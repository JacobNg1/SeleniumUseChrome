## 方便使用chrome自动化脚本

### pip安装

```commandline
pip install git+https://github.com/JacobNg1/SeleniumUseChrome.git #以包的形式安装
```
```commandline
from SeleniumUseChrome.actions import ChromeWindows, CHROME_FILE_PATH
CHROME_FILE_PATH = r'../Chrome/AutomationProfile' #指定Chrome配置文件路径
```


#### webdriver下载地址
```commandline
#旧版本
http://chromedriver.storage.googleapis.com/index.html 

#开发版
https://googlechromelabs.github.io/chrome-for-testing/#stable

```
下载完成后放到webdriver路径或者放到python的script目录