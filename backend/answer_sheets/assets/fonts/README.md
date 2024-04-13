Terry, diving into TTF (TrueType Font) files programmatically can be quite a fascinating endeavor. These font files pack a lot of information, from character mappings to glyph definitions, and dissecting them requires a bit of work. Here's how you could go about extracting the information you mentioned:

### 1. Determining UTF-8 Character Support

To find out if a TTF font supports UTF-8 characters, you'd essentially be looking to see if it includes a wide range of Unicode character mappings. TTF fonts use 'cmap' tables to map character codes to glyph indices. UTF-8 itself is an encoding that can represent any Unicode character, so what you're really checking is whether the font supports the necessary range of Unicode characters.

Python's `fontTools` library can help you inspect the 'cmap' table:

```python
from fontTools.ttLib import TTFont

def supports_utf8(font_path):
    font = TTFont(font_path)
    unicode_cmap = None

    # Find the Unicode cmap (platformID=0 or 3, platEncID=1 or 10 for full Unicode)
    for cmap in font['cmap'].tables:
        if (cmap.platformID == 0 or cmap.platformID == 3) and (cmap.platEncID == 1 or cmap.platEncID == 10):
            unicode_cmap = cmap
            break

    if unicode_cmap:
        # Check for a range of characters, this is a simplistic check
        for codepoint in range(0x20, 0x7F):  # Basic Latin characters range
            if codepoint not in unicode_cmap.cmap:
                return False
        return True
    return False

# Use the function with the path to your TTF file
print(supports_utf8("path_to_your_font.ttf"))
```

### 2. Checking for All Characters and Numbers 0-9

To verify that a font includes all basic characters (A-Z, a-z) and numbers (0-9), you'd check the 'cmap' table again to see if those specific character codes are mapped.

```python
def has_basic_chars_and_numbers(font_path):
    font = TTFont(font_path)
    unicode_cmap = None

    for cmap in font['cmap'].tables:
        if (cmap.platformID == 0 or cmap.platformID == 3) and (cmap.platEncID == 1 or cmap.platEncID == 10):
            unicode_cmap = cmap
            break

    if unicode_cmap:
        # Check for A-Z, a-z, and 0-9
        for codepoint in range(0x30, 0x3A) + range(0x41, 0x5B) + range(0x61, 0x7B):
            if codepoint not in unicode_cmap.cmap:
                return False
        return True
    return False

print(has_basic_chars_and_numbers("path_to_your_font.ttf"))
```

### 3. Detecting Bold, Italics, and Bold Italics

TrueType fonts don't inherently contain "bold" or "italic" glyphs as separate characters. Instead, these styles are typically applied by the rendering software. However, a font family might include separate TTF files for bold, italic, and bold italic variants (e.g., `FontName-Bold.ttf`, `FontName-Italic.ttf`, and `FontName-BoldItalic.ttf`).

To programmatically check for these, you'd typically look at the font's metadata, such as the 'name' table, which contains human-readable information about the font:

```python
def check_font_style(font_path, style):
    font = TTFont(font_path)
    name_table = font['name']

    # Look for style in the font's name entries (NameID 2 is the subfamily name, e.g., Bold or Italic)
    for name in name_table.names:
        if name.nameID == 2 and style.lower() in name.toUnicode().lower():
            return True
    return False

# Example usage
print(check_font_style("path_to_your_font.ttf", "Bold"))
print(check_font_style("path_to_your_font.ttf", "Italic"))
print(check_font_style("path_to_your_font.ttf", "Bold Italic"))
```

Keep in mind that these methods are somewhat simplistic. Real-world fonts can be quite complex, with features like font variations, ligatures, and more, which might require a deeper dive. The `fontTools` library is powerful and can handle much of this complexity, so it's worth exploring further if you need more detailed information.