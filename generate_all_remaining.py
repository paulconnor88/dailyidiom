#!/usr/bin/env python3
"""
Generate Sora videos for ALL remaining idioms
16 idioms × $0.50 = ~$8.00
Time: ~1.5 hours
"""
import requests
import time
import sys

API_KEY = "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"

idioms = [
    {
        'id': 1,
        'name': 'break_the_ice',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "break the ice" (meaning: make people comfortable in social situations). Show a person using a hammer to break a large block of ice. SNES Super Nintendo retro game style, bright colors, satisfying breaking motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 3,
        'name': 'piece_of_cake',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "piece of cake" (meaning: very easy). Show a perfect slice of layered cake on a plate with a fork. SNES Super Nintendo retro game style, bright appealing colors, gentle floating or rotating motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 5,
        'name': 'hit_the_nail_on_the_head',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "hit the nail on the head" (meaning: exactly right). Show a hammer coming down to strike a nail perfectly with a spark effect. SNES Super Nintendo retro game style, bright colors, satisfying impact motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 6,
        'name': 'let_the_cat_out_of_the_bag',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "let the cat out of the bag" (meaning: reveal a secret). Show a surprised cat jumping out of an open shopping bag. SNES Super Nintendo retro game style, playful colors, whimsical jumping motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 8,
        'name': 'costs_an_arm_and_a_leg',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "costs an arm and a leg" (meaning: very expensive). Show a person at a shop counter looking shocked at an expensive price tag with dollar signs. SNES Super Nintendo retro game style, exaggerated expression, comic book aesthetic. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 9,
        'name': 'under_the_weather',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "under the weather" (meaning: feeling ill). Show a person sitting with a dark rain cloud hovering directly over them. SNES Super Nintendo retro game style, muted colors, gentle rain falling. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 11,
        'name': 'barking_up_the_wrong_tree',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "barking up the wrong tree" (meaning: pursuing wrong course). Show a dog barking at the base of an empty tree while a cat sits smugly in a different tree. SNES Super Nintendo retro game style, bright colors, comic timing. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 12,
        'name': 'kill_two_birds_with_one_stone',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "kill two birds with one stone" (meaning: achieve two goals at once). Show a stone flying through the air toward two birds sitting on a branch with motion lines. SNES Super Nintendo retro game style, bright colors, dramatic moment. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 13,
        'name': 'the_ball_is_in_your_court',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "the ball is in your court" (meaning: your turn to act). Show a tennis ball bouncing on one side of a tennis court with a player waiting on the other side. SNES Super Nintendo retro game style, bright sports colors, gentle bouncing motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 14,
        'name': 'caught_between_a_rock_and_a_hard_place',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "caught between a rock and a hard place" (meaning: faced with two difficult choices). Show a person squeezed uncomfortably between a large boulder and a concrete wall. SNES Super Nintendo retro game style, claustrophobic but playful, slight wiggling motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 15,
        'name': 'burning_bridges',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "burning bridges" (meaning: destroying relationships). Show a wooden bridge on fire with flames rising and someone walking away in the foreground. SNES Super Nintendo retro game style, dramatic silhouette, flickering fire. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 16,
        'name': 'break_a_leg',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "break a leg" (meaning: good luck, especially in theater). Show a theater stage with spotlight and a performer taking a dramatic bow. SNES Super Nintendo retro game style, theatrical colors, graceful bowing motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 17,
        'name': 'a_blessing_in_disguise',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "a blessing in disguise" (meaning: good thing that seemed bad at first). Show an angel character wearing a funny disguise with fake glasses and mustache. SNES Super Nintendo retro game style, whimsical colors, gentle floating motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 19,
        'name': 'once_in_a_blue_moon',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "once in a blue moon" (meaning: very rarely). Show a large blue-colored moon in the night sky with stars twinkling and a calendar flipping pages. SNES Super Nintendo retro game style, dreamy colors, gentle glowing motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    {
        'id': 20,
        'name': 'teaching_your_grandmother_to_suck_eggs',
        'prompt': 'Create a 16-bit pixel art animation that serves as a visual clue for the English idiom "teaching your grandmother to suck eggs" (meaning: giving unwanted advice to someone experienced). Show an elderly grandmother with a skeptical expression while a young person tries to show her something with an egg. SNES Super Nintendo retro game style, humorous colors, gentle gesturing motion. The animation should be an obvious visual representation of the phrase without showing any text.'
    },
    # Skip idiom 4 (bite the bullet) - content filter issues
]

def create_video(idiom):
    """Create Sora video"""
    print(f"Creating: {idiom['name'].replace('_', ' ').title()}")
    
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
    print(f"  ✓ Job: {job['id']}")
    return job['id']

def wait_for_completion(video_id):
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
            print()
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
        print(f'  ✓ Saved!')
        return filename
    else:
        print(f'  ✗ Download failed')
        return None

def main():
    print("=" * 60)
    print("FULL BATCH SORA GENERATION")
    print("=" * 60)
    print(f"Idioms: {len(idioms)}")
    print(f"Cost: ~${len(idioms) * 0.5:.2f}")
    print(f"Time: ~{len(idioms) * 5} minutes")
    print("=" * 60)
    print()
    
    successful = []
    failed = []
    
    for i, idiom in enumerate(idioms, 1):
        print(f"\n[{i}/{len(idioms)}] Idiom #{idiom['id']}: {idiom['name'].replace('_', ' ')}")
        print("-" * 60)
        
        video_id = create_video(idiom)
        if not video_id:
            failed.append(idiom['name'])
            continue
        
        if wait_for_completion(video_id):
            result = download_video(video_id, idiom)
            if result:
                successful.append(idiom['name'])
            else:
                failed.append(idiom['name'])
        else:
            failed.append(idiom['name'])
        
        if i < len(idioms):
            print(f"  Waiting 10 seconds...")
            time.sleep(10)
    
    print()
    print("=" * 60)
    print("BATCH COMPLETE!")
    print("=" * 60)
    print(f"✓ Successful: {len(successful)}/{len(idioms)}")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")
    print()
    print("Next steps:")
    print("1. QA each video")
    print("2. Update HTML")
    print("3. Push to GitHub")
    print("4. LAUNCH! 🚀")

if __name__ == "__main__":
    main()
