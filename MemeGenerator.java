# MemeGenerator.java
/**
 * 🎭 Meme Generator – Top & Bottom Text (Java Edition)
 * Features: custom image URL, top/bottom text, HTML output, config save/load
 * Requires: Java 17+
 */

import java.io.*;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import java.util.regex.*;

public class MemeGenerator {
    // ─── Colors ────────────────────────────────────────────────────────────

    private static final String RESET = "\u001B[0m";
    private static final String BRIGHT = "\u001B[1m";
    private static final String DIM = "\u001B[2m";
    private static final String RED = "\u001B[31m";
    private static final String GREEN = "\u001B[32m";
    private static final String YELLOW = "\u001B[33m";
    private static final String BLUE = "\u001B[34m";
    private static final String MAGENTA = "\u001B[35m";
    private static final String CYAN = "\u001B[36m";

    private static String c(String text, String color) { return color + text + RESET; }

    // ─── Templates ─────────────────────────────────────────────────────────

    private static final Map<String, String[]> TEMPLATES = new LinkedHashMap<>();
    static {
        TEMPLATES.put("1", new String[]{"Drake", "https://i.imgflip.com/30b1gx.jpg"});
        TEMPLATES.put("2", new String[]{"Distracted Boyfriend", "https://i.imgflip.com/1ur9b0.jpg"});
        TEMPLATES.put("3", new String[]{"Two Buttons", "https://i.imgflip.com/1g8my4.jpg"});
        TEMPLATES.put("4", new String[]{"Change My Mind", "https://i.imgflip.com/24y43o.jpg"});
        TEMPLATES.put("5", new String[]{"Custom URL", ""});
    }
    private static final String DEFAULT_IMAGE = "https://i.imgflip.com/30b1gx.jpg";

    // ─── HTML Generator ──────────────────────────────────────────────────

    private static void generateHTML(String topText, String bottomText, String imageUrl,
                                     int fontSize, String color, String output) throws IOException {
        String topEsc = topText.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
        String botEsc = bottomText.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
        String html = String.format("""
            <!DOCTYPE html>
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
            </html>
            """, color, fontSize, fontSize, fontSize, fontSize/2, imageUrl, topEsc, botEsc);
        Files.writeString(Paths.get(output), html);
        System.out.println(c("✅ Meme saved to " + output, GREEN));
        System.out.println(c("   Open this file in your browser to view the meme.", DIM));
    }

    // ─── Main App ──────────────────────────────────────────────────────────

    private final Scanner scanner;
    private String topText, bottomText, imageUrl, color;
    private int fontSize;

    public MemeGenerator() {
        scanner = new Scanner(System.in);
        topText = "";
        bottomText = "";
        imageUrl = DEFAULT_IMAGE;
        fontSize = 40;
        color = "#ffffff";
    }

    private String ask(String prompt) {
        System.out.print(prompt);
        return scanner.nextLine().trim();
    }

    private int askInt(String prompt, int def) {
        while (true) {
            String ans = ask(prompt);
            if (ans.isEmpty()) return def;
            try {
                int val = Integer.parseInt(ans);
                if (val >= 10 && val <= 200) return val;
                System.out.println(c("⚠️  Please enter a number between 10 and 200.", YELLOW));
            } catch (NumberFormatException e) {
                System.out.println(c("⚠️  Invalid number.", YELLOW));
            }
        }
    }

    private void showMenu() {
        System.out.println("\n" + c("═".repeat(50), CYAN));
        System.out.println(c("🎭 MEME GENERATOR", BRIGHT + CYAN));
        System.out.println(c("═".repeat(50), CYAN));
        System.out.println("  Top: " + (topText.isEmpty() ? "(empty)" : topText));
        System.out.println("  Bottom: " + (bottomText.isEmpty() ? "(empty)" : bottomText));
        String img = imageUrl.length() > 40 ? imageUrl.substring(0, 40) + "..." : imageUrl;
        System.out.println("  Image: " + img);
        System.out.println(c("═".repeat(50), CYAN));
        System.out.println("  1. 📝 Set Top Text");
        System.out.println("  2. 📝 Set Bottom Text");
        System.out.println("  3. 🖼️ Choose Image/Template");
        System.out.println("  4. 🎨 Set Font Size");
        System.out.println("  5. 🌈 Set Text Color");
        System.out.println("  6. 💾 Generate Meme (HTML)");
        System.out.println("  7. 🖼️ Export as PNG (optional)");
        System.out.println("  8. 💾 Save/Load Config");
        System.out.println("  0. 🚪 Exit");
        System.out.println(c("═".repeat(50), CYAN));
    }

    private void setTopText() {
        String text = ask("Top text (current: " + topText + "): ");
        if (!text.isEmpty()) topText = text;
    }

    private void setBottomText() {
        String text = ask("Bottom text (current: " + bottomText + "): ");
        if (!text.isEmpty()) bottomText = text;
    }

    private void chooseImage() {
        System.out.println("Choose template:");
        for (Map.Entry<String, String[]> e : TEMPLATES.entrySet()) {
            System.out.println("  " + e.getKey() + ". " + e.getValue()[0]);
        }
        String choice = ask("Select template: ");
        if (TEMPLATES.containsKey(choice)) {
            String url = TEMPLATES.get(choice)[1];
            if (url.isEmpty()) {
                url = ask("Enter custom image URL: ");
                if (url.isEmpty()) url = DEFAULT_IMAGE;
            }
            imageUrl = url;
            System.out.println(c("✅ Image updated.", GREEN));
        } else {
            System.out.println(c("❌ Invalid choice.", RED));
        }
    }

