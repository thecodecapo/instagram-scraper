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
    from apify_scraper import run_scraper
    data = run_scraper("testuser")
    assert isinstance(data, list), "Should return a list"
    assert len(data) > 0, "Should return some data"

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
    from analyze_hashtags import extract_hashtags
    import pandas as pd
    
    captions = pd.Series(["Test #hashtag1", "Another #hashtag1 #hashtag2", ""])
    hashtags = extract_hashtags(captions)
    assert len(hashtags) > 0, "Should extract hashtags"

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

def test_visualizer():
    """Test the visualizer module"""
    from visualizer import show_schedule_heatmap, show_engagement_heatmap
    import pandas as pd
    
    # Test with empty data (should not crash)
    empty_df = pd.DataFrame()
    show_schedule_heatmap(empty_df)
    show_engagement_heatmap(empty_df)

def main():
    """Run all tests"""
    print("🧪 Running module tests...\n")
    
    tests = [
        ("Apify Scraper", test_apify_scraper),
        ("Data Cleaner", test_data_cleaner),
        ("Hashtag Analyzer", test_hashtag_analyzer),
        ("Schedule Analyzer", test_schedule_analyzer),
        ("Engagement Estimator", test_engagement_estimator),
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
