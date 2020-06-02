#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/5/9 11:50
# @Author: Jtyoui@qq.com
from pyunit_calendar import *

"""单元测试"""


def test_BatchCalendar():
    """测试天干地支转化日历"""

    bc = BatchCalendar()
    print('-----------------------------')
    # 农历
    print(bc.ctc_to_sc('1984年闰十月初三'))  # 农历转阳历 1984年11月25日
    print(bc.ctc_to_td('1984年闰十月初三'))  # 农历转天干地支 甲子年乙亥月癸亥日
    print('-----------------------------')
    # 阳历
    print(bc.sc_to_ctc('1984年11月25日'))  # 阳历转农历 1984年闰十月初三
    print(bc.sc_to_td('1984年11月25日'))  # 阳历转天干地支 甲子年乙亥月癸亥日
    print('-----------------------------')
    # 天干地支
    print(bc.td_to_ctc('甲子年乙亥月癸亥日'))  # 天干地支转农历:['1984年闰十月初三', '2044年九月廿一']
    print(bc.td_to_sc('甲子年乙亥月癸亥日'))  # 天干地支转阳历:['1984年11月25日', '2044年11月10日']


def test_CTC():
    """测试农历转阳历"""
    c = CTC(ctc_year=2017, ctc_mon=-6, ctc_day=8)  # 农历的日期2017年闰6月初八
    print(c.find_sc())  # 阳历：2017年7月30日
    print(c.get_year())  # 2017
    print(c.get_month())  # 7
    print(c.get_day())  # 30


def test_SC():
    """测试阳历转农历"""
    lun = SC(year=2019, month=8, day=14)
    print(lun.y)  # 农历的年,中文字符 二零一九
    print(lun.year)  # 农历的年，阿拉伯数字 2019
    print(lun.m)  # 农历的月份 中文字符 七
    print(lun.month)  # 农历的月份 阿拉伯字符 7
    print(lun.d)  # 农历的日期 中文字符 十四
    print(lun.day)  # 阳历的日期 阿拉伯数字 14 ，注意。和农历不一样
    print(lun.w)  # 星期几 中文字符
    print(lun.week)  # 星期几、英文字符
    print(lun.h)  # 节日
    print(lun)  # 二零一九年 七月 十四 星期四 无


def test_LSC():
    """测试简单快速的农历和阳历互转"""
    converter = LunarSolarDateConverter()
    lunar = converter.solar_to_lunar(SolarDate(2019, 12, 6))
    print(lunar)
    # {'isleap': False, 'lunarDay': 11, 'lunarMonth': 11, 'lunarYear': 2019}
    solar = converter.lunar_to_solar(LunarDate(2019, 11, 10))
    print(solar)
    # {'solarDay': 5, 'solarMonth': 12, 'solarYear': 2019}


if __name__ == '__main__':
    test_BatchCalendar()
    test_CTC()
    test_SC()
    test_LSC()
