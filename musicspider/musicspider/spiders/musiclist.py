# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy
import sys

# 返回musicspider目录
sys.path.append('.\\.\\musicspider')
from musicspider.items import MusicspiderItem


def get_lyric(song_id):
    headers = {
        "user-agent": "Mozilla/5.0",
        "Referer": "http://music.163.com",
        "Host": "music.163.com"
    }
    if not isinstance(song_id, str):
        song_id = str(song_id)

    url = f"http://music.163.com/api/song/lyric?id={song_id}+&lv=1&tv=-1"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    json_obj = json.loads(r.text)
    return json_obj["lrc"]["lyric"]

class MusiclistSpider(scrapy.Spider):
    name = 'musiclist'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover/toplist?id=3778678']

    def parse(self, response):
        items = []

        # 获取歌手的名字
        js = response.xpath('//textarea[@id="song-list-pre-data"]')

        # 使用正则表达式提取其中的json
        pattern = re.compile('"artists":\[{.*?}]')

        jss = pattern.findall(js.extract()[0])

        pattern = re.compile('"name":".*?"')

        music_author_list = []

        for name in jss:

            names = pattern.findall(name)
            nn = ''
            for n in names:
                nn += n
            nn = nn.replace('""name":"', "@").replace('"name":"', "").replace('"', "")
            music_author = nn
            music_author = music_author.replace('@', '+')
            music_author_list.append(music_author)

        # 利用xpath获得歌曲的id和名字
        llist = response.xpath('//ul[@class="f-hide"]/li')

        music_url_list = response.xpath('//div/ul[@class="f-hide"]/li/a/@href').extract()
        music_name_list = []

        for music in llist:
            music_name = music.xpath('./a/text()').extract()[0]

            music_name_list.append(music_name)

        for i in range(len(music_author_list)):
            item = MusicspiderItem()
            item['song_url'] = 'https://music.163.com/' + music_url_list[i]
            item['song_name'] = music_name_list[i]
            item['singer_name'] = music_author_list[i]
            items.append(item)
        # 遍历排行榜URLS，获取歌单信息
        for item in items:
            yield scrapy.Request(url=item['song_url'], meta={'meta_1': item}, callback=self.second_parse)

    # 获取歌单信息
    def second_parse(self, response):
        items = []
        meta_1 = response.meta['meta_1']

        song_id = meta_1['song_url'].split('?')
        song_id = song_id[1][3:]
        lyrics = get_lyric(song_id)

        # 处理歌词，把时间戳去掉
        regex = re.compile(r"\[.*?\]")
        lyrics = regex.sub('', lyrics)


        item = MusicspiderItem()
        item['song_url'] = meta_1['song_url']
        item['song_name'] = meta_1['song_name']
        item['singer_name'] = meta_1['singer_name']
        item['lyric'] = lyrics

        yield item


