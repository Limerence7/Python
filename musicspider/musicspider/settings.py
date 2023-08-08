BOT_NAME = 'musicspider'

SPIDER_MODULES = ['musicspider.spiders']
NEWSPIDER_MODULE = 'musicspider.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'musicspider.pipelines.MusicspiderPipeline': 300,
}
