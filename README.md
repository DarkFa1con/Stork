# 🕊️ **Stork** – The Ultimate Deep Dork Generator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/OSINT-Security-red.svg">
  <img src="https://img.shields.io/badge/Google%20Dorking-Advanced-brightgreen">
</p>

<p align="center">
  <b>Created with ❤️ by Muhammad Hassnain</b><br>
  <i>Unlock the power of Google search with 100+ pre‑built dorks & 20+ operators</i>
</p>

---

## 📸 **Demo**

![Stork Demo](https://github.com/user-attachments/assets/7d909f83-5d46-4013-84a6-faf8737c10f2)

*Stork generates color‑highlighted dorks ready to copy & paste.*

---

## 🚀 **Features at a Glance**

| Category | Description |
|----------|-------------|
| 🔓 **Vulnerability Discovery** | SQLi, LFI, XSS, Open Redirects & more |
| 🔑 **Credential Exposure** | AWS keys, DB passwords, API keys, SSH keys |
| ☁️ **Cloud Infrastructure** | S3 buckets, Jenkins, Kubernetes, Docker |
| 👑 **Admin Panels** | WordPress, phpMyAdmin, routers, web shells |
| 📄 **Sensitive Files** | Backups, configs, logs, confidential PDFs |
| 📷 **IoT & Cameras** | IP cameras, DVRs, network printers |
| 📂 **Open Directories** | Directory listings, parent directories |
| 🕵️ **OSINT** | Emails, employee info, metadata |

**Plus:** 20+ Google operators, interactive builder, template customization, colorized output, and clipboard copy.

---

## 📦 **Installation**

### 1. **Get Stork**
```bash
git clone https://github.com/yourusername/stork.git
cd stork
# or simply download stork.py
```

### 2. **Install dependencies (recommended)**
```bash
pip install colorama pyperclip
```

> Without these, Stork still works – you'll just miss colors & clipboard.

### 3. **Run Stork**
```bash
python stork.py
```

---

## 🎮 **How to Use**

Stork’s interactive menu guides you every step of the way.

```
╔══════════════════════════════════════════════════════════╗
║     Stork - Advanced Deep Dork Generator                 ║
║     Created by Muhammad Hassnain                         ║
║     • 100+ Advanced Templates • 20+ Google Operators    ║
║     • OSINT & Security Focused • Color Output           ║
╚══════════════════════════════════════════════════════════╝

Main Menu:
1. Build custom dork
2. Browse advanced templates (categorized)
3. Exit
```

### **Option 1: Build Custom Dork**
Answer a few questions (all optional). Example:
```
General keywords: vulnerability report
Exact phrase: "zero day"
File type(s): pdf,doc
Site: example.org
... (more prompts)
```
Output:
```
============================================================
Generated Google Dork:

vulnerability report "zero day" filetype:pdf OR filetype:doc site:example.org intitle:security inurl:advisory intext:patch -outdated -deprecated
============================================================
Copy this dork to clipboard? (y/N)
```

### **Option 2: Browse Templates**
Choose a category, pick a dork, and optionally customize it.
```
1. 🔓 Vulnerability Discovery
2. 🔑 Credential & Secret Exposure
...
Select category: 1

1. SQL Injection Points
   inurl:index.php?id= ...
   📝 Common SQL injection vulnerable parameters
2. Local File Inclusion (LFI)
   ...
```

---

## 🧪 **Example Dorks**

| Purpose | Dork |
|--------|------|
| Find exposed AWS keys | `filetype:json intext:"aws_access_key_id" OR filetype:json intext:"aws_secret_access_key"` |
| Locate WordPress admin | `site:target.com inurl:/wp-admin OR inurl:/wp-login.php` |
| Discover Jenkins | `inurl:/jenkins intext:"Dashboard" OR intitle:"Jenkins"` |
| Find database backups | `intitle:"index of" /backup ext:sql \| ext:zip \| ext:tar` |
| Search confidential PDFs | `filetype:pdf "confidential" OR "internal use only" site:.gov` |

---

## ⚙️ **Supported Google Operators**

```
intitle:     allintitle:    inurl:       allinurl:
intext:      allintext:     inanchor:    allinanchor:
filetype:    site:          link:        related:
cache:       daterange:     * (wildcard) .. (number range)
- (exclude)  OR             "exact phrase"
```

---

## 🧰 **Requirements**

- Python 3.6+
- *Optional:* `colorama`, `pyperclip`

---

## ⚠️ **Ethical Warning**

Stork is designed for **educational purposes and authorized security testing only**.  
- Always obtain permission before testing any system.  
- Use responsibly and follow responsible disclosure.  
- The author assumes no liability for misuse.

---

## 👨‍💻 **Author**

**Muhammad Hassnain**  
- 🔗 [GitHub](https://github.com/darkfa1con)  
- 💼 [LinkedIn](https://linkedin.com/in/muhammad-hassnain)  

If you find Stork useful, consider giving it a ⭐ on GitHub!

---

## 📜 **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Happy Dorking! 🔍🕊️</b>
</p>
