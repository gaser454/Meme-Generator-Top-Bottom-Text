# meme_generator.go
/**
 * 🎭 Meme Generator – Top & Bottom Text (Go Edition)
 * Features: custom image URL, top/bottom text, HTML output, config save/load
 */

package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

// ─── Colors ──────────────────────────────────────────────────────────────────

const (
	reset  = "\x1b[0m"
	bright = "\x1b[1m"
	dim    = "\x1b[2m"
	red    = "\x1b[31m"
	green  = "\x1b[32m"
	yellow = "\x1b[33m"
	blue   = "\x1b[34m"
	magenta = "\x1b[35m"
	cyan   = "\x1b[36m"
)

func c(str, color string) string {
	return color + str + reset
}

// ─── Templates ─────────────────────────────────────────────────────────────

var TEMPLATES = map[string]struct{ Name, URL string }{
	"1": {"Drake", "https://i.imgflip.com/30b1gx.jpg"},
	"2": {"Distracted Boyfriend", "https://i.imgflip.com/1ur9b0.jpg"},
	"3": {"Two Buttons", "https://i.imgflip.com/1g8my4.jpg"},
	"4": {"Change My Mind", "https://i.imgflip.com/24y43o.jpg"},
	"5": {"Custom URL", ""},
}
const DEFAULT_IMAGE = "https://i.imgflip.com/30b1gx.jpg"

// ─── Config ──────────────────────────────────────────────────────────────────

type Config struct {
	TopText    string `json:"topText"`
	BottomText string `json:"bottomText"`
	ImageURL   string `json:"imageUrl"`
	FontSize   int    `json:"fontSize"`
	Color      string `json:"color"`
}

// ─── HTML Generator ──────────────────────────────────────────────────────

func generateHTML(topText, bottomText, imageURL string, fontSize int, color, output string) {
	if output == "" {
		output = fmt.Sprintf("meme_%s.html", time.Now().Format("20060102_150405"))
	}
	topEsc := strings.ReplaceAll(topText, "&", "&amp;")
	topEsc = strings.ReplaceAll(topEsc, "<", "&lt;")
	topEsc = strings.ReplaceAll(topEsc, ">", "&gt;")
	botEsc := strings.ReplaceAll(bottomText, "&", "&amp;")
	botEsc = strings.ReplaceAll(botEsc, "<", "&lt;")
	botEsc = strings.ReplaceAll(botEsc, ">", "&gt;")

	html := fmt.Sprintf(`<!DOCTYPE html>
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
            max-width: 90%%;
            box-shadow: 0 0 30px rgba(0,0,0,0.7);
            border-radius: 8px;
            overflow: hidden;
        }
        .meme-image {
            display: block;
            width: 100%%;
            height: auto;
        }
        .meme-text {
            position: absolute;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px 20px;
            color: %s;
            font-size: %dpx;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }
        .meme-text.top { top: 10px; font-size: %dpx; }
        .meme-text.bottom { bottom: 10px; font-size: %dpx; }
        @media (max-width: 600px) {
            .meme-text { font-size: %dpx !important; padding: 5px 10px; }
        }
    </style>
</head>
<body>
    <div class="meme-container">
        <img class="meme-image" src="%s" alt="Meme image">
        <div class="meme-text top">%s</div>
        <div class="meme-text bottom">%s</div>
    </div>
</body>
</html>`,
		color, fontSize, fontSize, fontSize, fontSize/2, imageURL, topEsc, botEsc)

	ioutil.WriteFile(output, []byte(html), 0644)
	fmt.Printf("%s\n", c(fmt.Sprintf("✅ Meme saved to %s", output), green))
	fmt.Printf("%s\n", c("   Open this file in your browser to view the meme.", dim))
}

// ─── Main App ──────────────────────────────────────────────────────────────

type MemeApp struct {
	reader     *bufio.Reader
	topText    string
	bottomText string
	imageURL   string
	fontSize   int
	color      string
}

