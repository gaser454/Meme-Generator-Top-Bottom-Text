# MemeGenerator.cs
/**
 * 🎭 Meme Generator – Top & Bottom Text (C# Edition)
 * Features: custom image URL, top/bottom text, HTML output, config save/load
 * Requires: .NET 6.0+
 */

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

class MemeGenerator
{
    // ─── Colors ────────────────────────────────────────────────────────────

    private static readonly string Reset = "\u001B[0m";
    private static readonly string Bright = "\u001B[1m";
    private static readonly string Dim = "\u001B[2m";
    private static readonly string Red = "\u001B[31m";
    private static readonly string Green = "\u001B[32m";
    private static readonly string Yellow = "\u001B[33m";
    private static readonly string Blue = "\u001B[34m";
    private static readonly string Magenta = "\u001B[35m";
    private static readonly string Cyan = "\u001B[36m";

    private static string C(string text, string color) => color + text + Reset;

    // ─── Templates ─────────────────────────────────────────────────────────

    private static readonly Dictionary<string, (string Name, string Url)> Templates = new()
    {
        ["1"] = ("Drake", "https://i.imgflip.com/30b1gx.jpg"),
        ["2"] = ("Distracted Boyfriend", "https://i.imgflip.com/1ur9b0.jpg"),
        ["3"] = ("Two Buttons", "https://i.imgflip.com/1g8my4.jpg"),
        ["4"] = ("Change My Mind", "https://i.imgflip.com/24y43o.jpg"),
        ["5"] = ("Custom URL", "")
    };
    private const string DefaultImage = "https://i.imgflip.com/30b1gx.jpg";

    // ─── HTML Generator ──────────────────────────────────────────────────

    private static void GenerateHTML(string topText, string bottomText, string imageUrl,
                                     int fontSize, string color, string output)
    {
        string topEsc = topText.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;");
        string botEsc = bottomText.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;");
        string html = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
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
            font-size: {fontSize}px;
            font-weight: bold;
            text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000;
            word-wrap: break-word;
            line-height: 1.2;
        }}
        .meme-text.top {{ top: 10px; font-size: {fontSize}px; }}
        .meme-text.bottom {{ bottom: 10px; font-size: {fontSize}px; }}
        @media (max-width: 600px) {{
            .meme-text {{ font-size: {fontSize/2}px !important; padding: 5px 10px; }}
        }}
    </style>
</head>
<body>
    <div class=""meme-container"">
        <img class=""meme-image"" src=""{imageUrl}"" alt=""Meme image"">
        <div class=""meme-text top"">{topEsc}</div>
        <div class=""meme-text bottom"">{botEsc}</div>
    </div>
