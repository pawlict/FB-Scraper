# FB-Scraper
Facebook friends list scraper (manual scroll)

A simple GUI tool to collect a Facebook profile's **friends** list (manual scroll) using **Playwright** + **Tkinter**.  
Includes:
- **PL/EN internationalization** (switch in the **Settings** tab),
- **Info** tab with **Author** and full **MIT License (AS IS)**,
- Config persisted to `fb_scraper_config.json`,
- Manual cookie setup for authenticated access.

> ⚠️ Use responsibly and in accordance with Facebook’s Terms of Service and local law. This tool does **not** bypass authentication; it relies on your own session cookies.

## Features
- Manual “scroll friends page then parse” flow
- Works with **Chromium** (via `playwright install chromium`)
- **Polish / English** UI toggle
- Save results to **CSV**

## Quick Start
1) Get the code

   

```bash 
sudo apt update && sudo apt install -y git
git clone https://github.com/pawlict/FB-Scraper.git
cd FB-Scraper
```
# (ZIP alternative: GitHub → Code → Download ZIP → extract → cd into the folder)



