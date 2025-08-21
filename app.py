import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import our modules
from apify_scraper import run_scraper, run_scraper_by_domain
from data_cleaner import normalize_data
from analyze_hashtags import extract_hashtags, analyze_domain_hashtags, find_trending_hashtags
from engagement_estimator import estimate_avg_engagement
from config import DOMAIN_HASHTAGS, USE_TRENDING_HASHTAGS
from trending_hashtags import get_hashtags_for_domain

# Page configuration
st.set_page_config(
    page_title="Instagram Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Premium Instagram Analytics Tool - Powered by AI"
    }
)

# Custom CSS for premium styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Success/Error message styling */
    .success-message {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Hashtag chip styling */
    .hashtag-chip {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display the premium header section"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📊 Instagram Analytics Pro</h1>
        <p class="header-subtitle">Premium AI-Powered Social Media Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

def display_metrics_cards(metrics_data):
    """Display metrics in premium cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics_data.get('total_posts', 0)}</p>
            <p class="metric-label">Total Posts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics_data.get('total_hashtags', 0)}</p>
            <p class="metric-label">Total Hashtags</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics_data.get('unique_hashtags', 0)}</p>
            <p class="metric-label">Unique Hashtags</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics_data.get('diversity', 0)}%</p>
            <p class="metric-label">Hashtag Diversity</p>
        </div>
        """, unsafe_allow_html=True)

def create_hashtag_chart(hashtag_data):
    """Create an interactive hashtag frequency chart"""
    if not hashtag_data:
        return None
    
    hashtags, counts = zip(*hashtag_data[:15])
    
    fig = px.bar(
        x=counts,
        y=hashtags,
        orientation='h',
        title="🏷️ Top Trending Hashtags",
        labels={'x': 'Frequency', 'y': 'Hashtags'},
        color=counts,
        color_continuous_scale=['#667eea', '#764ba2']
    )
    
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        title_font_color="#2c3e50",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_engagement_heatmap(engagement_df):
    """Create an engagement heatmap"""
    if engagement_df.empty:
        return None
    
    # Prepare data for heatmap
    heatmap_data = engagement_df.pivot_table(
        values='likesCount', 
        index='day', 
        columns='hour', 
        fill_value=0
    )
    
    fig = px.imshow(
        heatmap_data,
        title="📈 Engagement Heatmap by Day & Hour",
        labels=dict(x="Hour", y="Day of Week", color="Avg Likes"),
        color_continuous_scale=['#667eea', '#764ba2']
    )
    
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        title_font_color="#2c3e50",
        height=400
    )
    
    return fig

def create_domain_distribution_chart(domain_categories):
    """Create a pie chart for domain distribution"""
    if not domain_categories:
        return None
    
    domain_names = []
    domain_counts = []
    
    for domain, hashtags in domain_categories.items():
        if hashtags:
            domain_names.append(domain.title())
            domain_counts.append(len(hashtags))
    
    if not domain_names:
        return None
    
    fig = px.pie(
        values=domain_counts,
        names=domain_names,
        title="🎯 Hashtag Distribution by Domain",
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    )
    
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        title_font_color="#2c3e50",
        height=400
    )
    
    return fig

def display_hashtag_chips(hashtags, title):
    """Display hashtags as premium chips"""
    st.markdown(f"### {title}")
    
    chips_html = ""
    for hashtag, count in hashtags[:20]:
        chips_html += f'<span class="hashtag-chip">{hashtag} ({count})</span>'
    
    st.markdown(chips_html, unsafe_allow_html=True)

