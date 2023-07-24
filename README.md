### Setup 
1. Copy / download `youtube_nowplaying.py` to your Hexchat addons directory: `%appdata%\HexChat\addons`
2. Install [PyGetWindow](https://pypi.org/project/PyGetWindow/)
3. In Hexchat, load the script with `/LOAD youtube_nowplaying.py`
   

### Usage
1. Play a song from YouTube in Chrome, Brave, Edge or Firefox.
2. Type `/ytnp` into your desired channel

### Output:   
<img width="873" alt="image" src="https://github.com/Moodkiller/YouTube-NowPlaying/assets/11341653/1c06045a-4e70-45d0-803f-6ac2a5e3ac36">

Note: the two lines above can be disabled, they are just part of the debugging.

### Features
* Uses API to scrape any info you like from a video. Currently setup to show Title, Channel, Views (human format), Likes (human format) and Uploaded timeframe (human format)
* Will display the current active playing song (i.e you can have mulitple YouTube tabs open but the script will only use the active tab as its source)
* Debugging: Will display any errors if the API call failed (i.e in the case of reaching a limit)
* If API reaches its limit / fails, script will fall back to just showing the title pulled from the active tab in the browser
