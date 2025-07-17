import requests

proxy = {
    "http": "49.145.63.88:8082"
    
}

try:
    response = requests.post(
        "https://www.instagram.com/api/v1/web/login_page/",
        proxies=proxy,
        timeout=10
    )
    if "challenge_required" in response.text or "ip_block" in response.text:
        print("❌ Proxy engellenmiş (Instagram Kara Listesi)")
    else:
        print("✅ Proxy aktif")
except Exception as e:
    print(f"🚨 Hata: {str(e)} (Muhtemelen engelli)")