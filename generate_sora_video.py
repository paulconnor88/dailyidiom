#!/usr/bin/env python3
"""
Generate Sora video using existing pixel art as reference
"""
import requests
import time
import sys

# Your OpenAI API key
API_KEY = "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"

def create_video():
    """Create Sora video with image reference"""
    print("Creating Sora video...")
    print()
    
        'model': 'sora-2',  # Use sora-2 for testing (faster, cheaper)
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "raining cats and dogs" (meaning: heavy rain). Show cats and dogs literally falling from dark rain clouds in a whimsical, playful way. SNES Super Nintendo retro game style, bright colors, continuous gentle falling motion. The animation should be an obvious visual representation of the phrase without showing any text.',
        'seconds': '4',  # Start with 4 seconds
        'size': '1280x720',  # Square format
    }
    
    response = requests.post(
        'https://api.openai.com/v1/videos',
        headers={'Authorization': f'Bearer {API_KEY}'},
        data=data
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    video_job = response.json()
    print(f"✓ Video job created: {video_job['id']}")
    print(f"  Status: {video_job['status']}")
    print()
    
    return video_job['id']

def check_status(video_id):
    """Poll video status until complete"""
    print("Waiting for video to generate...")
    bar_length = 30
    
    while True:
        response = requests.get(
            f'https://api.openai.com/v1/videos/{video_id}',
            headers={'Authorization': f'Bearer {API_KEY}'}
        )
        
        job = response.json()
        status = job['status']
        progress = job.get('progress', 0)
        
        # Progress bar
        filled = int((progress / 100) * bar_length)
        bar = '=' * filled + '-' * (bar_length - filled)
        
        sys.stdout.write(f'\rProgress: [{bar}] {progress}% - Status: {status}')
        sys.stdout.flush()
        
        if status == 'completed':
            print('\n✓ Video completed!')
            return True
        elif status == 'failed':
            print(f'\n✗ Video failed: {job.get("error", {})}')
            return False
        
        time.sleep(5)  # Check every 5 seconds

def download_video(video_id):
    """Download the completed video"""
    print('Downloading video...')
    
    response = requests.get(
        f'https://api.openai.com/v1/videos/{video_id}/content',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    
    if response.status_code == 200:
        filename = 'idiom_images_pixel/idiom_07_raining_cats_and_dogs.mp4'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'✓ Saved: {filename}')
        return filename
    else:
        print(f'✗ Download failed: {response.status_code}')
        return None

def main():
    print("=" * 60)
    print("Sora Video Generation: Raining Cats and Dogs")
    print("=" * 60)
    print()
    print("Model: sora-2 (fast)")
    print("Duration: 4 seconds")
    print("Cost: ~$0.50")
    print()
    print("=" * 60)
    print()
    
    # Step 1: Create video
    video_id = create_video()
    if not video_id:
        return
    
    # Step 2: Wait for completion
    if not check_status(video_id):
        return
    
    # Step 3: Download
    result = download_video(video_id)
    
    if result:
        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print()
        print(f"Video saved: {result}")
        print()
        print("Next steps:")
        print("1. Preview the video")
        print("2. Update HTML to use .mp4 instead of .png")
        print("3. Push to GitHub")

if __name__ == "__main__":
    main()