    private void setFontSize() {
        fontSize = askInt("Font size (current: " + fontSize + "): ", fontSize);
        System.out.println(c("✅ Font size set to " + fontSize, GREEN));
    }

    private void setColor() {
        String col = ask("Text color (hex, current: " + color + "): ");
        if (col.isEmpty()) return;
        Pattern p = Pattern.compile("^#[0-9a-fA-F]{6}$|^#[0-9a-fA-F]{3}$");
        if (p.matcher(col).matches()) {
            color = col;
            System.out.println(c("✅ Color set to " + color, GREEN));
        } else {
            System.out.println(c("⚠️  Please use hex format, e.g. #ff0000", YELLOW));
        }
    }

    private void generate() throws IOException {
        if (topText.isEmpty() && bottomText.isEmpty()) {
            System.out.println(c("⚠️  Please set at least top or bottom text.", YELLOW));
            String ans = ask("Continue anyway? (y/n): ");
            if (!ans.equalsIgnoreCase("y")) return;
        }
        String ts = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String filename = "meme_" + ts + ".html";
        generateHTML(topText, bottomText, imageUrl, fontSize, color, filename);
        String open = ask("Open in browser? (y/n): ");
        if (open.equalsIgnoreCase("y")) {
            // Try to open with system browser
            try {
                String os = System.getProperty("os.name").toLowerCase();
                Runtime rt = Runtime.getRuntime();
                if (os.contains("win")) {
                    rt.exec("rundll32 url.dll,FileProtocolHandler " + filename);
                } else if (os.contains("mac")) {
                    rt.exec("open " + filename);
                } else {
                    rt.exec("xdg-open " + filename);
                }
            } catch (Exception e) {
                System.out.println(c("⚠️  Could not open browser: " + e.getMessage(), YELLOW));
            }
        }
    }

    private void exportPNG() {
        System.out.println(c("⚠️  PNG export requires additional libraries. Skipping.", YELLOW));
    }

    private void saveConfig() throws IOException {
        String fname = ask("Config filename (default meme_config.json): ");
        if (fname.isEmpty()) fname = "meme_config.json";
        String json = String.format("""
            {
              "topText": "%s",
              "bottomText": "%s",
              "imageUrl": "%s",
              "fontSize": %d,
              "color": "%s"
            }
            """, topText, bottomText, imageUrl, fontSize, color);
        Files.writeString(Paths.get(fname), json);
        System.out.println(c("✅ Config saved to " + fname, GREEN));
    }

    private void loadConfig() throws IOException {
        String fname = ask("Config filename (default meme_config.json): ");
        if (fname.isEmpty()) fname = "meme_config.json";
        String content;
        try {
            content = Files.readString(Paths.get(fname));
        } catch (NoSuchFileException e) {
            System.out.println(c("❌ File not found: " + fname, RED));
            return;
        }
        // Simple manual parse (not robust, but demo)
        topText = extractString(content, "topText");
        bottomText = extractString(content, "bottomText");
        imageUrl = extractString(content, "imageUrl");
        if (imageUrl.isEmpty()) imageUrl = DEFAULT_IMAGE;
        fontSize = extractInt(content, "fontSize", 40);
        color = extractString(content, "color");
        if (color.isEmpty()) color = "#ffffff";
        System.out.println(c("✅ Config loaded from " + fname, GREEN));
    }

    private String extractString(String json, String key) {
        Pattern p = Pattern.compile("\"" + key + "\"\\s*:\\s*\"([^\"]*)\"");
        Matcher m = p.matcher(json);
        return m.find() ? m.group(1) : "";
    }

    private int extractInt(String json, String key, int def) {
        Pattern p = Pattern.compile("\"" + key + "\"\\s*:\\s*(\\d+)");
        Matcher m = p.matcher(json);
        return m.find() ? Integer.parseInt(m.group(1)) : def;
    }

    public void run() throws IOException {
        System.out.print("\033[H\033[2J");
        System.out.flush();
        System.out.println(c("\n🎭 Meme Generator – Top & Bottom Text", BRIGHT + CYAN));
        System.out.println(c("Create your own memes in seconds!", DIM));

        while (true) {
            showMenu();
            String choice = ask("Your choice: ");
            switch (choice) {
                case "1": setTopText(); break;
                case "2": setBottomText(); break;
                case "3": chooseImage(); break;
                case "4": setFontSize(); break;
                case "5": setColor(); break;
                case "6": generate(); break;
                case "7": exportPNG(); break;
                case "8": {
                    String sub = ask("Save (s) or Load (l)? ");
                    if (sub.equals("s")) saveConfig();
                    else if (sub.equals("l")) loadConfig();
                    else System.out.println(c("Invalid choice.", RED));
                    break;
                }
                case "0":
                    System.out.println(c("👋 Happy memeing!", CYAN));
                    return;
                default:
                    System.out.println(c("❌ Invalid choice.", RED));
            }
            if (!choice.equals("0")) {
                System.out.print("\nPress Enter to continue...");
                scanner.nextLine();
            }
        }
    }

    public static void main(String[] args) {
        try {
            new MemeGenerator().run();
        } catch (Exception e) {
            System.err.println(c("❌ Unexpected error: " + e.getMessage(), RED));
            e.printStackTrace();
            System.exit(1);
        }
    }
}
