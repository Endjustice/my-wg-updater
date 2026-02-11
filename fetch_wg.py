from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os

def get_config():
    # تنظیمات مرورگر برای اجرا در محیط گیت‌هاب
    co = ChromiumOptions()
    co.set_argument('--headless')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    
    page = ChromiumPage(co)
    
    try:
        print("🚀 Opening VPNBook...")
        page.get('https://www.vpnbook.com/freevpn/wireguard-vpn')
        
        # صبر می‌کنیم تا چالش کلاودفلر رد شود
        time.sleep(10) 
        
        print("🔘 Selecting Server and Port...")
        # کلیک روی دکمه تولید (بر اساس اطلاعاتی که خودت استخراج کردی)
        # در اینجا مستقیم از API داخلی صفحه برای ارسال فرم استفاده می‌کنیم
        page.run_js("document.querySelector('select[name=\"server\"]').value = 'us16';")
        page.run_js("document.querySelector('select[name=\"port\"]').value = '123';")
        
        print("💾 Clicking Generate...")
        page.ele('@@tag()=button@@text()=Generate').click()
        
        # صبر برای دریافت پاسخ
        time.sleep(5)
        
        # محتوای صفحه را چک می‌کنیم
        content = page.html
        if "[Interface]" in content:
            # پاک کردن تگ‌های HTML اضافی اگر وجود داشت (فقط متن کانفیگ)
            config_text = page.ele('tag:body').text
            with open("wg0.conf", "w") as f:
                f.write(config_text)
            print("✅ Success! wg0.conf created.")
        else:
            print("❌ Config not found in page content.")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        page.quit()

if __name__ == "__main__":
    get_config()
            
