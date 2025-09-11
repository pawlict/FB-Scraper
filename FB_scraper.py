# -*- coding: utf-8 -*-
"""
FB_scraper.py
Wersja 1.0 — (MIT)
====================================================================

MIT License

Copyright (c) 2025 pawlict

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import json, random, re, time, urllib.parse as up
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from playwright.sync_api import sync_playwright, Error as PwError
from bs4 import BeautifulSoup

# ----------  STAŁE / KONFIG  --------------------------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
}
PREFERRED_CHANNEL = "chrome"           # fallback → chromium
COOKIE_FILE = Path("fb_cookies.json")
CONFIG_FILE = Path("fb_scraper_config.json")
HUMAN_DELAY = (30, 55)                 # 1 profil ≈ 15–25 s

AUTHOR = "pawlict"
VERSION = "1.0"

# ----------  I18N  -------------------------------------------------------
LANG = {
    "pl": {
        "app_title": f"FB Scraper {VERSION} — znajomi (manual)",
        "tab_scraper": "Skraper",
        "tab_settings": "Ustawienia",
        "tab_info": "Info",
        "label_profile": "Profil:",
        "btn_start": "Start",
        "btn_save_csv": "Zapisz CSV",
        "status_enter_url": "Podaj URL profilu",
        "status_manual_scroll": "Przewiń listę ręcznie…",
        "status_done_n": "Gotowe — {n} znajomych (manual)",
        "error_title": "Błąd",
        "error_need_url": "Podaj URL profilu",
        "info_title": "Informacja",
        "info_saved": "Zapisano",
        "info_no_data_title": "Brak danych",
        "info_no_data_body": "Najpierw pobierz listę.",
        "manual_title": "Tryb ręczny",
        "manual_body": "Przewiń listę znajomych do końca, potem kliknij OK.",
        "settings_language": "Język aplikacji",
        "settings_hint": "Wybierz język interfejsu",
        "radio_pl": "Polski",
        "radio_en": "English",
        "btn_apply": "Zastosuj",
        "about_header": f"Autor: {AUTHOR}\nWersja: {VERSION}\nLicencja: MIT (poniżej pełny tekst)",
        "license_header": "Licencja MIT (AS IS):\n",
    },
    "en": {
        "app_title": f"FB Scraper {VERSION} — friends (manual)",
        "tab_scraper": "Scraper",
        "tab_settings": "Settings",
        "tab_info": "Info",
        "label_profile": "Profile:",
        "btn_start": "Start",
        "btn_save_csv": "Save CSV",
        "status_enter_url": "Enter profile URL",
        "status_manual_scroll": "Manually scroll the list…",
        "status_done_n": "Done — {n} friends (manual)",
        "error_title": "Error",
        "error_need_url": "Enter a profile URL",
        "info_title": "Info",
        "info_saved": "Saved",
        "info_no_data_title": "No data",
        "info_no_data_body": "Fetch the list first.",
        "manual_title": "Manual mode",
        "manual_body": "Scroll the friends list to the end, then click OK.",
        "settings_language": "Application language",
        "settings_hint": "Choose UI language",
        "radio_pl": "Polski",
        "radio_en": "English",
        "btn_apply": "Apply",
        "about_header": f"Author: {AUTHOR}\nVersion: {VERSION}\nLicense: MIT (full text below)",
        "license_header": "MIT License (AS IS):\n",
    },
}

MIT_LICENSE_TEXT = """MIT License

Copyright (c) 2025 pawlict

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

_CURRENT_LANG = "pl"  # nadpisywane z configu

def t(key: str) -> str:
    return LANG.get(_CURRENT_LANG, LANG["pl"]).get(key, key)

def load_config():
    global _CURRENT_LANG
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            _CURRENT_LANG = cfg.get("lang", "pl")
        except Exception:
            _CURRENT_LANG = "pl"
    else:
        _CURRENT_LANG = "pl"

def save_config():
    CONFIG_FILE.write_text(json.dumps({"lang": _CURRENT_LANG}, indent=2), encoding="utf-8")

# ----------  COOKIE SETUP  ----------------------------------------------
def get_cookies():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel=PREFERRED_CHANNEL, headless=False)
        except PwError:
            browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(); page = ctx.new_page()
        if COOKIE_FILE.exists():
            ctx.add_cookies(json.loads(COOKIE_FILE.read_text())); page.goto("https://m.facebook.com/")
        else:
            page.goto("https://m.facebook.com/login")
            input("Zaloguj się w otwartym oknie przeglądarki, potem naciśnij ENTER… ")
            COOKIE_FILE.write_text(json.dumps(ctx.cookies(), indent=2), encoding="utf-8")
        cookies = {c["name"]: c["value"] for c in ctx.cookies()}
        browser.close()
        return cookies

# (Uwaga: logowanie pozostaje manualne, i18n dotyczy interfejsu aplikacji.)

