from django.shortcuts import render, get_object_or_404
import requests
import json
from django.http import JsonResponse
import os
from django.conf import settings
from datetime import datetime
import markdown
from slugify import slugify
from django.shortcuts import render
from .yt_utils import get_channel_playlists, get_playlist_videos
from django.http import HttpResponse
from slugify import slugify

# API Key and Channel ID
API_KEY = "AIzaSyAY6i8feTdUJwlaGJm6EqctLvXsGFFLfjY"
CHANNEL_ID = "UCoJiWVXfDYdAQmad0ljB4pw"  # Your Channel ID

# Mapping for title slugs → playlist IDs
playlist_slug_map = {}


def playlist_detail(slug):
    playlists = get_channel_playlists(API_KEY, CHANNEL_ID)  # Use the global API_KEY and CHANNEL_ID
    
    # Search for the playlist using slugified title
    for playlist in playlists:
        if slugify(playlist["snippet"]["title"]) == slug:
            return playlist["id"], playlist["snippet"]["title"]
    return None, None

def content_list(request):
    # Fetch all playlists
    playlists = get_channel_playlists(API_KEY, CHANNEL_ID)

    # Update slug map and create embed URLs
    global playlist_slug_map
    playlist_slug_map = {slugify(p["snippet"]["title"]): p["id"] for p in playlists}

    # Create embed URLs for each playlist
    for playlist in playlists:
        playlist['embed_url'] = f"https://www.youtube.com/embed/?listType=playlist&list={playlist['id']}"
        playlist['slug'] = slugify(playlist["snippet"]["title"])

    # Render the template with playlists
    return render(request, "core/content.html", {"playlists": playlists})

def playlist_detail_view(request, slug):
    playlist_id, playlist_title = playlist_detail(slug)
    if not playlist_id:
        return HttpResponse("Playlist not found", status=404)
    
    videos = get_playlist_videos(API_KEY, playlist_id)
    
    # Add embed URLs to each video
    for video in videos:
        video_id = video["contentDetails"]["videoId"]
        video["embed_url"] = f"https://www.youtube.com/embed/{video_id}"

    return render(request, "core/playlist_detail.html", {
        "videos": videos,
        "title": playlist_title
    })


def load_response(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'responses', file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_name} was not found at {file_path}")
    
    # Reading the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Parse the content into a dictionary
    responses = {}
    current_key = None
    current_content = []

    # Split content by lines
    for line in content.splitlines():
        if line.startswith('# '):  # New section starts with '# '
            if current_key:
                responses[current_key] = '\n'.join(current_content).strip()
            current_key = line[2:].strip()  # Remove the '# ' and store the section name
            current_content = []
        else:
            current_content.append(line.strip())

    # Add the last collected content to the dictionary
    if current_key:
        responses[current_key] = '\n'.join(current_content).strip()

    return responses

def ai(request):
    responses = load_response('responses.md')
    
    context = {
        'gaza': responses.get('Gaza', ''),
        'israel': responses.get('Israel', ''),
        'reason': responses.get('Reason of the War', ''),
        'aims': responses.get('Aims of the Conflict', ''),
        'world': responses.get('World Status', ''),
        'timeline': responses.get('Timeline', ''),
        'media': responses.get('Media Coverage', ''),
        'ummah': responses.get('Ummah\'s Response', ''),
    }
    
    return render(request, 'core/ai.html', context)

def home(request):
    return render(request, 'core/home.html')

def courses(request):
    return render(request, 'core/courses.html')

def about(request):
    return render(request, 'core/about.html')



def ai_details(request, topic):
    """
    Display detailed content for a specific AI topic
    from text files stored in the responses directory.
    """
    # List of valid topics for security
    valid_topics = [
        'gaza', 'israel', 'reason', 'aims', 
        'world', 'timeline', 'media', 'ummah'
    ]
    
    # Validate the topic
    if topic not in valid_topics:
        raise Http404("Topic not found")
    
    # Path to the text file
    file_path = os.path.join('responses', f'{topic}.md')
    
    try:
        # Try to read the content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Convert the Markdown content to HTML
        content_html = markdown.markdown(content)
        
        # Get file modification time
        modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Format topic name for display (capitalize words)
        topic_name = topic.replace('_', ' ')
        
        # Render the template with the file content
        return render(request, 'core/ai_details.html', {
            'topic': topic,
            'topic_name': topic_name,
            'content': content_html,  # Pass the HTML-formatted content
            'last_updated': modification_time,
        })
    
    except FileNotFoundError:
        # If the file doesn't exist, show an error message
        content = f"Detailed information for '{topic}' is not available yet."
        return render(request, 'core/ai_details.html', {
            'topic': topic,
            'topic_name': topic.replace('_', ' '),
            'content': content,
            'last_updated': datetime.now(),
        })

