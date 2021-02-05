# -*- coding: utf-8 -*-
import datetime
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import traceback

import requests

import configparser


class Student:
    def __init__(self, id, password):
        self.id = id
        self.password = password

    def check_in(self):
        check_session = requests.session()
        ids_url = 'http://ids.hhu.edu.cn/amserver/UI/Login'
        check_url = 'http://form.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid=A335B048C8456F75E0538101600A6A04&userId=' + self.id
        info_url = 'http://form.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq'

        form_data = {
            'IDToken0': '',
            'IDToken1': '',
            'IDToken2': '',
            'IDButton': 'Submit',
            'goto': 'aHR0cDovL2Zvcm0uaGh1LmVkdS5jbi9wZGMvZm9ybS9saXN0',
            'encoded': 'true',
            'inputCode': '',
            'gx_charset': 'UTF-8'
        }

        check_data = {
        }

        req_header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }

        form_data['IDToken1'] = self.id
        form_data['IDToken2'] = self.password

        check_session.post(ids_url, headers=req_header, data=form_data)
        response = check_session.get(info_url)

        responselist = response.content.decode('utf-8').split("\n")

        for line in responselist:
            if ('fillDetail' in line):
                dic = json.loads("{" + line.split('[')[1].split(']')[0].split('},{')[1] + "}")
                break
        i = datetime.datetime.now()

        check_data['DATETIME_CYCLE'] = "%d/%02d/%02d" % (i.year, i.month, i.day)
        check_data['XGH_336526'] = dic['XGH_336526']
        check_data['XM_1474'] = dic['XM_1474']

        check_data['SFZJH_859173'] = dic['SFZJH_859173']
        check_data['SELECT_941320'] = dic['SELECT_941320']
        check_data['SELECT_459666'] = dic['SELECT_459666']
        check_data['SELECT_814855'] = dic['SELECT_814855']
        check_data['SELECT_525884'] = dic['SELECT_525884']
        check_data['SELECT_125597'] = dic['SELECT_125597']
        check_data['TEXT_950231'] = dic['TEXT_950231']
        check_data['TEXT_937296'] = dic['TEXT_937296']
        check_data['RADIO_853789'] = dic['RADIO_853789']
        check_data['RADIO_43840'] = dic['RADIO_43840']
        check_data['RADIO_579935'] = dic['RADIO_579935']
        check_data['RADIO_138407'] = dic['RADIO_138407']
        check_data['RADIO_546905'] = dic['RADIO_546905']

        check_data['RADIO_314799'] = dic['RADIO_314799']
        check_data['RADIO_209256'] = dic['RADIO_209256']
        check_data['RADIO_836972'] = dic['RADIO_836972']
        check_data['RADIO_302717'] = dic['RADIO_302717']
        check_data['RADIO_701131'] = dic['RADIO_701131']

        check_data['RADIO_438985'] = dic['RADIO_438985']
        check_data['RADIO_467360'] = dic['RADIO_467360']
        check_data['PICKER_956186'] = dic['PICKER_956186']
        check_data['TEXT_434598'] = dic['TEXT_434598']
        check_data['TEXT_515297'] = dic['TEXT_515297']
        check_data['TEXT_752063'] = dic['TEXT_752063']

        if check_data['TEXT_752063'] != 0:
            check_data['RADIO_138407'] = "否"

        response = check_session.post(check_url, headers=req_header, data=check_data)
        return response.content


class QQBot:
    def __init__(self, qq, mirai_authKey, mirai_url):
        self.qq = qq
        self.mirai_authKey = mirai_authKey
        self.mirai_url = mirai_url

    def Session_auth(self):
        form_data = {
        }

        req_header = {
            "Content-Type": "application/json"
        }

        form_data["authKey"] = self.mirai_authKey
        send_Session = requests.Session()
        req_res = send_Session.post(self.mirai_url + '/auth', data=json.dumps(form_data), headers=req_header)
        self.mirai_session = json.loads(req_res.content)['session']

    def Session_verify(self):
        form_data = {
        }

        req_header = {
            "Content-Type": "application/json"
        }

        form_data["sessionKey"] = self.mirai_session
        form_data["qq"] = int(self.qq)

        send_Session = requests.Session()
        form_data = json.dumps(form_data)
        req_res = send_Session.post(self.mirai_url + '/verify', data=form_data, headers=req_header)

    def Session_sendfriendmsg(self, messege, Targetqq):
        list = []
        form_data = {
        }

        req_header = {
            "Content-Type": "application/json"
        }

        form_data["sessionKey"] = self.mirai_session
        form_data["qq"] = Targetqq
        list.append({"type": "Plain", "text": messege + "\n"})
        form_data["messageChain"] = list
        send_Session = requests.Session()
        res = send_Session.get(self.mirai_url + "/friendList?sessionKey=" + self.mirai_session)
        form_data = json.dumps(form_data)
        print(form_data)
        req_res = send_Session.post(self.mirai_url + '/sendFriendMessage', data=form_data, headers=req_header)


class mail:
    def __init__(self, username, password, mailsvr, port, method):
        self.username = username
        self.password = password
        self.mailsvr = mailsvr
        self.port = port
        self.method = method

    def sendmsg(self, messege, receiver, subject):
        msg = MIMEText(messege, 'plain', 'utf-8')
        msg["from"] = self.username
        msg["to"] = receiver
        msg['Subject'] = Header(subject, 'utf-8')
        i = datetime.datetime.now()
        msg['Date'] = "%d/%02d/%02d" % (i.year, i.month, i.day)
        if self.method == "SSL":
            smtp = smtplib.SMTP_SSL()
        elif self.method == "PLAIN":
            smtp = smtplib.SMTP()
        smtp.connect(self.mailsvr, self.port)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.username, receiver, msg.as_string())
        smtp.quit()


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.conf')

    studentId = config.get('Student','studentId')
    studentPassword = config.get('Student','studentPassword')

    mailEnable = int(config.get('Mail','mailEnable'))
    if mailEnable == 1:
        sourceMail = config.get('Mail','sourceMail')
        dstMail = config.get('Mail','dstMail')
        mailPassword = config.get('Mail','mailPassword')
        mailSvr = config.get('Mail','mailSvr')
        mailPort = int(config.get('Mail','mailPort'))
        mailMethod = config.get('Mail','mailMethod')

    error = 'server_error'
    error_flag = False

    try:
        stu = Student(studentId, studentPassword)
        res = stu.check_in()
        resdict = json.loads(res.decode('utf-8'))
    except Exception:
        error = traceback.format_exc()
        error_flag = True
    if mailEnable == 1:
        send_mail = mail(sourceMail, mailPassword, mailSvr, mailPort,
                         mailMethod)
        if error_flag or not resdict['result']:
            send_mail.sendmsg('尊敬的' + stu.id + "打卡失败！请检查服务情况或联系管理员" + "\n" + error, dstMail, '打卡失败！')
        else:
            send_mail.sendmsg('尊敬的' + stu.id + "您今日的打卡已经成功", dstMail, '打卡成功！')

    # TODO:configure the mirai Bot framework
    # QB = QQBot(2984597389,"maria_fengcheng_aliyun",'http://localhost:8082')
    # QB.Session_auth()
    # QB.Session_verify()
    # QB.Session_sendfriendmsg(messege= "hello",Targetqq=1007430174)
