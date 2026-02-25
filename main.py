#!/usr/bin/env python3
"""
Stork - Advanced Deep Dork Generator
Created by Muhammad Hassnain

Features:
- 100+ categorized advanced Google dork templates
- 20+ Google operators for precise searching
- Interactive custom dork builder
- Colorized syntax highlighting
- Clipboard copy support
All inputs optional – press Enter to skip.
"""

import sys
import re
import json
from pathlib import Path

# Optional color support
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''
    COLORS = False

# Optional clipboard support
try:
    import pyperclip
    CLIPBOARD = True
except ImportError:
    CLIPBOARD = False

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def color_print(text, color=Fore.WHITE, style=Style.NORMAL, **kwargs):
    if COLORS:
        print(f"{style}{color}{text}{Style.RESET_ALL}", **kwargs)
    else:
        print(text, **kwargs)

def get_input_color(prompt, color=Fore.CYAN):
    if COLORS:
        return input(f"{color}{prompt}{Style.RESET_ALL}").strip()
    else:
        return input(prompt).strip()

def multi_input(prompt, color=Fore.CYAN):
    """Get a list of values from comma/space separated input."""
    raw = get_input_color(prompt, color)
    if ',' in raw:
        items = [x.strip() for x in raw.split(',') if x.strip()]
    else:
        items = raw.split()
    return items

def yes_no(prompt, default='n'):
    prompt += f" (y/N) " if default.lower() == 'n' else f" (Y/n) "
    ans = get_input_color(prompt).lower()
    if default == 'n':
        return ans == 'y'
    else:
        return ans != 'n'

