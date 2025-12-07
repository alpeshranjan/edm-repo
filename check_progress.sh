#!/bin/bash
cd "/Users/alpesh/Downloads/untitled folder 2"

echo "=== Process Status ==="
if pgrep -f "python -m src.cli" > /dev/null; then
    echo "✓ Process is running"
    ps aux | grep "[p]ython -m src.cli" | awk '{print "  PID:", $2, "CPU:", $3"%", "Memory:", $4"%"}'
else
    echo "✗ Process is not running"
fi

echo ""
echo "=== Output File Status ==="
if [ -f tracklist.md ]; then
    lines=$(wc -l < tracklist.md)
    size=$(ls -lh tracklist.md | awk '{print $5}')
    echo "✓ Output file exists"
    echo "  Size: $size"
    echo "  Lines: $lines"
    echo ""
    echo "=== Last 5 tracks found ==="
    tail -10 tracklist.md | grep -E "^[0-9]{2}:" || tail -5 tracklist.md
else
    echo "✗ Output file not created yet (still processing)"
fi

echo ""
echo "=== Temporary Files ==="
temp_count=$(find /tmp -name "segment_*.wav" 2>/dev/null | wc -l | tr -d ' ')
echo "Temporary segment files: $temp_count"

