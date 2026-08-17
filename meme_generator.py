# meme_generator.py
#!/usr/bin/env python3
"""
🎭 Meme Generator – Top & Bottom Text (Python Edition)
Features: custom image URL, top/bottom text, HTML output, optional PNG export
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Install 'rich' for enhanced UI: pip install rich")


# ─── Colors ──────────────────────────────────────────────────────────────────

def c(text: str, color: str) -> str:
    colors = {
        "reset": "\033[0m", "bright": "\033[1m", "dim": "\033[2m",
        "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


# ─── Default Templates ────────────────────────────────────────────────────

TEMPLATES = {
    "1": {"name": "Drake", "url": "https://i.imgflip.com/30b1gx.jpg"},
    "2": {"name": "Distracted Boyfriend", "url": "https://i.imgflip.com/1ur9b0.jpg"},
    "3": {"name": "Two Buttons", "url": "https://i.imgflip.com/1g8my4.jpg"},
    "4": {"name": "Change My Mind", "url": "https://i.imgflip.com/24y43o.jpg"},
    "5": {"name": "Custom URL", "url": None}
}

DEFAULT_IMAGE = "https://i.imgflip.com/30b1gx.jpg"  # Drake template


# ─── HTML Generator ────────────────────────────────────────────────────────

def generate_html(top_text: str, bottom_text: str, image_url: str, 
                  font_size: int = 40, color: str = "#ffffff",
                  output: str = "meme.html") -> None:
    """Generate an HTML page with the meme."""
    # Escape text for HTML
    top_esc = top_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    bot_esc = bottom_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meme Generator</title>
    <style>
        body {{
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #1a1a2e;
            font-family: 'Impact', 'Arial Black', sans-serif;
        }}
        .meme-container {{
            position: relative;
            display: inline-block;
            max-width: 90%;
            box-shadow: 0 0 30px rgba(0,0,0,0.7);
            border-radius: 8px;
            overflow: hidden;
        }}
        .meme-image {{
            display: block;
            width: 100%;
            height: auto;
        }}
        .meme-text {{
            position: absolute;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px 20px;
            color: {color};
            font-size: {font_size}px;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }}
        .meme-text.top {{
            top: 10px;
            font-size: {font_size}px;
        }}
        .meme-text.bottom {{
            bottom: 10px;
            font-size: {font_size}px;
        }}
        @media (max-width: 600px) {{
            .meme-text {{
                font-size: {max(18, font_size//2)}px !important;
                padding: 5px 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="meme-container">
        <img class="meme-image" src="{image_url}" alt="Meme image">
        <div class="meme-text top">{top_esc}</div>
        <div class="meme-text bottom">{bot_esc}</div>
    </div>
</body>
</html>"""
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(c(f"✅ Meme saved to {output}", "green"))
    print(c("   Open this file in your browser to view the meme.", "dim"))


# ─── PNG Export (optional) ─────────────────────────────────────────────────

