import urllib.request
import json

TOKEN = "8769762592:AAEuc3FqaVMISQOSEisXm0uS4MvbZ9f30HA"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