func NewMemeApp() *MemeApp {
	return &MemeApp{
		reader:     bufio.NewReader(os.Stdin),
		imageURL:   DEFAULT_IMAGE,
		fontSize:   40,
		color:      "#ffffff",
	}
}

func (app *MemeApp) ask(prompt string) string {
	fmt.Print(prompt)
	line, _ := app.reader.ReadString('\n')
	return strings.TrimSpace(line)
}

func (app *MemeApp) askInt(prompt string, def int) int {
	for {
		ans := app.ask(prompt)
		if ans == "" {
			return def
		}
		if val, err := strconv.Atoi(ans); err == nil && val >= 10 && val <= 200 {
			return val
		}
		fmt.Println(c("⚠️  Please enter a number between 10 and 200.", yellow))
	}
}

func (app *MemeApp) showMenu() {
	fmt.Println("\n" + c(strings.Repeat("═", 50), cyan))
	fmt.Println(c("🎭 MEME GENERATOR", bright+cyan))
	fmt.Println(c(strings.Repeat("═", 50), cyan))
	fmt.Printf("  Top: %s\n", app.topText)
	if app.topText == "" {
		fmt.Print("(empty)")
	}
	fmt.Printf("  Bottom: %s\n", app.bottomText)
	if app.bottomText == "" {
		fmt.Print("(empty)")
	}
	fmt.Printf("  Image: %s\n", app.imageURL[:min(40, len(app.imageURL))])
	fmt.Println(c(strings.Repeat("═", 50), cyan))
	fmt.Println("  1. 📝 Set Top Text")
	fmt.Println("  2. 📝 Set Bottom Text")
	fmt.Println("  3. 🖼️ Choose Image/Template")
	fmt.Println("  4. 🎨 Set Font Size")
	fmt.Println("  5. 🌈 Set Text Color")
	fmt.Println("  6. 💾 Generate Meme (HTML)")
	fmt.Println("  7. 🖼️ Export as PNG (optional)")
	fmt.Println("  8. 💾 Save/Load Config")
	fmt.Println("  0. 🚪 Exit")
	fmt.Println(c(strings.Repeat("═", 50), cyan))
}

func (app *MemeApp) setTopText() {
	text := app.ask(fmt.Sprintf("Top text (current: %s): ", app.topText))
	if text != "" {
		app.topText = text
	}
}

func (app *MemeApp) setBottomText() {
	text := app.ask(fmt.Sprintf("Bottom text (current: %s): ", app.bottomText))
	if text != "" {
		app.bottomText = text
	}
}

func (app *MemeApp) chooseImage() {
	fmt.Println("Choose template:")
	for key, tpl := range TEMPLATES {
		fmt.Printf("  %s. %s\n", key, tpl.Name)
	}
	choice := app.ask("Select template: ")
	if tpl, ok := TEMPLATES[choice]; ok {
		url := tpl.URL
		if url == "" {
			url = app.ask("Enter custom image URL: ")
		}
		if url != "" {
			app.imageURL = url
		} else {
			app.imageURL = DEFAULT_IMAGE
		}
		fmt.Println(c("✅ Image updated.", green))
	} else {
		fmt.Println(c("❌ Invalid choice.", red))
	}
}

func (app *MemeApp) setFontSize() {
	app.fontSize = app.askInt("Font size (current: %d): ", app.fontSize)
	fmt.Printf(c("✅ Font size set to %d\n", green), app.fontSize)
}

func (app *MemeApp) setColor() {
	color := app.ask(fmt.Sprintf("Text color (hex, current: %s): ", app.color))
	if matched, _ := regexp.MatchString(`^#[0-9a-fA-F]{6}$`, color); matched || regexp.MustCompile(`^#[0-9a-fA-F]{3}$`).MatchString(color) {
		app.color = color
		fmt.Printf(c("✅ Color set to %s\n", green), color)
	} else if color != "" {
		fmt.Println(c("⚠️  Please use hex format, e.g. #ff0000", yellow))
	}
}

