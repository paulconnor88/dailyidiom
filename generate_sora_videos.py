#!/usr/bin/env python3
"""
Sora Video Generator for Daily Idiom
Reads prompts from a .txt file and generates videos via OpenAI Sora API

Usage:
    export OPENAI_API_KEY="your-key-here"
    python3 generate_sora_videos.py idiom_prompts.txt
"""

import os
import sys
import time
import re
import requests

API_KEY = os.environ.get('OPENAI_API_KEY')
OUTPUT_DIR = 'idiom_images_pixel/To Review'
WAIT_BETWEEN_JOBS = 70  # seconds between starting new jobs

def parse_prompts_file(filepath):
    """Parse the txt file and extract idiom prompts"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by section dividers
    sections = re.split(r'={50,}', content)
    
    idioms = []
    for section in sections:
        # Look for NEW SORA PROMPT: or SORA PROMPT:
        prompt_match = re.search(r'(?:NEW SORA PROMPT|SORA PROMPT):\s*\n(.+?)(?=\n={50,}|\Z)', section, re.DOTALL)
        
        if prompt_match:
            prompt = prompt_match.group(1).strip()
            
            # Extract idiom name (look for numbered title like "1. SPILL THE BEANS")
            name_match = re.search(r'\d+\.\s+([A-Z][A-Z\s\']+)\n', section)
            if name_match:
                name = name_match.group(1).strip()
                
                # Convert to filename format
                safe_name = name.lower().replace("'", "").replace(" ", "_")
                safe_name = re.sub(r'[^a-z0-9_]', '', safe_name)
                
                idioms.append({
                    'name': name,
                    'filename': safe_name,
                    'prompt': prompt
                })
    
    return idioms


def create_video(idiom):
    """Create Sora video job"""
    print(f"\n{'='*60}")
    print(f"Creating: {idiom['name']}")
    print(f"{'='*60}")
    
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
    print(f"  ✓ Job started: {job['id']}")
    return job['id']


def wait_for_completion(video_id):
    """Poll until video is complete"""
    bar_length = 30
    
    while True:
        response = requests.get(
            f'https://api.openai.com/v1/videos/{video_id}',
            headers={'Authorization': f'Bearer {API_KEY}'}
        )
        
        job = response.json()
        status = job.get('status', 'unknown')
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
        filename = f"{OUTPUT_DIR}/{idiom['filename']}.mp4"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"  ✓ Saved: {filename}")
        return True
    else:
        print(f"  ✗ Download failed: {response.status_code}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_sora_videos.py <prompts_file.txt>")
        print("Example: python3 generate_sora_videos.py idiom_prompts.txt")
        sys.exit(1)
    
    if not API_KEY:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Run: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    prompts_file = sys.argv[1]
    
    if not os.path.exists(prompts_file):
        print(f"ERROR: File not found: {prompts_file}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Parse prompts
    idioms = parse_prompts_file(prompts_file)
    
    if not idioms:
        print("ERROR: No prompts found in file")
        print("Make sure your file has sections with 'NEW SORA PROMPT:' or 'SORA PROMPT:'")
        sys.exit(1)
    
    print(f"\nFound {len(idioms)} idioms to generate:")
    for i, idiom in enumerate(idioms, 1):
        print(f"  {i}. {idiom['name']}")
    
    print(f"\nEstimated cost: ${len(idioms) * 0.50:.2f}")
    print(f"Estimated time: ~{len(idioms) * 2} minutes\n")
    
    input("Press Enter to start generation (Ctrl+C to cancel)...")
    
    # Process each idiom
    successful = 0
    failed = 0
    
    for i, idiom in enumerate(idioms):
        video_id = create_video(idiom)
        
        if video_id:
            if wait_for_completion(video_id):
                if download_video(video_id, idiom):
                    successful += 1
                else:
                    failed += 1
            else:
                failed += 1
        else:
            failed += 1
        
        # Wait between jobs (except for last one)
        if i < len(idioms) - 1:
            print(f"\n  Waiting {WAIT_BETWEEN_JOBS}s before next job...")
            time.sleep(WAIT_BETWEEN_JOBS)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"{'='*60}")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    print(f"  Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
