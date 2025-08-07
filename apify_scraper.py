import requests
import time
import json
from config import APIFY_TOKEN, MAX_POSTS, SEARCH_TYPE, MAX_RETRIES, RETRY_DELAY

PUBLIC_ACTOR_ID = "apify~instagram-scraper"


def run_scraper(username):
    """
    Run Instagram scraper using Apify actor that requires profile URLs
    """
    run_url = f"https://api.apify.com/v2/acts/{PUBLIC_ACTOR_ID}/runs?token={APIFY_TOKEN}"
    
    # Convert username to full Instagram profile URL
    profile_url = f"https://www.instagram.com/{username}/"
    
    # Try different payload formats that the actor might expect
    payload = {
        "directUrls": [profile_url],
        "resultsLimit": MAX_POSTS,
        "searchType": "user",
        "addParentData": False,
        "searchLimit": MAX_POSTS,
        "proxy": {
            "useApifyProxy": True
        }
    }
    
    # Alternative payload if the above doesn't work
    # payload = {
    #     "profileUrls": [profile_url],
    #     "resultsLimit": MAX_POSTS,
    #     "searchType": "user"
    # }
    
    try:
        print(f"Starting Instagram scraper for profile: {profile_url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(run_url, json=payload)
        response.raise_for_status()
        run_data = response.json()
        run_id = run_data['data']['id']
        print(f"Actor run started with ID: {run_id}")
        
        # Poll for run status
        for attempt in range(MAX_RETRIES * 6):  # up to 3 minutes
            status_url = f"https://api.apify.com/v2/acts/{PUBLIC_ACTOR_ID}/runs/{run_id}?token={APIFY_TOKEN}"
            status_response = requests.get(status_url)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data['data']['status']
            print(f"Run status: {status}")
            
            if status == 'SUCCEEDED':
                print("✅ Run completed successfully!")
                break
            elif status in ['FAILED', 'ABORTED']:
                print(f"❌ Actor run failed with status: {status}")
                print(f"Full status response: {json.dumps(status_data, indent=2)}")
                return None
            elif status == 'RUNNING':
                print(f"⏳ Run is still running... (attempt {attempt + 1})")
            else:
                print(f"⚠️  Unexpected status: {status}")
            
            time.sleep(RETRY_DELAY)
        
        # Fetch dataset items
        dataset_id = status_data['data']['defaultDatasetId']
        print(f"📊 Fetching data from dataset: {dataset_id}")
        
        results_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}"
        results_response = requests.get(results_url)
        results_response.raise_for_status()
        data = results_response.json()
        
        print(f"📈 Retrieved {len(data) if data else 0} items from dataset")
        
        if not data:
            print(f"❌ No data found for profile: {profile_url}. The profile may not exist or is private.")
            return None
            
        # Check if the data contains error objects
        if len(data) == 1 and isinstance(data[0], dict) and "error" in data[0]:
            print(f"❌ Actor returned error: {data[0]['error']} - {data[0].get('errorDescription', 'No description')}")
            print("This suggests the actor cannot access Instagram data due to anti-scraping measures.")
            return None
            
        return data
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error running scraper: {e}")
        return None

if __name__ == "__main__":
    data = run_scraper("natgeo")
    if data:
        print(f"Retrieved {len(data)} posts")
        print(json.dumps(data[:2], indent=2))  # Print first 2 items as sample
    else:
        print("No data returned.")
