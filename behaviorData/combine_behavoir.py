# -*- coding: utf-8 -*-
"""
Created on Sat May 11 15:21:04 2019

@author: Ye
合并每个被试的行为数据，即8个block合并为一组
"""
import pandas as pd
import os
import logging


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  \
                    %(levelname)s - %(message)s')
file_src = r'E:\expdata\exp2\data'
output_src = ''
os.chdir(file_src)

trial_length = 66  # 每个block的试次数


def get_file_list(file_src):
    """
    获取待处理的文件名称.

    :param files_src: 输入路径
    """
    file_lists = []
    for foldername, subfolders, folders in os.walk(file_src):
        for i in folders:
            if i.endswith('csv'):
                file_lists.append(i)

    return file_lists


def generate_df(file):
    """ 
    生成汇总列表.

    :param file: 待处理文件
    """
    df2 = pd.DataFrame()
    df = pd.read_csv(file)[3:]

    df2['participant'] = [df['participant'].iloc[1]] * trial_length
    df2['block'] = pd.Series([int(file.split('.')[0][-1])] * trial_length)
    df2['correct'] = pd.Series(df['main_resp.corr']).reset_index(drop=True)
#    df2['secResp'] = df['sec_resp.corr']
    df2['rt'] = pd.Series(df['main_resp.rt']).reset_index(drop=True)
    df2['trigger'] = pd.Series(df['trigger']).reset_index(drop=True)

    return df2


def main():
    df_out = pd.DataFrame(columns=['participant', 'block', 'correct',
                                   'rt', 'trigger'])

    file_lists = get_file_list(file_src)
    for i in file_lists:
        df = generate_df(i)
        df_out = pd.concat([df_out, df])
        logging.debug(i + ' is finished!')

    df_out.to_excel('total.xlsx', index=False,)


if __name__ == '__main__':
    main()
