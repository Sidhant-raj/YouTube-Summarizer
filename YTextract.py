# !pip install youtube-transcript-api
import re
from youtube_transcript_api import YouTubeTranscriptApi

def is_youtube_link(url):
    return re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/', url) is not None


def youtubeCaptionExtractor(video_url: str):
    if is_youtube_link(video_url):
        try:
            video_id = video_url.split("v=")[1]
        except Exception as e:
            try:
                video_id = re.search(r'be/(.*?)[?&]', video_url).group(1)
            except Exception as e:
                return -2
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = " ".join([entry['text'] for entry in transcript])
            return str(transcript_text)
        except Exception as e:
            return -1
    else:
        return -2
