#!/usr/bin/env python3
"""
Launch script for Instagram Analytics Pro UI
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import plotly
        print("✅ All UI dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing required dependencies...")
        return False

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def launch_ui():
    """Launch the Streamlit UI"""
    try:
        print("🚀 Launching Instagram Analytics Pro UI...")
        print("🌐 Opening in your default browser...")
        print("📊 Access the app at: http://localhost:8501")
        print("\n" + "="*50)
        print("🎯 Premium Instagram Analytics Interface")
        print("📈 Real-time trending hashtag discovery")
        print("🏷️  Advanced domain categorization")
        print("📊 Interactive visualizations")
        print("💼 Export functionality")
        print("="*50 + "\n")
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Instagram Analytics Pro UI stopped")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")

def main():
    """Main function"""
    print("📊 Instagram Analytics Pro - UI Launcher")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the Instagram-scraper directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("pip install streamlit plotly altair")
            sys.exit(1)
    
    # Launch UI
    launch_ui()

if __name__ == "__main__":
    main()