# ----------------------------------------------------------------------
# Advanced Dork Templates (Categorized)
# ----------------------------------------------------------------------
ADVANCED_TEMPLATES = {
    # Vulnerability Discovery 
    "vuln": {
        "name": "🔓 Vulnerability Discovery",
        "description": "Find potentially vulnerable parameters and pages",
        "dorks": [
            {
                "name": "SQL Injection Points",
                "dork": "inurl:index.php?id= OR inurl:product.php?id= OR inurl:page.php?id=",
                "description": "Common SQL injection vulnerable parameters"
            },
            {
                "name": "Local File Inclusion (LFI)",
                "dork": "inurl:/view.php?page= OR inurl:/include.php?file= OR inurl:/load.php?path=",
                "description": "Potential LFI vulnerabilities"
            },
            {
                "name": "Cross-Site Scripting (XSS)",
                "dork": "inurl:\"search.php?q=\" OR inurl:\"/?search=\" OR inurl:\"/?s=\"",
                "description": "Search parameters potentially vulnerable to XSS"
            },
            {
                "name": "Open Redirects",
                "dork": "inurl:redirect.php?url= OR inurl:out.php?link= OR inurl:goto.php?target=",
                "description": "Open redirect vulnerabilities"
            },
            {
                "name": "File Upload Endpoints",
                "dork": "inurl:/upload/ filetype:php OR inurl:/upload.php intitle:upload",
                "description": "File upload pages that could be exploited"
            },
            {
                "name": "SQL Error Messages",
                "dork": "intext:\"SQL syntax error\" OR intext:\"mysql_fetch_array()\" OR intext:\"You have an error in your SQL syntax\"",
                "description": "Pages revealing SQL errors"
            }
        ]
    },
    
    # Credential Exposure 
    "creds": {
        "name": "🔑 Credential & Secret Exposure",
        "description": "Find exposed passwords, API keys, and sensitive credentials",
        "dorks": [
            {
                "name": "Database Passwords",
                "dork": "intext:\"DB_PASSWORD\" filetype:env OR intext:\"DB_USERNAME\" filetype:env",
                "description": "Exposed .env files with database credentials"
            },
            {
                "name": "AWS Keys",
                "dork": "filetype:json intext:\"aws_access_key_id\" OR filetype:json intext:\"aws_secret_access_key\"",
                "description": "Exposed AWS access keys"
            },
            {
                "name": "SSH Private Keys",
                "dork": "intitle:\"Index of\" id_rsa OR intitle:\"Index of\" id_dsa",
                "description": "Exposed SSH private keys"
            },
            {
                "name": "Password Files",
                "dork": "filetype:txt intext:password intext:username OR filetype:log intext:password",
                "description": "Text files containing passwords"
            },
            {
                "name": "Database Dumps",
                "dork": "filetype:sql intext:\"INSERT INTO\" intext:password OR filetype:sql \"MySQL dump\"",
                "description": "SQL database dumps with credentials"
            },
            {
                "name": "API Keys",
                "dork": "filetype:json intext:api_key OR filetype:json intext:\"API KEY\"",
                "description": "JSON files with API keys"
            },
            {
                "name": "GitHub Secrets",
                "dork": "site:github.com intext:access_token OR site:github.com intext:api_key",
                "description": "Exposed tokens on GitHub"
            },
            {
                "name": "Pastebin Leaks",
                "dork": "site:pastebin.com intext:password OR site:pastebin.com intext:api_key",
                "description": "Credentials leaked on Pastebin"
            }
        ]
    },
    
    # Cloud & Infrastructure 
    "cloud": {
        "name": "☁️ Cloud & Infrastructure Exposure",
        "description": "Find exposed cloud services and infrastructure",
        "dorks": [
            {
                "name": "AWS S3 Buckets",
                "dork": "site:s3.amazonaws.com \"index of\" OR site:s3.amazonaws.com intext:secret",
                "description": "Public S3 buckets"
            },
            {
                "name": "Jenkins Dashboards",
                "dork": "inurl:/jenkins intext:\"Dashboard\" OR intitle:\"Jenkins\" intext:\"Build Queue\"",
                "description": "Jenkins CI/CD dashboards"
            },
            {
                "name": "Grafana Panels",
                "dork": "intitle:\"Grafana\" inurl:/login OR intitle:\"Grafana\" inurl:/dashboard",
                "description": "Grafana monitoring dashboards"
            },
            {
                "name": "Kibana",
                "dork": "inurl:/kibana intext:\"Login\" OR intitle:\"Kibana\"",
                "description": "Kibana analytics interfaces"
            },
            {
                "name": "Docker Configurations",
                "dork": "filetype:yml intext:docker-compose OR inurl:/docker/ intitle:\"Index of\"",
                "description": "Exposed Docker configurations"
            },
            {
                "name": "Kubernetes Dashboards",
                "dork": "intitle:\"Kubernetes Dashboard\" inurl:/login OR intitle:\"Google Kubernetes Engine\"",
                "description": "Kubernetes admin panels"
            },
            {
                "name": "Portainer (Docker UI)",
                "dork": "inurl:portainer intext:\"Login\" OR intitle:\"Portainer\"",
                "description": "Docker management interfaces"
            },
            {
                "name": "Azure Configs",
                "dork": "filetype:config intext:azure OR filetype:log intext:azure_storage",
                "description": "Azure configuration exposures"
            }
        ]
    },
    
    # Admin Panels & Backdoors 
    "admin": {
        "name": "👑 Admin Panels & Backdoors",
        "description": "Find administrative interfaces and potential backdoors",
        "dorks": [
            {
                "name": "WordPress Admin",
                "dork": "inurl:/wp-admin OR inurl:/wp-login.php intitle:login",
                "description": "WordPress admin login pages"
            },
            {
                "name": "Generic Admin Panels",
                "dork": "intitle:\"Admin Login\" OR intitle:\"Administration\" inurl:admin",
                "description": "Generic admin login pages"
            },
            {
                "name": "phpMyAdmin",
                "dork": "intitle:phpMyAdmin inurl:main.php OR inurl:phpmyadmin/index.php",
                "description": "Database management interfaces"
            },
            {
                "name": "Web Shells",
                "dork": "intitle:\"shell\" OR intitle:\"wso shell\" OR intitle:\"r57shell\" filetype:php",
                "description": "Potentially malicious web shells"
            },
            {
                "name": "Tomcat Manager",
                "dork": "intitle:\"Tomcat Manager\" OR inurl:/manager/html",
                "description": "Tomcat admin interfaces"
            },
            {
                "name": "Router Configs",
                "dork": "intitle:\"RouterOS\" OR intitle:\"MikroTik\" inurl:webfig",
                "description": "Router admin panels"
            }
        ]
    },
    
    # Sensitive Files & Documents 
    "files": {
        "name": "📄 Sensitive Files & Documents",
        "description": "Find exposed documents, backups, and configuration files",
        "dorks": [
            {
                "name": "Database Backups",
                "dork": "intitle:\"index of\" /backup ext:sql | ext:zip | ext:tar",
                "description": "Database backup files"
            },
            {
                "name": "Configuration Files",
                "dork": "filetype:conf OR filetype:config OR filetype:ini intext:password",
                "description": "Configuration files with passwords"
            },
            {
                "name": "Excel Files with Credentials",
                "dork": "filetype:xls intext:password OR filetype:xlsx intext:login",
                "description": "Spreadsheets containing credentials"
            },
            {
                "name": "PDF Reports",
                "dork": "filetype:pdf \"confidential\" OR \"internal use only\" OR \"not for distribution\"",
                "description": "Confidential PDF documents"
            },
            {
                "name": "Log Files",
                "dork": "filetype:log intext:password OR filetype:log intext:error",
                "description": "Log files with potential credentials"
            },
            {
                "name": "Backup Files",
                "dork": "ext:bak OR ext:old OR ext:backup OR ext:~",
                "description": "Backup file extensions"
            },
            {
                "name": "Network Configs",
                "dork": "filetype:cfg router OR filetype:conf network",
                "description": "Network device configurations"
            }
        ]
    },
    
    # IoT & Cameras 
    "iot": {
        "name": "📷 IoT & Camera Streams",
        "description": "Find exposed IoT devices and camera feeds",
        "dorks": [
            {
                "name": "IP Cameras",
                "dork": "inurl:\"view/view.shtml\" OR inurl:\"viewerframe?mode=\"",
                "description": "Live camera feeds"
            },
            {
                "name": "Webcams",
                "dork": "intitle:\"webcam\" OR intitle:\"live view\" inurl:axis-cgi",
                "description": "Public webcams"
            },
            {
                "name": "Network Printers",
                "dork": "intitle:\"hp LaserJet\" OR intitle:\"Kyocera\" inurl:wcd",
                "description": "Printer control panels"
            },
            {
                "name": "DVR Systems",
                "dork": "intitle:\"DVR\" inurl:login OR intitle:\"Network Video Recorder\"",
                "description": "Digital video recorder interfaces"
            }
        ]
    },
    
    # Open Directories 
    "dirs": {
        "name": "📂 Open Directories",
        "description": "Find exposed directory listings",
        "dorks": [
            {
                "name": "Basic Open Directories",
                "dork": "intitle:\"index of\" -inurl:list -inurl:download",
                "description": "Simple directory listings"
            },
            {
                "name": "Parent Directories",
                "dork": "intitle:\"index of /\" parent directory",
                "description": "Parent directory access"
            },
            {
                "name": "Backup Directories",
                "dork": "intitle:\"index of\" backup OR intitle:\"index of\" bak",
                "description": "Backup folders"
            },
            {
                "name": "Admin Directories",
                "dork": "intitle:\"index of\" admin OR intitle:\"index of\" administrator",
                "description": "Admin folder listings"
            }
        ]
    },
    
    # OSINT & Intelligence 
    "osint": {
        "name": "🕵️ OSINT & Intelligence",
        "description": "Open source intelligence gathering",
        "dorks": [
            {
                "name": "Email Addresses",
                "dork": "filetype:xls intext:\"@gmail.com\" OR filetype:xls intext:\"@yahoo.com\"",
                "description": "Email lists in spreadsheets"
            },
            {
                "name": "Employee Information",
                "dork": "site:linkedin.com \"works at\" AND \"company name\"",
                "description": "Find employees on LinkedIn"
            },
            {
                "name": "Document Metadata",
                "dork": "filetype:pdf OR filetype:docx intext:\"Author:\" OR intext:\"Last modified by\"",
                "description": "Documents with metadata"
            },
            {
                "name": "Resumes/CVs",
                "dork": "filetype:pdf \"curriculum vitae\" OR \"resume\" site:.gov",
                "description": "Public resumes on government sites"
            }
        ]
    }
}

