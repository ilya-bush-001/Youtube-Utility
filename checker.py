import re
from datetime import datetime
import pytz
from googleapiclient.discovery import build
import os
from typing import Optional, Tuple, Dict, List

API_KEY = "AIzaSyBLnj5udMgmy59Z2s01FOcCfufyHu_JLEg"  

def extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_details(video_id: str) -> Optional[Tuple[Dict, Dict, List[str]]]:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response['items']:
            return None
        
        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']
        tags = snippet.get('tags', [])
        
        return snippet, statistics, tags
    
    except Exception as e:
        print(f"[❌] Error receiving data: {e}")
        return None

def format_views(view_count: str) -> str:
    try:
        count = int(view_count)
        return f"{count:,}".replace(",", " ")
    except:
        return view_count

def display_video_info(snippet: Dict, statistics: Dict, tags: List[str]):
    publish_time = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    publish_time = publish_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Kiev'))
    
    # Data collection
    title = snippet['title']
    views = format_views(statistics.get('viewCount', 'N/A'))
    likes = format_views(statistics.get('likeCount', 'N/A'))
    comments = format_views(statistics.get('commentCount', 'N/A'))
    channel_title = snippet['channelTitle']

    # Information output
    print("\n" + "="*50)
    print(f"📺 Video title: {title}")
    print(f"👤 Channel: {channel_title}")
    print(f"⏰ Publish time: {publish_time.strftime('%H:%M (%d.%m.%Y)')}")
    print(f"👀 Views: {views}")
    print(f"👍 Likes: {likes}")
    print(f"💬 Comments: {comments}")

    # Output tags, if any
    if tags:
        print("\n🏷️ Tags:")
        print(", ".join(tags))
    else:
        print("\nℹ️ No tags available")
    
    print("="*50)

def main():
    # Initialization of the API key
    if API_KEY == "YOUR_API_KEY":
        print("\n⚠️ Please set your YouTube Data API key in the script!")
        print("You can get the key here: https://console.cloud.google.com/")
        input("\nPress Enter to exit...")
        return
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("====- YouTube Video Analyzer -====")
        print("Select an action:")
        print("1. Check video information")
        print("2. Exit")
        print("="*34)
        
        choice = input("Your choice: ").strip()
        
        if choice == "2":
            print("\nThank you for using the app!")
            break
            
        elif choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*34)
            url = input("Enter the link to the video (for example: https://youtube.com/watch?v=dQw4w9WgXcQ): ")
            print("="*34)
            
            video_id = extract_video_id(url)
            if not video_id:
                print("\n❌ Error: Invalid link format or video not found!")
                input("\nPress Enter to continue...")
                continue
            
            result = get_video_details(video_id)
            if not result:
                print("\n❌ Error: Unable to retrieve video data!")
                input("\nPress Enter to continue...")
                continue
            
            snippet, statistics, tags = result
            display_video_info(snippet, statistics, tags)
            
            input("\nPress Enter to continue...")
            
        else:
            print("\n❌ Wrong choice, try again!")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()