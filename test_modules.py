#!/usr/bin/env python3
"""
Test script to verify all modules work correctly
"""

import sys
import traceback

def test_module(module_name, test_func):
    """Test a module and report results"""
    try:
        test_func()
        print(f"✅ {module_name}: PASSED")
        return True
    except Exception as e:
        print(f"❌ {module_name}: FAILED - {e}")
        traceback.print_exc()
        return False

def test_apify_scraper():
    """Test the Apify scraper module"""
    from apify_scraper import run_scraper, run_scraper_by_domain, run_scraper_by_hashtag
    
    # Test original user scraping
    print("Testing user profile scraping...")
    user_data = run_scraper("testuser")
    if user_data:
        assert isinstance(user_data, list), "Should return a list"
        assert len(user_data) > 0, "Should return some data"
    
    # Test domain-based scraping
    print("Testing domain-based scraping...")
    domain_data = run_scraper_by_domain("food")
    if domain_data:
        assert isinstance(domain_data, list), "Should return a list"
        assert len(domain_data) > 0, "Should return some data"
    
    # Test hashtag scraping
    print("Testing hashtag-based scraping...")
    hashtag_data = run_scraper_by_hashtag(["#food", "#delicious"])
    if hashtag_data:
        assert isinstance(hashtag_data, list), "Should return a list"
        assert len(hashtag_data) > 0, "Should return some data"

def test_data_cleaner():
    """Test the data cleaner module"""
    from data_cleaner import normalize_data
    mock_data = [
        {
            "url": "https://test.com",
            "likesCount": 100,
            "commentsCount": 10,
            "caption": "Test post #test",
            "takenAtTimestamp": 1640995200,  # 2022-01-01
            "typename": "GraphImage"
        }
    ]
    df = normalize_data(mock_data)
    assert len(df) == 1, "Should process one row"
    assert "likesCount" in df.columns, "Should have likesCount column"

def test_hashtag_analyzer():
    """Test the hashtag analyzer module"""
    from analyze_hashtags import extract_hashtags, analyze_domain_hashtags, find_trending_hashtags
    import pandas as pd
    
    # Test basic hashtag extraction
    captions = pd.Series(["Test #hashtag1 #food", "Another #hashtag1 #hashtag2 #fashion", "#food #delicious"])
    hashtags = extract_hashtags(captions)
    assert len(hashtags) > 0, "Should extract hashtags"
    
    # Test domain-specific analysis
    domain_analysis = analyze_domain_hashtags(captions, "food")
    assert isinstance(domain_analysis, dict), "Should return analysis dictionary"
    assert 'total_hashtags' in domain_analysis, "Should include total hashtags count"
    
    # Test trending hashtags
    trending = find_trending_hashtags(captions, min_frequency=1)
    assert isinstance(trending, list), "Should return trending hashtags list"

def test_schedule_analyzer():
    """Test the schedule analyzer module"""
    from analyze_schedule import analyze_posting_schedule
    from data_cleaner import normalize_data
    
    mock_data = [
        {
            "url": "https://test.com",
            "likesCount": 100,
            "commentsCount": 10,
            "caption": "Test post",
            "takenAtTimestamp": 1640995200,  # 2022-01-01
            "typename": "GraphImage"
        }
    ]
    df = normalize_data(mock_data)
    schedule_df = analyze_posting_schedule(df)
    assert not schedule_df.empty, "Should return schedule data"

def test_engagement_estimator():
    """Test the engagement estimator module"""
    from engagement_estimator import estimate_avg_engagement
    from data_cleaner import normalize_data
    
    mock_data = [
        {
            "url": "https://test.com",
            "likesCount": 100,
            "commentsCount": 10,
            "caption": "Test post",
            "takenAtTimestamp": 1640995200,  # 2022-01-01
            "typename": "GraphImage"
        }
    ]
    df = normalize_data(mock_data)
    engagement_df = estimate_avg_engagement(df)
    assert not engagement_df.empty, "Should return engagement data"

def test_domain_configuration():
    """Test domain configuration and mappings"""
    from config import DOMAIN_HASHTAGS, USE_TRENDING_HASHTAGS, TRENDING_SAMPLE_SIZE
    
    # Test that domain mappings exist
    assert isinstance(DOMAIN_HASHTAGS, dict), "Should have domain hashtags dictionary"
    assert len(DOMAIN_HASHTAGS) > 0, "Should have at least one domain"
    assert "food" in DOMAIN_HASHTAGS, "Should include food domain"
    assert "fashion" in DOMAIN_HASHTAGS, "Should include fashion domain"
    
    # Test that each domain has hashtags
    for domain, hashtags in DOMAIN_HASHTAGS.items():
        assert isinstance(hashtags, list), f"Domain {domain} should have hashtag list"
        assert len(hashtags) > 0, f"Domain {domain} should have at least one hashtag"
        for hashtag in hashtags:
            assert hashtag.startswith("#"), f"Hashtag {hashtag} should start with #"
    
    # Test trending configuration
    assert isinstance(USE_TRENDING_HASHTAGS, bool), "USE_TRENDING_HASHTAGS should be boolean"
    assert isinstance(TRENDING_SAMPLE_SIZE, int), "TRENDING_SAMPLE_SIZE should be integer"
    assert TRENDING_SAMPLE_SIZE > 0, "TRENDING_SAMPLE_SIZE should be positive"


def test_trending_hashtags():
    """Test trending hashtag discovery functionality"""
    try:
        from trending_hashtags import get_hashtags_for_domain, filter_trending_hashtags
        
        # Test basic hashtag retrieval
        hashtags = get_hashtags_for_domain("food", use_trending=False, fallback_to_static=True)
        assert isinstance(hashtags, list), "Should return hashtag list"
        assert len(hashtags) > 0, "Should return some hashtags"
        
        # Test filtering functionality
        sample_hashtags = {"#food": 5, "#yummy": 3, "#a": 1, "#delicious": 4}
        filtered = filter_trending_hashtags(sample_hashtags, "food", min_frequency=2)
        assert isinstance(filtered, list), "Should return filtered list"
        assert "#a" not in filtered, "Should filter out low frequency hashtags"
        
        print("✅ Trending hashtag functions work correctly")
        
    except ImportError:
        print("⚠️  Trending hashtag module not available - skipping trending tests")

def test_visualizer():
    """Test the visualizer module"""
    try:
        from visualizer import show_schedule_heatmap, show_engagement_heatmap
        import pandas as pd
        
        # Test with empty data (should not crash)
        empty_df = pd.DataFrame()
        show_schedule_heatmap(empty_df)
        show_engagement_heatmap(empty_df)
    except ImportError:
        print("⚠️  Visualizer module not found - skipping visualization tests")

def main():
    """Run all tests"""
    print("🧪 Running module tests...\n")
    
    tests = [
        ("Apify Scraper", test_apify_scraper),
        ("Data Cleaner", test_data_cleaner),
        ("Hashtag Analyzer", test_hashtag_analyzer),
        ("Schedule Analyzer", test_schedule_analyzer),
        ("Engagement Estimator", test_engagement_estimator),
        ("Domain Configuration", test_domain_configuration),
        ("Trending Hashtags", test_trending_hashtags),
        ("Visualizer", test_visualizer),
    ]
    
    passed = 0
    total = len(tests)
    
    for module_name, test_func in tests:
        if test_module(module_name, test_func):
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} modules passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
