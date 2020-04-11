# 西南交通大学每日健康状况填报自动化脚本，支持短信通知填报状态
利用crontab自动化执行sh脚本，sh调用python来实现网页的自动化操作。
Python需要使用的包：selenium、twilio(用于短信通知，不需要可以不使用)

# 脚本包含的文件
main.py 操作执行的代码文件
repeat.sh sh脚本，用于调用python文件（crontab直接调用python可能会出现问题）
on_time_start.log 日志文件，用于记录脚本每日的执行结果
chromedriver Chrome的webdriver，selenium使用时需要调用

# 前期准备
下载selenium、twilio包
```
pip install selenium
pip install twilio
```

下载chromedriver（可以使用Firefox、IE等，但不推荐Safari，Safari会在crontab自动执行脚本时调用webdriver失败）
首先查看Chrome的版本，在Chrome中输入：chrome://version/
在 https://sites.google.com/a/chromium.org/chromedriver/home 下载对应Chrome版本的chromedriver，解压放到和代码相同的文件夹下。

# 网页执行代码更改
在main.py下修改以下内容：
```
StudentId = "" # 学号
Name = "" # 姓名
StuCard = "" # 身份证后6位
chrome_driver = r'' # chromedriver路径
```
在repeat.sh下修改以下内容：
```
cd 代码所在文件夹的路径
export DISPLAY=:0.0
python环境的绝对路径 main.py的绝对路径 >> on_time_start.log的绝对路径
```

# twilio短信消息提醒（不需要可以将相关代码注释掉）
twilio是一家提供SMS短信服务、电话服务等的公司，可以使用twilio向指定的手机发送指定的信息，0.03美元一条短信，给15.5美元的免费额度，足够很长时间的免费短信通知了。
首先在 https://www.twilio.com/ 上注册账号，按照流程验证手机号，选择SMS服务，在Dashboard中选择手机号用于向你发送短信。
选择完成之后在Dashboard页面会看到ACCOUNT SID和ACCOUNT TOKEN，这些需要在代码中使用。
修改main.py的下列代码：
```
account_sid = '' # ACCOUNT SID
auth_token = '' # ACCOUNT TOKEN
self.client = Client(account_sid,auth_token)
self.text_from = '' # 短信发送者，你选择的手机号
self.text_to = '' # 短信接收者，你自己的手机号
```

# crontab自动化脚本
由于crontab是Linux、MacOS的计划任务管理工具，Windows下需要使用请自行百度查找安装的方法。
在终端中输入 crontab -e进入编写自动化脚本，写入代码：
```
0 7 * * * repeat.sh的绝对路径
```
上述代码表示每日7:00自动化执行repeat.sh来实现自动填报的功能，如需更改填报的时间，请更改前两个数字。停止crontab脚本只需要crontab -e将所有编写的命令删除就可以了。

在MacOS下可能会出现无法使用crontab的问题，解决方案如下：
在终端中输入下列命令
```
# 定时任务统统由 launchctl 来管理的，看看 cron 任务有没有在里面
sudo launchctl list | grep cron 
# 有记录。查看一下启动项的配置
locate com.vix.cron
# 创建一个database
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.locate.plist
# 查看 /etc/crontab 是否存在
ls -alF /etc/crontab
# 创建该文件
sudo touch /etc/crontab
```
Windows和Linux下遇到的问题请自行百度解决。

推荐在使用前先执行一下python脚本看看是否正常执行。
