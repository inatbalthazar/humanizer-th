# ตัวอย่าง 03: บทเกมแฟนตาซี (CSV)

- **บริบท:** เกม RPG เรื่องสมมติ ผู้เล่นเลือกเพศได้ แต่ไฟล์ไม่มีตัวแปรเพศ เอลารา (อัศวินหญิง ระแวงคนแปลกหน้า) แบรม (พ่อค้าแก่ อารมณ์ดี) และทหารยาม
- **ประเภทงาน:** บทเกม CSV 11 แถว มีบทพูด ชื่อไอเทม เควสต์ เสียงตะโกน และสอนเล่น
- **โหมด:** `แปล`

## ต้นฉบับ

```csv
ID,Speaker,Context,MaxLength,English,Thai
Q1_001,Elara,"First meeting, suspicious",60,"You're not from around here. Who sent you?",
Q1_002,Player,Reply option,40,"No one. I'm just passing through.",
Q1_003,Elara,,60,"Nobody just passes through the Whispering Woods.",
Q1_004,Bram,"Merchant, cheerful old man",80,"Ah, a customer! Take a look, friend. Best prices this side of the river!",
Q1_005,Bram,,80,"That'll be {0} gold. No haggling, my back can't take it.",
ITEM_001,,Item name,20,Frostbite Blade,
ITEM_001_DESC,,Item description,120,Deals {0} ice damage and slows enemies for {1} seconds.,
QUEST_001,,Quest title,30,A Stranger in the Woods,
QUEST_001_OBJ,,Quest objective,50,Talk to Elara at the forest gate (0/1),
BARK_001,Guard,Combat bark,20,Enemy spotted!,
TUT_001,,Tutorial,60,Press [Interact] to talk to characters.,
```

## คำแปล

```csv
ID,Speaker,Context,MaxLength,English,Thai
Q1_001,Elara,"First meeting, suspicious",60,"You're not from around here. Who sent you?",เจ้าไม่ใช่คนแถวนี้ ใครส่งมา
Q1_002,Player,Reply option,40,"No one. I'm just passing through.",ไม่มีใครส่งมา แค่ผ่านทางเฉยๆ
Q1_003,Elara,,60,"Nobody just passes through the Whispering Woods.",ป่ากระซิบไม่ใช่ทางที่ใครจะเดินผ่านเล่นๆ
Q1_004,Bram,"Merchant, cheerful old man",80,"Ah, a customer! Take a look, friend. Best prices this side of the river!",อ้า ลูกค้ามาแล้ว เชิญดูก่อนเลย ฝั่งนี้ของแม่น้ำไม่มีใครขายถูกกว่าข้าแล้ว
Q1_005,Bram,,80,"That'll be {0} gold. No haggling, my back can't take it.",ทั้งหมด {0} ทอง ห้ามต่อนะ ข้าแก่แล้ว เถียงไม่ไหว
ITEM_001,,Item name,20,Frostbite Blade,ดาบเยือกแข็ง
ITEM_001_DESC,,Item description,120,Deals {0} ice damage and slows enemies for {1} seconds.,สร้างความเสียหายน้ำแข็ง {0} หน่วย และทำให้ศัตรูช้าลง {1} วินาที
QUEST_001,,Quest title,30,A Stranger in the Woods,คนแปลกหน้าในป่า
QUEST_001_OBJ,,Quest objective,50,Talk to Elara at the forest gate (0/1),คุยกับเอลาราที่ประตูป่า (0/1)
BARK_001,Guard,Combat bark,20,Enemy spotted!,เจอศัตรู
TUT_001,,Tutorial,60,Press [Interact] to talk to characters.,กด [Interact] เพื่อคุยกับตัวละคร
```

## บันทึกการแปล

```text
- ตัวละคร: เอลาราและแบรมใช้ "ข้า" กับ "เจ้า" ตามแนวแฟนตาซี ผู้เล่นไม่มีสรรพนามและไม่มีคำลงท้าย เพราะเกมไม่รู้เพศผู้เล่น
- ชื่อเฉพาะ: Elara = เอลารา (ทับศัพท์) / Whispering Woods = ป่ากระซิบ (แปล เพราะชื่อมีความหมาย) ใช้แบบนี้ทั้งเกม
- Q1_004: ตัด "friend" เพราะไม่รู้เพศผู้เล่น และคำว่า "สหาย" ฟังเหมือนแปล
- Q1_005: มุก "my back can't take it" ปรับเป็น "ข้าแก่แล้ว เถียงไม่ไหว" ให้ได้มุกเรื่องแก่และขี้เกียจต่อราคาเหมือนเดิม
- TUT_001: คง [Interact] ไว้ เพราะเป็นตัวแปรชื่อปุ่ม
```

## ตรวจด้วยสคริปต์

```text
$ python3 skills/localize-th/scripts/check_translation.py game.csv
0 error(s), 0 warning(s)
```

ตัวแปร `{0}` `{1}` `[Interact]` ครบ และไม่มีแถวไหนยาวเกินคอลัมน์ MaxLength
