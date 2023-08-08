import xlrd
import xlwt
import os
from xlutils.copy import copy

class MusicspiderPipeline(object):
    def open_spider(self, spider):
        dir_path = "./lyrics"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    def process_item(self, item, spider):
        file_name = './lyrics/{}-{}.txt'.format(item['song_name'], item['singer_name'])
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(item['lyric'])

        # 初始化sheetname
        sheetnames = []
        filename = 'MUsicList.xls'
        # 判断是否存在写入文件，不存在则新建filename文件，存在则继续写入
        if os.path.exists(filename):
            file = xlrd.open_workbook(filename, formatting_info = True)

            nrows = file.sheet_by_name('网易云热歌榜').nrows
            summary = copy(file)
            sheet = summary.get_sheet('网易云热歌榜')
            style = self.setXlsStyle(sheet)
            sheet.write(nrows, 0, item['song_name'], style)
            sheet.write(nrows, 1, item['singer_name'], style)
            sheet.write(nrows, 2, item['song_url'], style)
            summary.save(filename)
        else:
            file = xlwt.Workbook()
            sheet = file.add_sheet('网易云热歌榜')
            style = self.setXlsStyle(sheet)
            sheet.write(0, 0, '歌曲名', style)
            sheet.write(0, 1, '歌手名', style)
            sheet.write(0, 2, '歌曲URLs', style)
            file.save(filename)

    # 设置表格格式
    def setXlsStyle(self, sheet):
        style = xlwt.XFStyle()

        al = xlwt.Alignment()
        al.horz = 0x01
        al.vert = 0x01
        style.Alignment = al

        font = xlwt.Font()
        font.name = u'微软雅黑'    	#字体
        font.bold = True            #加粗
        font.underline = False      #下划线
        font.italic = False         #斜体
        font.height = 200
        style.font = font

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 1
        style.pattern = pattern

        sheet.col(0).width = 6300
        sheet.col(1).width = 6300
        sheet.col(2).width = 12300

        return style

