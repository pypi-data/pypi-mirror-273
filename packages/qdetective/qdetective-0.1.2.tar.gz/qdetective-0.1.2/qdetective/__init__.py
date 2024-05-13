# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 08:53:25 2023

@author: Suliang

Email: suliang_321@sina.com

TO: QDer, GO GO GO!

"""

__version__ = '0.1.2'

import csv
import paramiko
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import datetime as dt

from tqdm import tqdm


class DataChannel():
    def __init__(self, username, password, host='8.tcp.cpolar.cn', port=10008):
        """
        host: SFTP服务器地址
        port: 端口
        username: 账号
        password: 密码
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = 10008
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 这句话很重要，否则无法识别
            ssh.connect(self.host, self.port, self.username, self.password)
            ssh.close()
            print("【{}】已成功链接服务器...有问题请联系suliang".format(username))
            self.get_factor_info()
        except:
            print("服务器下线，请联系管理员")
            ssh.close()
    
    def get_factor_info(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 这句话很重要，否则无法识别
        ssh.connect(self.host, self.port, self.username, self.password)
        sftp = ssh.open_sftp()
        
        # 获取当前可供现在的因子列表
        factor_list = sftp.listdir('/【量化大侦探】因子库')
        # result = pd.DataFrame(index=pd.Series(factor_list, name='因子名称'))
        result = []
        for factor_name in tqdm(factor_list, '正在检索因子库，请稍后...'):
            file_list = sorted([x.split(' ')[-1].split('.')[0] for x in sftp.listdir('【量化大侦探】因子库/{}'.format(factor_name))])
            if len(file_list) == 0:
                continue
            result.append((factor_name, min(file_list), max(file_list)))
            # result.loc[factor_name, '起始日期'], result.loc[factor_name, '最新日期'] = min(file_list), max(file_list)
        
        result = pd.DataFrame(result, columns=['因子名称', '起始日期', '最新日期']).set_index(['因子名称'])
        self.contents = result
        ssh.close()
        return None
    
    def get_factor(self, factor_name, start_date='20180101', end_date=None):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 这句话很重要，否则无法识别
        ssh.connect(self.host, self.port, self.username, self.password)
        sftp = ssh.open_sftp()
        
        
        # 下载因子数据
        def read_file(sftp, remotepath):
            with sftp.open(remotepath) as csvfile:
                data = pd.DataFrame(csv.DictReader(csvfile))
            data = data.set_index(['﻿证券代码'])['因子暴露']
            return data
        
        # 获取因子历史样本的日期列表
        date_list = pd.Series([x.split('.')[0] for x in list(sftp.listdir(r'/【量化大侦探】因子库/{}'.format(factor_name)))])
        
        if end_date is None:
            end_date = dt.datetime.now().strftime('%Y%m%d')   # 取当前最新一期
            temp_date_list = sorted(date_list[(date_list>=start_date)&(date_list<=end_date)])
        elif isinstance(end_date, list):
            temp_date_list = sorted(set(end_date).intersection(set(date_list)))
        else:
            temp_date_list = sorted(date_list[(date_list>=start_date)&(date_list<=end_date)])
        
        try:
            # 读取数据, 速度可能偏慢
            result = []
            for date in tqdm(temp_date_list):
                result.append(read_file(sftp, r'/【量化大侦探】因子库/{}/{}.csv'.format(factor_name, date)))
            result = pd.concat(result,keys=temp_date_list,names=['日期']).reset_index().set_index(['日期', '﻿证券代码'])['因子暴露'].unstack()
        except PermissionError:
            print('权限错误，无法提取该因子，请与管理员联系！')
        
        ssh.close()
        return result
    
    def download_file(self, remotepath, localpath):
        """
        remotepath: 远程路径
        localpath: 本地路径
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 这句话很重要，否则无法识别
        ssh.connect(self.host, self.port, self.username, self.password)
        sftp = ssh.open_sftp()
        
        sftp.get(remotepath, localpath)
        
        ssh.close()
        return None
    
    def upload_file(self, remotepath, localpath):
        """
        remotepath: 远程路径
        localpath: 本地路径
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 这句话很重要，否则无法识别
        ssh.connect(self.host, self.port, self.username, self.password)
        sftp = ssh.open_sftp()
        
        sftp.put(localpath, remotepath)
        
        ssh.close()
        return None

    

if __name__ == '__main__':
    pass
    
    
