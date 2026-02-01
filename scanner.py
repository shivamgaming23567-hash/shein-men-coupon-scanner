import requests
import time

# ===== CONFIG =====
COUPONS = [
    "SVCT9QX6G4IYXNW",
    "SVC9R2P8ZA4JDAU"
]

HEADERS = {
    "user-agent": "Mozilla/5.0",
    "content-type": "application/json",
    "cookie": "PASTE_YOUR_SHEIN_COOKIE_HERE"
}

# ===== FILTERS =====
def is_mens_product(p):
    text = (
        p.get("title", "") +
        p.get("category_name", "") +
        p.get("url", "")
    ).lower()
    return any(k in text for k in ["men", "mens", "male"])

def is_not_shein_verse(p):
    text = (
        p.get("title", "") +
        p.get("category_name", "") +
        p.get("url", "")
    ).lower()
    return not any(k in text for k in ["verse", "sverse", "shein verse"])

def valid_mens_non_verse(p):
    return is_mens_product(p) and is_not_shein_verse(p)

# ===== COUPON CHECK =====
def coupon_works(goods_id, coupon):
    url = "https://api.shein.com/checkout/coupon/preview"
    payload = {
        "goods_id": goods_id,
        "coupon_code": coupon
    }
    r = requests.post(url, json=payload, headers=HEADERS, timeout=10)
    data = r.json()
    return data.get("discount_amount", 0) > 0

# ===== MAIN =====
def main():
    # abhi example product hai (test ke liye)
    products = [
        {
            "id": "123456",
            "title": "Men Solid T Shirt",
            "category_name": "Men Clothing",
            "url": "https://shein.com/men-shirt"
        }
    ]

    for p in products:
        if not valid_mens_non_verse(p):
            continue

        for cpn in COUPONS:
            try:
                if coupon_works(p["id"], cpn):
                    print("🔥 FOUND MEN NON-VERSE")
                    print(p["title"], cpn)
                    break
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()
