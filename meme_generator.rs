# meme_generator.rs
/**
 * 🎭 Meme Generator – Top & Bottom Text (Rust Edition)
 * Features: custom image URL, top/bottom text, HTML output, config save/load
 * Dependencies: serde, serde_json, colored, chrono
 */

use chrono::Local;
use colored::*;
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, Write, BufRead};
use std::process::Command;

// ─── Types ──────────────────────────────────────────────────────────────────

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    top_text: String,
    bottom_text: String,
    image_url: String,
    font_size: u32,
    color: String,
}

// ─── Templates ─────────────────────────────────────────────────────────────

const TEMPLATES: &[(&str, &str, &str)] = &[
    ("1", "Drake", "https://i.imgflip.com/30b1gx.jpg"),
    ("2", "Distracted Boyfriend", "https://i.imgflip.com/1ur9b0.jpg"),
    ("3", "Two Buttons", "https://i.imgflip.com/1g8my4.jpg"),
    ("4", "Change My Mind", "https://i.imgflip.com/24y43o.jpg"),
    ("5", "Custom URL", ""),
];
const DEFAULT_IMAGE: &str = "https://i.imgflip.com/30b1gx.jpg";

// ─── HTML Generator ────────────────────────────────────────────────────────

fn generate_html(top_text: &str, bottom_text: &str, image_url: &str,
                 font_size: u32, color: &str, output: &str) {
    let top_esc = top_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    let bot_esc = bottom_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    let html = format!(r#"<!DOCTYPE html>
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
            color: {};
            font-size: {}px;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }}
        .meme-text.top {{ top: 10px; font-size: {}px; }}
        .meme-text.bottom {{ bottom: 10px; font-size: {}px; }}
        @media (max-width: 600px) {{
            .meme-text {{ font-size: {}px !important; padding: 5px 10px; }}
        }}
    </style>
</head>
<body>
    <div class="meme-container">
        <img class="meme-image" src="{}" alt="Meme image">
        <div class="meme-text top">{}</div>
        <div class="meme-text bottom">{}</div>
    </div>
</body>
</html>"#,
        color, font_size, font_size, font_size, font_size/2, image_url, top_esc, bot_esc);
    fs::write(output, html).unwrap();
    println!("{}", format!("✅ Meme saved to {}", output).green());
    println!("{}", "   Open this file in your browser to view the meme.".dimmed());
}

// ─── Main App ──────────────────────────────────────────────────────────────

struct MemeApp {
    top_text: String,
    bottom_text: String,
    image_url: String,
    font_size: u32,
    color: String,
}

impl MemeApp {
    fn new() -> Self {
        Self {
            top_text: String::new(),
            bottom_text: String::new(),
            image_url: DEFAULT_IMAGE.to_string(),
            font_size: 40,
            color: "#ffffff".to_string(),
        }
    }

    fn ask(&self, prompt: &str) -> String {
        print!("{}", prompt);
        io::stdout().flush().unwrap();
        let mut line = String::new();
        io::stdin().read_line(&mut line).unwrap();
        line.trim().to_string()
    }

    fn ask_u32(&self, prompt: &str, def: u32) -> u32 {
        loop {
            let ans = self.ask(prompt);
            if ans.is_empty() { return def; }
            if let Ok(val) = ans.parse::<u32>() {
                if val >= 10 && val <= 200 {
                    return val;
                }
            }
            println!("{}", "⚠️  Please enter a number between 10 and 200.".yellow());
        }
    }

    fn show_menu(&self) {
        println!("\n{}", "═".repeat(50).cyan());
        println!("{}", "🎭 MEME GENERATOR".bright().cyan());
        println!("{}", "═".repeat(50).cyan());
        println!("  Top: {}", if self.top_text.is_empty() { "(empty)" } else { &self.top_text });
        println!("  Bottom: {}", if self.bottom_text.is_empty() { "(empty)" } else { &self.bottom_text });
        let img = if self.image_url.len() > 40 { &self.image_url[0..40] } else { &self.image_url };
        println!("  Image: {}...", img);
        println!("{}", "═".repeat(50).cyan());
        println!("  1. 📝 Set Top Text");
        println!("  2. 📝 Set Bottom Text");
        println!("  3. 🖼️ Choose Image/Template");
        println!("  4. 🎨 Set Font Size");
        println!("  5. 🌈 Set Text Color");
        println!("  6. 💾 Generate Meme (HTML)");
        println!("  7. 🖼️ Export as PNG (optional)");
        println!("  8. 💾 Save/Load Config");
        println!("  0. 🚪 Exit");
        println!("{}", "═".repeat(50).cyan());
    }

    fn set_top_text(&mut self) {
        let text = self.ask(&format!("Top text (current: {}): ", self.top_text));
        if !text.is_empty() { self.top_text = text; }
    }

    fn set_bottom_text(&mut self) {
        let text = self.ask(&format!("Bottom text (current: {}): ", self.bottom_text));
        if !text.is_empty() { self.bottom_text = text; }
    }