# ----------  HELPERS  ---------------------------------------------------
def norm(url: str) -> str:
    url = url if url.startswith("http") else "https://" + url
    parsed = up.urlparse(url)
    if "facebook.com" not in parsed.netloc.lower():
        raise ValueError("To nie wygląda na link FB / This doesn't look like a FB link.")
    return up.urlunparse(("https", "m.facebook.com", parsed.path.rstrip("/"), "", parsed.query, ""))

PAT_PROFILE = re.compile(r"(?:/profile\.php\?id=\d+|/people/[^/]+/\d+|/[0-9]{5,}|/[A-Za-z0-9.\-]+)$")
BAD = ("/help", "/privacy", "/policies", "/ads", "/settings", "/terms")

def parse_friends(html: str, base: str):
    soup = BeautifulSoup(html, "html.parser")
    friends, seen = [], set()
    for a in soup.select("a[href]"):
        href = up.urljoin(base, a["href"])
        if any(b in href for b in BAD):
            continue
        path = up.urlparse(href).path
        if PAT_PROFILE.search(path):
            name = a.get_text(" ", strip=True)
            if not name or any(k in name.lower() for k in ("znajomi", "friends")):
                continue
            clean = href.split("?", 1)[0] if "/profile.php" not in path else href.split("&", 1)[0]
            if clean not in seen:
                friends.append({"name": name, "url": clean}); seen.add(clean)
    return friends

# ----------  SCRAPER  ---------------------------------------------------
def scrape_manual(url: str):
    """Otwiera zakładkę Friends; użytkownik ręcznie przewija listę."""
    def wait():
        time.sleep(random.uniform(*HUMAN_DELAY))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(); ctx.add_cookies(json.loads(COOKIE_FILE.read_text()))
        page = ctx.new_page(); page.goto(norm(url), wait_until="domcontentloaded")
        # przejście na Friends, jeśli trzeba
        if not re.search(r"(/friends|[?&](?:v|sk)=friends)", page.url):
            tab = page.locator("a:has-text('Znajomi'), a:has-text('Friends')").first
            if tab.count():
                tab.click(); page.wait_for_load_state("networkidle")
        if not re.search(r"(/friends|[?&](?:v|sk)=friends)", page.url):
            page.goto(page.url.rstrip("/") + "/friends", wait_until="networkidle")

        messagebox.showinfo(t("manual_title"), t("manual_body"))
        wait()  # „ludzkie” tempo – jeden widok
        html = page.content(); browser.close()
    return parse_friends(html, url)

