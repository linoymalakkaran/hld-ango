# PNG Export Instructions for JUL Diagrams

## Step-by-Step Guide to Export Diagrams to PNG

### Prerequisites
- Draw.io Desktop application installed (version 28.0.6 or later)
- All 18 `.drawio` files in the `drawio/` folder have been updated

### Method 1: Individual Export (Manual)

For each diagram file:

1. **Open the diagram**
   - Navigate to `drawio/` folder
   - Double-click on the `.drawio` file (e.g., `01_System_Context_Diagram.drawio`)
   - File opens in Draw.io application

2. **Export to PNG**
   - Click **File** → **Export as** → **PNG...**
   - Or press `Ctrl+Shift+E` (Windows) / `Cmd+Shift+E` (Mac)

3. **Configure Export Settings**
   ```
   ✓ Zoom: 100%
   ✓ Border Width: 10 pixels
   ✓ Transparent Background: NO (unchecked)
   ✓ Shadow: NO (unchecked)
   ✓ Grid: NO (unchecked)
   ✓ Selection Only: NO (unchecked)
   ✓ Crop: NO (unchecked)
   ✓ Size: Width=827, Height=1169 (should be automatic)
   ```

4. **Save the file**
   - Navigate to `png/` folder
   - Keep the same filename: `01_System_Context_Diagram.png`
   - Click **Save**

5. **Verify the export**
   - Open the PNG file
   - Verify image dimensions: 827 x 1169 pixels
   - Check that all text is readable
   - Confirm no elements are cut off

6. **Repeat for all 18 diagrams**

### Method 2: Batch Export (Faster)

Draw.io supports batch export through command line:

#### Windows PowerShell:
```powershell
cd "C:\Users\malakkaran.pappachan\OneDrive - Abu Dhabi Ports\Desktop\docs\Angla-doc\HLD"

# Path to Draw.io executable (adjust if different)
$drawio = "C:\Program Files\draw.io\draw.io.exe"

# Export all diagrams
Get-ChildItem "drawio\*.drawio" | ForEach-Object {
    $outputFile = "png\$($_.BaseName).png"
    & $drawio -x -f png -o $outputFile $_.FullName
    Write-Host "Exported: $outputFile"
}
```

#### Bash (Git Bash on Windows):
```bash
cd "/c/Users/malakkaran.pappachan/OneDrive - Abu Dhabi Ports/Desktop/docs/Angla-doc/HLD"

# Path to Draw.io (adjust if needed)
DRAWIO="/c/Program Files/draw.io/draw.io.exe"

# Export all diagrams
for file in drawio/*.drawio; do
    basename=$(basename "$file" .drawio)
    "$DRAWIO" -x -f png -o "png/${basename}.png" "$file"
    echo "Exported: png/${basename}.png"
done
```

### Export Settings Explained

| Setting | Value | Reason |
|---------|-------|--------|
| **Zoom** | 100% | Standard size for documents |
| **Border Width** | 10 pixels | Adds white space around diagram |
| **Transparent BG** | NO | Better for Word documents |
| **Size** | 827 x 1169 | A4 portrait dimensions |
| **DPI** | 96 (default) | Standard screen resolution |

### Quality Check

After exporting, verify each PNG:

```bash
# Check PNG dimensions (using ImageMagick if installed)
cd png
for file in *.png; do
    echo "$file:"
    identify "$file" | grep -o '[0-9]*x[0-9]*'
done
```

Expected output: `827x1169` for all files

### Troubleshooting

#### Problem: Text appears blurry
**Solution**: 
- Increase zoom to 150% or 200%
- Export at higher DPI (144 or 192)
- Adjust in export settings

#### Problem: Diagram is cut off
**Solution**:
- Ensure "Selection Only" is unchecked
- Verify page size in Draw.io is 827 x 1169
- Check "Fit to Page" option

#### Problem: File size too large
**Solution**:
- Reduce border width to 5 pixels
- Use PNG optimization tool: `pngcrush` or `optipng`
- Accept 1-2MB per file as reasonable