    fn choose_image(&mut self) {
        println!("Choose template:");
        for (key, name, _) in TEMPLATES {
            println!("  {}. {}", key, name);
        }
        let choice = self.ask("Select template: ");
        if let Some((_, _, url)) = TEMPLATES.iter().find(|(k, _, _)| *k == choice) {
            let mut img = url.to_string();
            if img.is_empty() {
                img = self.ask("Enter custom image URL: ");
                if img.is_empty() { img = DEFAULT_IMAGE.to_string(); }
            }
            self.image_url = img;
            println!("{}", "✅ Image updated.".green());
        } else {
            println!("{}", "❌ Invalid choice.".red());
        }
    }

    fn set_font_size(&mut self) {
        self.font_size = self.ask_u32(&format!("Font size (current: {}): ", self.font_size), self.font_size);
        println!("{}", format!("✅ Font size set to {}", self.font_size).green());
    }

    fn set_color(&mut self) {
        let color = self.ask(&format!("Text color (hex, current: {}): ", self.color));
        if color.is_empty() { return; }
        if color.starts_with('#') && (color.len() == 4 || color.len() == 7) {
            self.color = color;
            println!("{}", format!("✅ Color set to {}", self.color).green());
        } else {
            println!("{}", "⚠️  Please use hex format, e.g. #ff0000".yellow());
        }
    }

    fn generate(&mut self) {
        if self.top_text.is_empty() && self.bottom_text.is_empty() {
            println!("{}", "⚠️  Please set at least top or bottom text.".yellow());
            let ans = self.ask("Continue anyway? (y/n): ");
            if ans.to_lowercase() != "y" { return; }
        }
        let ts = Local::now().format("%Y%m%d_%H%M%S");
        let filename = format!("meme_{}.html", ts);
        generate_html(&self.top_text, &self.bottom_text, &self.image_url,
                      self.font_size, &self.color, &filename);
        let open = self.ask("Open in browser? (y/n): ");
        if open.to_lowercase() == "y" {
            #[cfg(target_os = "macos")]
            let _ = Command::new("open").arg(&filename).status();
            #[cfg(target_os = "linux")]
            let _ = Command::new("xdg-open").arg(&filename).status();
            #[cfg(target_os = "windows")]
            let _ = Command::new("start").arg(&filename).status();
        }
    }

    fn export_png(&self) {
        println!("{}", "⚠️  PNG export requires additional libraries. Skipping.".yellow());
    }

    fn save_config(&self) {
        let fname = self.ask("Config filename (default meme_config.json): ");
        let file = if fname.is_empty() { "meme_config.json".to_string() } else { fname };
        let cfg = Config {
            top_text: self.top_text.clone(),
            bottom_text: self.bottom_text.clone(),
            image_url: self.image_url.clone(),
            font_size: self.font_size,
            color: self.color.clone(),
        };
        let json = serde_json::to_string_pretty(&cfg).unwrap();
        fs::write(&file, json).unwrap();
        println!("{}", format!("✅ Config saved to {}", file).green());
    }

    fn load_config(&mut self) {
        let fname = self.ask("Config filename (default meme_config.json): ");
        let file = if fname.is_empty() { "meme_config.json".to_string() } else { fname };
        let content = match fs::read_to_string(&file) {
            Ok(s) => s,
            Err(e) => { println!("{}", format!("❌ Error loading config: {}", e).red()); return; }
        };
        let cfg: Config = match serde_json::from_str(&content) {
            Ok(c) => c,
            Err(e) => { println!("{}", format!("❌ Invalid JSON: {}", e).red()); return; }
        };
        self.top_text = cfg.top_text;
        self.bottom_text = cfg.bottom_text;
        self.image_url = if cfg.image_url.is_empty() { DEFAULT_IMAGE.to_string() } else { cfg.image_url };
        self.font_size = if cfg.font_size == 0 { 40 } else { cfg.font_size };
        self.color = if cfg.color.is_empty() { "#ffffff".to_string() } else { cfg.color };
        println!("{}", format!("✅ Config loaded from {}", file).green());
    }

    fn run(&mut self) {
        println!("{}", "\n🎭 Meme Generator – Top & Bottom Text".bright().cyan());
        println!("{}", "Create your own memes in seconds!".dimmed());

        loop {
            self.show_menu();
            let choice = self.ask("Your choice: ");
            match choice.as_str() {
                "1" => self.set_top_text(),
                "2" => self.set_bottom_text(),
                "3" => self.choose_image(),
                "4" => self.set_font_size(),
                "5" => self.set_color(),
                "6" => self.generate(),
                "7" => self.export_png(),
                "8" => {
                    let sub = self.ask("Save (s) or Load (l)? ");
                    if sub == "s" { self.save_config(); }
                    else if sub == "l" { self.load_config(); }
                    else { println!("{}", "Invalid choice.".red()); }
                }
                "0" => {
                    println!("{}", "👋 Happy memeing!".cyan());
                    return;
                }
                _ => println!("{}", "❌ Invalid choice.".red()),
            }
            if choice != "0" {
                print!("\nPress Enter to continue...");
                io::stdout().flush().unwrap();
                let mut _dummy = String::new();
                io::stdin().read_line(&mut _dummy).unwrap();
            }
        }
    }
}

// ─── Main ────────────────────────────────────────────────────────────────────

fn main() {
    let mut app = MemeApp::new();
    app.run();
}
