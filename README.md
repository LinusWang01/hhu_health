## How to use

#### Deploy with docker（Recommended）

It is much easier to deploy this application with docker. First of all,pull image from repo:

`sudo docker pull registry.cn-shanghai.aliyuncs.com/icekingking/hhu_health:latest`

after that,write the config file `config.conf` ,here is an example：

```
[Student]
# the student ID of yourself in your school
studentId = 2001010101
# the password to log in to your school information portal
studentPassword = password
[Mail]
# Set mailEnable to 1 if you need to be notified of the execution result via email.if you don't got any smtp server,please set the mailEnable to 0 to disable the mailsend.
mailEnable = 1
# the email address to send mails
sourceMail = mail@163.com
# the email address to receive mails
dstMail = mail@qq.com
# the login password (or client authorization password, if set separately) of the mailbox to send mails
mailPassword = ICQAAABBBBCCCCC
# the SMTP server address of the mailbox to send mails
mailSvr = smtp.163.com
# the SMTP server port number of the mailbox to send mails.If you use a cloud computing service(PAAS) such as Aliyun,please use SSL protocol port
mailPort = 465
# The connection method of the SMTP server of the mailbox to send mails. Available values: SSL | PLAIN .If you use a cloud computing service(PAAS) such as Aliyun,please use SSL protocol
mailMethod = SSL
```

Then,run the image with docker:

`docker run --rm -v /etc/config.conf:/config.conf registry.cn-shanghai.aliyuncs.com/icekingking/hhu_health:latest`

Please edit the `/etc/config.conf` to the real absolute path of your config file. After run the docker,the target mailbox will receive a mail telling that you have checked in successfully.  

#### Deploy with Python(NOT Recommended)

Please deploy it with Python 3.6,other python version might be incompatible with this application. We have found that the Python 3.9 is incompatible. 

After you finish your config file,install the requirements and download the Python file to the same folder of config file. Then just run the Python file. 

#### Before register the crontab

Before register the crontab,run the docker manually to check the correction of config file. You might get some Exceptions from console or mail. Correct your config file with hints of exceptions. 

#### Register the crontab（Ubuntu）

We only provide the method of docker deployment.

edit the `/etc/crontab`，echo the following sentence to the last line：

`0  10   * * *   root    docker run --rm -v /etc/config.conf:/config.conf registry.cn-shanghai.aliyuncs.com/icekingking/hhu_health:latest`

Please edit the `/etc/config.conf` to the real absolute path of your config file. 

You can edit the second parameter `10` in the sentence to change the execution time.

Restart crontab after save the file:

`sudo systemctl restart cron`

Other Linux release version might have insignificant differences. 
