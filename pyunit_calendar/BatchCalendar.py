#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/5/10 9:15
# @Author: Jtyoui@qq.com
from urllib.request import urlretrieve
import zipfile
import hashlib
import os

"""
该方法属于大量日期转化。消耗内存为代价提高速度。该类只能查询1901-2099年。
"""
_CTC = {}
_TIANGAN_DIZHI = {}
_SC = {}


def _get_file_md5(file_path):
    """获取文件的MD5值

    :param file_path: 文件地址
    :return: MD5校验值
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path}文件不存在或者不是文件')
    hash_ = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        else:
            hash_.update(b)
    f.close()
    data = hash_.hexdigest()
    if data and isinstance(data, str):
        return data.upper()
    return ''


def _download_dev_tencent(file_path: str, username: str, package: str, save_path: str, md5: str):
    """下载数据

    下载数据在coding平台上

    :param file_path: 文件路径
    :param username: 账号
    :param package: 项目
    :param save_path: 保存文件在该文件夹
    :param md5: MD5校验值
    :return: 下载成功返回保存的地址
    """
    name = os.path.basename(file_path)
    url = f'https://dev.tencent.com/u/{username}/p/{package}/git/raw/master/{file_path}'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if os.path.isdir(save_path):
        save_path = os.path.join(save_path, name)
    urlretrieve(url, save_path)
    print('---------验证数据-------')
    if not os.path.exists(save_path):
        raise ConnectionRefusedError('下载失败！请检查网络。')
    elif _get_file_md5(save_path) != md5:
        print('下载失败、移除无效文件！')
        os.remove(save_path)
        return False
    else:
        print('\033[1;33m' + save_path)
    return save_path


def _unzip(zip_address, file_name, encoding='UTF-8'):
    """解压zip数据包

    :param zip_address: 压缩包的地址
    :param file_name: 压缩包里面文件的名字
    :param encoding: 文件的编码
    :return: 压缩包里面的数据：默认编码的UTF-8
    """
    f = zipfile.ZipFile(zip_address)
    fp = f.read(file_name)
    lines = fp.decode(encoding)
    return lines


def load_date(load_date_dir):
    global _CTC, _TIANGAN_DIZHI, _SC
    if not os.path.exists(load_date_dir + os.sep + 'date.zip'):
        _download_dev_tencent('date.zip', 'zhangwei0530', 'logo', load_date_dir, '79A5A43F33CA300CD2671DF1168B24E5')
    uz = _unzip(load_date_dir + os.sep + 'date.zip', 'date.txt')
    ls = uz.split('\r\n')
    for line in ls[:-1]:
        ctc, cs, td = line.split('\t')
        _CTC[ctc] = cs
        _SC[cs] = ctc
        if _TIANGAN_DIZHI.get(td):
            _TIANGAN_DIZHI[td].append(ctc)
        else:
            _TIANGAN_DIZHI[td] = [ctc]


def td_to_ctc(td):
    """天干地支纪年转农历

    :param td: 输入一个天干地支纪年
    :return: 农历
    """
    return _TIANGAN_DIZHI.get(td)


def td_to_sc(td):
    """天干地支纪年转阳历

    :param td: 输入一个天干地支纪年
    :return: 阳历
    """
    ctc = td_to_ctc(td)
    return [ctc_to_sc(c) for c in ctc]


def ctc_to_sc(ctc):
    """农历转阳历

    :param ctc: 农历
    :return: 阳历
    """
    return _CTC.get(ctc)


def ctc_to_td(ctc):
    """农历转天干地支

    :param ctc: 农历
    :return: 天干地支,找不到返回空
    """
    for td_, ctc_ in _TIANGAN_DIZHI.items():
        if ctc in ctc_:
            return td_
    return ''


def sc_to_ctc(sc):
    """阳历转农历

    :param sc: 阳历
    :return: 农历
    """
    return _SC.get(sc)


def sc_to_td(sc):
    """阳历转天干地支纪年

    :param sc: 阳历
    :return: 天干地支纪年
    """
    ctc = sc_to_ctc(sc)
    return ctc_to_td(ctc)
