import hexchat
import pygetwindow as gw
import re
import requests
import json
from datetime import datetime

__module_name__ = "YouTube Now Playing"
__module_author__ = "Moodkiller"
__module_version__ = "1.1"
__module_description__ = "Displays the currently playing YouTube video information"

# Your YouTube Data API key
API_KEY = "PLACE_YOUR_API_KEY_HERE"

def get_youtube_info():
    try:
        # Get all open windows
        all_windows = gw.getWindowsWithTitle('')

        # Check if any window title contains YouTube video information
        for window in all_windows:
            window_title = window.title
            hexchat.prnt(f"Detected Window Title: {window_title}")
            match = re.search(r"^(.*?)\s-\sYouTube\s-\s(Google Chrome|Brave|Mozilla Firefox|Microsoft Edge)$", window_title)
            if match:
                browser_name = match.group(2)
		# Uncomment the below to see the matching windows for troubleshooting
                # hexchat.prnt(f"Matching YouTube Window Title in {browser_name}: {match.group(1)}")
                title = match.group(1)
                video_id = get_video_id(title)
                if video_id:
                    video_info = get_video_details(video_id)
                    if video_info:
                        views = format_views(video_info["viewCount"])
                        upload_date = video_info["publishedAt"]
                        upload_ago = calculate_time_difference(upload_date)
                        channel = video_info["channelTitle"]
                        likes = format_views(video_info["likeCount"])
                        message = f"me is now playing \x034{title}\x03\x0f	from \x034{channel}\x03 (\x0310Views:\x03 {views} • \x0310Likes:\x03 {likes} • \x0310Uploaded:\x03 {upload_ago}\x03\x0f) in {browser_name}"
                        send_message_to_channel(message)
                        return

        # No matching window title found
        #title = get_current_song_title()
        if title:
            message = f"me is now playing: \x02\x034{title}\x03\x02"
            send_message_to_channel(message)

    except Exception as e:
        hexchat.prnt(f"Error retrieving YouTube video information: {str(e)}")


def get_video_id(title):
    try:
        # Make a request to the YouTube Data API search endpoint to get video details
        url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&type=video&q={title}"
        response = requests.get(url)
        data = response.json()

        # Check if any video search results are returned
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]
            return video_id

        # Check if quota exceeded error occurred
        if "error" in data and "quotaExceeded" in [err["reason"] for err in data["error"]["errors"]]:
            hexchat.prnt("YouTube Data API quota exceeded. Please try again later.")

    except Exception as e:
        hexchat.prnt(f"Error retrieving video ID: {str(e)}")

    return None


def get_video_details(video_id):
    try:
        # Make a request to the YouTube Data API videos endpoint to get video details
        url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&part=statistics,snippet&id={video_id}"
        response = requests.get(url)
        data = response.json()

        # Print the response data for debugging
        #hexchat.prnt(f"Video Details Response: {data}")

        # Check if video details are returned
        if "items" in data and len(data["items"]) > 0:
            video_info = data["items"][0]
            return {
                "viewCount": video_info["statistics"]["viewCount"],
                "publishedAt": video_info["snippet"]["publishedAt"],
                "channelTitle": video_info["snippet"]["channelTitle"],
				"likeCount": video_info["statistics"]["likeCount"]
            }

    except Exception as e:
        hexchat.prnt(f"Error retrieving video details: {str(e)}")

    return None


def format_views(views):
    try:
        views = int(views)
        if views >= 1_000_000_000:
            views = views / 1_000_000_000
            return f"{views:.1f}B"
        elif views >= 1_000_000:
            views = views / 1_000_000
            return f"{views:.1f}M"
        elif views >= 1_000:
            views = views / 1_000
            return f"{views:.1f}K"
        else:
            return str(views)
    except ValueError:
        return views


def calculate_time_difference(upload_date):
    try:
        now = datetime.now()
        upload_datetime = datetime.strptime(upload_date, "%Y-%m-%dT%H:%M:%SZ")
        time_difference = now - upload_datetime

        years = time_difference.days // 365
        months = time_difference.days % 365 // 30

        if years > 0:
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif months > 0:
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            return "Less than a month ago"
    except Exception as e:
        hexchat.prnt(f"Error calculating time difference: {str(e)}")

    return ""


def send_message_to_channel(message):
    hexchat.command("ME " + message)


# Callback function for the /ytnp command
def youtube_now_playing(word, word_eol, userdata):
    get_youtube_info()
    return hexchat.EAT_ALL


# Register the command /ytnp to retrieve YouTube video information
hexchat.hook_command('ytnp', youtube_now_playing, help="/ytnp - Get the currently playing YouTube video information")

hexchat.prnt("YouTube Now Playing plugin loaded")
