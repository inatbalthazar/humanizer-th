# ตัวอย่าง 02: ข้อความในแอปสั่งอาหาร (JSON)

- **บริบท:** แอปสั่งอาหารเดลิเวอรีเรื่องสมมติ ไฟล์ภาษาของ react-intl ที่ใช้รูปแบบพหูพจน์แบบ ICU
- **ประเภทงาน:** ข้อความ UI ไฟล์ JSON 14 key
- **ระดับภาษา:** `ไม่เป็นทางการ`
- **โหมด:** `แปล`

## ต้นฉบับ

```json
{
  "home": {
    "title": "Home",
    "search_placeholder": "Search for restaurants or dishes",
    "greeting": "Good evening, {name}! What are you craving?"
  },
  "cart": {
    "title": "Your cart",
    "items": "{count, plural, one {# item} other {# items}}",
    "checkout": "Proceed to checkout",
    "empty": "Your cart is empty. Let's find something delicious!"
  },
  "order": {
    "placed": "Your order has been placed successfully!",
    "eta": "Estimated delivery: {minutes} min",
    "track": "Track your order"
  },
  "errors": {
    "network": "Unable to connect. Please check your internet connection and try again.",
    "payment_failed": "Payment failed. Please try another payment method.",
    "required": "This field is required."
  },
  "promo": {
    "invalid": "The promo code \"{code}\" is invalid or has expired."
  }
}
```

## คำแปล

```json
{
  "home": {
    "title": "หน้าแรก",
    "search_placeholder": "ค้นหาร้านหรือเมนู",
    "greeting": "เย็นนี้กินอะไรดี {name}"
  },
  "cart": {
    "title": "ตะกร้า",
    "items": "{count, plural, one {# รายการ} other {# รายการ}}",
    "checkout": "ชำระเงิน",
    "empty": "ตะกร้ายังว่างอยู่ ไปหาของอร่อยกัน"
  },
  "order": {
    "placed": "สั่งอาหารแล้ว",
    "eta": "ถึงในประมาณ {minutes} นาที",
    "track": "ติดตามคำสั่งซื้อ"
  },
  "errors": {
    "network": "เชื่อมต่อไม่ได้ ตรวจอินเทอร์เน็ตแล้วลองอีกครั้ง",
    "payment_failed": "ชำระเงินไม่สำเร็จ ลองใช้วิธีชำระเงินอื่น",
    "required": "จำเป็นต้องกรอก"
  },
  "promo": {
    "invalid": "โค้ด \"{code}\" ใช้ไม่ได้หรือหมดอายุแล้ว"
  }
}
```

## บันทึกการแปล

```text
- home.greeting: ย้าย {name} ไปท้ายประโยคให้เป็นลำดับคำไทย และตัด "Good evening" ที่แปลตรงแล้วแข็ง ถ้าข้อความนี้ขึ้นทุกช่วงเวลา ไม่ใช่เฉพาะตอนเย็น บอกได้ จะเปลี่ยนเป็น "วันนี้กินอะไรดี {name}"
- cart.items: ภาษาไทยมีรูปพหูพจน์เดียว แต่คง branch one ไว้ตามต้นฉบับ ใส่ข้อความเดียวกัน
```

## จุดที่เลี่ยง

| ต้นฉบับ | แปลแข็ง | ที่ใช้ | รหัส |
|---|---|---|---|
| Your cart | ตะกร้าของคุณ | ตะกร้า | TH14 |
| Proceed to checkout | ดำเนินการต่อไปยังการชำระเงิน | ชำระเงิน | `ui.md` ปุ่ม |
| ...delicious! | ...อร่อยๆ กันเถอะ! | ไปหาของอร่อยกัน | TH29 |
| Your order has been placed successfully! | คำสั่งซื้อของคุณได้รับการดำเนินการเรียบร้อยแล้ว! | สั่งอาหารแล้ว | TH04, TH29 |
| Unable to connect. | ไม่สามารถเชื่อมต่อได้ | เชื่อมต่อไม่ได้ | TH21 |
| Payment failed. | การชำระเงินล้มเหลว | ชำระเงินไม่สำเร็จ | TH02 |
| Please... | กรุณา... | (ละ) | LT10 |

## ตรวจด้วยสคริปต์

```text
$ python3 skills/localize-th/scripts/check_translation.py en.json th.json
0 error(s), 0 warning(s)
```

key ครบและอยู่ลำดับเดิม ตัวแปร `{name}` `{minutes}` `{code}` และโครง ICU `{count, plural, ...}` อยู่ครบทุกตัว
