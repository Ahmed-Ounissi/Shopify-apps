import scrapy

class ShopifyScraperItem(scrapy.Item):
    # Basic Info
    title = scrapy.Field()
    logo_url = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    app_id = scrapy.Field()
    
    # Developer Info
    developer = scrapy.Field()
    developer_location = scrapy.Field()
    developer_website = scrapy.Field()
    
    # App Details
    launch_date = scrapy.Field()
    pricing = scrapy.Field()
    pricing_details = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    languages = scrapy.Field()
    works_with = scrapy.Field()
    categories = scrapy.Field()
    is_built_for_shopify = scrapy.Field()
    
    # Timestamps
    last_updated = scrapy.Field()
    status = scrapy.Field()