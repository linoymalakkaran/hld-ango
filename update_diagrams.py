#!/usr/bin/env python3
"""
Script to update all Draw.io diagrams to proper A4 size (827 x 1169 pixels)
and increase font sizes for better readability
"""

import re
import os
from pathlib import Path

def update_diagram_sizing(file_path):
    """Update diagram to A4 size and increase font sizes"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update page size to A4 (827 x 1169)
    content = re.sub(
        r'pageWidth="[^"]*"\s*pageHeight="[^"]*"',
        'pageWidth="827" pageHeight="1169"',
        content
    )
    
    # Update dx and dy for proper viewport
    content = re.sub(
        r'<mxGraphModel\s+dx="[^"]*"\s+dy="[^"]*"',
        '<mxGraphModel dx="827" dy="1169"',
        content
    )
    
    # Increase font sizes (add 2-4 to existing sizes)
    def increase_font_size(match):
        size = int(match.group(1))
        new_size = size + 3 if size < 12 else size + 2
        return f'fontSize="{new_size}"'
    
    content = re.sub(r'fontSize="(\d+)"', increase_font_size, content)
    
    # Increase stroke widths for better visibility
    content = re.sub(r'strokeWidth="1"', 'strokeWidth="2"', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Update all drawio files in the directory"""
    
    drawio_dir = Path(r"C:\Users\malakkaran.pappachan\OneDrive - Abu Dhabi Ports\Desktop\docs\Angla-doc\HLD\drawio")
    
    if not drawio_dir.exists():
        print(f"Directory not found: {drawio_dir}")
        return
    
    files = list(drawio_dir.glob("*.drawio"))
    print(f"Found {len(files)} drawio files to update\n")
    
    for file_path in sorted(files):
        print(f"Updating: {file_path.name}...")
        try:
            update_diagram_sizing(file_path)
            print(f"  ✓ Successfully updated {file_path.name}")
        except Exception as e:
            print(f"  ✗ Error updating {file_path.name}: {e}")
    
    print(f"\n✓ Completed updating {len(files)} diagrams")
    print("\nAll diagrams now have:")
    print("  - A4 page size (827 x 1169 pixels)")
    print("  - Increased font sizes (+2 to +3)")
    print("  - Thicker stroke widths (minimum 2px)")

if __name__ == "__main__":
    main()
