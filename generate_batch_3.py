#!/usr/bin/env python3
"""
Generate Sora videos for 3 idioms
"""
import requests
import time
import sys

API_KEY = "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"

idioms = [
    {
        'id': 2,
        'name': 'spill_the_beans',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "spill the beans" (meaning: reveal a secret). Show a jar tipping over with colorful beans spilling and bouncing everywhere. SNES Super Nintendo retro game style, bright playful colors, continuous motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 10,
        'name': 'kick_the_bucket',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "kick the bucket" (meaning: to die, but show it playfully). Show a foot in a shoe kicking a wooden bucket that tips over and bounces. SNES Super Nintendo retro game style, bright cheerful colors, simple playful motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 18,
        'name': 'the_elephant_in_the_room',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "the elephant in the room" (meaning: obvious problem everyone ignores). Show a large elephant standing in a living room while people sit on furniture pretending not to notice. SNES Super Nintendo retro game style, absurd humor, subtle movements. The animation should be an obvious visual representation of the phrase without showing any text.'
    }
]

def create_video(idiom):
    """Create Sora video"""
    print(f"Creating video for: {idiom['name']}")
    
    data = {
        'model': 'sora-2',
        'prompt': idiom['prompt'],
        'seconds': '4',
        'size': '1280x720',
    }
    
    response = requests.post(
        'https://api.openai.com/v1/videos',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    if response.status_code != 200:
        print(f"  ✗ Error: {response.status_code}")
        print(response.text)
        return None
    
    job = response.json()
    print(f"  ✓ Job created: {job['id']}")
    return job['id']

def wait_for_completion(video_id, idiom_name):
    """Poll until complete"""
    bar_length = 30
    
    while True:
        response = requests.get(
            f'https://api.openai.com/v1/videos/{video_id}',
            headers={'Authorization': f'Bearer {API_KEY}'}
        )
        
        job = response.json()
        status = job['status']
        progress = job.get('progress', 0)
        
        filled = int((progress / 100) * bar_length)
        bar = '=' * filled + '-' * (bar_length - filled)
        
        sys.stdout.write(f'\r  [{bar}] {progress}% - {status}     ')
        sys.stdout.flush()
        
        if status == 'completed':
            print('\n  ✓ Completed!')
            return True
        elif status == 'failed':
            print(f'\n  ✗ Failed: {job.get("error", {})}')
            return False
        
        time.sleep(5)

def download_video(video_id, idiom):
    """Download completed video"""
    response = requests.get(
        f'https://api.openai.com/v1/videos/{video_id}/content',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    
    if response.status_code == 200:
        filename = f"idiom_images_pixel/idiom_{idiom['id']:02d}_{idiom['name']}_sora.mp4"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'  ✓ Saved: {filename}')
        return filename
    else:
        print(f'  ✗ Download failed')
        return None

def main():
    print("=" * 60)
    print("Batch Sora Video Generation")
    print("=" * 60)
    print(f"Idioms: 3")
    print(f"Cost: ~$1.50")
    print(f"Time: ~10-15 minutes")
    print("=" * 60)
    print()
    
    successful = []
    failed = []
    
    for i, idiom in enumerate(idioms, 1):
        print(f"\n[{i}/3] {idiom['name'].replace('_', ' ').title()}")
        print("-" * 60)
        
        video_id = create_video(idiom)
        if not video_id:
            failed.append(idiom['name'])
            continue
        
        if wait_for_completion(video_id, idiom['name']):
            result = download_video(video_id, idiom)
            if result:
                successful.append(idiom['name'])
            else:
                failed.append(idiom['name'])
        else:
            failed.append(idiom['name'])
        
        if i < len(idioms):
            print(f"\n  Waiting 10 seconds before next video...")
            time.sleep(10)
    
    print()
    print("=" * 60)
    print("BATCH COMPLETE")
    print("=" * 60)
    print(f"✓ Successful: {len(successful)}/3")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")
    print()
    print("Next: Update HTML and push to GitHub!")

if __name__ == "__main__":
    main()
