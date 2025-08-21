import requests
import json
import time
import random
from config import APIFY_TOKEN, MAX_RETRIES, RETRY_DELAY, DOMAIN_HASHTAGS

PUBLIC_ACTOR_ID = "apify~instagram-scraper"

def discover_trending_hashtags_for_domain(domain, sample_size=3):
    """
    Discover trending hashtags for a domain by sampling multiple seed hashtags
    and analyzing the most co-occurring hashtags
    """
    if domain.lower() not in DOMAIN_HASHTAGS:
        print(f"❌ Unknown domain: {domain}")
        return DOMAIN_HASHTAGS.get(domain.lower(), [])
    
    seed_hashtags = DOMAIN_HASHTAGS[domain.lower()]
    print(f"🔍 Discovering trending hashtags for {domain.upper()} domain...")
    print(f"🌱 Using seed hashtags: {', '.join(seed_hashtags[:sample_size])}")
    
    all_discovered_hashtags = {}
    
    # Sample a few seed hashtags to get diverse data
    sample_hashtags = random.sample(seed_hashtags, min(sample_size, len(seed_hashtags)))
    
    for seed_hashtag in sample_hashtags:
        print(f"📊 Sampling from {seed_hashtag}...")
        hashtags = scrape_hashtags_from_tag(seed_hashtag, max_posts=20)
        
        if hashtags:
            for hashtag, count in hashtags.items():
                if hashtag not in all_discovered_hashtags:
                    all_discovered_hashtags[hashtag] = 0
                all_discovered_hashtags[hashtag] += count
        
        # Small delay between requests
        time.sleep(2)
    
    # Filter and rank discovered hashtags
    trending_hashtags = filter_trending_hashtags(all_discovered_hashtags, domain, min_frequency=2)
    
    print(f"✅ Discovered {len(trending_hashtags)} trending hashtags for {domain}")
    return trending_hashtags[:15]  # Return top 15


def scrape_hashtags_from_tag(hashtag, max_posts=20):
    """
    Scrape a small sample of posts from a hashtag to discover co-occurring hashtags
    """
    try:
        run_url = f"https://api.apify.com/v2/acts/{PUBLIC_ACTOR_ID}/runs?token={APIFY_TOKEN}"
        
        # Clean hashtag
        clean_hashtag = hashtag.replace('#', '')
        hashtag_url = f"https://www.instagram.com/explore/tags/{clean_hashtag}/"
        
        payload = {
            "directUrls": [hashtag_url],
            "resultsLimit": max_posts,
            "searchType": "hashtag",
            "addParentData": False,
            "searchLimit": max_posts,
            "proxy": {
                "useApifyProxy": True
            }
        }
        
        # Start the scraping run
        response = requests.post(run_url, json=payload)
        response.raise_for_status()
        run_data = response.json()
        run_id = run_data['data']['id']
        
        # Poll for completion (shorter timeout for discovery)
        for attempt in range(MAX_RETRIES * 2):
            status_url = f"https://api.apify.com/v2/acts/{PUBLIC_ACTOR_ID}/runs/{run_id}?token={APIFY_TOKEN}"
            status_response = requests.get(status_url)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data['data']['status']
            
            if status == 'SUCCEEDED':
                break
            elif status in ['FAILED', 'ABORTED']:
                print(f"⚠️  Sample from {hashtag} failed")
                return {}
            
            time.sleep(RETRY_DELAY)
        
        # Get the data
        if status == 'SUCCEEDED':
            dataset_id = status_data['data']['defaultDatasetId']
            results_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}"
            results_response = requests.get(results_url)
            results_response.raise_for_status()
            data = results_response.json()
            
            # Extract hashtags from captions
            hashtag_counts = {}
            if data:
                for post in data:
                    caption = post.get('caption', '')
                    if caption:
                        import re
                        found_hashtags = re.findall(r"#\w+", caption.lower())
                        for tag in found_hashtags:
                            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
            
            return hashtag_counts
        
        return {}
        
    except Exception as e:
        print(f"⚠️  Error sampling {hashtag}: {e}")
        return {}


def filter_trending_hashtags(hashtag_counts, domain, min_frequency=2):
    """
    Filter and rank hashtags to find the most relevant trending ones for a domain
    """
    # Remove hashtags that appear too infrequently
    filtered = {tag: count for tag, count in hashtag_counts.items() 
                if count >= min_frequency and len(tag) > 2}
    
    # Sort by frequency
    sorted_hashtags = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    
    # Extract just the hashtag names
    trending_list = [tag for tag, count in sorted_hashtags]
    
    # Remove exact duplicates of seed hashtags (but keep variations)
    seed_hashtags = [tag.lower() for tag in DOMAIN_HASHTAGS.get(domain.lower(), [])]
    trending_list = [tag for tag in trending_list if tag not in seed_hashtags]
    
    return trending_list


def get_hashtags_for_domain(domain, use_trending=True, fallback_to_static=True):
    """
    Main function to get hashtags for a domain - tries trending first, falls back to static
    """
    hashtags = []
    
    if use_trending:
        try:
            hashtags = discover_trending_hashtags_for_domain(domain)
            if hashtags:
                print(f"🚀 Using {len(hashtags)} trending hashtags for {domain}")
                return hashtags
        except Exception as e:
            print(f"⚠️  Trending discovery failed: {e}")
    
    if fallback_to_static and domain.lower() in DOMAIN_HASHTAGS:
        hashtags = DOMAIN_HASHTAGS[domain.lower()]
        print(f"🔄 Falling back to static hashtags for {domain}")
        return hashtags
    
    print(f"❌ No hashtags found for domain: {domain}")
    return []


def get_instagram_trending_topics():
    """
    Discover general trending topics on Instagram (optional enhancement)
    """
    # This could be enhanced to discover completely new trending topics
    # For now, we'll focus on domain-specific trending hashtags
    trending_domains = {
        "viral": ["#viral", "#trending", "#fyp", "#explore"],
        "reels": ["#reels", "#reelsvideo", "#reelsinstagram", "#reelitfeelit"],
        "general": ["#instagood", "#photooftheday", "#love", "#instagram"]
    }
    return trending_domains


if __name__ == "__main__":
    # Test the trending hashtag discovery
    print("🧪 Testing trending hashtag discovery...")
    trending = discover_trending_hashtags_for_domain("food", sample_size=2)
    print(f"Discovered trending food hashtags: {trending[:10]}")
