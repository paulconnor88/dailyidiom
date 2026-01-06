#!/usr/bin/env python3
"""
Stitch animation frames into a looping GIF
"""
from PIL import Image
import os

def create_gif():
    """Create animated GIF from frames"""
    print("Creating animated GIF...")
    
    # Load all frames
    frames = []
    for i in range(1, 5):
        filename = f"animation_frames/raining_cats_dogs_frame_{i}.png"
        if os.path.exists(filename):
            img = Image.open(filename)
            frames.append(img)
            print(f"  ✓ Loaded frame {i}")
        else:
            print(f"  ✗ Missing frame {i}: {filename}")
            return None
    
    if len(frames) != 4:
        print(f"Error: Expected 4 frames, got {len(frames)}")
        return None
    
    # Create GIF
    output_path = "idiom_images_pixel/idiom_07_raining_cats_and_dogs.gif"
    
    # Save as animated GIF
    # duration = milliseconds per frame (500ms = 0.5 seconds per frame = 2 second loop)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,  # 500ms per frame
        loop=0  # Loop forever
    )
    
    print()
    print(f"✓ Created animated GIF: {output_path}")
    print(f"  - 4 frames")
    print(f"  - 0.5 seconds per frame")
    print(f"  - 2 second loop")
    
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("Creating Animated GIF")
    print("=" * 60)
    print()
    
    result = create_gif()
    
    if result:
        print()
        print("=" * 60)
        print("SUCCESS! Now update HTML to use .gif instead of .png")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Open the GIF to preview it")
        print("2. Update index.html: change .png to .gif for idiom 7")
        print("3. Push to GitHub")
