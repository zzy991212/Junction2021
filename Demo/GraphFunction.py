# -*- coding:utf-8 -*-
import pymysql.cursors
import json
import base64

def handler (event, context):
    msg = json.loads(base64.b64decode(event["body"]))
    username = msg['user_name']
    opname = msg['option_name']
    ishide = msg['if_hide']
    body = {"ok":"yes"}
    # Connect to the database
    connection = pymysql.connect(host='124.70.94.106',
                                 user='root',
                                 password='Nokia666',
                                 db='cloud',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 检测用户名是否存在
            sql = "SELECT * FROM data \
                WHERE username = '%s'" % (username)
            cursor.execute(sql)
            result = cursor.fetchone()
            # 用户不存在
            if(result == None):
                body["ok"] = "no"
            else:
                sql = "INSERT INTO data (username, opname, ishide) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, opname, int(ishide)))
        if(body["ok"] == 'yes'):
            connection.commit()
    finally:
        connection.close()
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }