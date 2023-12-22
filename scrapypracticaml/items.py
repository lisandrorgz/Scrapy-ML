import scrapy


class GraphicCItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    cuote_cant = scrapy.Field()
    cuote_price = scrapy.Field()
    stock = scrapy.Field()
    calification = scrapy.Field()
    description = scrapy.Field()
    time = scrapy.Field()
    chunks = scrapy.Field()
