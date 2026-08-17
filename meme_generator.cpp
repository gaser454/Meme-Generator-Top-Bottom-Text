# meme_generator.cpp
/**
 * 🎭 Meme Generator – Top & Bottom Text (C++ Edition)
 * Features: custom image URL, top/bottom text, HTML output, config save/load
 * Uses only STL, no external libraries.
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <cctype>

#ifdef _WIN32
#include <windows.h>
#endif

// ─── Colors ──────────────────────────────────────────────────────────────────

#ifdef _WIN32
HANDLE hConsole;
void setColor(int color) { SetConsoleTextAttribute(hConsole, color); }
#define RESET_COLOR setColor(7)
#define COLOR_RED setColor(12)
#define COLOR_GREEN setColor(10)
#define COLOR_YELLOW setColor(14)
#define COLOR_BLUE setColor(9)
#define COLOR_MAGENTA setColor(13)
#define COLOR_CYAN setColor(11)
#define COLOR_BRIGHT setColor(15)
#define COLOR_DIM setColor(8)
#else
#define RESET_COLOR std::cout << "\x1b[0m"
#define COLOR_RED std::cout << "\x1b[31m"
#define COLOR_GREEN std::cout << "\x1b[32m"
#define COLOR_YELLOW std::cout << "\x1b[33m"
#define COLOR_BLUE std::cout << "\x1b[34m"
#define COLOR_MAGENTA std::cout << "\x1b[35m"
#define COLOR_CYAN std::cout << "\x1b[36m"
#define COLOR_BRIGHT std::cout << "\x1b[1m"
#define COLOR_DIM std::cout << "\x1b[2m"
#endif

#define C(str, color) color << str << RESET_COLOR

// ─── Helpers ─────────────────────────────────────────────────────────────────

std::string trim(const std::string& s) {
    auto start = s.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    auto end = s.find_last_not_of(" \t\n\r");
    return s.substr(start, end - start + 1);
}

std::string replace_all(std::string s, const std::string& from, const std::string& to) {
    size_t pos = 0;
    while ((pos = s.find(from, pos)) != std::string::npos) {
        s.replace(pos, from.length(), to);
        pos += to.length();
    }
    return s;
}

std::string escape_html(const std::string& s) {
    std::string out = s;
    out = replace_all(out, "&", "&amp;");
    out = replace_all(out, "<", "&lt;");
    out = replace_all(out, ">", "&gt;");
    return out;
}

// ─── Templates ─────────────────────────────────────────────────────────────

const std::map<std::string, std::pair<std::string, std::string>> TEMPLATES = {
    {"1", {"Drake", "https://i.imgflip.com/30b1gx.jpg"}},
    {"2", {"Distracted Boyfriend", "https://i.imgflip.com/1ur9b0.jpg"}},
    {"3", {"Two Buttons", "https://i.imgflip.com/1g8my4.jpg"}},
    {"4", {"Change My Mind", "https://i.imgflip.com/24y43o.jpg"}},
    {"5", {"Custom URL", ""}}
};
const std::string DEFAULT_IMAGE = "https://i.imgflip.com/30b1gx.jpg";

// ─── HTML Generator ──────────────────────────────────────────────────────

void generateHTML(const std::string& topText, const std::string& bottomText,
                  const std::string& imageURL, int fontSize,
                  const std::string& color, const std::string& output) {
    std::string topEsc = escape_html(topText);
    std::string botEsc = escape_html(bottomText);
    std::ofstream file(output);
    file << R"(<!DOCTYPE html>
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
            color: )" << color << R"(;
            font-size: )" << fontSize << R"(px;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }
        .meme-text.top { top: 10px; font-size: )" << fontSize << R"(px; }
        .meme-text.bottom { bottom: 10px; font-size: )" << fontSize << R"(px; }
        @media (max-width: 600px) {
            .meme-text { font-size: )" << (fontSize/2) << R"(px !important; padding: 5px 10px; }
        }
    </style>
</head>
<body>
    <div class="meme-container">
        <img class="meme-image" src=")" << imageURL << R"(" alt="Meme image">
        <div class="meme-text top">)" << topEsc << R"(</div>
        <div class="meme-text bottom">)" << botEsc << R"(</div>
    </div>
</body>
</html>)";
    file.close();
    std::cout << C("✅ Meme saved to " + output, COLOR_GREEN) << std::endl;
    std::cout << C("   Open this file in your browser to view the meme.", COLOR_DIM) << std::endl;
}

// ─── Main App ──────────────────────────────────────────────────────────────

class MemeApp {
public:
    MemeApp() : topText(""), bottomText(""), imageURL(DEFAULT_IMAGE), fontSize(40), color("#ffffff") {}

    void run() {
        std::cout << "\033[2J\033[1;1H";
        std::cout << C("\n🎭 Meme Generator – Top & Bottom Text", COLOR_BRIGHT) << C("", COLOR_CYAN) << std::endl;
        std::cout << C("Create your own memes in seconds!", COLOR_DIM) << std::endl;

        while (true) {
            showMenu();
            std::string choice = ask("Your choice: ");
            if (choice == "1") setTopText();
            else if (choice == "2") setBottomText();
            else if (choice == "3") chooseImage();
            else if (choice == "4") setFontSize();
            else if (choice == "5") setColor();
            else if (choice == "6") generate();
            else if (choice == "7") exportPNG();
            else if (choice == "8") {
                std::string sub = ask("Save (s) or Load (l)? ");
                if (sub == "s") saveConfig();
                else if (sub == "l") loadConfig();
                else std::cout << C("Invalid choice.", COLOR_RED) << std::endl;
            }
            else if (choice == "0") {
                std::cout << C("👋 Happy memeing!", COLOR_CYAN) << std::endl;
                break;
            } else {
                std::cout << C("❌ Invalid choice.", COLOR_RED) << std::endl;
            }
            if (choice != "0") {
                std::cout << "\nPress Enter to continue...";
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                std::cin.get();
            }
        }
    }

private:
    std::string topText, bottomText, imageURL, color;
    int fontSize;

    std::string ask(const std::string& prompt) {
        std::cout << prompt;
        std::string line;
        std::getline(std::cin, line);
        return trim(line);
    }

    int askInt(const std::string& prompt, int def) {
        while (true) {
            std::string ans = ask(prompt);
            if (ans.empty()) return def;
            try { int val = std::stoi(ans); if (val >= 10 && val <= 200) return val; }
            catch (...) {}
            std::cout << C("⚠️  Please enter a number between 10 and 200.", COLOR_YELLOW) << std::endl;
        }
    }

    void showMenu() {
        std::cout << "\n" << C(std::string(50, '═'), COLOR_CYAN) << std::endl;
        std::cout << C("🎭 MEME GENERATOR", COLOR_BRIGHT) << C("", COLOR_CYAN) << std::endl;
        std::cout << C(std::string(50, '═'), COLOR_CYAN) << std::endl;
        std::cout << "  Top: " << (topText.empty() ? "(empty)" : topText) << std::endl;
        std::cout << "  Bottom: " << (bottomText.empty() ? "(empty)" : bottomText) << std::endl;
        std::cout << "  Image: " << imageURL.substr(0, 40) << "..." << std::endl;
        std::cout << C(std::string(50, '═'), COLOR_CYAN) << std::endl;
        std::cout << "  1. 📝 Set Top Text" << std::endl;
        std::cout << "  2. 📝 Set Bottom Text" << std::endl;
        std::cout << "  3. 🖼️ Choose Image/Template" << std::endl;
        std::cout << "  4. 🎨 Set Font Size" << std::endl;
        std::cout << "  5. 🌈 Set Text Color" << std::endl;
        std::cout << "  6. 💾 Generate Meme (HTML)" << std::endl;
        std::cout << "  7. 🖼️ Export as PNG (optional)" << std::endl;
        std::cout << "  8. 💾 Save/Load Config" << std::endl;
        std::cout << "  0. 🚪 Exit" << std::endl;
        std::cout << C(std::string(50, '═'), COLOR_CYAN) << std::endl;
    }

    void setTopText() {
        std::string text = ask("Top text (current: " + topText + "): ");
        if (!text.empty()) topText = text;
    }

    void setBottomText() {
        std::string text = ask("Bottom text (current: " + bottomText + "): ");
        if (!text.empty()) bottomText = text;
    }

    void chooseImage() {
        std::cout << "Choose template:" << std::endl;
        for (const auto& [key, val] : TEMPLATES) {
            std::cout << "  " << key << ". " << val.first << std::endl;
        }
        std::string choice = ask("Select template: ");
        auto it = TEMPLATES.find(choice);
        if (it != TEMPLATES.end()) {
            std::string url = it->second.second;
            if (url.empty()) {
                url = ask("Enter custom image URL: ");
                if (url.empty()) url = DEFAULT_IMAGE;
            }
            imageURL = url;
            std::cout << C("✅ Image updated.", COLOR_GREEN) << std::endl;
        } else {
            std::cout << C("❌ Invalid choice.", COLOR_RED) << std::endl;
        }
    }

    void setFontSize() {
        fontSize = askInt("Font size (current: " + std::to_string(fontSize) + "): ", fontSize);
        std::cout << C("✅ Font size set to " + std::to_string(fontSize), COLOR_GREEN) << std::endl;
    }

    void setColor() {
        std::string col = ask("Text color (hex, current: " + color + "): ");
        if (col.empty()) return;
        if ((col[0] == '#') && (col.length() == 4 || col.length() == 7)) {
            color = col;
            std::cout << C("✅ Color set to " + color, COLOR_GREEN) << std::endl;
        } else {
            std::cout << C("⚠️  Please use hex format, e.g. #ff0000", COLOR_YELLOW) << std::endl;
        }
    }

    void generate() {
        if (topText.empty() && bottomText.empty()) {
            std::cout << C("⚠️  Please set at least top or bottom text.", COLOR_YELLOW) << std::endl;
            std::string ans = ask("Continue anyway? (y/n): ");
            if (ans != "y" && ans != "Y") return;
        }
        std::time_t t = std::time(nullptr);
        std::tm* tm = std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(tm, "meme_%Y%m%d_%H%M%S.html");
        std::string filename = oss.str();
        generateHTML(topText, bottomText, imageURL, fontSize, color, filename);
        std::string open = ask("Open in browser? (y/n): ");
        if (open == "y" || open == "Y") {
#ifdef _WIN32
            std::string cmd = "start " + filename;
#elif __APPLE__
            std::string cmd = "open " + filename;
#else
            std::string cmd = "xdg-open " + filename;
#endif
            system(cmd.c_str());
        }
    }

    void exportPNG() {
        std::cout << C("⚠️  PNG export requires additional libraries. Skipping.", COLOR_YELLOW) << std::endl;
    }

    void saveConfig() {
        std::string fname = ask("Config filename (default meme_config.json): ");
        if (fname.empty()) fname = "meme_config.json";
        std::ofstream file(fname);
        file << "{\n";
        file << "  \"topText\": \"" << topText << "\",\n";
        file << "  \"bottomText\": \"" << bottomText << "\",\n";
        file << "  \"imageUrl\": \"" << imageURL << "\",\n";
        file << "  \"fontSize\": " << fontSize << ",\n";
        file << "  \"color\": \"" << color << "\"\n";
        file << "}\n";
        file.close();
        std::cout << C("✅ Config saved to " + fname, COLOR_GREEN) << std::endl;
    }

    void loadConfig() {
        std::string fname = ask("Config filename (default meme_config.json): ");
        if (fname.empty()) fname = "meme_config.json";
        std::ifstream file(fname);
        if (!file) {
            std::cout << C("❌ File not found: " + fname, COLOR_RED) << std::endl;
            return;
        }
        // Very simple parsing – in production use a JSON library
        std::string line;
        while (std::getline(file, line)) {
            if (line.find("\"topText\"") != std::string::npos) {
                size_t start = line.find("\"") + 1;
                size_t end = line.rfind("\"");
                if (start != std::string::npos && end != std::string::npos && end > start) {
                    topText = line.substr(start, end - start);
                }
            } else if (line.find("\"bottomText\"") != std::string::npos) {
                size_t start = line.find("\"") + 1;
                size_t end = line.rfind("\"");
                if (start != std::string::npos && end != std::string::npos && end > start) {
                    bottomText = line.substr(start, end - start);
                }
            } else if (line.find("\"imageUrl\"") != std::string::npos) {
                size_t start = line.find("\"") + 1;
                size_t end = line.rfind("\"");
                if (start != std::string::npos && end != std::string::npos && end > start) {
                    imageURL = line.substr(start, end - start);
                    if (imageURL.empty()) imageURL = DEFAULT_IMAGE;
                }
            } else if (line.find("\"fontSize\"") != std::string::npos) {
                size_t start = line.find(":") + 1;
                try { fontSize = std::stoi(trim(line.substr(start))); }
                catch (...) { fontSize = 40; }
            } else if (line.find("\"color\"") != std::string::npos) {
                size_t start = line.find("\"") + 1;
                size_t end = line.rfind("\"");
                if (start != std::string::npos && end != std::string::npos && end > start) {
                    color = line.substr(start, end - start);
                    if (color.empty()) color = "#ffffff";
                }
            }
        }
        std::cout << C("✅ Config loaded from " + fname, COLOR_GREEN) << std::endl;
    }
};

int main() {
#ifdef _WIN32
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
#endif
    try {
        MemeApp app;
        app.run();
    } catch (const std::exception& e) {
        std::cerr << C("❌ Unexpected error: ", COLOR_RED) << e.what() << std::endl;
        return 1;
    }
    return 0;
}
