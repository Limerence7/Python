import os
# scrapy 框架的运行
os.system("scrapy crawl musiclist")

# 进入 lyric_analyze 文件夹并运行 analyze.py 文件
os.system("cd lyric_analyze && python analyze.py")
# 进入 lyric_analyze 文件夹并运行 show_wordcloud.py 文件
os.system("cd lyric_analyze && python show_wordcloud.py")
