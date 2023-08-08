import os
import re  # 正则表达式库
import collections  # 词频统计库
import numpy as np  # numpy库
import jieba  # 结巴分词
import jieba.analyse  # 导入关键字提取库
import pandas as pd
import wordcloud  # 词云展示库
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt  # 图像展示库
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts

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
    object_list = []  # 建立空列表用于存储分词结果
    for filename in os.listdir(path):
        # 读取文本数据
        string_data = pre_deal(path + '/' + filename)
        fn2 = open(r'stop.txt', encoding='utf-8')   #停词文本
        remove_words = fn2.read()
        fn2.close()
        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|一|:|;|\）|\（|\?|"|、|\s+')  # 建立正则表达式匹配模式
        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符串替换掉
        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=True)  # 精确模式分词[默认模式]
        for word in seg_list_exact:  # 迭代读出每个分词对象
            if word not in remove_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表

    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(10)  # 获取前10个频率最高的词
    for w, c in word_counts_top10:  # 分别读出每条词和出现从次数
        print(w, c)  # 打印输出
    # 词频展示
    mask = np.array(Image.open(r'../image/background.png'))  # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/msyh.ttc',  # 设置字体格式，不设置将无法显示中文
        mask=mask,  # 设置背景图
        background_color='white',    # 设置背景颜色为白色
        max_words=150,  # 设置最大显示的词数
        max_font_size=800  # 设置字体最大值
    )
    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.savefig('../image/word_cloud.png')   # 保存图片
    plt.show()  # 显示图像

    # 读入数据，需要更改
    # 可视化
    # 设置颜色
    color_series = ['#2C6BA0', '#2B55A1', '#2D3D8E', '#44388E', '#6A368B'
                    '#7D3990', '#A63F98', '#C31C88', '#D52178', '#D5225B',]
    # 实例化Pie类
    pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
    # 设置颜色
    pie1.set_colors(color_series)
    # 添加数据，设置饼图的半径，是否展示成南丁格尔图
    pie1.add("", word_counts_top10,
             radius=["30%", "135%"],
             center=["50%", "65%"],
             rosetype="area"
             )
    # 设置全局配置项
    # TitleOpts标题配置项
    # LegendOpts图例配置项  is_show是否显示图例组件
    # ToolboxOpts()工具箱配置项 默认项为显示工具栏组件

    pie1.set_global_opts(title_opts=opts.TitleOpts(title='词频 TOP 10'),
                         legend_opts=opts.LegendOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts())
    # 设置系列配置项
    # LabelOpts标签配置项  is_show是否显示标签；  font_size字体大小；
    # position="inside"标签的位置，文字显示在图标里面； font_style文字风格
    # font_family文字的字体系列
    pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                                   formatter="{b}:{c}次出现", font_style="italic",
                                                   font_weight="bold", font_family="Microsoft YaHei"
                                                   ),
                         )
    # 生成html文档
    pie1.render("../image/玫瑰图.html")
    print("玫瑰图保存成功！")

    print("-----" * 15)
    # print(df['创建者'].values.tolist())
    word_list = []
    time_list = []
    for w, c in word_counts_top10:
        word_list.append(w)
        time_list.append(c)

    bar = (
        Bar()
        .add_xaxis(word_list)
        .add_yaxis('词频排名前十的词对应的出现次数', time_list)
    )
    bar.render("../image/条形图.html")
    print("柱形图保存成功！")

