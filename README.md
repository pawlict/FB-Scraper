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
1) System packages
```bash 
sudo apt update
sudo apt install -y python3-venv python3-tk python3-dev build-essential
```
2) Install Playwright browser (Chromium + deps)
```bash 
python -m playwright install --with-deps chromium
```
3) Get the code
```bash 
sudo apt update && sudo apt install -y git
git clone https://github.com/pawlict/FB-Scraper.git
cd FB-Scraper
```
4) Create & activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel
```
5) Python dependencies
```bash
pip install -r requirements.txt
```
6) Run the app
```bash
python FB_scraper.py
```
## First run – what to expect
A Chromium window opens → log in to Facebook normally.
Close the browser; cookies are saved to fb_cookies.json.
In Scraper tab: paste profile URL → Start → when prompted, scroll Friends to the end → OK.
Use Save CSV to export results.
Switch PL/EN in Settings (stored in fb_scraper_config.json).

## Troubleshooting

Playwright not installed
```bash
pip install playwright
python -m playwright install --with-deps chromium
```

tkinter missing
```bash
sudo apt install -y python3-tk
```

Chromium fails to launch / missing libs
```bash
python -m playwright install --with-deps chromium
sudo apt install -y libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libasound2 libxshmfence1 libgbm1
```

Use Google Chrome instead of Chromium (optional)

```bash
python -m playwright install chrome
```
