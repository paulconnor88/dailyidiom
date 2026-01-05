#!/usr/bin/env python3
"""
Generate pixel art DALL-E images for all 20 idioms
"""
import os
import requests
import time
from pathlib import Path

# Your OpenAI API key - REMEMBER TO REGENERATE THIS AFTER THE SESSION
API_KEY = "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"

# Create images directory
Path("idiom_images_pixel").mkdir(exist_ok=True)

# All 20 idioms with PIXEL ART prompts
idioms = [
    {
        "id": 1,
        "text": "break the ice",
        "prompt": "16-bit pixel art: Person with hammer breaking giant ice block. SNES game style, chunky pixels, bright colors, simple scene."
    },
    {
        "id": 2,
        "text": "spill the beans",
        "prompt": "16-bit pixel art: Jar tipping over with beans spilling everywhere. Game Boy aesthetic, colorful beans, retro gaming style."
    },
    {
        "id": 3,
        "text": "piece of cake",
        "prompt": "16-bit pixel art: Single slice of cake on plate with fork. SNES style, vibrant colors, simple clean pixels."
    },
    {
        "id": 4,
        "text": "bite the bullet",
        "prompt": "16-bit pixel art: Determined character face with serious expression, golden star-shaped object nearby. SNES game style, no weapons, heroic theme."
    },
    {
        "id": 5,
        "text": "hit the nail on the head",
        "prompt": "16-bit pixel art: Hammer striking nail with perfect precision, spark effect. SNES style construction game aesthetic."
    },
    {
        "id": 6,
        "text": "let the cat out of the bag",
        "prompt": "16-bit pixel art: Cat jumping out of shopping bag, surprised expression. Game Boy style, cute pixel cat, simple scene."
    },
    {
        "id": 7,
        "text": "raining cats and dogs",
        "prompt": "16-bit pixel art: Cats and dogs falling from clouds, umbrellas below. SNES weather game style, whimsical pixels."
    },
    {
        "id": 8,
        "text": "costs an arm and a leg",
        "prompt": "16-bit pixel art: Character at shop counter looking shocked at expensive price tag with dollar signs. SNES RPG shop style."
    },
    {
        "id": 9,
        "text": "under the weather",
        "prompt": "16-bit pixel art: Character sitting under dark rain cloud, looking tired. Game Boy style, simple weather sprite."
    },
    {
        "id": 10,
        "text": "kick the bucket",
        "prompt": "16-bit pixel art: Foot kicking wooden bucket that's tipping over. SNES action game style, motion lines, simple scene."
    },
    {
        "id": 11,
        "text": "barking up the wrong tree",
        "prompt": "16-bit pixel art: Dog barking at empty tree while cat sits in different tree. Game Boy style, cute animals, simple forest."
    },
    {
        "id": 12,
        "text": "kill two birds with one stone",
        "prompt": "16-bit pixel art: Stone flying toward two birds on branch. SNES game style, motion trail, bright birds."
    },
    {
        "id": 13,
        "text": "the ball is in your court",
        "prompt": "16-bit pixel art: Tennis ball on tennis court with player waiting. SNES sports game style, overhead view."
    },
    {
        "id": 14,
        "text": "caught between a rock and a hard place",
        "prompt": "16-bit pixel art: Character squeezed between large boulder and wall. SNES puzzle game style, claustrophobic scene."
    },
    {
        "id": 15,
        "text": "burning bridges",
        "prompt": "16-bit pixel art: Wooden bridge on fire, character walking away. SNES adventure game style, flame animation frames."
    },
    {
        "id": 16,
        "text": "break a leg",
        "prompt": "16-bit pixel art: Theater stage with spotlight and performer taking dramatic bow. SNES stage performance style."
    },
    {
        "id": 17,
        "text": "a blessing in disguise",
        "prompt": "16-bit pixel art: Angel character wearing funny disguise with fake glasses and mustache. Game Boy style, cute sprite."
    },
    {
        "id": 18,
        "text": "the elephant in the room",
        "prompt": "16-bit pixel art: Large elephant in living room while people sit on furniture ignoring it. SNES interior scene, absurd humor."
    },
    {
        "id": 19,
        "text": "once in a blue moon",
        "prompt": "16-bit pixel art: Large blue moon in night sky with calendar showing crossed off days. SNES RPG night scene style."
    },
    {
        "id": 20,
        "text": "teaching your grandmother to suck eggs",
        "prompt": "16-bit pixel art: Elderly grandmother character with skeptical expression while young person gestures at egg. SNES character portrait style."
    }
]

def generate_image(idiom_data):
    """Generate a single image using DALL-E"""
    print(f"Generating image {idiom_data['id']}/20: '{idiom_data['text']}'...")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "dall-e-3",
                "prompt": idiom_data['prompt'],
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
        
        # Download the image
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code == 200:
            filename = f"idiom_images_pixel/idiom_{idiom_data['id']:02d}_{idiom_data['text'].replace(' ', '_')}.png"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"  ✓ Saved: {filename}")
            return filename
        
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return None

def main():
    print("=" * 60)
    print("PIXEL ART Image Generation for Daily Idiom")
    print("=" * 60)
    print(f"Total images: 20")
    print(f"Style: 16-bit pixel art / SNES / Game Boy")
    print(f"Estimated cost: ~$0.80 (20 images × $0.04)")
    print(f"Estimated time: ~25 minutes (with rate limiting)")
    print("=" * 60)
    print()
    
    generated = []
    failed = []
    
    for i, idiom in enumerate(idioms, 1):
        # Check if image already exists
        filename = f"idiom_images_pixel/idiom_{idiom['id']:02d}_{idiom['text'].replace(' ', '_')}.png"
        if os.path.exists(filename):
            print(f"[{i}/20] Skipping '{idiom['text']}' - already exists")
            generated.append(filename)
            continue
        
        result = generate_image(idiom)
        
        if result:
            generated.append(result)
        else:
            failed.append(idiom['text'])
        
        # Rate limiting: Wait 70 seconds between requests (free tier = 1/min)
        if i < len(idioms):
            print(f"  ⏱  Waiting 70 seconds before next image... ({i}/20 complete)")
            time.sleep(70)
    
    print()
    print("=" * 60)
    print(f"✓ Successfully generated: {len(generated)}/20 images")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")
    print("=" * 60)
    print()
    print(f"Pixel art images saved in ./idiom_images_pixel/ directory")
    print()
    print("IMPORTANT: Regenerate your OpenAI API key after this session!")
    print("Go to: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