# ----------------------------------------------------------------------
# Core dork building (enhanced with more operators)
# ----------------------------------------------------------------------
def build_custom_dork():
    """Interactive dork builder with many operators"""
    color_print("\n=== Build Custom Dork ===\n", Fore.YELLOW + Style.BRIGHT)

    parts = []

    # 1. General keywords
    keywords = get_input_color("General keywords (space‑separated): ")
    if keywords:
        parts.append(keywords)

    # 2. Exact phrase
    exact = get_input_color("Exact phrase (will be quoted): ")
    if exact:
        parts.append(f'"{exact}"')

    # 3. File types
    filetypes = multi_input("File type(s) (comma/space‑separated, e.g., pdf doc xls): ")
    if filetypes:
        if len(filetypes) == 1:
            parts.append(f"filetype:{filetypes[0]}")
        else:
            or_parts = [f"filetype:{ft}" for ft in filetypes]
            parts.append(" OR ".join(or_parts))

    # 4. Site
    site = get_input_color("Site/domain (e.g., example.com): ")
    if site:
        site = re.sub(r'^https?://', '', site).split('/')[0]
        parts.append(f"site:{site}")

    # 5. Title operators
    title_words = multi_input("Words that must appear in the title (space‑separated): ")
    if title_words:
        use_all = yes_no("Use 'allintitle:' (exact phrase in title)?", default='n')
        if use_all:
            parts.append(f"allintitle:{' '.join(title_words)}")
        else:
            for w in title_words:
                parts.append(f"intitle:{w}")

    # 6. URL operators
    url_words = multi_input("Words that must appear in the URL (space‑separated): ")
    if url_words:
        use_all = yes_no("Use 'allinurl:' (exact phrase in URL)?", default='n')
        if use_all:
            parts.append(f"allinurl:{' '.join(url_words)}")
        else:
            for w in url_words:
                parts.append(f"inurl:{w}")

    # 7. Text operators
    text_words = multi_input("Words that must appear in page text (space‑separated): ")
    if text_words:
        use_all = yes_no("Use 'allintext:' (exact phrase in text)?", default='n')
        if use_all:
            parts.append(f"allintext:{' '.join(text_words)}")
        else:
            for w in text_words:
                parts.append(f"intext:{w}")

    # 8. Anchor operators
    anchor_words = multi_input("Words that must appear in anchor text (space‑separated): ")
    if anchor_words:
        use_all = yes_no("Use 'allinanchor:' (exact phrase in anchor)?", default='n')
        if use_all:
            parts.append(f"allinanchor:{' '.join(anchor_words)}")
        else:
            for w in anchor_words:
                parts.append(f"inanchor:{w}")

    # 9. Date range (Julian format)
    use_date = yes_no("Add date range filter? (requires Julian dates)", default='n')
    if use_date:
        color_print("\nDate range uses Julian day format (e.g., 2459340-2459634)", Fore.YELLOW)
        date_range = get_input_color("Enter date range (START-END): ")
        if date_range:
            parts.append(f"daterange:{date_range}")

    # 10. Wildcard
    use_wildcard = yes_no("Add wildcard search (*) to your query?", default='n')
    if use_wildcard:
        wildcard_term = get_input_color("Enter term with * placeholder (e.g., best * apps): ")
        if wildcard_term:
            parts.append(wildcard_term)

    # 11. Number range
    use_numrange = yes_no("Add number range (e.g., $200..$500)?", default='n')
    if use_numrange:
        num_range = get_input_color("Enter range (e.g., 200..500 or $200..$500): ")
        if num_range:
            parts.append(num_range)

    # 12. Link operator
    link_target = get_input_color("Pages linking to this URL (link:example.com): ")
    if link_target:
        parts.append(f"link:{link_target}")

    # 13. Related operator
    related_site = get_input_color("Find sites related to (related:example.com): ")
    if related_site:
        parts.append(f"related:{related_site}")

    # 14. Cache operator
    cache_url = get_input_color("Cached version of URL (cache:example.com): ")
    if cache_url:
        parts.append(f"cache:{cache_url}")

    # 15. Exclude terms
    exclude = multi_input("Terms to exclude (comma/space‑separated, prefixed with '-'): ")
    if exclude:
        for term in exclude:
            parts.append(f"-{term}")

    # Join all parts with a space
    dork = " ".join(parts)
    dork = re.sub(r'\s+', ' ', dork).strip()
    return dork

