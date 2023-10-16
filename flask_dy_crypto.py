
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


    # 读取历史开单记录
    p = []
    with open("/root/upload_data/csv_from_chen.csv", 'r', encoding="UTF-8") as fr:
        reader = csv.reader(fr)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            p.append(line)
    res_data = pd.DataFrame(p)
    res_data['crypto_time'] = res_data.iloc[:,0]
    res_data['crypto_id'] = res_data.iloc[:,1]
    res_data['crypto_name'] = res_data.iloc[:,2]
    res_data['crypto_direction'] = res_data.iloc[:,3]
    res_data['crypto_type'] = res_data.iloc[:,4]
    res_data['crypto_open'] = res_data.iloc[:,5]
    res_data['crypto_win'] = res_data.iloc[:,6]
    res_data['crypto_loss'] = res_data.iloc[:,7]
    res_data = res_data.reset_index(drop=True)
    price_res = []
    for i in range(len(res_data)):
        crypto_time = res_data['crypto_time'][i]
        crypto_id = res_data['crypto_id'][i]
        crypto_name = res_data['crypto_name'][i]
        crypto_direction = res_data['crypto_direction'][i]
        crypto_type = res_data['crypto_type'][i]
        crypto_open = res_data['crypto_open'][i]
        crypto_win = res_data['crypto_win'][i]
        crypto_loss = res_data['crypto_loss'][i]
        price_res.append({'crypto_time':crypto_time,'crypto_id':crypto_id,'crypto_name':crypto_name,'crypto_direction':crypto_direction,'crypto_type':crypto_type,'crypto_open':crypto_open,'crypto_win':crypto_win,'crypto_loss':crypto_loss})


    res_dict = {'value':'correct','price_res':str(price_res)}
    ans_str = json.dumps(res_dict)

    return ans_str

if __name__ == '__main__':
    app.run("0.0.0.0", port=5070)