func (app *MemeApp) generate() {
	if app.topText == "" && app.bottomText == "" {
		fmt.Println(c("⚠️  Please set at least top or bottom text.", yellow))
		ans := app.ask("Continue anyway? (y/n): ")
		if strings.ToLower(ans) != "y" {
			return
		}
	}
	filename := fmt.Sprintf("meme_%s.html", time.Now().Format("20060102_150405"))
	generateHTML(app.topText, app.bottomText, app.imageURL, app.fontSize, app.color, filename)
	open := app.ask("Open in browser? (y/n): ")
	if strings.ToLower(open) == "y" {
		// Try to open with system command
		cmd := "open" // macOS
		if _, err := exec.LookPath("xdg-open"); err == nil {
			cmd = "xdg-open"
		} else if _, err := exec.LookPath("start"); err == nil {
			cmd = "start"
		}
		exec.Command(cmd, filename).Run()
	}
}

func (app *MemeApp) exportPNG() {
	fmt.Println(c("⚠️  PNG export requires additional libraries. Skipping.", yellow))
}

func (app *MemeApp) saveConfig() {
	fname := app.ask("Config filename (default meme_config.json): ")
	if fname == "" {
		fname = "meme_config.json"
	}
	cfg := Config{
		TopText:    app.topText,
		BottomText: app.bottomText,
		ImageURL:   app.imageURL,
		FontSize:   app.fontSize,
		Color:      app.color,
	}
	data, _ := json.MarshalIndent(cfg, "", "  ")
	ioutil.WriteFile(fname, data, 0644)
	fmt.Printf(c("✅ Config saved to %s\n", green), fname)
}

func (app *MemeApp) loadConfig() {
	fname := app.ask("Config filename (default meme_config.json): ")
	if fname == "" {
		fname = "meme_config.json"
	}
	data, err := ioutil.ReadFile(fname)
	if err != nil {
		fmt.Printf(c("❌ Error loading config: %v\n", red), err)
		return
	}
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		fmt.Printf(c("❌ Invalid JSON: %v\n", red), err)
		return
	}
	app.topText = cfg.TopText
	app.bottomText = cfg.BottomText
	app.imageURL = cfg.ImageURL
	if app.imageURL == "" {
		app.imageURL = DEFAULT_IMAGE
	}
	app.fontSize = cfg.FontSize
	if app.fontSize == 0 {
		app.fontSize = 40
	}
	app.color = cfg.Color
	if app.color == "" {
		app.color = "#ffffff"
	}
	fmt.Printf(c("✅ Config loaded from %s\n", green), fname)
}

func (app *MemeApp) run() {
	fmt.Print("\033[H\033[2J")
	fmt.Printf("%s\n", c("\n🎭 Meme Generator – Top & Bottom Text", bright+cyan))
	fmt.Printf("%s\n", c("Create your own memes in seconds!", dim))

	for {
		app.showMenu()
		choice := app.ask("Your choice: ")
		switch choice {
		case "1":
			app.setTopText()
		case "2":
			app.setBottomText()
		case "3":
			app.chooseImage()
		case "4":
			app.setFontSize()
		case "5":
			app.setColor()
		case "6":
			app.generate()
		case "7":
			app.exportPNG()
		case "8":
			sub := app.ask("Save (s) or Load (l)? ")
			if sub == "s" {
				app.saveConfig()
			} else if sub == "l" {
				app.loadConfig()
			} else {
				fmt.Println(c("Invalid choice.", red))
			}
		case "0":
			fmt.Printf("%s\n", c("👋 Happy memeing!", cyan))
			return
		default:
			fmt.Println(c("❌ Invalid choice.", red))
		}
		if choice != "0" {
			fmt.Print("\nPress Enter to continue...")
			app.reader.ReadString('\n')
		}
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	app := NewMemeApp()
	app.run()
}
