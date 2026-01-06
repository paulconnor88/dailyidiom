#!/usr/bin/env python3
"""
Generate 4 animation frames for 'raining cats and dogs'
Then we'll stitch them into a GIF
"""
import os
import requests
import time
from pathlib import Path

# Your OpenAI API key
API_KEY = "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"

# Create animation frames directory
Path("animation_frames").mkdir(exist_ok=True)

# 4 frames for the animation
frames = [
    {
        "frame": 1,
        "prompt": "16-bit pixel art: Dark rain clouds at top of frame, cats and dogs just starting to fall from clouds. SNES game style, bright colors, simple scene, animals high in sky."
    },
    {
        "frame": 2,
        "prompt": "16-bit pixel art: Cats and dogs falling through mid-air from rain clouds, halfway down the frame. SNES game style, motion lines, various poses, whimsical."
    },
    {
        "frame": 3,
        "prompt": "16-bit pixel art: Cats and dogs falling lower, nearly reaching ground level, umbrellas visible at bottom. SNES game style, anticipation of landing, colorful."
    },
    {
        "frame": 4,
        "prompt": "16-bit pixel art: Cats and dogs gently landed on ground with umbrellas, some still in air at top. SNES game style, complete cycle ready to loop, cheerful scene."
    }
]

def generate_frame(frame_data):
    """Generate a single animation frame using DALL-E"""
    print(f"Generating frame {frame_data['frame']}/4...")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "dall-e-3",
                "prompt": frame_data['prompt'],
                "n": 1,
                "size": "1024x1024",
                "quality": "standard"
            },
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        image_url = data['data'][0]['url']
        
        # Download the frame
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code == 200:
            filename = f"animation_frames/raining_cats_dogs_frame_{frame_data['frame']}.png"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"  ✓ Saved: {filename}")
            return filename
        
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return None

def main():
    print("=" * 60)
    print("Generating Animation Frames: Raining Cats and Dogs")
    print("=" * 60)
    print(f"Frames: 4")
    print(f"Cost: ~$0.16 (4 frames × $0.04)")
    print(f"Time: ~5 minutes")
    print("=" * 60)
    print()
    
    generated = []
    
    for i, frame in enumerate(frames, 1):
        result = generate_frame(frame)
        
        if result:
            generated.append(result)
        
        # Wait 70 seconds between requests (rate limit)
        if i < len(frames):
            print(f"  ⏱  Waiting 70 seconds... ({i}/4 complete)")
            time.sleep(70)
    
    print()
    print("=" * 60)
    print(f"✓ Generated {len(generated)}/4 frames")
    print("=" * 60)
    print()
    print("Next step: Stitch frames into animated GIF")
    print("Run: python3 create_gif.py")

if __name__ == "__main__":
    main()