def run_analysis(analysis_type, target, use_trending):
    """Run the Instagram analysis"""
    try:
        # Update configuration based on user choice
        if analysis_type == "Domain Analysis":
            import config
            config.USE_TRENDING_HASHTAGS = use_trending
            raw_data = run_scraper_by_domain(target)
        else:
            raw_data = run_scraper(target)
        
        if not raw_data:
            return None, "❌ No data retrieved. Please check your input and try again."
        
        # Normalize data
        df = normalize_data(raw_data)
        
        # Perform analysis
        if analysis_type == "Domain Analysis":
            hashtag_analysis = analyze_domain_hashtags(df["caption"], target.lower())
        else:
            hashtags = extract_hashtags(df["caption"])
            hashtag_analysis = {
                'total_hashtags': len([h for sublist in df["caption"].str.findall(r'#\w+') for h in sublist]),
                'unique_hashtags': len(set([h for sublist in df["caption"].str.findall(r'#\w+') for h in sublist])),
                'top_hashtags': hashtags,
                'hashtag_diversity': 0
            }
        
        engagement_df = estimate_avg_engagement(df)
        
        return {
            'raw_data': raw_data,
            'df': df,
            'hashtag_analysis': hashtag_analysis,
            'engagement_df': engagement_df
        }, None
        
    except Exception as e:
        return None, f"❌ Error during analysis: {str(e)}"

