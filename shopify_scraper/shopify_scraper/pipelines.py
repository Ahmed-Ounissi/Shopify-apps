from supabase import create_client, Client
from datetime import datetime
import json

class SupabasePipeline:
    def __init__(self):
        # Initialize Supabase client
        # Use your Supabase KEYS
        self.url = ""
        self.key = ""
        self.supabase: Client = create_client(self.url, self.key)
        
    def process_item(self, item, spider):
        # Prepare the data
        data = {
            "title": item.get("title"),
            "logo_url": item.get("logo_url"),
            "description": item.get("description"),
            "url": item.get("url"),
            "app_id": item.get("app_id"),
            "developer": item.get("developer"),
            "developer_location": item.get("developer_location"),
            "developer_website": item.get("developer_website"),
            "launch_date": item.get("launch_date"),
            "pricing": item.get("pricing"),
            "pricing_details": json.dumps(item.get("pricing_details", [])),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "languages": json.dumps(item.get("languages", [])),
            "works_with": json.dumps(item.get("works_with", [])),
            "categories": json.dumps(item.get("categories", [])),
            "is_built_for_shopify": item.get("is_built_for_shopify"),
            "last_updated": datetime.utcnow().isoformat(),
            "status": "active"
        }

        try:
            # Check if app exists
            existing_app = self.supabase.table("shopify_apps").select("*").eq("app_id", item["app_id"]).execute()

            if existing_app.data:
                # App exists, update it
                old_data = existing_app.data[0]
                
                # Check if data has changed
                need_update = any(
                    old_data.get(key) != data.get(key)
                    for key in data.keys()
                )
                
                if need_update:
                    response = self.supabase.table("shopify_apps")\
                        .update(data)\
                        .eq("app_id", item["app_id"])\
                        .execute()
                    if response.data:
                        spider.logger.info(f"Updated: {data['title']}")
                    else:
                        spider.logger.error(f"Failed to update data: {response}")
            else:
                # New app, insert it
                response = self.supabase.table("shopify_apps").insert(data).execute()
                if response.data:
                    spider.logger.info(f"Inserted new app: {data['title']}")
                else:
                    spider.logger.error(f"Failed to insert data: {response}")

        except Exception as e:
            spider.logger.error(f"Exception while processing data in Supabase: {str(e)}")
            
        return item

    def close_spider(self, spider):
        """Mark apps as inactive if they weren't updated in this run"""
        try:
            # Get the timestamp from when the spider started
            cutoff_time = (datetime.utcnow().isoformat())
            
            # Update status of apps not seen in this run
            self.supabase.table("shopify_apps")\
                .update({"status": "inactive"})\
                .lt("last_updated", cutoff_time)\
                .execute()
                
            spider.logger.info("Marked old apps as inactive")
        except Exception as e:
            spider.logger.error(f"Error in close_spider: {str(e)}")