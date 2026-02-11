import requests
import os

def get_config():
    url = "https://www.vpnbook.com/freevpn/wireguard-vpn"
    # پارامترهایی که خودت استخراج کردی
    data = {
        'server': 'us16',
        'port': '123',
        'action': 'generate'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("Connecting to VPNBook...")
    response = requests.post(url, data=data, headers=headers)
    
    if "[Interface]" in response.text:
        with open("wg0.conf", "w") as f:
            f.write(response.text)
        print("✅ Config saved successfully!")
    else:
        print("❌ Failed to get config. Cloudflare might be blocking.")
        # برای عیب‌یابی در لاگ‌های گیت‌هاب
        print(response.text[:500]) 

if __name__ == "__main__":
    get_config()
  
