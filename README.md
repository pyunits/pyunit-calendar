# **pyUnit_calendar** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]


## 这是一个阳历转化农历的程序(注意该模块严重依赖时间,所以系统中的时间和时区必须是:中国北京时间和中国时区)
[![](https://img.shields.io/badge/Python-3.8-green.svg)](https://pypi.org/project/pyunit-calendar/2019.5.9/)
[![](https://img.shields.io/badge/项目-jtyoui.plunar-black.svg)](https://github.com/jtyoui/Jtyoui)

#### 介绍
Python版阳历转农历

#### 安装
    pip install pyunit-calendar

## 如果阳历和农历相互转换推荐使用
```python
from pyunit_calendar import LunarDate,LunarSolarDateConverter,SolarDate
if __name__ == "__main__":
    """测试简单快速的农历和阳历互转"""
    converter = LunarSolarDateConverter()
    lunar = converter.solar_to_lunar(SolarDate(2019, 12, 6))
    print(lunar)
    # {"isleap": False, "lunarDay": 11, "lunarMonth": 11, "lunarYear": 2019}
    solar = converter.lunar_to_solar(LunarDate(2019, 11, 10))
    print(solar)
    # {"solarDay": 5, "solarMonth": 12, "solarYear": 2019}
```

## 如果只有阳历转农历推荐使用
```python
from pyunit_calendar import SC
    
if __name__ == "__main__":
    lun = SC(year=2018, month=1, day=2) #阳历转农历
    print(lun.y)  # 农历的年,中文字符 二零一九
    print(lun.year)  # 农历的年，阿拉伯数字 2019
    print(lun.m)  # 农历的月份 中文字符 七
    print(lun.month)  # 农历的月份 阿拉伯字符 7
    print(lun.d)  # 农历的日期 中文字符 十四
    print(lun.day)  # 阳历的日期 阿拉伯数字 15 ，注意。和农历不一样
    print(lun.w)  # 星期几 中文字符
    print(lun.week)  # 星期几、英文字符
    print(lun.h)  # 节日
    print(lun)  # 二零一九年 七月 十四 星期四 无
```

## 如果只有农历转阳历推荐使用
```python
from pyunit_calendar import CTC
if __name__ == "__main__":
    c = CTC(ctc_year=2017, ctc_mon=-6, ctc_day=8)  # 农历的日期2017年闰6月初八
    print(c.find_sc())  # 阳历：2017年7月30日
    print(c.get_year())  # 2017
    print(c.get_month())  # 7
    print(c.get_day())  # 30

```

## 天干地支转日历(转阳历和农历)
```python
from pyunit_calendar import BatchCalendar

if __name__ == "__main__":
    bc=BatchCalendar() #下载数据
    print("-----------------------------")
    # 农历
    print(bc.ctc_to_sc("1984年闰十月初三"))  # 农历转阳历 1984年11月25日
    print(bc.ctc_to_td("1984年闰十月初三"))  # 农历转天干地支 甲子年乙亥月癸亥日
    print("-----------------------------")
    # 阳历
    print(bc.sc_to_ctc("1984年11月25日"))  # 阳历转农历 1984年闰十月初三
    print(bc.sc_to_td("1984年11月25日"))  # 阳历转天干地支 甲子年乙亥月癸亥日
    print("-----------------------------")
    # 天干地支
    print(bc.td_to_ctc("甲子年乙亥月癸亥日"))  # 天干地支转农历:["1984年闰十月初三", "2044年九月廿一"]
    print(bc.td_to_sc("甲子年乙亥月癸亥日"))  # 天干地支转阳历:["1984年11月25日", "2044年11月10日"]
```

## Docker安装(注意该模块严重依赖时间,所以系统中的时间和时区必须是:中国北京时间和中国时区)
    docker pull pyunit-calendar
    docker run -P -v /etc/timezone:/etc/timezone -v /etc/localtime:/etc/localtime -d pyunit-calendar


### 农历转阳历
|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|year|int|YES|输入阿拉伯数字的年|
|month|int|YES|输入阿拉伯数字的月(如果是闰月前面添加负号:如-4表示闰4月)|
|day|int|YES|输入阿拉伯数字的日|

### 请求示例
> #### Python3 Requests测试
```python
import requests

url = "http://127.0.0.1:32768/pyunit/calendar/LunarCalendar"
data = {
    "year": 2020,
    "month": -4,
    "day": 11
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, data=data, headers=headers).json()
print(response)
``` 

> #### 返回结果
```json
{
	"code": 200,
	"result": {
		"date": "2020年6月2日",
		"day": "2",
		"month": "6",
		"year": "2020"
	}
}
```

### 阳历转农历
|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|year|int|YES|输入阿拉伯数字的年|
|month|int|YES|输入阿拉伯数字的月|
|day|int|YES|输入阿拉伯数字的日|

### 请求示例
> #### Python3 Requests测试
```python
import requests

url = "http://127.0.0.1:32768/pyunit/calendar/SolarCalendar"
data = {
    "year": 2020,
    "month": 6,
    "day": 2
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, data=data, headers=headers).json()
print(response)
``` 

> #### 返回结果
```json
{
	"code": 200,
	"result": {
		"date": "二零二零年 闰四月 十一 星期二 节日：无",
		"day": "十一",
		"holiday": "无",
		"is_leap": "是",
		"month": "闰四",
		"week": "星期二",
		"year": "二零二零"
	}
}
```

### 天干地支和农历和阳历相互转日期
|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|date|string|YES|输入当前的日期:可以输入三种格式,具体看请求示例|

### 请求示例
> #### Python3 Requests测试
```python
import requests

url = "http://127.0.0.1:32768/pyunit/calendar/BatchCalendar"
data = {
    "date": '2020年四月十一',  # 农历格式:阿拉伯数字+年+中文数字+月+中文数字
    # "date": "2020年05月03日",  # 农历格式:阿拉伯数字+年+阿拉伯数字+月+阿拉伯数字+日
    # "date": "庚子年庚辰月丙午日",  # 农历格式:天干地支+年+天干地支+月+天干地支+日
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, data=data, headers=headers).json()
print(response)
``` 

> #### 返回结果
```json
{
	"code": 200,
	"result": {
		"HSTTB": "庚子年庚辰月丙午日",
		"LunarCalendar": "2020年四月十一",
		"SolarCalendar": "2020年05月03日"
	}
}
```

[1]: https://blog.jtyoui.com