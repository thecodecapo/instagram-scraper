import re
from collections import Counter

def extract_hashtags(captions):
    """
    Extract and count hashtags from Instagram captions
    """
    if captions.empty:
        print("⚠️  No captions found for hashtag analysis")
        return []
    
    hashtags = []
    for caption in captions.dropna():
        if isinstance(caption, str):
            # Find all hashtags in the caption
            found_hashtags = re.findall(r"#\w+", caption.lower())
            hashtags.extend(found_hashtags)
    
    if not hashtags:
        print("⚠️  No hashtags found in the captions")
        return []
    
    # Count hashtags and return top 10
    hashtag_counts = Counter(hashtags)
    return hashtag_counts.most_common(10)
