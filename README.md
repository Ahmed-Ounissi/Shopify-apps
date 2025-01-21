Shopify App Scraper - README

This document will guide you through setting up the environment for the Shopify App Scraper, including Supabase, Zyte, and ScrapeOps, as well as configuring the project to run successfully.

1. Setting Up the Supabase Table

Step 1.1: Create the Table with SQL

Run the following SQL query in the Supabase SQL editor to create the shopify_apps table:

	CREATE TABLE shopify_apps (
    		id SERIAL PRIMARY KEY,
    		app_id TEXT,
    		title TEXT,
    		logo_url TEXT,
    		description TEXT,
    		url TEXT,
    		developer TEXT,
    		developer_location TEXT,
    		developer_website TEXT,
    		launch_date TEXT,
    		pricing TEXT,
   		pricing_details JSONB,
    		rating TEXT,
    		reviews TEXT,
    		languages JSONB,
    		works_with JSONB,
    		categories JSONB,
    		last_updated TIMESTAMPTZ,
    		status TEXT,
    		is_built_for_shopify BOOLEAN
	);



	CREATE INDEX idx_app_id ON shopify_apps(app_id);


Explanation of Columns

	id: Unique identifier for each app (Primary Key).

	app_id: The unique app ID from Shopify.

	title: App title.

	logo_url: URL of the app logo.

	description: App description.

	url: URL of the app on the Shopify App Store.

	developer: Name of the developer or company.

	developer_location: Location of the developer.

	developer_website: Developer's website.

	launch_date: App launch date.

	pricing: Pricing tier or information.

	pricing_details: Detailed pricing structure in JSON format.

	rating: Average app rating.

	reviews: Number of reviews.

	languages: Supported languages in JSON format.

	works_with: Platforms or integrations supported in JSON format.

	categories: Categories the app belongs to in JSON format.

	last_updated: Timestamp of the last update.

	status: Current status of the app.

	is_built_for_shopify: Boolean indicating if the app is built by Shopify.

2. Configuring Zyte and ScrapeOps

Step 2.1: Set Up Zyte API

	Sign up for a Zyte account at https://www.zyte.com.

	Obtain your API key from the Zyte dashboard.

Step 2.2: Set Up ScrapeOps

	Sign up for a ScrapeOps account at https://scrapeops.io.

	Obtain your API key from the ScrapeOps dashboard.

3. Configuring the Project

Step 3.1: Replace API Keys in Code

	Open the settings.py file.

	Replace the placeholders with your actual keys:

	SCRAPEOPS_API_KEY = 'your_scrapeops_api_key_here'
	ZYTE_API_KEY = 'your_zyte_api_key_here'

Step 3.2: Configure Supabase Connection

	Open the pipelines.py file.

	Replace the placeholders with your actual Supabase details:

	supabase_url = 'your_supabase_url_here'
	supabase_key = 'your_supabase_anon_key_here'

4. Running the Scraper

Step 4.1: Install Dependencies

	Run the following command to install required dependencies:

	pip install -r requirements.txt

Step 4.2: Start Scraping

	Run the scraper with:

	scrapy crawl shopify

5. Deployment

	Step 5.1: Deploy to Vercel

	Install the Vercel CLI:

	npm install -g vercel

	Deploy the project:

	vercel --prod

6. Post-Run Checks

Step 6.1: Verify Data in Supabase

	Run the following query in the Supabase SQL editor to check the total number of scraped apps:

	SELECT COUNT(*) FROM shopify_apps;

Step 6.2: Check for Duplicates

	Run this query to ensure no duplicates exist:

	SELECT app_id, COUNT(*)
	FROM shopify_apps
	GROUP BY app_id
	HAVING COUNT(*) > 1;

Notes

Make sure to regularly monitor Supabase performance as the dataset grows.

Use logs and debug files (debug.html) to troubleshoot any scraping issues.

Let me know if you encounter any issues during setup or execution!