def export_png(html_file: str, png_file: str = None) -> bool:
    """Convert HTML to PNG using wkhtmltoimage or PIL (if available)."""
    if not PIL_AVAILABLE:
        print(c("⚠️  PIL not installed. Install 'Pillow' for PNG export.", "yellow"))
        return False
    
    if not png_file:
        png_file = html_file.replace('.html', '.png')
    
    # For simplicity, we create a simple image with text using PIL
    # But we need to download the image, so we'll use requests
    try:
        import requests
        from io import BytesIO
        
        # Parse HTML to extract image URL and text (simplified)
        with open(html_file, 'r') as f:
            content = f.read()
        import re
        img_match = re.search(r'src="([^"]+)"', content)
        top_match = re.search(r'<div class="meme-text top">(.*?)</div>', content, re.DOTALL)
        bottom_match = re.search(r'<div class="meme-text bottom">(.*?)</div>', content, re.DOTALL)
        if not img_match:
            print(c("❌ Could not extract image URL from HTML.", "red"))
            return False
        img_url = img_match.group(1)
        top_text = top_match.group(1) if top_match else ""
        bottom_text = bottom_match.group(1) if bottom_match else ""
        
        # Download image
        resp = requests.get(img_url, timeout=10)
        img = Image.open(BytesIO(resp.content))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("impact.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Place text
        # Center text on image
        width, height = img.size
        # Top text
        if top_text:
            bbox = draw.textbbox((0,0), top_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((width-tw)//2, 10), top_text, fill="white", font=font, stroke_width=2, stroke_fill="black")
        if bottom_text:
            bbox = draw.textbbox((0,0), bottom_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((width-tw)//2, height-th-10), bottom_text, fill="white", font=font, stroke_width=2, stroke_fill="black")
        
        img.save(png_file)
        print(c(f"✅ PNG exported to {png_file}", "green"))
        return True
    except Exception as e:
        print(c(f"❌ PNG export failed: {e}", "red"))
        return False


# ─── Main App ──────────────────────────────────────────────────────────────

class MemeApp:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.top_text = ""
        self.bottom_text = ""
        self.image_url = DEFAULT_IMAGE
        self.font_size = 40
        self.color = "#ffffff"

    def show_menu(self):
        if self.console:
            panel = Panel(
                f"[bold cyan]🎭 Meme Generator[/bold cyan]\n"
                f"  Top: {self.top_text or '(empty)'}\n"
                f"  Bottom: {self.bottom_text or '(empty)'}\n"
                f"  Image: {self.image_url[:40]}...",
                title="📋 Main Menu",
                border_style="blue"
            )
            self.console.print(panel)
            self.console.print(" [1] 📝 Set Top Text")
            self.console.print(" [2] 📝 Set Bottom Text")
            self.console.print(" [3] 🖼️ Choose Image/Template")
            self.console.print(" [4] 🎨 Set Font Size")
            self.console.print(" [5] 🌈 Set Text Color")
            self.console.print(" [6] 💾 Generate Meme (HTML)")
            self.console.print(" [7] 🖼️ Export as PNG (optional)")
            self.console.print(" [8] 💾 Save/Load Config")
            self.console.print(" [0] 🚪 Exit")
        else:
            print("\n" + "="*50)
            print(c("🎭 MEME GENERATOR", "bright"))
            print("="*50)
            print(f"  Top: {self.top_text or '(empty)'}")
            print(f"  Bottom: {self.bottom_text or '(empty)'}")
            print(f"  Image: {self.image_url[:40]}...")
            print("="*50)
            print("  1. 📝 Set Top Text")
            print("  2. 📝 Set Bottom Text")
            print("  3. 🖼️ Choose Image/Template")
            print("  4. 🎨 Set Font Size")
            print("  5. 🌈 Set Text Color")
            print("  6. 💾 Generate Meme (HTML)")
            print("  7. 🖼️ Export as PNG (optional)")
            print("  8. 💾 Save/Load Config")
            print("  0. 🚪 Exit")
            print("="*50)

    def set_top_text(self):
        if self.console:
            text = Prompt.ask("Enter top text", default=self.top_text)
        else:
            text = input(f"Top text (current: {self.top_text}): ").strip()
        self.top_text = text if text else self.top_text

    def set_bottom_text(self):
        if self.console:
            text = Prompt.ask("Enter bottom text", default=self.bottom_text)
        else:
            text = input(f"Bottom text (current: {self.bottom_text}): ").strip()
        self.bottom_text = text if text else self.bottom_text

    def choose_image(self):
        if self.console:
            self.console.print("[bold]Choose template:[/bold]")
            for key, tpl in TEMPLATES.items():
                self.console.print(f"  [{key}] {tpl['name']}")
            choice = Prompt.ask("Select template", choices=list(TEMPLATES.keys()))
        else:
            print("Choose template:")
            for key, tpl in TEMPLATES.items():
                print(f"  {key}. {tpl['name']}")
            choice = input("Select template: ").strip()
        
        if choice in TEMPLATES:
            url = TEMPLATES[choice]["url"]
            if url is None:
                if self.console:
                    url = Prompt.ask("Enter custom image URL")
                else:
                    url = input("Enter custom image URL: ").strip()
            self.image_url = url if url else DEFAULT_IMAGE
            print(c("✅ Image updated.", "green"))

    def set_font_size(self):
        if self.console:
            size = Prompt.ask("Font size (px)", default=str(self.font_size))
        else:
            size = input(f"Font size (current: {self.font_size}): ").strip()
        try:
            s = int(size)
            if 10 <= s <= 200:
                self.font_size = s
                print(c(f"✅ Font size set to {s}", "green"))
            else:
                print(c("⚠️  Size must be between 10 and 200.", "yellow"))
        except ValueError:
            print(c("⚠️  Please enter a number.", "yellow"))

    def set_color(self):
        if self.console:
            color = Prompt.ask("Text color (hex, e.g. #ffffff)", default=self.color)
        else:
            color = input(f"Text color (hex, current: {self.color}): ").strip()
        if color.startswith('#') and len(color) in (4,7):
            self.color = color
            print(c(f"✅ Color set to {color}", "green"))
        else:
            print(c("⚠️  Please use hex format, e.g. #ff0000", "yellow"))

    def generate(self):
        if not self.top_text and not self.bottom_text:
            print(c("⚠️  Please set at least top or bottom text.", "yellow"))
            if self.console and not Confirm.ask("Continue anyway?"):
                return
        # Auto‑generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meme_{timestamp}.html"
        generate_html(self.top_text, self.bottom_text, self.image_url,
                      self.font_size, self.color, filename)
        # Optionally open in browser
        import webbrowser
        if self.console and Confirm.ask("Open in browser?"):
            webbrowser.open(filename)

    def export_png(self):
        # find latest html file
        html_files = sorted(Path.cwd().glob("meme_*.html"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not html_files:
            print(c("❌ No HTML meme found. Generate one first.", "red"))
            return
        html_file = html_files[0]
        png_file = html_file.with_suffix(".png")
        export_png(str(html_file), str(png_file))

    def save_config(self):
        if self.console:
            fname = Prompt.ask("Config filename", default="meme_config.json")
        else:
            fname = input("Config filename (default meme_config.json): ").strip() or "meme_config.json"
        config = {
            "top_text": self.top_text,
            "bottom_text": self.bottom_text,
            "image_url": self.image_url,
            "font_size": self.font_size,
            "color": self.color
        }
        with open(fname, 'w') as f:
            json.dump(config, f, indent=2)
        print(c(f"✅ Config saved to {fname}", "green"))

    def load_config(self):
        if self.console:
            fname = Prompt.ask("Config filename", default="meme_config.json")
        else:
            fname = input("Config filename (default meme_config.json): ").strip() or "meme_config.json"
        try:
            with open(fname, 'r') as f:
                config = json.load(f)
            self.top_text = config.get("top_text", "")
            self.bottom_text = config.get("bottom_text", "")
            self.image_url = config.get("image_url", DEFAULT_IMAGE)
            self.font_size = config.get("font_size", 40)
            self.color = config.get("color", "#ffffff")
            print(c(f"✅ Config loaded from {fname}", "green"))
        except FileNotFoundError:
            print(c(f"❌ File not found: {fname}", "red"))
        except json.JSONDecodeError:
            print(c("❌ Invalid JSON.", "red"))

    def run(self):
        if self.console:
            self.console.print(Panel.fit("[bold cyan]🎭 Meme Generator – Top & Bottom Text[/bold cyan]", border_style="cyan"))
        else:
            print(c("\n🎭 Meme Generator – Top & Bottom Text", "bright"))
            print(c("Create your own memes in seconds!", "dim"))

        while True:
            self.show_menu()
            if self.console:
                choice = Prompt.ask("Your choice", choices=["0","1","2","3","4","5","6","7","8"])
            else:
                choice = input("Your choice: ").strip()

            if choice == "1":
                self.set_top_text()
            elif choice == "2":
                self.set_bottom_text()
            elif choice == "3":
                self.choose_image()
            elif choice == "4":
                self.set_font_size()
            elif choice == "5":
                self.set_color()
            elif choice == "6":
                self.generate()
            elif choice == "7":
                self.export_png()
            elif choice == "8":
                if self.console:
                    subchoice = Prompt.ask("Save (s) or Load (l)?", choices=["s","l"])
                else:
                    subchoice = input("Save (s) or Load (l)? ").strip().lower()
                if subchoice == "s":
                    self.save_config()
                elif subchoice == "l":
                    self.load_config()
                else:
                    print(c("Invalid choice.", "red"))
            elif choice == "0":
                print(c("👋 Happy memeing!", "cyan"))
                break
            else:
                print(c("❌ Invalid choice.", "red"))

            if choice != "0":
                if self.console:
                    self.console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                else:
                    input("\nPress Enter to continue...")


def main():
    try:
        app = MemeApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(c(f"❌ Unexpected error: {e}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
