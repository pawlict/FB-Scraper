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
1) System update && upgrade
```bash 
sudo apt-get update && sudo apt-get upgrade -y
```
2) System packages
```bash 
sudo apt install -y python3-venv python3-tk python3-dev build-essential
```

3) Get the code inside venv folder
```bash
mkdir -p ~/projects && cd ~/projects/FB_Scraper
git clone https://github.com/pawlict/FB_Scraper.git
python3 -m venv .FB_Scraper
source .FB_Scraper/bin/activate
cd FB_Scraper
pip install -r requirements.txt
```
4) Start program
```bash 
python3 FB_scraper.py
```

## First run – what to expect
A Chromium window opens → log in to Facebook normally.
Close the browser; cookies are saved to fb_cookies.json.
In Scraper tab: paste profile URL → Start → when prompted, scroll Friends to the end → OK.
Use Save CSV to export results.
Switch PL/EN in Settings (stored in fb_scraper_config.json).

##  ⚠️ Troubleshooting ⚠️ 

NO_PUBKEY ED65462EC8D5E4C5
```bash
# 1) Fetch the new keyring directly into the system keyrings directory

sudo wget -O /usr/share/keyrings/kali-archive-keyring.gpg https://archive.kali.org/archive-keyring.gpg

# 2) Set the official repo with signed-by (HTTPS!). This file can coexist with others,
#    but avoid duplicates. Ideally, use this single definition going forward.
echo 'deb [signed-by=/usr/share/keyrings/kali-archive-keyring.gpg] https://http.kali.org/kali kali-rolling main non-free non-free-firmware contrib' \
| sudo tee /etc/apt/sources.list.d/kali-official.list >/dev/null

# (optional) Comment out old "kali" entries in /etc/apt/sources.list to avoid duplicates:
# sudo sed -i 's|^deb .*kali.*|# &|' /etc/apt/sources.list

# 3) Refresh package indexes
sudo apt-get update
```

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
