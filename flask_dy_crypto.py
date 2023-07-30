
# coding: utf-8

import json
import base64
from flask import Flask, request
import requests
import numpy as np
import pandas as pd
import csv

app = Flask(__name__)


@app.route("/dy_crypto_chen", methods=['post'])
def dy_crypto_chen():
    date = request.form.get('date')
    api_key_value = request.form.get('api_key')
    order_value = request.form.get('order_value')
    ip_addr = request.remote_addr
    print(ip_addr)

    # 读取一个表，判断api_key 是不是在有效期内，有效的下单金额是多少
    p = []
    with open("/root/dy_data/base_information.csv", 'r', encoding="UTF-8") as fr:
        reader = csv.reader(fr)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            p.append(line)
    res_data = pd.DataFrame(p)
    res_data['api_key'] = res_data.iloc[:,0]
    res_data['end_date'] = res_data.iloc[:,1]
    res_data['api_type'] = res_data.iloc[:,3]
    res_data['ip_addr'] = res_data.iloc[:,6]

    api_key_judge = res_data[(res_data.api_key==api_key_value) & (res_data.ip_addr==ip_addr)]

    if len(api_key_judge) == 0:
        # 无效api，返回的都是不下单
        res_dict = {'value':'no_api','price_res':'no'}
        ans_str = json.dumps(res_dict)
    else:
        # 判断api是不是试用的，是不是在有效期
        api_key_judge = api_key_judge.reset_index()
        api_type = api_key_judge['api_type'][0]
        end_date = api_key_judge['end_date'][0]
        # 已经超时，返回不下单
        if pd.to_datetime(date) > pd.to_datetime(end_date):
            res_dict = {'value':'exit_date','price_res':'no'}
            ans_str = json.dumps(res_dict)
         # 试用期的api，不能超过200u
        elif api_type == 'shiyong' and int(order_value) >= 2200:
            res_dict = {'value':'exit_value','price_res':'no'}
            ans_str = json.dumps(res_dict)
        elif api_type == 'zhengshi' and int(order_value) >= 22000:
            res_dict = {'value':'exit_value','price_res':'no'}
            ans_str = json.dumps(res_dict)
        else:
            api_value = 'correct'
            # 读取历史开单记录
            p = []
            with open("/root/upload_date/csv_from_chen.csv", 'r', encoding="UTF-8") as fr:
                reader = csv.reader(fr)
                for index, line in enumerate(reader):
                    if index == 0:
                        continue
                    p.append(line)
            res_data = pd.DataFrame(p)
            res_data['crypto_name'] = res_data.iloc[:,0]
            res_data['crypto_direction'] = res_data.iloc[:,1]
            res_data['crypto_type'] = res_data.iloc[:,2]
            res_data['crypto_open'] = res_data.iloc[:,3]
            res_data['crypto_close'] = res_data.iloc[:,4]
            res_data = res_data.reset_index(drop=True)
            price_res = []
            for i in range(len(res_data)):
                crypto_name = res_data['crypto_name'][i]
                crypto_direction = res_data['crypto_direction'][i]
                crypto_open = res_data['crypto_open'][i]
                crypto_close = res_data['crypto_close'][i]
                price_res.append({'crypto_name':crypto_name,'crypto_direction':crypto_direction,'crypto_type':crypto_type,'crypto_open':crypto_open,'crypto_close':crypto_close})


            res_dict = {'value':api_value,'price_res':str(price_res)}
            ans_str = json.dumps(res_dict)

    return ans_str

if __name__ == '__main__':
    app.run("0.0.0.0", port=5070)


