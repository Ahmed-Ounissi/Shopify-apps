from setuptools import setup, find_packages

setup(
    name='shopify_scraper',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = shopify_scraper.settings']},
    install_requires=[
        'scrapy>=2.11.0',
        'scrapeops-scrapy>=0.5.2',
        'scrapy-crawlera>=1.7.0',
        'supabase>=2.11.0',
        'python-dotenv>=1.0.0',
    ],
)