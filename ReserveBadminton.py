import os
import time
from os import environ

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yagmail
import argparse
import datetime
from aip import AipOcr
from PIL import Image
""" 你的 APPID AK SK """
APP_ID = '24002442'
API_KEY = 'iKWWVACyiiMoMiUEYto8Gbac'
SECRET_KEY = 'QTQS4OIpWnrbiYGG5sDQ6ihvmXY3zKXF'


def login(username, password, browser):
    url = "https://uis.fudan.edu.cn/authserver/login"

    #先登录
    browser.get(url)

    browser.find_element_by_name("username").send_keys(username)
    browser.find_element_by_name("password").send_keys(password)
    sleep(17)
    #?
    if os.name != 'nt':
        browser.find_element_by_xpath("//*[@id='idcheckloginbtn']").click()
    url = "https://elife.fudan.edu.cn/public/front/search.htm?id=2c9c486e4f821a19014f82381feb0001"

    browser.get(url)
    
    browser.find_element_by_xpath("//*[@id='login_table_div']/div[2]/input").click()

def get_browser():
    chrome_options = Options()
    # headless本地报错
    if os.name != 'nt':
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    if os.name == 'nt':
        browser = webdriver.Chrome("C:\Github\科技强国\chrome\chromedriver.exe", chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    return browser

def get_account():
    # win10 本地测试
    if os.name == 'nt':
        try:
            with open("account.txt") as account:   
                username = account.readline()
                password = account.readline()
        except:
            print("FAK")
    # 在github上使用，系统是linux的话不要怪我
    else:
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
    return username, password

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_code(browser):
    xpath = '//*[@id="orderCommit"]/div/div[1]/div[2]/table/tbody/tr[5]/td[1]/img'
    img = browser.find_element_by_xpath(xpath)
    browser.save_screenshot('pictures.png')  # 全屏截
    page_snap_obj = Image.open('pictures.png')
    print(img)
    time.sleep(1)
    location = img.location
    size = img.size  # 获取验证码的大小参数
    print(img.size)
    print(img.location)
    left = 444#location['x']
    top = 518#location['y']
    right = 569#left + size['width']
    bottom = 550#top + size['height']
    image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    image_obj.show()  # 打开切割后的完整验证码

    image_obj = image_obj.convert("L")  # 转灰度图
    image_obj.save("new.png")
    image_obj = get_file_content('new.png')
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "false"
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    result = client.basicGeneral(image_obj)
   # print(result)
    return result

def reserve(browser, date, hour):
    for i in range(0, 5):
    #  url = "https://elife.fudan.edu.cn/login.jsp"
    #  url = "https://elife.fudan.edu.cn/public/front/myServices.htm?id=2c9c486e4f821a19014f82381feb0001"
        url = "https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=8aecc6ce749544fd01749a31a04332c2" + '&ordersId=&currentDate=2021-'+ date
        browser.get(url)
    # browser.find_element_by_xpath("//*[@id='login_table_div']/div[2]/input").click()
    # browser.find_element_by_xpath("/html/body/div/div/div[3]/table[2]/tbody/tr/td[2]/table/tbody/tr[5]/td/a").click()
        # 到羽毛球预约界面了。
        # 快进到正确日期
    #   current_url = browser.current_url
    #  url_2 = current_url 
    #  browser.get(url_2)
        time.sleep(10)
        #约个1600-1700的场
        #还得看看这玩意能约不
        xpth = "//*[font='" + hour + "']/../td[6]/img"
        flag = 0
        file = "[" + date + ',' + hour + "]"
        try: 
            ava = browser.find_element_by_xpath(xpth).get_attribute("src")
        except :
            file += "错误，请检查时间格式"
            return file, flag
        if(ava == 'https://elife.fudan.edu.cn/images/front/index/button/no.gif'):
            file += "指定时间已无空闲场次或您已预约"
            return file, flag

        # 进入预约场地
        browser.find_element_by_xpath(xpth).click()

        # 填写验证码
        
        
        
        imgCode = get_code(browser)#client.basicGeneral(img, options)

        print('识别出:')
        print(imgCode)
        ans = imgCode['words_result'][0]['words']
        browser.find_element_by_name("imageCodeName").send_keys(ans)


        #点击预约
        browser.find_element_by_xpath("//*[@id='btn_sub']").click()

        # 俺爷不知道咋验证
        if True:
            file += "预约成功"
            flag = 1
            return file, flag
    flag = 0
    file += '预约炸开'
    return file, flag


def writefile(res, path):
    with open(path, 'a') as f:
        f.write(res + '\n')

def send_mail(path, email):
    mail = yagmail.SMTP(
        user='fdureporter@163.com',
        password='WRSREHPSHPMOXCWM',
        host='smtp.163.com'
        )
    to = email
    with open(path, 'r') as f:
        content = f.read()
    mail.send(to = to, subject = '羽毛球预约', contents = content)

def get_time():
    # 获取0时区时间，变换为东八区时间
    # 原因：运行程序的服务器所处时区不确定
    t = datetime.datetime.utcnow()
    t = t + datetime.timedelta(hours=8)
    return t

def get_start_time(now_time):
    # 定在7点35分10秒搞事
    start_time = now_time.replace(hour = 7, minute = 35, second = 10)  
    return start_time

def to_time():
    now_time = get_time()
    print('现在时间是：北京时间')
    print(now_time)
    start_time = get_start_time(now_time)
    t = (start_time - now_time).total_seconds()
    print(str(t) + 's')
    if(t < 0):
        return 0
    else:
        return t

def main():
    if os.name != 'nt':
        badminton = os.environ['BADMINTON']
        if badminton != '1':
            return 0
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--day", default = "02")#默认周一周三
    parser.add_argument("--hour", default = "16:00")#默认1600-1700
    args = parser.parse_args()
    hour = args.hour
    day = args.day  
    days = []
    
    current_day = time.localtime()[6]

    path = './res.txt'
    
    print('get_browser')
    browser = get_browser()
    username, password = get_account()
    login(username, password, browser)
    """
    #格式：date: "11-24" hour: "16:00"
    """
    #date = "11-24"
    #hour = "16:00"
    flag = 0
    FLAG = 0 #FLAG = 1: 预约成功
    for ch in day:
        target_day = int(ch)
        x = (target_day - current_day + 7)%7
        if(x <= 3):
            date = (datetime.datetime.now() + datetime.timedelta(days = x)).strftime("%m-%d")
            print('尝试预约' , date, hour)
            res, flag = reserve(browser, date, hour)
            print(res)
            writefile(res, path)
            FLAG = FLAG + flag
    if FLAG:
        send_mail(path, os.environ['EMAIL'])

if __name__ == "__main__":
    time.sleep(max(to_time(), 0)) #不是不闹，时候未到
    main()
