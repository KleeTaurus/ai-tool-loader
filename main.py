import os
import requests
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def main():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    response = supabase.table("submit").select("*").eq("status", 0).execute()
    for row in response.data:
        print(f"Processing {row["name"]} {row["url"]}")
        # supabase.table("submit").update({"status": 1}).eq("id", row["id"]).execute()
        call_ai_service(row["name"], row["url"])


# make a restful api call to the AI service
def call_ai_service(name: str, url: str):
    # Define the URL and headers
   url = os.getenv("CRAWLER_ENDPOINT_URL")
   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {os.getenv('CRAWLER_AUTH_SECRET')}"  # Replace with your actual Authorization token
   }
   
   # Define the payload
   payload = {
       "url": url,
       "tags": [],
       "languages": ["中文"]
   }
   
   # Make the POST request
   response = requests.post(url, headers=headers, data=json.dumps(payload))
   
   # Check if the request was successful
   if response.status_code == 200:
       # Parse the JSON response
       response_data = response.json()
       print(json.dumps(response_data, indent=4, ensure_ascii=False))
   else:
       print(f"Request failed with status code {response.status_code}")
       print(response.text)


if __name__ == "__main__":
    main()
