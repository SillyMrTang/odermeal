# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     core
   Description :
   Author :       Administrator
   date：          2019/5/20 0020
-------------------------------------------------
   Change Activity:
                   2019/5/20 0020:
-------------------------------------------------
"""
import datetime
import requests
import json
import pymysql


class DataBaseHandle(object):
    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.password = pwd
        self.database = db
        self.port = port
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, self.port)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def select(self, sql):
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        print(sql)
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print('select db error', e)

        finally:
            self.cursor.close()

    def select_all(self, sql):
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print('select db error', e)

        finally:
            self.cursor.close()

    def update(self, sql):
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print('修改成功')
            self.close()
        except Exception as e:
            print('回滚', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def delete(self, sql):
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # 执行sql
            self.cursor.execute(sql)
            self.db.commit()
            print('删除成功')
            self.close()
        except Exception as e:
            print('回滚', e)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def close(self):
        self.db.close()

    def send_template(self, res):
        # res = [{'num': 1}, {'num': 2}, {'num': 3}]
        num = 0
        for i in res:
            num += int(i['num'])

        token = self.get_token()
        form = self.select('''SELECT * FROM form''')
        receiver = self.select('''SELECT * FROM template''')
        pk = receiver['user_id']
        user = self.select('SELECT * FROM user where id={}'.format(pk))
        print(user['openid'])
        if form is not None:
            formid = form['forId']
            self.delete('delete from form where id ={}'.format(form['id']))
            url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=' + token
            data = {
                'touser': user['openid'],
                'template_id': 'Ll1RZPUI6VaGyCOwjyh0y-VtwGsVmFx7-b4HUhX_PWY',
                'form_id': formid,
                'data': {
                    "keyword1": {
                        "value": {0: '早餐', 1: '午餐', 2: '晚餐'}[self.compare()]
                    },
                    "keyword2": {
                        "value": str(num) + '人'
                    },
                    "keyword3": {
                        "value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            }
            res = requests.post(url, json.dumps(data))
            print(res.json())
            return res.json()

        self.close()
        return {"errcode": 1}

    def get_token(self):
        print('get token ing')
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': 'wxf49edacad8eb4029',
            'secret': 'b8b72122f2a2b85ff7acc4c6a9251326'
        }
        res = requests.get(url, params=params)
        return res.json()['access_token']

    def compare(self):
        import datetime
        t1 = '06:00'
        t2 = '10:30'
        t3 = '16:00'
        now = datetime.datetime.now().strftime("%H:%M")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print("当前时间:" + date)
        if now <= t1:
            return 0
        elif t1 < now <= t2:
            return 1
        elif t2 < now <= t3:
            return 2
        else:
            return 2


def task():
    db = DataBaseHandle("127.0.0.1", "root", "mysql", "project", 3306)
    date = db.select_all('select * from reserve where status=1')
    res = list(date)
    if len(res) > 0:
        data = db.send_template(res)
        if data['errcode'] == 41029 or data['errcode']== 41028:
            task()
        elif data['errcode'] == 1:
            print('formId is None')

        else:
            print('success send')
    else:
        now = datetime.datetime.now().strftime("%H:%M")
        print('暂无----', now)


def task_two():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("修改状态 当前时间:" + date)
    db = DataBaseHandle("127.0.0.1", "root", "mysql", "project", 3306)
    db.update('update reserve set status=0 where status=1')


