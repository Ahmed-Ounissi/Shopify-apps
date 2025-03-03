import scrapy
from datetime import datetime
from ..items import ShopifyScraperItem

class ShopifySpider(scrapy.Spider):
    name = "shopify"
    allowed_domains = ["apps.shopify.com"]
    start_urls = [
        "https://apps.shopify.com/categories/marketing-and-conversion-advertising",
        "https://apps.shopify.com/categories/marketing-and-conversion-checkout",
        "https://apps.shopify.com/categories/marketing-and-conversion-customer-loyalty",
        "https://apps.shopify.com/categories/marketing-and-conversion-gifts",
        "https://apps.shopify.com/categories/marketing-and-conversion-marketing",
        "https://apps.shopify.com/categories/marketing-and-conversion-promotions",
        "https://apps.shopify.com/categories/marketing-and-conversion-social-trust",
        "https://apps.shopify.com/categories/marketing-and-conversion-upsell-and-bundles",
        "https://apps.shopify.com/categories/orders-and-shipping-inventory",
        "https://apps.shopify.com/categories/orders-and-shipping-orders",
        "https://apps.shopify.com/categories/orders-and-shipping-returns-and-warranty",
        "https://apps.shopify.com/categories/orders-and-shipping-shipping-solutions",
        "https://apps.shopify.com/categories/finding-products-dropshipping",
        "https://apps.shopify.com/categories/finding-products-print-on-demand",
        "https://apps.shopify.com/categories/finding-products-wholesale",
        "https://apps.shopify.com/categories/store-management-finances",
        "https://apps.shopify.com/categories/store-management-operations",
        "https://apps.shopify.com/categories/store-management-security",
        "https://apps.shopify.com/categories/store-management-support",
        "https://apps.shopify.com/categories/sales-channels-selling-in-person",
        "https://apps.shopify.com/categories/sales-channels-selling-online",
        "https://apps.shopify.com/categories/selling-products-custom-products",
        "https://apps.shopify.com/categories/selling-products-digital-goods-and-services",
        "https://apps.shopify.com/categories/selling-products-payment-options",
        "https://apps.shopify.com/categories/selling-products-pricing",
        "https://apps.shopify.com/categories/store-design-content",
        "https://apps.shopify.com/categories/store-design-design-elements",
        "https://apps.shopify.com/categories/store-design-images-and-media",
        "https://apps.shopify.com/categories/store-design-internationalization",
        "https://apps.shopify.com/categories/store-design-notifications",
        "https://apps.shopify.com/categories/store-design-product-display",
        "https://apps.shopify.com/categories/store-design-search-and-navigation",
        "https://apps.shopify.com/categories/store-design-site-optimization",
        "https://apps.shopify.com/categories/store-design-storefronts", 
        
    ]

    def parse(self, response):
        """Extract subcategories and sub-subcategories from main category pages."""
        try:
            # Extract subcategories
            subcategories = response.css('ul li a::attr(href)').getall()
            self.logger.info(f"Found {len(subcategories)} subcategories in {response.url}")

            # Follow each subcategory
            for subcategory_url in subcategories:
                yield response.follow(subcategory_url, callback=self.parse_subcategory)

            # Extract sub-subcategories
            sub_subcategories = response.css('div.tw-pt-xl:nth-child(2) a::attr(href)').getall()
            self.logger.info(f"Found {len(sub_subcategories)} sub-subcategories in {response.url}")

            # Follow each sub-subcategory
            for sub_subcategory_url in sub_subcategories:
                yield response.follow(sub_subcategory_url, callback=self.parse_subcategory)
        except Exception as e:
            self.logger.error(f"Error parsing categories: {str(e)}")
            with open("category_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
                self.logger.error(f"Error parsing {response.url}: {str(e)}")

    def parse_subcategory(self, response):
        """Parse subcategory pages to find app links and handle pagination."""
        try:
            apps = response.css('div[data-controller="app-card"] a::attr(href)').getall()
            self.logger.info(f"Found {len(apps)} apps in {response.url}")

            for app in apps:
                yield response.follow(app, callback=self.parse_app_detail)

            # Handle pagination
            next_page = response.css('a[rel="next"]::attr(href)').get()
            if next_page:
                self.logger.info(f"Following next page: {next_page}")
                yield response.follow(next_page, callback=self.parse_subcategory)
        except Exception as e:
            self.logger.error(f"Error parsing subcategory page: {str(e)}")
            with open("subcategory_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)

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
            reviews_count = response.css('#reviews-link::text').re_first(r'\d+')  # Extract the number using regex
            reviews = reviews_count if reviews_count else '0'  # Default to '0' if no reviews are found
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
            
            # Check for "Built for Shopify" badge
            built_for_shopify_badge = response.css('#adp-hero > div > div.tw-grow.tw-flex.tw-flex-col.tw-gap-xl > div > div > div > div > div')
            is_built_for_shopify = bool(built_for_shopify_badge)

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
                'is_built_for_shopify': is_built_for_shopify,
                'last_updated': datetime.utcnow().isoformat(),
                'status': 'active'
            }

        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")
