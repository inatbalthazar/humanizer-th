# ทดสอบด้วยมือ v0.3.0

ทดสอบ skill ใหม่สองตัว คือ `localize-th` และ `script-th` โดยให้ Claude ทำตาม SKILL.md กับโจทย์ที่แต่งขึ้นเอง ผลอยู่ใน `examples/localize-th/` และ `examples/script-th/`

## localize-th

| โจทย์ | ไฟล์ | ผล `check_translation.py` | ตรวจด้วยตา |
|---|---|---|---|
| ซับซีรีส์ตลก 8 บล็อก | `examples/localize-th/01-subtitle-srt.md` | 0 error, 0 warning | สรรพนามคงที่ทั้งฉาก ไม่มีคำอุทานแปลตรง (LT05) |
| แอปสั่งอาหาร 14 key | `examples/localize-th/02-app-ui-json.md` | 0 error, 0 warning | ตัวแปรและโครง ICU ครบ ย้าย `{name}` ไปท้ายประโยคได้ |
| บทเกมแฟนตาซี 11 แถว | `examples/localize-th/03-game-dialogue-csv.md` | 0 error, 0 warning | ผู้เล่นไม่มีคำลงท้ายเพศ ชื่อเฉพาะตัดสินแบบเดียวทั้งไฟล์ |

สคริปต์ `check_translation.py` มีชุดทดสอบอัตโนมัติ 12 กรณีใน `tests/test_check_translation.py` (SRT, VTT, ASS, JSON, .strings, Android XML, PO, CSV, XLIFF) รันใน CI ทุกครั้ง

## script-th

| โจทย์ | ไฟล์ | ตรวจ |
|---|---|---|
| เขียนบทจากไอเดีย | `examples/script-th/01-write-short-drama.md` | มีตะขอในบรรทัดแรก จบแบบค้าง ตัวละคร 3 คนพูดต่างกัน ไม่มี "!" |
| เกลาบทที่ AI เขียน | `examples/script-th/02-polish-ai-script.md` | ข้อมูลในบทเดิมอยู่ครบทั้ง 6 ข้อ ลำดับผู้พูดเดิม |
| พรอมต์และบทพากย์ | `examples/script-th/03-shot-prompts-and-voice.md` | บทแต่ละช็อตไม่เกินจำนวนพยางค์ บทยาว 33 พยางค์ถูกแบ่งเป็นสองช็อต คำบรรยายหน้าตาเหมือนกันทุกช็อต |

## ยังไม่ได้ทดสอบ

- เอาพรอมต์ไปสร้างวิดีโอจริงในเว็บสร้างวิดีโอ AI
- เอาบทพากย์ไปให้เสียง AI ภาษาไทยอ่านจริง
- ค่าประมาณ 4 พยางค์ต่อวินาทีใน `voice.md` เป็นจุดเริ่มต้น ยังไม่ได้วัดกับเสียง AI ตัวใดตัวหนึ่ง
- ใช้ skill กับ AI ตัวอื่นที่ไม่ใช่ Claude
