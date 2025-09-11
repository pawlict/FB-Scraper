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

# INSTALL (Kali Linux) / INSTALACJA (Kali Linux)

> A step-by-step setup guide for **Kali Linux**.  
> See both **English** and **Polish** sections below.  
> Repo example: `https://github.com/pawlict/FB-Scraper`

---

## Table of contents
- [🇬🇧 Kali Linux — Installation (EN)](#-kali-linux--installation-en)
  - [Quickstart (one block)](#quickstart-one-block)
  - [1) Get the code](#1-get-the-code)
  - [2) System packages](#2-system-packages)
  - [3) Virtual environment](#3-virtual-environment)
  - [4) Python dependencies](#4-python-dependencies)
  - [5) Playwright browser (Chromium + deps)](#5-playwright-browser-chromium--deps)
  - [6) Run the app](#6-run-the-app)
  - [First run](#first-run)
  - [Troubleshooting](#troubleshooting)
- [🇵🇱 Kali Linux — Instalacja (PL)](#-kali-linux--instalacja-pl)
  - [Szybki start (jeden blok)](#szybki-start-jeden-blok)
  - [1) Pobierz kod](#1-pobierz-kod)
  - [2) Pakiety systemowe](#2-pakiety-systemowe)
  - [3) Wirtualne środowisko](#3-wirtualne-środowisko)
  - [4) Biblioteki Pythona](#4-biblioteki-pythona)
  - [5) Playwright (Chromium + zależności)](#5-playwright-chromium--zależności)
  - [6) Uruchom program](#6-uruchom-program)
  - [Pierwsze uruchomienie](#pierwsze-uruchomienie)
  - [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## 🇬🇧 Kali Linux — Installation (EN)

### Quickstart (one block)
```bash
sudo apt update && sudo apt install -y git python3-venv python3-tk python3-dev build-essential
git clone https://github.com/pawlict/FB-Scraper.git
cd FB-Scraper
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip wheel
pip install -r requirements.txt
python -m playwright install --with-deps chromium
python FB_scraper.py

