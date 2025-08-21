import re
from collections import Counter, defaultdict
from config import DOMAIN_HASHTAGS

def extract_hashtags(captions, top_n=20):
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
    
    # Count hashtags and return top N
    hashtag_counts = Counter(hashtags)
    return hashtag_counts.most_common(top_n)


def analyze_domain_hashtags(captions, domain=None):
    """
    Advanced hashtag analysis with domain-specific insights
    """
    if captions.empty:
        print("⚠️  No captions found for hashtag analysis")
        return {}
    
    hashtags = []
    for caption in captions.dropna():
        if isinstance(caption, str):
            found_hashtags = re.findall(r"#\w+", caption.lower())
            hashtags.extend(found_hashtags)
    
    if not hashtags:
        print("⚠️  No hashtags found in the captions")
        return {}
    
    hashtag_counts = Counter(hashtags)
    total_hashtags = len(hashtags)
    unique_hashtags = len(hashtag_counts)
    
    # Categorize hashtags by domain
    domain_categories = defaultdict(list)
    uncategorized = []
    
    for hashtag, count in hashtag_counts.items():
        categorized = False
        for domain_name, domain_tags in DOMAIN_HASHTAGS.items():
            if hashtag in [tag.lower() for tag in domain_tags]:
                domain_categories[domain_name].append((hashtag, count))
                categorized = True
                break
        
        if not categorized:
            uncategorized.append((hashtag, count))
    
    # Sort each category by count
    for domain_name in domain_categories:
        domain_categories[domain_name].sort(key=lambda x: x[1], reverse=True)
    
    # Sort uncategorized hashtags
    uncategorized.sort(key=lambda x: x[1], reverse=True)
    
    analysis = {
        'total_hashtags': total_hashtags,
        'unique_hashtags': unique_hashtags,
        'top_hashtags': hashtag_counts.most_common(20),
        'domain_categories': dict(domain_categories),
        'uncategorized': uncategorized[:15],  # Top 15 uncategorized
        'hashtag_diversity': round(unique_hashtags / total_hashtags * 100, 2) if total_hashtags > 0 else 0
    }
    
    return analysis


def find_trending_hashtags(captions, min_frequency=2):
    """
    Find trending hashtags that appear multiple times
    """
    hashtags = []
    for caption in captions.dropna():
        if isinstance(caption, str):
            found_hashtags = re.findall(r"#\w+", caption.lower())
            hashtags.extend(found_hashtags)
    
    hashtag_counts = Counter(hashtags)
    trending = [(tag, count) for tag, count in hashtag_counts.items() 
                if count >= min_frequency]
    
    return sorted(trending, key=lambda x: x[1], reverse=True)