</body>
</html>";
        File.WriteAllText(output, html);
        Console.WriteLine(C($"✅ Meme saved to {output}", Green));
        Console.WriteLine(C("   Open this file in your browser to view the meme.", Dim));
    }

    // ─── Main App ──────────────────────────────────────────────────────────

    private string topText = "", bottomText = "", imageUrl = DefaultImage, color = "#ffffff";
    private int fontSize = 40;

    private string Ask(string prompt)
    {
        Console.Write(prompt);
        return Console.ReadLine()?.Trim() ?? "";
    }

    private int AskInt(string prompt, int def)
    {
        while (true)
        {
            string ans = Ask(prompt);
            if (string.IsNullOrEmpty(ans)) return def;
            if (int.TryParse(ans, out int val) && val >= 10 && val <= 200)
                return val;
            Console.WriteLine(C("⚠️  Please enter a number between 10 and 200.", Yellow));
        }
    }

    private void ShowMenu()
    {
        Console.WriteLine("\n" + C(new string('═', 50), Cyan));
        Console.WriteLine(C("🎭 MEME GENERATOR", Bright + Cyan));
        Console.WriteLine(C(new string('═', 50), Cyan));
        Console.WriteLine($"  Top: {(string.IsNullOrEmpty(topText) ? "(empty)" : topText)}");
        Console.WriteLine($"  Bottom: {(string.IsNullOrEmpty(bottomText) ? "(empty)" : bottomText)}");
        string img = imageUrl.Length > 40 ? imageUrl[..40] + "..." : imageUrl;
        Console.WriteLine($"  Image: {img}");
        Console.WriteLine(C(new string('═', 50), Cyan));
        Console.WriteLine("  1. 📝 Set Top Text");
        Console.WriteLine("  2. 📝 Set Bottom Text");
        Console.WriteLine("  3. 🖼️ Choose Image/Template");
        Console.WriteLine("  4. 🎨 Set Font Size");
        Console.WriteLine("  5. 🌈 Set Text Color");
        Console.WriteLine("  6. 💾 Generate Meme (HTML)");
        Console.WriteLine("  7. 🖼️ Export as PNG (optional)");
        Console.WriteLine("  8. 💾 Save/Load Config");
        Console.WriteLine("  0. 🚪 Exit");
        Console.WriteLine(C(new string('═', 50), Cyan));
    }

    private void SetTopText()
    {
        string text = Ask($"Top text (current: {topText}): ");
        if (!string.IsNullOrEmpty(text)) topText = text;
    }

    private void SetBottomText()
    {
        string text = Ask($"Bottom text (current: {bottomText}): ");
        if (!string.IsNullOrEmpty(text)) bottomText = text;
    }

    private void ChooseImage()
    {
        Console.WriteLine("Choose template:");
        foreach (var kv in Templates)
            Console.WriteLine($"  {kv.Key}. {kv.Value.Name}");
        string choice = Ask("Select template: ");
        if (Templates.TryGetValue(choice, out var tpl))
        {
            string url = tpl.Url;
            if (string.IsNullOrEmpty(url))
            {
                url = Ask("Enter custom image URL: ");
                if (string.IsNullOrEmpty(url)) url = DefaultImage;
            }
            imageUrl = url;
            Console.WriteLine(C("✅ Image updated.", Green));
        }
        else
        {
            Console.WriteLine(C("❌ Invalid choice.", Red));
        }
    }

    private void SetFontSize()
    {
        fontSize = AskInt($"Font size (current: {fontSize}): ", fontSize);
        Console.WriteLine(C($"✅ Font size set to {fontSize}", Green));
    }

    private void SetColor()
    {
        string col = Ask($"Text color (hex, current: {color}): ");
        if (string.IsNullOrEmpty(col)) return;
        if (Regex.IsMatch(col, "^#[0-9a-fA-F]{6}$|^#[0-9a-fA-F]{3}$"))
        {
            color = col;
            Console.WriteLine(C($"✅ Color set to {color}", Green));
        }
        else
        {
            Console.WriteLine(C("⚠️  Please use hex format, e.g. #ff0000", Yellow));
        }
    }

    private void Generate()
    {
        if (string.IsNullOrEmpty(topText) && string.IsNullOrEmpty(bottomText))
        {
            Console.WriteLine(C("⚠️  Please set at least top or bottom text.", Yellow));
            string ans = Ask("Continue anyway? (y/n): ");
            if (!ans.Equals("y", StringComparison.OrdinalIgnoreCase)) return;
        }
        string ts = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        string filename = $"meme_{ts}.html";
        GenerateHTML(topText, bottomText, imageUrl, fontSize, color, filename);
        string open = Ask("Open in browser? (y/n): ");
        if (open.Equals("y", StringComparison.OrdinalIgnoreCase))
        {
            try
            {
                string os = Environment.OSVersion.Platform.ToString();
                if (os.Contains("Win"))
                    System.Diagnostics.Process.Start("explorer", filename);
                else if (os.Contains("Mac"))
                    System.Diagnostics.Process.Start("open", filename);
                else
                    System.Diagnostics.Process.Start("xdg-open", filename);
            }
            catch { /* ignore */ }
        }
    }

    private void ExportPNG()
    {
        Console.WriteLine(C("⚠️  PNG export requires additional libraries. Skipping.", Yellow));
    }

    private void SaveConfig()
    {
        string fname = Ask("Config filename (default meme_config.json): ");
        if (string.IsNullOrEmpty(fname)) fname = "meme_config.json";
        var json = $@"{{
  ""topText"": ""{topText}"",
  ""bottomText"": ""{bottomText}"",
  ""imageUrl"": ""{imageUrl}"",
  ""fontSize"": {fontSize},
  ""color"": ""{color}""
}}";
        File.WriteAllText(fname, json);
        Console.WriteLine(C($"✅ Config saved to {fname}", Green));
    }

    private void LoadConfig()
    {
        string fname = Ask("Config filename (default meme_config.json): ");
        if (string.IsNullOrEmpty(fname)) fname = "meme_config.json";
        if (!File.Exists(fname))
        {
            Console.WriteLine(C($"❌ File not found: {fname}", Red));
            return;
        }
        string content = File.ReadAllText(fname);
        topText = ExtractString(content, "topText");
        bottomText = ExtractString(content, "bottomText");
        imageUrl = ExtractString(content, "imageUrl");
        if (string.IsNullOrEmpty(imageUrl)) imageUrl = DefaultImage;
        fontSize = ExtractInt(content, "fontSize", 40);
        color = ExtractString(content, "color");
        if (string.IsNullOrEmpty(color)) color = "#ffffff";
        Console.WriteLine(C($"✅ Config loaded from {fname}", Green));
    }

    private string ExtractString(string json, string key)
    {
        var match = Regex.Match(json, $@"""{key}""\s*:\s*""([^""]*)""");
        return match.Success ? match.Groups[1].Value : "";
    }

    private int ExtractInt(string json, string key, int def)
    {
        var match = Regex.Match(json, $@"""{key}""\s*:\s*(\d+)");
        return match.Success ? int.Parse(match.Groups[1].Value) : def;
    }

    public void Run()
    {
        Console.Clear();
        Console.WriteLine(C("\n🎭 Meme Generator – Top & Bottom Text", Bright + Cyan));
        Console.WriteLine(C("Create your own memes in seconds!", Dim));

        while (true)
        {
            ShowMenu();
            string choice = Ask("Your choice: ");
            switch (choice)
            {
                case "1": SetTopText(); break;
                case "2": SetBottomText(); break;
                case "3": ChooseImage(); break;
                case "4": SetFontSize(); break;
                case "5": SetColor(); break;
                case "6": Generate(); break;
                case "7": ExportPNG(); break;
                case "8":
                    string sub = Ask("Save (s) or Load (l)? ");
                    if (sub == "s") SaveConfig();
                    else if (sub == "l") LoadConfig();
                    else Console.WriteLine(C("Invalid choice.", Red));
                    break;
                case "0":
                    Console.WriteLine(C("👋 Happy memeing!", Cyan));
                    return;
                default:
                    Console.WriteLine(C("❌ Invalid choice.", Red));
                    break;
            }
            if (choice != "0")
            {
                Console.Write("\nPress Enter to continue...");
                Console.ReadLine();
            }
        }
    }

    public static void Main()
    {
        try
        {
            new MemeGenerator().Run();
        }
        catch (Exception ex)
        {
            Console.WriteLine(C($"❌ Unexpected error: {ex.Message}", Red));
            Environment.Exit(1);
        }
    }
}
