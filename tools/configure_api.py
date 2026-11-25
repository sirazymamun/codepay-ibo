"""Apply the repository API-URL.txt setting before compiling the player."""
from pathlib import Path
import sys
from urllib.parse import urlsplit

root = Path(__file__).resolve().parent.parent
url = (root / 'API-URL.txt').read_text(encoding='utf-8-sig').strip()
parts = urlsplit(url)
if (parts.scheme != 'https' or not parts.hostname or parts.path != '/activation/api.php'
    or parts.username or parts.password or parts.query or parts.fragment
    or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:/.-[]' for c in url)
    or 'YOUR_DOMAIN' in url or '_' in parts.hostname):
    sys.exit('Set API-URL.txt to your MAIN HTTPS activation endpoint.')
source = root / sys.argv[1]
template = 'https://YOUR_DOMAIN/activation/api.php'
text = source.read_text(encoding='utf-8')
if text.count(template) != 1:
    sys.exit('Expected exactly one activation endpoint in the source template.')
source.write_text(text.replace(template, url), encoding='utf-8')
