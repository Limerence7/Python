import scrapy

class MusicspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 歌曲名，歌手名和歌曲url
    song_name = scrapy.Field()
    singer_name = scrapy.Field()
    song_url = scrapy.Field()
    lyric = scrapy.Field()

    pass
