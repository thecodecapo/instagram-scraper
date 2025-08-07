# Instagram Analytics Scraper

A comprehensive Instagram analytics tool that scrapes Instagram profiles and provides detailed insights including hashtag analysis, posting schedule analysis, and engagement metrics.

## Features

- 📱 **Instagram Profile Scraping**: Scrape Instagram posts using Apify API
- 📊 **Hashtag Analysis**: Extract and analyze most used hashtags
- 📅 **Posting Schedule Analysis**: Visualize posting patterns with heatmaps
- 📈 **Engagement Analysis**: Analyze likes and comments by posting time
- 🎨 **Data Visualization**: Beautiful heatmaps and charts using seaborn

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

### Basic Usage
```bash
python main.py
```
This will analyze the default profile "arc.graphique"

### Analyze Specific Profile
```bash
python main.py username
```
Replace `username` with the Instagram username you want to analyze.

### Example
```bash
python main.py natgeo
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

The tool provides:

1. **Top Hashtags**: Most frequently used hashtags in posts
2. **Posting Schedule Heatmap**: Visual representation of posting times
3. **Engagement Analysis**: Average likes and comments by posting time
4. **Engagement Heatmaps**: Visual representation of engagement patterns

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
- `MAX_POSTS`: Maximum number of posts to scrape
- Visualization settings (colors, figure sizes, etc.)

## Dependencies

- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and analysis
- `matplotlib`: Basic plotting library
- `seaborn`: Statistical data visualization

