#!/bin/bash

# Watermark all idiom videos with dailyidiom.com
# Saves as _watermarked.mp4

echo "=========================================="
echo "WATERMARKING IDIOM VIDEOS"
echo "=========================================="

cd idiom_images_pixel

# Watermark settings
WATERMARK="dailyidiom.com"
FONTSIZE=32
FONTCOLOR="white@0.8"
POSITION="x=W-tw-20:y=H-th-20"  # Bottom right, 20px padding

# Counter
count=0
total=$(ls *.mp4 | wc -l | tr -d ' ')

for video in *.mp4; do
    # Skip if already watermarked
    if [[ $video == *"_watermarked.mp4" ]]; then
        continue
    fi
    
    count=$((count+1))
    output="${video%.mp4}_watermarked.mp4"
    
    echo ""
    echo "[$count/$total] Processing: $video"
    
    ffmpeg -i "$video" \
        -vf "drawtext=text='$WATERMARK':fontsize=$FONTSIZE:fontcolor=$FONTCOLOR:$POSITION" \
        -codec:a copy \
        "$output" \
        -y -loglevel error
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Created: $output"
    else
        echo "  ✗ Failed: $video"
    fi
done

echo ""
echo "=========================================="
echo "WATERMARKING COMPLETE!"
echo "=========================================="
echo "Created $count watermarked videos"
echo ""
echo "Next steps:"
echo "1. Review watermarked videos"
echo "2. If happy, replace originals:"
echo "   for f in *_watermarked.mp4; do mv \"\$f\" \"\${f/_watermarked/}\"; done"
