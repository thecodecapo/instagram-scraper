from apify_scraper import run_scraper, run_scraper_by_domain
from data_cleaner import normalize_data
from analyze_hashtags import extract_hashtags, analyze_domain_hashtags, find_trending_hashtags
from analyze_schedule import analyze_posting_schedule
from engagement_estimator import estimate_avg_engagement
from config import DEFAULT_USERNAME, DOMAIN_HASHTAGS
import sys
import json

def print_usage():
    """Print usage instructions"""
    print("\n📋 Instagram Analytics Scraper Usage:")
    print("======================================")
    print("🎯 Domain-based analysis (with trending hashtag discovery):")
    print(f"   python main.py <domain>")
    print(f"   Available domains: {', '.join(DOMAIN_HASHTAGS.keys())}")
    print("\n📱 Profile-based analysis:")
    print("   python main.py <username>")
    print("\n🔧 Options:")
    print("   python main.py <domain> --static    # Use static hashtags only")
    print("   python main.py <domain> --trending  # Force trending discovery")
    print("\n💡 Examples:")
    print("   python main.py food          # Analyze food with trending hashtags")
    print("   python main.py fashion       # Analyze fashion with trending hashtags")
    print("   python main.py food --static # Analyze food with predefined hashtags")
    print("   python main.py natgeo        # Analyze @natgeo profile")
    print("\n")

def main():
    try:
        print("🚀 Starting Instagram Analytics...")
        
        # Check for help flag
        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
            return
        
        # Parse command line arguments
        input_arg = sys.argv[1] if len(sys.argv) > 1 else None
        use_static = '--static' in sys.argv
        force_trending = '--trending' in sys.argv
        
        if not input_arg:
            print_usage()
            print("🔄 Using default profile for demo...")
            input_arg = DEFAULT_USERNAME
        
        # Override global trending setting if specified
        if use_static:
            print("📋 Using static hashtags as requested")
            import config
            config.USE_TRENDING_HASHTAGS = False
        elif force_trending:
            print("🚀 Using trending hashtag discovery as requested")
            import config
            config.USE_TRENDING_HASHTAGS = True
        
        # Check if input is a domain or username
        if input_arg.lower() in DOMAIN_HASHTAGS:
            # Domain-based scraping
            domain = input_arg.lower()
            print(f"🎯 Analyzing Instagram domain: {domain.upper()}")
            print(f"🏷️  Target hashtags: {', '.join(DOMAIN_HASHTAGS[domain])}")
            raw_data = run_scraper_by_domain(domain)
        else:
            # Username-based scraping (original functionality)
            username = input_arg
            print(f"📱 Analyzing Instagram profile: @{username}")
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

        # Determine if this is domain-based analysis
        is_domain_analysis = input_arg and input_arg.lower() in DOMAIN_HASHTAGS
        
        if is_domain_analysis:
            # Enhanced domain-specific hashtag analysis
            print(f"\n📈 Domain-Specific Hashtag Analysis for {input_arg.upper()}:")
            print("=" * 50)
            
            hashtag_analysis = analyze_domain_hashtags(df["caption"], input_arg.lower())
            
            if hashtag_analysis:
                print(f"📊 Total hashtags found: {hashtag_analysis['total_hashtags']}")
                print(f"🏷️  Unique hashtags: {hashtag_analysis['unique_hashtags']}")
                print(f"🌟 Hashtag diversity: {hashtag_analysis['hashtag_diversity']}%")
                
                print(f"\n🔝 Top 15 Hashtags in {input_arg.upper()} Domain:")
                for hashtag, count in hashtag_analysis['top_hashtags'][:15]:
                    print(f"  {hashtag}: {count} posts")
                
                # Show domain categories
                print(f"\n🎯 Hashtag Categories Found:")
                for domain, tags in hashtag_analysis['domain_categories'].items():
                    if tags:
                        print(f"\n  {domain.upper()} ({len(tags)} tags):")
                        for hashtag, count in tags[:5]:  # Top 5 per category
                            print(f"    {hashtag}: {count}")
                
                # Show trending uncategorized hashtags
                if hashtag_analysis['uncategorized']:
                    print(f"\n🚀 Trending Uncategorized Hashtags:")
                    for hashtag, count in hashtag_analysis['uncategorized'][:10]:
                        print(f"  {hashtag}: {count}")
            
            # Find trending hashtags
            print(f"\n⭐ Trending Hashtags (appearing 2+ times):")
            trending = find_trending_hashtags(df["caption"], min_frequency=2)
            for hashtag, count in trending[:10]:
                print(f"  {hashtag}: {count} posts")
                
        else:
            # Original hashtag analysis for profile-based scraping
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
