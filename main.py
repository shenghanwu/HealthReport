from selenium import webdriver
import time
from twilio.rest import Client
#from PIL import Image
#import pytesseract

url = "http://xgsys.swjtu.edu.cn/SPCP/Web/UserLogin.aspx"
StudentId = "" # 学号
Name = "" # 姓名
StuCard = "" # 身份证后6位
codeInput = "" # 验证码(不用填)

class HealthReport:
    def __init__(self):
        chrome_driver = r'' # chromedriver路径
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        self.driver.get(url)
    
    def getCode(self): # 代替上面使用截图获取验证码的操作
        return self.driver.execute_script("return document.getElementById('code-box').textContent")
    
    def setLoginPage(self): # 登陆操作
        codeInput = self.getCode()
        self.driver.find_element_by_id('StudentId').send_keys(StudentId)
        self.driver.find_element_by_id('Name').send_keys(Name)
        self.driver.find_element_by_id('StuCard').send_keys(StuCard)
        self.driver.find_element_by_id('codeInput').send_keys(codeInput)
        time.sleep(1)
        self.driver.execute_script("SumbitVerify();")
        #self.driver.find_element_by_id('Submit').click()
    
    def report(self): # 由于服务器有缓存，只需要修改checkbox就可以
        time.sleep(3)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1]) # 获取当前页面的元素
        self.driver.find_element_by_id('Checkbox1').click()
        time.sleep(1)
        self.driver.find_element_by_id('Save_Btn').click()
        time.sleep(1)

# 使用Twilio发送提醒短信
class SendText:
    def __init__(self):
        account_sid = ''
        auth_token = ''
        self.client = Client(account_sid,auth_token)
        self.text_from = '' # 短信发送者
        self.text_to = '' # 短信接收者
    
    def sendMessage(self,body):
        self.client.messages.create(body=body,to=self.text_to,from_=self.text_from)

if __name__ == '__main__':
    health_report = HealthReport()
    send_text = SendText()
    try:
        health_report.setLoginPage()
        health_report.report()
        send_text.sendMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " 每日健康填报提交成功。")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " 每日健康填报提交成功。")
    except Exception:
        send_text.sendMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " 填报失败，请尽快检查。")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " 填报失败，可能在别处已提交。")
    health_report.driver.close()