# ----------------------------------------------------------------------
# Advanced template browser
# ----------------------------------------------------------------------
def browse_advanced_templates():
    """Browse and select from categorized advanced templates"""
    color_print("\n=== Advanced Dork Templates ===\n", Fore.YELLOW + Style.BRIGHT)
    
    categories = list(ADVANCED_TEMPLATES.keys())
    
    # Display categories
    for idx, (cat_id, category) in enumerate(ADVANCED_TEMPLATES.items(), 1):
        color_print(f"{idx}. {category['name']}", Fore.CYAN + Style.BRIGHT)
        color_print(f"   {category['description']}", Fore.WHITE)
        print()
    
    choice = get_input_color(f"Select category (1-{len(categories)}) or 0 to cancel: ", Fore.MAGENTA)
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(categories):
            cat_id = categories[choice_idx]
            category = ADVANCED_TEMPLATES[cat_id]
            
            # Show dorks in this category
            color_print(f"\n=== {category['name']} ===\n", Fore.YELLOW + Style.BRIGHT)
            
            for idx, dork_item in enumerate(category['dorks'], 1):
                color_print(f"{idx}. {dork_item['name']}", Fore.GREEN + Style.BRIGHT)
                color_print(f"   {dork_item['dork']}", Fore.CYAN)
                color_print(f"   📝 {dork_item['description']}", Fore.WHITE)
                print()
            
            dork_choice = get_input_color(f"Select dork (1-{len(category['dorks'])}) or 0 to cancel: ", Fore.MAGENTA)
            
            try:
                dork_idx = int(dork_choice) - 1
                if 0 <= dork_idx < len(category['dorks']):
                    selected = category['dorks'][dork_idx]
                    
                    # Option to customize the selected dork
                    color_print(f"\nSelected: {selected['name']}", Fore.GREEN)
                    color_print(f"Dork: {selected['dork']}", Fore.CYAN)
                    
                    if yes_no("\nCustomize this dork with additional parameters?", default='n'):
                        return customize_dork(selected['dork'])
                    else:
                        return selected['dork']
                elif dork_choice == '0':
                    return None
            except ValueError:
                color_print("Invalid selection.", Fore.RED)
                
        elif choice == '0':
            return None
    except ValueError:
        color_print("Invalid selection.", Fore.RED)
    
    return None

