# Instagram Analytics Scraper

A comprehensive Instagram analytics tool that scrapes Instagram content by **domain/topic** (food, fashion, travel, etc.) or specific profiles, providing detailed insights including hashtag analysis, posting schedule analysis, and engagement metrics.

## Features

- 🎯 **Domain-Based Scraping**: Scrape Instagram posts by topic (food, fashion, travel, fitness, etc.)
- 🚀 **Dynamic Trending Hashtag Discovery**: Automatically discover current trending hashtags for each domain
- 📱 **Instagram Profile Scraping**: Scrape Instagram posts from specific profiles using Apify API
- 📊 **Advanced Hashtag Analysis**: Extract, categorize, and analyze hashtags with domain-specific insights
- 🏷️  **Real-Time Trending Detection**: Identify currently trending hashtags within specific domains
- 📅 **Posting Schedule Analysis**: Analyze optimal posting times and patterns
- 📈 **Engagement Analysis**: Analyze likes and comments by posting time and content type
- 🔍 **Domain Intelligence**: Automatically categorize content across 10+ predefined domains
- 🔄 **Smart Fallback System**: Falls back to curated hashtags if trending discovery fails

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Instagram-Scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Apify API token:
   - Sign up at [Apify](https://apify.com)
   - Get your API token from your account settings
   - Update the `APIFY_TOKEN` in `config.py`

## Usage

### Domain-Based Analysis with Trending Discovery (NEW!)
Analyze Instagram content by topic/domain using **dynamically discovered trending hashtags**:

```bash
python main.py <domain>
```

**Available Domains:**
- `food` - Food, cooking, recipes, restaurants
- `fashion` - Fashion, style, outfits, trends  
- `travel` - Travel, vacation, wanderlust, destinations
- `fitness` - Fitness, gym, workouts, health
- `beauty` - Beauty, makeup, skincare, cosmetics
- `photography` - Photography, art, portraits, landscapes
- `technology` - Tech, innovation, gadgets, AI
- `business` - Business, entrepreneurship, startups
- `lifestyle` - Lifestyle, inspiration, wellness
- `art` - Art, creativity, design, illustration

### Hashtag Discovery Options
```bash
python main.py food              # Use trending hashtags (default)
python main.py food --trending   # Force trending hashtag discovery
python main.py food --static     # Use only predefined hashtags
```

### Examples
```bash
python main.py food       # Discover trending food hashtags and analyze
python main.py fashion    # Discover trending fashion hashtags and analyze  
python main.py travel     # Discover trending travel hashtags and analyze
```

**How Trending Discovery Works:**
1. Samples multiple seed hashtags from the domain
2. Scrapes recent posts to discover co-occurring hashtags  
3. Identifies trending hashtags based on frequency and relevance
4. Falls back to curated hashtags if discovery fails

### Profile-Based Analysis (Original)
Analyze specific Instagram profiles:

```bash
python main.py <username>
```

### Examples
```bash
python main.py natgeo     # Analyze @natgeo profile
python main.py          # Analyze default profile (@instagram)
```

### Help
```bash
python main.py help       # Show usage instructions
```

### Run Tests
```bash
python test_modules.py
```
This will run tests to verify all modules work correctly.

## Project Structure

```
Instagram-Scraper/
├── main.py                 # Main entry point
├── apify_scraper.py        # Instagram scraping using Apify API
├── data_cleaner.py         # Data normalization and cleaning
├── analyze_hashtags.py     # Hashtag extraction and analysis
├── analyze_schedule.py     # Posting schedule analysis
├── engagement_estimator.py # Engagement metrics analysis
├── visualizer.py          # Data visualization functions
├── config.py              # Configuration settings
├── test_modules.py        # Module testing script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Output

### Domain-Based Analysis Output
When analyzing by domain, the tool provides:

1. **Domain-Specific Hashtag Analysis**: 
   - Total and unique hashtag counts
   - Hashtag diversity metrics
   - Top hashtags within the target domain
   
2. **Hashtag Categorization**:
   - Automatic categorization of hashtags by domain (food, fashion, etc.)
   - Cross-domain hashtag identification
   - Trending uncategorized hashtags

3. **Trending Analysis**:
   - Hashtags appearing multiple times
   - Domain-specific trends
   - Popular hashtag combinations

4. **Engagement Insights**:
   - Best posting times for the domain
   - Average engagement by time slots
   - Posting pattern analysis

### Profile-Based Analysis Output
When analyzing profiles, the tool provides:

1. **Top Hashtags**: Most frequently used hashtags in posts
2. **Posting Schedule Analysis**: Optimal posting times and patterns
3. **Engagement Analysis**: Average likes and comments by posting time
4. **Best Time Recommendations**: Data-driven posting time suggestions

## Troubleshooting

### Common Issues

1. **404 Error**: The Apify actor might not be available or the API token might be invalid
   - Solution: The tool will automatically fall back to mock data for testing

2. **No Data Retrieved**: Instagram might be blocking the scraper
   - Solution: Try with a different username or check your internet connection

3. **Missing Dependencies**: Install required packages
   ```bash
   pip install requests pandas matplotlib seaborn
   ```

### API Token Issues

If you're getting authentication errors:
1. Check your Apify API token is correct in `config.py`
2. Ensure your Apify account has sufficient credits
3. The tool will use mock data if the API fails

## Configuration

The `config.py` file contains all configuration settings:
- `APIFY_TOKEN`: Your Apify API token
- `ACTOR_ID`: The Instagram scraper actor ID
- `DEFAULT_USERNAME`: Default Instagram username to analyze
- `MAX_POSTS`: Maximum number of posts to scrape (default: 50)
- `DOMAIN_HASHTAGS`: Predefined hashtag mappings for each domain
- `SEARCH_TYPE`: Set to "hashtag" for domain-based analysis
- Error handling and retry configurations

## Dependencies

- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and analysis
- `matplotlib`: Basic plotting library
- `seaborn`: Statistical data visualization

