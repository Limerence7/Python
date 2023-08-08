import os
import random

import jieba.analyse  # 导入关键字提取库
import pandas as pd  # 导入pandas
from pandas import ExcelWriter
import pyecharts.options as opts
from pyecharts.charts import Line

exclude_str = [':', "：", "「", "】", "（"]


def pre_deal(fn):
    filename = fn
    f = open(filename, 'r', encoding='utf-8')
    original = f.read()
    lyric_list = original.split('\n')[:-1]
    new_list = []
    for li in lyric_list:
        b = True
        for e_str in exclude_str:
            if e_str in li:
                b = False
                break
        if b:
            new_list.append(li)
    real_lyrics = ' '.join(new_list)
    f.close()
    return real_lyrics


if __name__ == '__main__':
    path = r'../lyrics'
    with ExcelWriter('../excel/lyric_analyze.xlsx') as writer:
        for filename in os.listdir(path):
            # 读取文本数据
            string_data = pre_deal(path + '/' + filename)

            # 关键字提取
            tags_pairs = jieba.analyse.extract_tags(string_data, withWeight=True, allowPOS=['ns', 'n', 'vn', 'v', 'a'],
                                                    withFlag=True)  # 提取关键字标签
            tags_list = []  # 空列表用来存储拆分后的三个值
            for i in tags_pairs:  # 打印标签、分组和TF-IDF权重
                tags_list.append((i[0].word, i[0].flag, i[1]))  # 拆分三个字段值
            if len(tags_list) <= 5:
                continue
            tags_pd = pd.DataFrame(tags_list, columns=['word', 'flag', 'weight'])  # 创建数据框
            song_name_list = filename.split('-')
            song_name = song_name_list[0]

            tags_pd.to_excel(writer,
                             sheet_name=song_name,
                             float_format='%.2f',  # 保留两位小数
                             na_rep='None')  # 空值的显示
            random.shuffle(tags_list)
            # x轴上的值
            datax = []
            # y轴上的值
            datay = []
            for x, y, w in tags_list:
                datax.append(x)
                w = ("%.4f" % w)
                datay.append(w)
            line = (
                Line()
                .add_xaxis(xaxis_data=datax)
                .add_yaxis(series_name=" ", y_axis=datay, symbol="arrow", is_symbol_show=True)
                .set_global_opts(title_opts=opts.TitleOpts(title=song_name + " 关键字权重"))
            )
            # 利用render()方法来进行图表保存
            line.render('../image/Line/' + song_name + '.html')
