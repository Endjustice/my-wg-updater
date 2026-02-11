from DrissionPage import ChromiumPage, ChromiumOptions
import time

def get_config():
    co = ChromiumOptions()
    co.set_argument('--headless')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    co.set_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    page = ChromiumPage(co)
    
    try:
        print("🚀 Opening VPNBook...")
        page.get('https://www.vpnbook.com/freevpn/wireguard-vpn')
        
        # صبر هوشمند برای عبور از کلاودفلر و بارگذاری المنت‌ها
        print("⏳ Waiting for elements to load...")
        # صبر می‌کنیم تا فیلد انتخاب سرور در صفحه ظاهر شود (حداکثر 30 ثانیه)
        if page.ele('@name=server', timeout=30):
            print("✅ Elements found!")
            
            print("🔘 Selecting Server (us16) and Port (123)...")
            page.ele('@name=server').select.by_value('us16')
            time.sleep(1)
            page.ele('@name=port').select.by_value('123')
            
            print("💾 Clicking Generate...")
            # پیدا کردن دکمه بر اساس متن دقیق
            btn = page.ele('tag:button@@text():Generate')
            btn.click()
            
            print("⏳ Waiting for config to appear...")
            # صبر می‌کنیم تا متن کانفیگ (که با [Interface] شروع می‌شود) ظاهر شود
            for _ in range(15):
                time.sleep(2)
                if "[Interface]" in page.html:
                    config_text = page.ele('tag:body').text
                    # استخراج فقط بخش کانفیگ (اگر متون اضافه بود)
                    if "[Interface]" in config_text:
                        final_config = config_text[config_text.find("[Interface]"):].strip()
                        with open("wg0.conf", "w") as f:
                            f.write(final_config)
                        print("🎉 Victory! wg0.conf is ready.")
                        return
            
            print("❌ Timeout: Config didn't appear.")
        else:
            print("❌ Error: Could not find 'server' dropdown. Page structure might be different.")
            
    except Exception as e:
        print(f"⚠️ Exception occurred: {e}")
    finally:
        page.quit()

if __name__ == "__main__":
    get_config()
