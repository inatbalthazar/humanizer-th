# ตัวอย่าง 03: พรอมต์ทีละช็อตและบทพากย์

- **โจทย์จากผู้ใช้:** "เอาฉากแรกของตอนที่ 1 (จากตัวอย่าง 01) ไปทำพรอมต์ คลิปละไม่เกิน 8 วินาที จะให้ AI พากย์เสียงไทยแยก แล้วทำลิปซิงก์"
- **โหมด:** `ทำพรอมต์` แล้วต่อด้วย `เตรียมบทพากย์`
- **วิธีใส่เสียง:** ข. วิดีโอเงียบ + เสียง AI + ลิปซิงก์

## คำบรรยายหน้าตาที่ล็อกไว้

```text
PA JAEW: a Thai woman in her mid-50s, short permed black hair, round face, gold-rimmed glasses, red apron over a floral blouse.
POOM: a Thai man in his early 30s, neat short hair, plain light-blue shirt with an employee lanyard, expensive steel wristwatch.
```

## การ์ดช็อต

```text
ช็อต 1 | ฉาก 1 | 8 วินาที | ผู้พูด: ป้าแจ๋ว

พรอมต์:
Vertical 9:16, cinematic, bright midday light. PA JAEW: a Thai woman in her mid-50s, short permed black hair, round face, gold-rimmed glasses, red apron over a floral blouse. Medium shot at a chicken rice stall on a Bangkok sidewalk in front of an office tower, steel cart with boiled chickens hanging behind glass. She chops chicken on a wooden board without looking up, a small knowing smile. She is speaking, mouth moving naturally. Street ambience, no music. No subtitles, no captions, no on-screen text.

บทพูด: ป้าแจ๋ว: ไม่ใส่หนัง น้ำจิ้มแยก ซุปไม่เอาฟัก วันนี้ท่านประธานจะเอาอะไรเพิ่มมั้ยจ๊ะ (22 พยางค์)
```

```text
ช็อต 2 | ฉาก 1 | 5 วินาที | ผู้พูด: ภูมิ

พรอมต์:
Vertical 9:16, cinematic, bright midday light. POOM: a Thai man in his early 30s, neat short hair, plain light-blue shirt with an employee lanyard, expensive steel wristwatch. Close-up, sitting on a red plastic stool at a Bangkok street food stall. He freezes, then glances left and right nervously. He is speaking, mouth moving naturally. Street ambience, no music. No subtitles, no captions, no on-screen text.

บทพูด: ภูมิ: ป้าพูดอะไรครับ (5 พยางค์)
```

```text
ช็อต 3 | ฉาก 1 | 5 วินาที | ผู้พูด: ป้าแจ๋ว

พรอมต์:
Vertical 9:16, cinematic, bright midday light. PA JAEW: a Thai woman in her mid-50s, short permed black hair, round face, gold-rimmed glasses, red apron over a floral blouse. Medium close-up at the chicken rice stall. She looks up, smiles, and slides a plate of chicken rice across the counter. She is speaking, mouth moving naturally. Street ambience, no music. No subtitles, no captions, no on-screen text.

บทพูด: ป้าแจ๋ว: ป้าขายตรงนี้มายี่สิบปี (8 พยางค์)
```

```text
ช็อต 4 | ฉาก 1 | 8 วินาที | ผู้พูด: ป้าแจ๋ว

พรอมต์:
Vertical 9:16, cinematic, bright midday light. PA JAEW: a Thai woman in her mid-50s, short permed black hair, round face, gold-rimmed glasses, red apron over a floral blouse. Over-the-shoulder shot from behind a man's shoulder, focus on her face. She raises an eyebrow and nods toward the man's wrist, teasing. She is speaking, mouth moving naturally. Street ambience, no music. No subtitles, no captions, no on-screen text.

บทพูด: ป้าแจ๋ว: ใครใส่นาฬิกาเรือนละล้าน มานั่งกินข้าวสี่สิบห้าบาททุกวัน ป้าก็ต้องสงสัยมั่งแหละ (25 พยางค์)
หมายเหตุ: บทเดิมของป้าแจ๋วยาว 33 พยางค์ เกินช็อต 8 วินาที (SC08) จึงแบ่งเป็นช็อต 3 กับ 4
```

```text
ช็อต 5 | ฉาก 1 | 5 วินาที | ผู้พูด: ภูมิ

พรอมต์:
Vertical 9:16, cinematic, bright midday light. POOM: a Thai man in his early 30s, neat short hair, plain light-blue shirt with an employee lanyard, expensive steel wristwatch. Close-up on his hands as he pulls his shirt sleeve down over the watch, then tilt up to his face, trying to look calm. He is speaking, mouth moving naturally. Street ambience, no music. No subtitles, no captions, no on-screen text.

บทพูด: ภูมิ: ของปลอมครับ (4 พยางค์)
```

## บทพากย์

```text
| ช็อต | ตัวละคร | ทิศทางเสียง | ข้อความให้ AI อ่าน | ข้อความขึ้นซับ | พยางค์ / เวลา |
|---|---|---|---|---|---|
| 1 | ป้าแจ๋ว | อารมณ์ดี พูดเร็ว เหมือนท่องเมนูประจำ | ไม่ใส่หนัง น้ำจิ้มแยก ซุปไม่เอาฟัก วันนี้ท่านประธานจะเอาอะไรเพิ่มมั้ยจ๊ะ | ไม่ใส่หนัง น้ำจิ้มแยก ซุปไม่เอาฟัก วันนี้ท่านประธานจะเอาอะไรเพิ่มมั้ยจ๊ะ | 22 / 8 วินาที |
| 2 | ภูมิ | เบา ตกใจ แต่พยายามนิ่ง | ป้าพูดอะไรครับ | ป้าพูดอะไรครับ | 5 / 5 วินาที |
| 3 | ป้าแจ๋ว | ยิ้มในเสียง ช้าลง | ป้าขายตรงนี้มายี่สิบปี | ป้าขายตรงนี้มา 20 ปี | 8 / 5 วินาที |
| 4 | ป้าแจ๋ว | แซว เน้นคำว่า ล้าน | ใครใส่นาฬิกาเรือนละล้าน มานั่งกินข้าวสี่สิบห้าบาททุกวัน ป้าก็ต้องสงสัยมั่งแหละ | ใครใส่นาฬิกาเรือนละล้าน มานั่งกินข้าว 45 บาททุกวัน ป้าก็ต้องสงสัยมั่งแหละ | 25 / 8 วินาที |
| 5 | ภูมิ | เรียบ เร็ว อยากจบเรื่อง | ของปลอมครับ | ของปลอมครับ | 4 / 5 วินาที |

หมายเหตุ:
- ช่องให้ AI อ่าน เขียนตัวเลขเป็นคำ ช่องซับใช้ตัวเลข เพื่อให้อ่านเร็ว
- เสียงที่แนะนำ: ป้าแจ๋วใช้เสียงผู้หญิงวัยกลางคน ภูมิใช้เสียงผู้ชายวัยทำงาน ทุ้ม ใช้เสียงเดิมทุกตอน
- ฟังช็อต 4 ก่อน ถ้าพูดเร็วเกิน ตัด "ป้าก็" ออกได้โดยความหมายไม่เปลี่ยน
```
