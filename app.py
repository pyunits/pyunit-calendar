# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/06/02 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
from flask import Flask, jsonify, request

from pyunit_calendar import CTC, SC, BatchCalendar
from pyunit_calendar.config import chinese_mon

app = Flask(__name__)
bc = BatchCalendar()


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' == requests.content_type:
            data = requests.form
        else:  # 无法被解析出来的数据
            raise Exception('POST的Content-Type必须是:application/x-www-form-urlencoded')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    return data


@app.route('/')
def hello():
    return jsonify(code=200, result='welcome to pyunit_calendar')


@app.route('/pyunit/calendar/LunarCalendar', methods=['POST', 'GET'])
def lunar_calendar():
    try:
        data = flask_content_type(request)
        year = int(data['year'])
        mon = int(data['month'])
        day = int(data['day'])
        c = CTC(ctc_year=year, ctc_mon=mon, ctc_day=day)
        sc = c.find_sc()  # 阳历：2017年7月30日
        y = c.get_year()  # 2017
        m = c.get_month()  # 7
        d = c.get_day()  # 30
        return jsonify(code=200, result={'date': sc, 'year': y, 'month': m, 'day': d})
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/calendar/SolarCalendar', methods=['POST', 'GET'])
def solar_calendar():
    try:
        data = flask_content_type(request)
        year = int(data['year'])
        mon = int(data['month'])
        day = int(data['day'])
        lun = SC(year=year, month=mon, day=day)
        y = lun.y  # 农历的年,中文字符 二零一九
        d = lun.d  # 农历的日期 中文字符 十四
        w = lun.w  # 星期几 中文字符
        h = lun.h  # 节日
        leap = '是' if lun.leap else '否'
        m = ('闰' + lun.m) if lun.leap else lun.m  # 农历的月份 中文字符 七
        return jsonify(code=200, result={'date': str(lun), 'year': y, 'month': m, 'day': d, 'week': w, 'holiday': h,
                                         'is_leap': leap})
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/calendar/BatchCalendar', methods=['POST', 'GET'])
def batch_calendar():
    try:
        result = {}
        lc, hs, sc = '', '', ''
        data = flask_content_type(request)
        date = data['date']
        message = date.replace('年', '').replace('月', '').replace('日', '')
        if message and isinstance(message, str):
            if message.isdigit():
                lc = bc.sc_to_ctc(date)  # 阳历转农历 1984年闰十月初三
                hs = bc.sc_to_td(date)  # 阳历转天干地支 甲子年乙亥月癸亥日
                sc = date
            elif set(chinese_mon).intersection(set(message)):
                sc = bc.ctc_to_sc(date)  # 农历转阳历 1984年11月25日
                hs = bc.ctc_to_td(date)  # 农历转天干地支 甲子年乙亥月癸亥日
                lc = date
            else:
                lc = bc.td_to_ctc(date)  # 天干地支转农历:['1984年闰十月初三', '2044年九月廿一']
                sc = bc.td_to_sc(date)  # 天干地支转阳历:['1984年11月25日', '2044年11月10日']
                hs = date
        result['LunarCalendar'] = lc
        result['HSTTB'] = hs
        result['SolarCalendar'] = sc
        return jsonify(code=200, result=result)
    except Exception as e:
        return jsonify(code=500, error=str(e))


if __name__ == '__main__':
    app.run(port=32768)