def main():
    """Main Streamlit app"""
    display_header()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Domain Analysis", "Profile Analysis"],
            help="Choose between domain-based hashtag analysis or profile-specific analysis"
        )
        
        if analysis_type == "Domain Analysis":
            st.markdown("### 🎯 Domain Selection")
            target = st.selectbox(
                "Select Domain",
                list(DOMAIN_HASHTAGS.keys()),
                format_func=lambda x: x.title(),
                help="Select the domain/topic you want to analyze"
            )
            
            st.markdown("### 🚀 Hashtag Discovery")
            use_trending = st.toggle(
                "Use Trending Hashtag Discovery",
                value=USE_TRENDING_HASHTAGS,
                help="Enable dynamic trending hashtag discovery for more current results"
            )
            
            if use_trending:
                st.success("🔥 Will discover current trending hashtags")
            else:
                st.info("📋 Will use predefined hashtag sets")
                
        else:
            st.markdown("### 📱 Profile Selection")
            target = st.text_input(
                "Instagram Username",
                placeholder="Enter username (e.g., natgeo)",
                help="Enter the Instagram username to analyze (without @)"
            )
            use_trending = False
        
        # Analysis button
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if target:
                st.session_state.run_analysis = True
                st.session_state.analysis_config = {
                    'type': analysis_type,
                    'target': target,
                    'use_trending': use_trending
                }
            else:
                st.error("Please provide a target for analysis")
    
    # Main content area
    if hasattr(st.session_state, 'run_analysis') and st.session_state.run_analysis:
        config = st.session_state.analysis_config
        
        # Show analysis info
        st.markdown("## 📊 Analysis In Progress")
        
        if config['type'] == "Domain Analysis":
            st.info(f"🎯 Analyzing {config['target'].title()} domain with {'trending' if config['use_trending'] else 'static'} hashtags")
        else:
            st.info(f"📱 Analyzing @{config['target']} profile")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run analysis
        with st.spinner("🔍 Analyzing Instagram data..."):
            progress_bar.progress(25)
            status_text.text("Fetching data from Instagram...")
            
            results, error = run_analysis(config['type'], config['target'], config['use_trending'])
            
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
        
        # Clear the run flag
        st.session_state.run_analysis = False
        
        if error:
            st.error(error)
        elif results:
            # Display results
            st.markdown("## 📈 Analysis Results")
            
            # Metrics cards
            hashtag_analysis = results['hashtag_analysis']
            metrics_data = {
                'total_posts': len(results['df']),
                'total_hashtags': hashtag_analysis.get('total_hashtags', 0),
                'unique_hashtags': hashtag_analysis.get('unique_hashtags', 0),
                'diversity': hashtag_analysis.get('hashtag_diversity', 0)
            }
            display_metrics_cards(metrics_data)
            
            # Charts section
            col1, col2 = st.columns(2)
            
            with col1:
                # Hashtag frequency chart
                if hashtag_analysis.get('top_hashtags'):
                    fig = create_hashtag_chart(hashtag_analysis['top_hashtags'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Domain distribution chart
                if config['type'] == "Domain Analysis" and hashtag_analysis.get('domain_categories'):
                    fig = create_domain_distribution_chart(hashtag_analysis['domain_categories'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            # Engagement heatmap
            if not results['engagement_df'].empty:
                st.markdown("### 📊 Engagement Analysis")
                
                # Prepare data for heatmap
                engagement_data = results['engagement_df'].reset_index()
                if not engagement_data.empty:
                    fig = create_engagement_heatmap(engagement_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                # Best posting time
                if not results['engagement_df'].empty:
                    best_time = results['engagement_df'].sort_values('likesCount', ascending=False).iloc[0]
                    st.success(f"⭐ Best time to post: **{best_time.name[0]} at {best_time.name[1]}:00** (Avg Likes: {best_time['likesCount']:.2f})")
            
            # Hashtag insights
            if config['type'] == "Domain Analysis":
                st.markdown("### 🏷️ Hashtag Insights")
                
                tab1, tab2, tab3 = st.tabs(["Top Hashtags", "Domain Categories", "Trending"])
                
                with tab1:
                    if hashtag_analysis.get('top_hashtags'):
                        display_hashtag_chips(hashtag_analysis['top_hashtags'], "Most Popular Hashtags")
                
                with tab2:
                    if hashtag_analysis.get('domain_categories'):
                        for domain, hashtags in hashtag_analysis['domain_categories'].items():
                            if hashtags:
                                st.markdown(f"**{domain.title()} ({len(hashtags)} hashtags)**")
                                display_hashtag_chips(hashtags[:10], "")
                
                with tab3:
                    if hashtag_analysis.get('uncategorized'):
                        display_hashtag_chips(hashtag_analysis['uncategorized'], "Trending Uncategorized Hashtags")
            
            # Export options
            st.markdown("### 📥 Export Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Download Data (CSV)", use_container_width=True):
                    csv = results['df'].to_csv(index=False)
                    st.download_button(
                        label="📁 Download CSV",
                        data=csv,
                        file_name=f"instagram_analysis_{config['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📋 Download Hashtags (JSON)", use_container_width=True):
                    hashtag_json = json.dumps(hashtag_analysis, indent=2)
                    st.download_button(
                        label="📁 Download JSON",
                        data=hashtag_json,
                        file_name=f"hashtag_analysis_{config['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col3:
                if st.button("📈 Generate Report", use_container_width=True):
                    st.info("📄 Report generation feature coming soon!")
    
    else:
        # Welcome screen
        st.markdown("## 🌟 Welcome to Instagram Analytics Pro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Domain Analysis
            Analyze trending hashtags and engagement patterns for specific topics like:
            - 🍕 Food & Cooking
            - 👗 Fashion & Style  
            - ✈️ Travel & Adventure
            - 💪 Fitness & Health
            - And 6 more domains!
            """)
        
        with col2:
            st.markdown("""
            ### 📱 Profile Analysis
            Deep dive into specific Instagram profiles:
            - 📊 Posting patterns
            - 🏷️ Hashtag strategies
            - ⏰ Optimal posting times
            - 📈 Engagement analysis
            """)
        
        st.markdown("""
        ---
        ### 🚀 Getting Started
        1. **Select your analysis type** in the sidebar
        2. **Choose a domain or enter a username**
        3. **Configure hashtag discovery settings**
        4. **Click "Start Analysis"** and get insights!
        """)
        
        # Feature showcase
        st.markdown("### ✨ Premium Features")
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            **🔥 Trending Discovery**
            - Real-time hashtag trends
            - AI-powered recommendations
            - Dynamic content analysis
            """)
        
        with feature_col2:
            st.markdown("""
            **📊 Advanced Analytics**
            - Interactive visualizations
            - Engagement heatmaps
            - Domain categorization
            """)
        
        with feature_col3:
            st.markdown("""
            **💼 Export & Reports**
            - CSV data export
            - JSON hashtag reports
            - Custom analysis reports
            """)

if __name__ == "__main__":
    main()
