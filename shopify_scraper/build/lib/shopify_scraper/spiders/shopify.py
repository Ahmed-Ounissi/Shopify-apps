import scrapy
from datetime import datetime
from ..items import ShopifyScraperItem

class ShopifySpider(scrapy.Spider):
    name = "shopify"
    allowed_domains = ["apps.shopify.com"]
    start_urls = ["https://apps.shopify.com/browse"]

    def parse(self, response):
        """Parse the main browse page to find category links"""
        categories = response.css('div.tw-grid.tw-grid-cols-2 a::attr(href)').getall()
        self.logger.info(f"Found {len(categories)} main categories")

        for category_url in categories:
            yield response.follow(category_url, callback=self.parse_category)

    def parse_category(self, response):
        """Parse a category page to find app links"""
        apps = response.css('div[data-controller="app-card"]')
        self.logger.info(f"Found {len(apps)} apps on {response.url}")

        # Follow each app's detail page
        for app in apps:
            app_url = app.css('a::attr(href)').get()
            if app_url:
                yield response.follow(app_url, callback=self.parse_app_detail)

        # Handle pagination
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            self.logger.info(f"Following next page: {next_page}")
            yield response.follow(next_page, callback=self.parse_category)

    def parse_app_detail(self, response):
        """Parse individual app detail pages"""
        try:
            # Basic Info
            title = response.css('h1.tw-text-heading-lg::text').get()
            if not title:
                title = response.css('h1::text').get()
            
            # Initialize an empty list to store parts of the description
            description_parts = []

            # Extract the meta description first
            meta_description = response.css('meta[name="description"]::attr(content)').get()
            if meta_description:
                description_parts.append(meta_description.strip())

            # Extract the main heading from the app details section
            main_heading = response.css('div#app-details h2::text').get()
            if main_heading:
                description_parts.append(main_heading.strip())

            # Extract the primary description, fallback to span for smaller screens
            primary_description = response.css('div#app-details p.tw-text-body-md::text').get()
            if not primary_description:
                primary_description = response.css('div#app-details span[data-truncate-content-copy]::text').get()
            if primary_description:
                description_parts.append(primary_description.strip())

            # Extract bulleted features
            features = response.css('div#app-details ul.tw-list-disc li::text').getall()
            if features:
                description_parts.extend([feature.strip() for feature in features])

            # Combine all parts into a single string
            description = ' '.join(description_parts).strip()

            logo_url = response.css('figure.tw-overflow-hidden img::attr(src)').get()
            if not logo_url:
                logo_url = response.css('img[class*="appIcon"]::attr(src)').get()

            # Developer Info
            developer = response.css('div.tw-col-span-full a[href*="/partners/"]::text').get()
            if developer:
                developer = developer.strip()

            dev_website = response.css('div.tw-col-span-full a[target="_blank"][href^="http"]::attr(href)').get()
            if dev_website:
                dev_website = dev_website.strip()

            dev_location = ' '.join(response.css('div.tw-col-span-full p.tw-text-fg-tertiary::text').getall()).strip()

            # Launch Date
            launch_date = response.css('div.tw-grid p.tw-col-span-full.sm\\:tw-col-span-3.tw-text-fg-secondary.tw-text-body-md::text').get()
            if launch_date:
                launch_date = launch_date.strip()

            
            pricing_div = response.css('div.app-details-pricing-plan-card')
            pricing = pricing_div.css('span[data-test-id="price"]::text').get()
            if not pricing:
                pricing = pricing_div.css('p[data-test-id="additional-charges"]::text').get()
                
            # Pricing Details
            price_details = response.css('#adp-pricing p::text').getall()
            price_details = [p.strip() for p in price_details if p.strip()]

            # Ratings & Reviews
            reviews_count = response.css('#adp-reviews h2::text').get()
            reviews = reviews_count.strip('()') if reviews_count else '0'
            rating = response.css('div[aria-label*="out of 5 stars"]::text').get()

            # Categories
            categories = response.css('#adp-details-section > div.tw-mt-lg.lg\\:tw-mt-2xl > div a::text').getall()
            categories = [c.strip() for c in categories if c.strip()]

            # Languages
            languages = response.css('#adp-details-section > div.tw-flex.tw-flex-col.tw-gap-lg.lg\\:tw-gap-2xl > div:nth-child(1) p.tw-text-fg-secondary.tw-text-body-md::text').getall()
            languages = [lang.strip() for lang in languages if lang.strip()]
            
            # Works With
            works_with = response.css('#adp-details-section > div.tw-flex.tw-flex-col.tw-gap-lg.lg\\:tw-gap-2xl > div.tw-grid.tw-grid-cols-4.tw-gap-x-gutter--mobile.lg\\:tw-gap-x-gutter--desktop.tw-border-t.tw-border-t-stroke-secondary.tw-flex.tw-pt-sm ul li::text').getall()
            works_with = [item.strip() for item in works_with if item.strip()]

            yield {
                'title': title.strip() if title else None,
                'description': description if description else None,
                'logo_url': logo_url,
                'url': response.url,
                'app_id': response.url.split('/')[-1].split('?')[0],
                'developer': developer.strip() if developer else None,
                'developer_location': dev_location.strip() if dev_location else None,
                'developer_website': dev_website,
                'launch_date': launch_date.strip() if launch_date else None,
                'pricing': pricing.strip() if pricing else None,
                'pricing_details': price_details,
                'rating': rating.strip() if rating else None,
                'reviews': reviews,
                'languages': languages,
                'works_with': works_with,
                'categories': categories,
                'last_updated': datetime.utcnow().isoformat(),
                'status': 'active'
            }

        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")
