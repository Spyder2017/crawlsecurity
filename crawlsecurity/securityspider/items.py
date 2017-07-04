from scrapy.item import Item, Field


class SecurityItem(Item):

    title = Field()
    description = Field()
    url = Field()
    keywords = Field()
    author = Field()
    datetime = Field()