#### Problem: Colors look different
**Solution**:
- Ensure color profile is sRGB
- Check monitor calibration
- Preview on different device

### File Naming Convention

All PNG files should follow this pattern:

```
{number}_{description}.png

Examples:
01_System_Context_Diagram.png
02_High_Level_Architecture.png
03_Deployment_Architecture.png
...
18_WCO_Data_Model_ER.png
```

### Expected Results

After export, you should have:

```
png/
├── 01_System_Context_Diagram.png         (827x1169, ~800KB-1.5MB)
├── 02_High_Level_Architecture.png        (827x1169, ~1-2MB)
├── 03_Deployment_Architecture.png        (827x1169, ~800KB-1.5MB)
├── 04_Kubernetes_Architecture.png        (827x1169, ~1-2MB)
├── 05_Network_Architecture.png           (827x1169, ~800KB-1.5MB)
├── 06_Microservices_Architecture.png     (827x1169, ~1-2MB)
├── 07_Declaration_Lifecycle_State_Machine.png (827x1169, ~600KB-1MB)
├── 08_Integration_Architecture.png       (827x1169, ~800KB-1.5MB)
├── 09_Data_Flow_Declaration_Process.png  (827x1169, ~1-1.5MB)
├── 10_ASYCUDA_Integration_Flow.png       (827x1169, ~800KB-1.2MB)
├── 11_SINTECE_Integration_Flow.png       (827x1169, ~800KB-1.2MB)
├── 12_IAM_Keycloak_Architecture.png      (827x1169, ~800KB-1.5MB)
├── 13_Document_Management_MinIO.png      (827x1169, ~600KB-1MB)
├── 14_Master_Data_Sync.png               (827x1169, ~800KB-1.2MB)
├── 15_Security_Architecture.png          (827x1169, ~1-1.5MB)
├── 16_CICD_Pipeline.png                  (827x1169, ~800KB-1.5MB)
├── 17_Monitoring_Architecture.png        (827x1169, ~800KB-1.5MB)
└── 18_WCO_Data_Model_ER.png              (827x1169, ~1-2MB)
```

### Using in Microsoft Word

1. **Insert Image**
   - Place cursor where diagram should appear
   - **Insert** → **Pictures** → **This Device**
   - Select PNG file from `png/` folder
   - Click **Insert**

2. **Resize Image**
   - Right-click image → **Size and Position**
   - Set width to **6.5 inches** (A4 width minus margins)
   - Check **Lock aspect ratio**
   - Height will auto-adjust to ~9.2 inches

3. **Caption**
   - Right-click image → **Insert Caption**
   - Label: "Figure"
   - Example: "Figure 1: JUL System Context Diagram"

4. **Text Wrapping**
   - Right-click image → **Wrap Text** → **Top and Bottom**
   - Or **In Line with Text** for simplicity

### Advanced: Automated Export Script

Save this as `export_all_pngs.py`:

```python
#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

DRAWIO_PATH = r"C:\Program Files\draw.io\draw.io.exe"
SOURCE_DIR = Path("drawio")
OUTPUT_DIR = Path("png")

OUTPUT_DIR.mkdir(exist_ok=True)

for drawio_file in sorted(SOURCE_DIR.glob("*.drawio")):
    output_file = OUTPUT_DIR / f"{drawio_file.stem}.png"
    
    cmd = [
        DRAWIO_PATH,
        "-x",  # Export
        "-f", "png",  # Format
        "-o", str(output_file),  # Output
        str(drawio_file)  # Input
    ]
    
    print(f"Exporting: {drawio_file.name} → {output_file.name}")
    subprocess.run(cmd, check=True)
    
print(f"\n✓ Exported {len(list(SOURCE_DIR.glob('*.drawio')))} diagrams")
```

Run with:
```bash
python export_all_pngs.py
```

---

## Summary

✅ **18 diagrams** ready for export
✅ **A4 size** (827 x 1169 pixels)
✅ **High quality** PNG format
✅ **Ready for Word** documents

**Choose your method and start exporting! 🎨**