# ----------  GUI  -------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang_var = tk.StringVar(value=_CURRENT_LANG)
        self.title(f"{t('app_title')} — by {AUTHOR}")
        self.geometry("920x680"); self.resizable(False, False)

        # Notebook: Skraper / Settings / Info
        self.nb = ttk.Notebook(self)
        self.tab_scraper = ttk.Frame(self.nb)
        self.tab_settings = ttk.Frame(self.nb)
        self.tab_info = ttk.Frame(self.nb)
        self.nb.add(self.tab_scraper, text=t("tab_scraper"))
        self.nb.add(self.tab_settings, text=t("tab_settings"))
        self.nb.add(self.tab_info, text=t("tab_info"))
        self.nb.pack(fill="both", expand=True)

        # --- Skraper UI
        self.url_var = tk.StringVar()
        self.msg = tk.StringVar(value=t("status_enter_url"))
        self._build_scraper_ui(self.tab_scraper)

        # --- Settings UI
        self._build_settings_ui(self.tab_settings)

        # --- Info UI
        self._build_info_ui(self.tab_info)

        # Ustaw i18n
        self.apply_language(initial=True)

        # Przygotuj cookies na starcie (jak wcześniej)
        if not COOKIE_FILE.exists():
            try:
                get_cookies()
            except Exception as e:
                messagebox.showerror(t("error_title"), str(e))

    # --- UI builders
    def _build_scraper_ui(self, root):
        top = ttk.Frame(root, padding=10); top.pack(fill="x")
        self.lbl_profile = ttk.Label(top, text=t("label_profile"))
        self.lbl_profile.pack(side="left")
        self.ent_url = ttk.Entry(top, textvariable=self.url_var, width=72)
        self.ent_url.pack(side="left", padx=5)
        self.btn_start = ttk.Button(top, text=t("btn_start"), command=self.run)
        self.btn_start.pack(side="left")

        ttk.Label(root, textvariable=self.msg, foreground="blue").pack(pady=(0,5))

        self.text = tk.Text(root, wrap="none", font=("Consolas", 10))
        self.text.pack(fill="both", expand=True, padx=10)
        y = ttk.Scrollbar(root, orient="vertical", command=self.text.yview)
        y.place(relx=1, rely=0.08, relheight=0.80, anchor="ne")
        self.text.configure(yscrollcommand=y.set)

        self.btn_save = ttk.Button(root, text=t("btn_save_csv"), command=self.save)
        self.btn_save.pack(pady=6)

    def _build_settings_ui(self, root):
        frm = ttk.Frame(root, padding=16); frm.pack(fill="both", expand=True)
        self.lbl_lang = ttk.Label(frm, text=t("settings_language"))
        self.lbl_lang.grid(row=0, column=0, sticky="w")
        self.lbl_hint = ttk.Label(frm, text=t("settings_hint"))
        self.lbl_hint.grid(row=1, column=0, sticky="w", pady=(0,12))

        rb_wrap = ttk.Frame(frm); rb_wrap.grid(row=2, column=0, sticky="w", pady=(0,12))
        self.rb_pl = ttk.Radiobutton(rb_wrap, text=t("radio_pl"), value="pl",
                                     variable=self.lang_var, command=self.on_lang_change)
        self.rb_en = ttk.Radiobutton(rb_wrap, text=t("radio_en"), value="en",
                                     variable=self.lang_var, command=self.on_lang_change)
        self.rb_pl.pack(side="left", padx=(0,16)); self.rb_en.pack(side="left")

        self.btn_apply = ttk.Button(frm, text=t("btn_apply"), command=self.apply_language)
        self.btn_apply.grid(row=3, column=0, sticky="w")

        frm.columnconfigure(0, weight=1)

    def _build_info_ui(self, root):
        top = ttk.Frame(root, padding=10); top.pack(fill="x")
        self.lbl_about = ttk.Label(top, text=t("about_header"))
        self.lbl_about.pack(anchor="w")

        wrap = ttk.Frame(root, padding=10); wrap.pack(fill="both", expand=True)
        self.info_text = tk.Text(wrap, wrap="word", font=("Consolas", 10))
        self.info_text.pack(fill="both", expand=True, side="left")
        scroll = ttk.Scrollbar(wrap, orient="vertical", command=self.info_text.yview)
        scroll.pack(fill="y", side="right")
        self.info_text.configure(yscrollcommand=scroll.set)
        self._render_license_text()

    # --- Actions
    def on_lang_change(self):
        # natychmiastowe podmiany etykiet radiobuttonów robi apply_language
        pass

    def apply_language(self, initial: bool=False):
        global _CURRENT_LANG
        _CURRENT_LANG = self.lang_var.get()
        # Tytuł okna i zakładki
        self.title(f"{t('app_title')} — by {AUTHOR}")
        self.nb.tab(self.tab_scraper, text=t("tab_scraper"))
        self.nb.tab(self.tab_settings, text=t("tab_settings"))
        self.nb.tab(self.tab_info, text=t("tab_info"))
        # Skraper
        self.lbl_profile.config(text=t("label_profile"))
        self.btn_start.config(text=t("btn_start"))
        self.btn_save.config(text=t("btn_save_csv"))
        # Status (nie nadpisuj jeśli użytkownik coś już robi)
        if initial or self.msg.get() in (LANG["pl"]["status_enter_url"], LANG["en"]["status_enter_url"]):
            self.msg.set(t("status_enter_url"))
        # Settings
        self.lbl_lang.config(text=t("settings_language"))
        self.lbl_hint.config(text=t("settings_hint"))
        self.rb_pl.config(text=t("radio_pl"))
        self.rb_en.config(text=t("radio_en"))
        self.btn_apply.config(text=t("btn_apply"))
        # Info
        self.lbl_about.config(text=t("about_header"))
        self._render_license_text()
        # Zapisz wybór
        save_config()

    def _render_license_text(self):
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("end", t("license_header"))
        self.info_text.insert("end", MIT_LICENSE_TEXT.strip() + "\n")
        self.info_text.configure(state="disabled")

    def run(self):
        url = self.url_var.get().strip()
        self.text.delete("1.0", "end")
        if not url:
            messagebox.showerror(t("error_title"), t("error_need_url")); return
        self.msg.set(t("status_manual_scroll")); self.update()
        # upewnij się, że mamy cookies
        if not COOKIE_FILE.exists():
            try:
                get_cookies()
            except Exception as e:
                messagebox.showerror(t("error_title"), str(e)); self.msg.set(LANG[_CURRENT_LANG]["status_enter_url"]); return
        try:
            friends = scrape_manual(url)
        except Exception as e:
            messagebox.showerror(t("error_title"), str(e)); self.msg.set("Przerwano / Aborted"); return
        self.text.insert("end", "name,url\n")
        for fr in friends:
            self.text.insert("end", f"{fr['name']},{fr['url']}\n")
        self.msg.set(t("status_done_n").format(n=len(friends)))

    def save(self):
        data = self.text.get("1.0", "end").strip()
        if not data:
            messagebox.showinfo(t("info_no_data_title"), t("info_no_data_body")); return
        fname = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if fname:
            Path(fname).write_text(data, encoding="utf-8")
            messagebox.showinfo(t("info_title"), f"{t('info_saved')}: {fname}")

# ----------  MAIN  ------------------------------------------------------
if __name__ == "__main__":
    load_config()
    App().mainloop()
