#!/usr/bin/env python3
"""
Generate DALL-E images for all 20 idioms with rate limiting
"""
import os
import requests
import time
from pathlib import Path

# Your OpenAI API key - REMEMBER TO REGENERATE THIS AFTER THE SESSION
API_KEY = "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"

# Create images directory
Path("idiom_images").mkdir(exist_ok=True)

# All 20 idioms with prompts
idioms = [
    {
        "id": 1,
        "text": "break the ice",
        "prompt": "A person using a hammer to break a large block of ice at a social gathering, surrounded by other people looking relieved and starting to smile. Vintage retro illustration style, warm colors, friendly atmosphere."
    },
    {
        "id": 2,
        "text": "spill the beans",
        "prompt": "Someone accidentally knocking over a large jar, with hundreds of colorful beans spilling out everywhere across a table. Vintage retro illustration style, comic book aesthetic."
    },
    {
        "id": 3,
        "text": "piece of cake",
        "prompt": "A single perfect slice of layered cake on a plate with a fork beside it, simple and inviting. Vintage retro illustration style, pastel colors."
    },
    {
        "id": 4,
        "text": "bite the bullet",
        "prompt": "A person with determined expression holding a bullet near their mouth, preparing to bite it. Vintage retro illustration style, dramatic lighting, no gore."
    },
    {
        "id": 5,
        "text": "hit the nail on the head",
        "prompt": "A hammer coming down precisely on the head of a nail, with a perfect impact spark. Vintage retro illustration style, close-up view, satisfying precision."
    },
    {
        "id": 6,
        "text": "let the cat out of the bag",
        "prompt": "A surprised cat jumping out of an open shopping bag, with someone holding the bag looking shocked. Vintage retro illustration style, playful and whimsical."
    },
    {
        "id": 7,
        "text": "raining cats and dogs",
        "prompt": "Cats and dogs literally falling from rain clouds in the sky, umbrellas open below. Vintage retro illustration style, whimsical and surreal."
    },
    {
        "id": 8,
        "text": "costs an arm and a leg",
        "prompt": "A person at a counter gesturing dramatically at an expensive item with price tag, looking shocked at the cost. Vintage retro illustration style, exaggerated expression."
    },
    {
        "id": 9,
        "text": "under the weather",
        "prompt": "A person sitting under a dark storm cloud that's following them around, looking tired and unwell. Vintage retro illustration style, muted colors."
    },
    {
        "id": 10,
        "text": "kick the bucket",
        "prompt": "A foot literally kicking over a wooden bucket. Vintage retro illustration style, simple composition, clear action."
    },
    {
        "id": 11,
        "text": "barking up the wrong tree",
        "prompt": "A dog barking enthusiastically at the base of a tree, while a cat sits smugly in a completely different tree nearby. Vintage retro illustration style, comic timing."
    },
    {
        "id": 12,
        "text": "kill two birds with one stone",
        "prompt": "A stone flying through the air toward two birds sitting on a branch. Vintage retro illustration style, motion lines, dramatic moment."
    },
    {
        "id": 13,
        "text": "the ball is in your court",
        "prompt": "A tennis ball sitting on one side of a tennis court, with a player on the other side waiting. Vintage retro illustration style, sports aesthetic."
    },
    {
        "id": 14,
        "text": "caught between a rock and a hard place",
        "prompt": "A person squeezed uncomfortably between a large boulder and a concrete wall. Vintage retro illustration style, claustrophobic composition."
    },
    {
        "id": 15,
        "text": "burning bridges",
        "prompt": "A wooden bridge on fire with flames rising, someone walking away in the foreground. Vintage retro illustration style, dramatic silhouette."
    },
    {
        "id": 16,
        "text": "break a leg",
        "prompt": "A theater stage with a spotlight and a person dramatically bending their leg in an exaggerated bow. Vintage retro illustration style, theatrical and dramatic."
    },
    {
        "id": 17,
        "text": "a blessing in disguise",
        "prompt": "An angel wearing a comical disguise with fake glasses and mustache. Vintage retro illustration style, whimsical and charming."
    },
    {
        "id": 18,
        "text": "the elephant in the room",
        "prompt": "A large elephant standing obviously in the middle of a living room while people sit around on furniture pretending not to notice. Vintage retro illustration style, absurd humor."
    },
    {
        "id": 19,
        "text": "once in a blue moon",
        "prompt": "A large blue-colored moon in the night sky with a calendar showing many crossed-off days. Vintage retro illustration style, dreamy atmosphere."
    },
    {
        "id": 20,
        "text": "teaching your grandmother to suck eggs",
        "prompt": "An elderly grandmother with a knowing, skeptical expression while a young person tries to show her how to handle an egg. Vintage retro illustration style, humorous generational contrast."
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
            filename = f"idiom_images/idiom_{idiom_data['id']:02d}_{idiom_data['text'].replace(' ', '_')}.png"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"  ✓ Saved: {filename}")
            return filename
        
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return None

def main():
    print("=" * 60)
    print("DALL-E Image Generation for Daily Idiom")
    print("=" * 60)
    print(f"Total images: 20")
    print(f"Estimated cost: ~$0.80 (20 images × $0.04)")
    print(f"Estimated time: ~25 minutes (with rate limiting)")
    print("=" * 60)
    print()
    
    generated = []
    failed = []
    
    for i, idiom in enumerate(idioms, 1):
        # Check if image already exists
        filename = f"idiom_images/idiom_{idiom['id']:02d}_{idiom['text'].replace(' ', '_')}.png"
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
    print(f"Images saved in ./idiom_images/ directory")
    print()
    print("IMPORTANT: Regenerate your OpenAI API key after this session!")
    print("Go to: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