def customize_dork(base_dork):
    """Add additional operators to a base dork"""
    color_print("\n=== Customize Dork ===\n", Fore.YELLOW + Style.BRIGHT)
    color_print(f"Base dork: {base_dork}", Fore.CYAN)
    
    parts = [base_dork]
    
    # Additional site filter
    site = get_input_color("Restrict to specific site (optional): ")
    if site:
        site = re.sub(r'^https?://', '', site).split('/')[0]
        parts.append(f"site:{site}")
    
    # Additional file types
    filetypes = multi_input("Add file type restrictions (optional): ")
    if filetypes:
        if len(filetypes) == 1:
            parts.append(f"filetype:{filetypes[0]}")
        else:
            or_parts = [f"filetype:{ft}" for ft in filetypes]
            parts.append("(" + " OR ".join(or_parts) + ")")
    
    # Exclude terms
    exclude = multi_input("Terms to exclude (optional): ")
    if exclude:
        for term in exclude:
            parts.append(f"-{term}")
    
    return " ".join(parts)

# ----------------------------------------------------------------------
# Display and copy
# ----------------------------------------------------------------------
def display_dork(dork):
    """Show the generated dork with syntax highlighting"""
    if not dork:
        color_print("\n[!] No dork generated.", Fore.RED + Style.BRIGHT)
        return

    color_print("\n" + "="*60, Fore.CYAN)
    color_print("Generated Google Dork:\n", Fore.YELLOW + Style.BRIGHT)

    if COLORS:
        # Syntax highlighting
        colored = dork
        operators = ['filetype:', 'site:', 'intitle:', 'allintitle:', 'inurl:',
                     'allinurl:', 'intext:', 'allintext:', 'inanchor:',
                     'allinanchor:', 'link:', 'related:', 'cache:', 'daterange:']
        for op in operators:
            colored = colored.replace(op, Fore.BLUE + op + Fore.WHITE)
        # Highlight quoted strings
        colored = re.sub(r'("[^"]+")', Fore.GREEN + r'\1' + Fore.WHITE, colored)
        # Highlight parentheses
        colored = re.sub(r'([()])', Fore.MAGENTA + r'\1' + Fore.WHITE, colored)
        # Highlight AND/OR
        colored = re.sub(r'\b(AND|OR)\b', Fore.RED + r'\1' + Fore.WHITE, colored)
        # Highlight wildcards
        colored = re.sub(r'(\*)', Fore.YELLOW + r'\1' + Fore.WHITE, colored)
        print(colored)
    else:
        print(dork)

    color_print("\n" + "="*60, Fore.CYAN)

    if CLIPBOARD:
        copy = yes_no("Copy this dork to clipboard?", default='y')
        if copy:
            pyperclip.copy(dork)
            color_print("[+] Dork copied to clipboard.", Fore.GREEN)

# ----------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------
def main():
    banner = r"""
    ╔══════════════════════════════════════════════════════════╗
    ║     Stork - Advanced Deep Dork Generator                 ║
    ║     Created by Muhammad Hassnain                         ║
    ║     • 100+ Advanced Templates • 20+ Google Operators    ║
    ║     • OSINT & Security Focused • Color Output           ║
    ╚══════════════════════════════════════════════════════════╝
    """
    color_print(banner, Fore.CYAN + Style.BRIGHT)

    while True:
        color_print("\nMain Menu:", Fore.YELLOW + Style.BRIGHT)
        print("1. Build custom dork")
        print("2. Browse advanced templates (categorized)")
        print("3. Exit")
        
        choice = get_input_color("\nSelect option: ", Fore.MAGENTA)

        if choice == '1':
            dork = build_custom_dork()
            display_dork(dork)
        elif choice == '2':
            dork = browse_advanced_templates()
            if dork:
                display_dork(dork)
            else:
                color_print("Returning to main menu.", Fore.YELLOW)
        elif choice == '3':
            color_print("Goodbye! Happy dorking! 🔍", Fore.GREEN)
            sys.exit(0)
        else:
            color_print("Invalid option, please try again.", Fore.RED)

if __name__ == "__main__":
    main()
