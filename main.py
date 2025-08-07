from apify_scraper import run_scraper
from data_cleaner import normalize_data
from analyze_hashtags import extract_hashtags
from analyze_schedule import analyze_posting_schedule
from engagement_estimator import estimate_avg_engagement
from config import DEFAULT_USERNAME
import sys
import json

def main():
    try:
        print("🚀 Starting Instagram Analytics...")
        
        # Get username from command line or use default
        username = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USERNAME
        print(f"📱 Analyzing Instagram profile: @{username}")
        
        # Run scraper
        raw_data = run_scraper(username)
        
        if not raw_data:
            print("❌ No data retrieved. Exiting.")
            sys.exit(1)
            
        print(f"✅ Retrieved {len(raw_data)} posts")
        
        # Debug: Print raw API response
        # print("\n🔍 DEBUG: Raw API Response:")
        # print(json.dumps(raw_data, indent=2))
        # print("\n" + "="*50 + "\n")
        
        # Clean and normalize data
        df = normalize_data(raw_data)
        print(f"📊 Processed {len(df)} posts for analysis")

        # Analyze hashtags
        print("\n📈 Top Hashtags:")
        hashtags = extract_hashtags(df["caption"])
        for hashtag, count in hashtags:
            print(f"  {hashtag}: {count}")

        # Analyze engagement
        print("\n📊 Estimated Average Engagement by Time Slot:")
        engagement_df = estimate_avg_engagement(df)
        print(engagement_df.head(10))  # Top 10 time slots

        # Find the best time slot (highest average likesCount)
        if not engagement_df.empty:
            best_row = engagement_df.sort_values(by="likesCount", ascending=False).iloc[0]
            best_day = best_row.name[0]
            best_hour = best_row.name[1]
            best_likes = best_row["likesCount"]
            print(f"\n⭐ Best time to post: {best_day} at {best_hour}:00 (Avg Likes: {best_likes})")
        else:
            print("\n⚠️  Not enough data to determine the best time to post.")

        print("\n✅ Analysis complete!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
