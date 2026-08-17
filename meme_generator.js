# meme_generator.js
/**
 * 🎭 Meme Generator – Top & Bottom Text (Node.js Edition)
 * Features: custom image URL, top/bottom text, HTML output, optional PNG export
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { exec } = require('child_process');

// ─── Colors ──────────────────────────────────────────────────────────────────

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

const c = (str, color) => `${color}${str}${colors.reset}`;

// ─── Templates ─────────────────────────────────────────────────────────────

const TEMPLATES = {
  '1': { name: 'Drake', url: 'https://i.imgflip.com/30b1gx.jpg' },
  '2': { name: 'Distracted Boyfriend', url: 'https://i.imgflip.com/1ur9b0.jpg' },
  '3': { name: 'Two Buttons', url: 'https://i.imgflip.com/1g8my4.jpg' },
  '4': { name: 'Change My Mind', url: 'https://i.imgflip.com/24y43o.jpg' },
  '5': { name: 'Custom URL', url: null }
};
const DEFAULT_IMAGE = 'https://i.imgflip.com/30b1gx.jpg';

// ─── HTML Generator ────────────────────────────────────────────────────────

function generateHTML(topText, bottomText, imageUrl, fontSize = 40, color = '#ffffff', output = 'meme.html') {
  const topEsc = topText.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const botEsc = bottomText.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meme Generator</title>
    <style>
        body {
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #1a1a2e;
            font-family: 'Impact', 'Arial Black', sans-serif;
        }
        .meme-container {
            position: relative;
            display: inline-block;
            max-width: 90%;
            box-shadow: 0 0 30px rgba(0,0,0,0.7);
            border-radius: 8px;
            overflow: hidden;
        }
        .meme-image {
            display: block;
            width: 100%;
            height: auto;
        }
        .meme-text {
            position: absolute;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px 20px;
            color: ${color};
            font-size: ${fontSize}px;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }
        .meme-text.top { top: 10px; font-size: ${fontSize}px; }
        .meme-text.bottom { bottom: 10px; font-size: ${fontSize}px; }
        @media (max-width: 600px) {
            .meme-text { font-size: ${Math.max(18, Math.floor(fontSize/2))}px !important; padding: 5px 10px; }
        }
    </style>
</head>
<body>
    <div class="meme-container">
        <img class="meme-image" src="${imageUrl}" alt="Meme image">
        <div class="meme-text top">${topEsc}</div>
        <div class="meme-text bottom">${botEsc}</div>
    </div>
</body>
</html>`;
  fs.writeFileSync(output, html);
  console.log(c(`✅ Meme saved to ${output}`, colors.green));
  console.log(c('   Open this file in your browser to view the meme.', colors.dim));
  return output;
}

// ─── PNG Export ───────────────────────────────────────────────────────────

function exportPNG(htmlFile, pngFile = null) {
  if (!pngFile) pngFile = htmlFile.replace('.html', '.png');
  // Try using wkhtmltoimage if available (optional)
  console.log(c('⚠️  PNG export requires wkhtmltoimage or a library like "canvas".', colors.yellow));
  console.log(c('   Falling back to HTML only.', colors.dim));
  return false;
}

// ─── Main App ──────────────────────────────────────────────────────────────

class MemeApp {
  constructor() {
    this.rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    this.topText = '';
    this.bottomText = '';
    this.imageUrl = DEFAULT_IMAGE;
    this.fontSize = 40;
    this.color = '#ffffff';
  }

  _ask(prompt) {
    return new Promise(resolve => this.rl.question(prompt, resolve));
  }

  async _showMenu() {
    console.log('\n' + c('═'.repeat(50), colors.cyan));
    console.log(c('🎭 MEME GENERATOR', colors.bright + colors.cyan));
    console.log(c('═'.repeat(50), colors.cyan));
    console.log(`  Top: ${this.topText || '(empty)'}`);
    console.log(`  Bottom: ${this.bottomText || '(empty)'}`);
    console.log(`  Image: ${this.imageUrl.slice(0,40)}...`);
    console.log(c('═'.repeat(50), colors.cyan));
    console.log('  1. 📝 Set Top Text');
    console.log('  2. 📝 Set Bottom Text');
    console.log('  3. 🖼️ Choose Image/Template');
    console.log('  4. 🎨 Set Font Size');
    console.log('  5. 🌈 Set Text Color');
    console.log('  6. 💾 Generate Meme (HTML)');
    console.log('  7. 🖼️ Export as PNG (optional)');
    console.log('  8. 💾 Save/Load Config');
    console.log('  0. 🚪 Exit');
    console.log(c('═'.repeat(50), colors.cyan));
  }

  async setTopText() {
    const text = await this._ask(`Top text (current: ${this.topText}): `);
    if (text.trim()) this.topText = text.trim();
  }

  async setBottomText() {
    const text = await this._ask(`Bottom text (current: ${this.bottomText}): `);
    if (text.trim()) this.bottomText = text.trim();
  }

  async chooseImage() {
    console.log('Choose template:');
    for (const [key, tpl] of Object.entries(TEMPLATES)) {
      console.log(`  ${key}. ${tpl.name}`);
    }
    const choice = await this._ask('Select template: ');
    if (TEMPLATES[choice]) {
      let url = TEMPLATES[choice].url;
      if (url === null) {
        url = await this._ask('Enter custom image URL: ');
      }
      this.imageUrl = url || DEFAULT_IMAGE;
      console.log(c('✅ Image updated.', colors.green));
    } else {
      console.log(c('❌ Invalid choice.', colors.red));
    }
  }

  async setFontSize() {
    const size = await this._ask(`Font size (current: ${this.fontSize}): `);
    const s = parseInt(size);
    if (!isNaN(s) && s >= 10 && s <= 200) {
      this.fontSize = s;
      console.log(c(`✅ Font size set to ${s}`, colors.green));
    } else {
      console.log(c('⚠️  Size must be between 10 and 200.', colors.yellow));
    }
  }

  async setColor() {
    const color = await this._ask(`Text color (hex, current: ${this.color}): `);
    if (color.match(/^#[0-9a-fA-F]{6}$/) || color.match(/^#[0-9a-fA-F]{3}$/)) {
      this.color = color;
      console.log(c(`✅ Color set to ${color}`, colors.green));
    } else {
      console.log(c('⚠️  Please use hex format, e.g. #ff0000', colors.yellow));
    }
  }

  async generate() {
    if (!this.topText && !this.bottomText) {
      console.log(c('⚠️  Please set at least top or bottom text.', colors.yellow));
      const ans = await this._ask('Continue anyway? (y/n): ');
      if (ans.toLowerCase() !== 'y') return;
    }
    const ts = new Date().toISOString().replace(/[:.]/g, '').slice(0,14);
    const filename = `meme_${ts}.html`;
    const filepath = generateHTML(this.topText, this.bottomText, this.imageUrl, this.fontSize, this.color, filename);
    const open = await this._ask('Open in browser? (y/n): ');
    if (open.toLowerCase() === 'y') {
      const { exec } = require('child_process');
      exec(`open ${filepath}`); // works on macOS; for others use 'start' or 'xdg-open'
    }
  }

  async exportPNG() {
    // find latest html
    const files = fs.readdirSync('.').filter(f => f.startsWith('meme_') && f.endsWith('.html'));
    if (files.length === 0) {
      console.log(c('❌ No HTML meme found. Generate one first.', colors.red));
      return;
    }
    files.sort((a,b) => fs.statSync(b).mtime - fs.statSync(a).mtime);
    const htmlFile = files[0];
    const pngFile = htmlFile.replace('.html', '.png');
    const result = exportPNG(htmlFile, pngFile);
    if (result) console.log(c(`✅ PNG exported to ${pngFile}`, colors.green));
  }

  async saveConfig() {
    const fname = await this._ask('Config filename (default meme_config.json): ');
    const file = fname.trim() || 'meme_config.json';
    const config = {
      topText: this.topText,
      bottomText: this.bottomText,
      imageUrl: this.imageUrl,
      fontSize: this.fontSize,
      color: this.color
    };
    fs.writeFileSync(file, JSON.stringify(config, null, 2));
    console.log(c(`✅ Config saved to ${file}`, colors.green));
  }

  async loadConfig() {
    const fname = await this._ask('Config filename (default meme_config.json): ');
    const file = fname.trim() || 'meme_config.json';
    try {
      const content = fs.readFileSync(file, 'utf8');
      const config = JSON.parse(content);
      this.topText = config.topText || '';
      this.bottomText = config.bottomText || '';
      this.imageUrl = config.imageUrl || DEFAULT_IMAGE;
      this.fontSize = config.fontSize || 40;
      this.color = config.color || '#ffffff';
      console.log(c(`✅ Config loaded from ${file}`, colors.green));
    } catch (err) {
      console.log(c(`❌ Error loading config: ${err.message}`, colors.red));
    }
  }

  async run() {
    console.clear();
    console.log(c('\n🎭 Meme Generator – Top & Bottom Text', colors.bright + colors.cyan));
    console.log(c('Create your own memes in seconds!', colors.dim));

    while (true) {
      await this._showMenu();
      const choice = await this._ask('Your choice: ');
      switch (choice.trim()) {
        case '1': await this.setTopText(); break;
        case '2': await this.setBottomText(); break;
        case '3': await this.chooseImage(); break;
        case '4': await this.setFontSize(); break;
        case '5': await this.setColor(); break;
        case '6': await this.generate(); break;
        case '7': await this.exportPNG(); break;
        case '8': {
          const sub = await this._ask('Save (s) or Load (l)? ');
          if (sub.toLowerCase() === 's') await this.saveConfig();
          else if (sub.toLowerCase() === 'l') await this.loadConfig();
          else console.log(c('Invalid choice.', colors.red));
          break;
        }
        case '0':
          console.log(c('👋 Happy memeing!', colors.cyan));
          this.rl.close();
          return;
        default:
          console.log(c('❌ Invalid choice.', colors.red));
      }
      if (choice !== '0') {
        console.log('\nPress Enter to continue...');
        await this._ask('');
      }
    }
  }
}

// ─── Main ────────────────────────────────────────────────────────────────────

const main = async () => {
  try {
    const app = new MemeApp();
    await app.run();
  } catch (e) {
    console.error(c(`❌ Unexpected error: ${e.message}`, colors.red));
    process.exit(1);
  }
};

main();
