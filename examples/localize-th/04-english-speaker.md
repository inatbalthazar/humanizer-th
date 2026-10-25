# ตัวอย่าง 04: ผู้ใช้ที่อ่านไทยไม่ออก แปลเมนูเกม (JSON)

- **บริบท:** นักพัฒนาเกมอินดี้ต่างชาติ เกมเรื่องสมมติ สั่งเป็นภาษาอังกฤษ และอ่านภาษาไทยไม่ออก
- **ประเภทงาน:** ข้อความ UI เกม ไฟล์ JSON 12 key
- **ระดับภาษา:** `ไม่เป็นทางการ`
- **โหมด:** `แปล`
- **ภาษาของคำตอบ:** คำแปลเป็นภาษาไทย บันทึกเป็นภาษาอังกฤษตามภาษาของคำขอ และแนบคำแปลกลับ เพราะงานไม่เกิน 30 key

## คำขอ

> Translate our game menu strings into Thai. I don't read Thai, so please tell me what you changed and why.

## ต้นฉบับ

```json
{
  "menu.continue": "Continue",
  "menu.new_game": "New Game",
  "menu.settings": "Settings",
  "menu.quit_confirm": "Are you sure you want to quit? Unsaved progress will be lost.",
  "shop.buy": "Buy",
  "shop.not_enough_gold": "You need {amount} more gold.",
  "shop.purchased": "{item} added to your bag.",
  "quest.complete": "Quest complete!",
  "quest.reward": "Reward: {xp} XP",
  "save.slot": "Slot {number} – {date}",
  "settings.subtitles": "Subtitles",
  "settings.language_restart": "Restart the game to apply the new language."
}
```

## คำตอบ

```json
{
  "menu.continue": "เล่นต่อ",
  "menu.new_game": "เกมใหม่",
  "menu.settings": "ตั้งค่า",
  "menu.quit_confirm": "ออกจากเกมไหม ความคืบหน้าที่ยังไม่ได้บันทึกจะหายไป",
  "shop.buy": "ซื้อ",
  "shop.not_enough_gold": "ทองไม่พอ ขาดอีก {amount}",
  "shop.purchased": "เก็บ {item} ลงกระเป๋าแล้ว",
  "quest.complete": "เควสต์สำเร็จ",
  "quest.reward": "รางวัล: {xp} XP",
  "save.slot": "ช่อง {number} – {date}",
  "settings.subtitles": "คำบรรยาย",
  "settings.language_restart": "ปิดเกมแล้วเปิดอีกครั้งเพื่อใช้ภาษาใหม่"
}
```

```text
---
Translation notes:
- Type: game UI strings, JSON, 12 keys. All keys and placeholders ({amount}, {item}, {xp}, {number}, {date}) are unchanged.
- No "you" and no polite particles. Thai game menus talk to the player without pronouns, so "You need {amount} more gold" became "Not enough gold, {amount} short".
- No "!" in "Quest complete". Thai UI rarely uses exclamation marks; the words carry the tone.
- settings.language_restart: I avoided "เริ่มเกมใหม่" ("restart the game"), because it reads almost the same as your New Game button "เกมใหม่". The Thai says "close the game and open it again" instead.
- Terms follow common Thai game usage: "เควสต์" (quest), "ทอง" (gold), "กระเป๋า" (bag), "คำบรรยาย" (subtitles, the word Thai streaming apps use). "XP" stays in English, which Thai players know. Say if you prefer "ค่าประสบการณ์" (experience points).
- {date}: if your engine formats dates by locale, th-TH may show the Buddhist year (2569 instead of 2026). Check which one you want.

Back-translation:
| Key | Thai | Back-translation |
|---|---|---|
| menu.continue | เล่นต่อ | Keep playing |
| menu.new_game | เกมใหม่ | New game |
| menu.settings | ตั้งค่า | Settings |
| menu.quit_confirm | ออกจากเกมไหม ความคืบหน้าที่ยังไม่ได้บันทึกจะหายไป | Quit the game? Progress that hasn't been saved will be lost. |
| shop.buy | ซื้อ | Buy |
| shop.not_enough_gold | ทองไม่พอ ขาดอีก {amount} | Not enough gold, {amount} short |
| shop.purchased | เก็บ {item} ลงกระเป๋าแล้ว | Put {item} in the bag (done) |
| quest.complete | เควสต์สำเร็จ | Quest succeeded |
| quest.reward | รางวัล: {xp} XP | Reward: {xp} XP |
| save.slot | ช่อง {number} – {date} | Slot {number} – {date} |
| settings.subtitles | คำบรรยาย | Subtitles |
| settings.language_restart | ปิดเกมแล้วเปิดอีกครั้งเพื่อใช้ภาษาใหม่ | Close the game and open it again to use the new language |
```

## ทำไมคำตอบเป็นแบบนี้

- **บันทึกเป็นภาษาอังกฤษ:** ผู้ใช้สั่งเป็นภาษาอังกฤษ บันทึก หัวข้อ และคำอธิบายจึงเป็นภาษาอังกฤษ คำไทยที่ยกมาอ้างคงเป็นภาษาไทยแล้วบอกความหมายในวงเล็บ
- **มีคำแปลกลับ:** ผู้ใช้อ่านไทยไม่ออก และงานมี 12 key ไม่เกิน 30 จึงแนบท้ายคำตอบ คำแปลกลับแปลตามภาษาไทยจริง เช่น "Quest succeeded" ไม่ใช่ "Quest complete" ตามต้นฉบับ ผู้ใช้จะได้เห็นว่าภาษาไทยพูดว่าอะไรจริงๆ
- **คำแปลกลับไม่อยู่ในไฟล์:** ไฟล์ JSON มีแต่ภาษาไทย เอาไปใช้ได้ทันที

## จุดที่เลี่ยง

| ต้นฉบับ | แปลแบบทั่วไป | ที่ใช้ | เหตุผล |
|---|---|---|---|
| Are you sure you want to quit? | คุณแน่ใจหรือไม่ว่าคุณต้องการออก? | ออกจากเกมไหม | LT01 คำถามยืนยันใน UI ไทยถามสั้นๆ ไม่มี "คุณ" และไม่ใช้ "?" |
| You need {amount} more gold. | คุณต้องการทองเพิ่มอีก {amount} | ทองไม่พอ ขาดอีก {amount} | LT02 "You need" ในที่นี้ไม่ได้แปลว่า "ต้องการ" |
| {item} added to your bag. | {item} ถูกเพิ่มลงในกระเป๋าของคุณ | เก็บ {item} ลงกระเป๋าแล้ว | TH04 "ถูก" แบบแปล และ TH14 "ของคุณ" |
| Restart the game to apply the new language. | รีสตาร์ทเกมเพื่อใช้ภาษาใหม่ หรือ เริ่มเกมใหม่... | ปิดเกมแล้วเปิดอีกครั้งเพื่อใช้ภาษาใหม่ | "เริ่มเกมใหม่" สับสนกับปุ่ม New Game |

## ตรวจด้วยสคริปต์

```text
$ python3 skills/localize-th/scripts/check_translation.py en.json th.json
0 error(s), 0 warning(s)
```

key ครบและอยู่ลำดับเดิม ตัวแปร `{amount}` `{item}` `{xp}` `{number}` `{date}` อยู่ครบทุกตัว
