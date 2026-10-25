# humanizer-th

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg) ![version](https://img.shields.io/badge/version-0.1.2-green.svg)

A Claude skill that rewrites and edits Thai text so it reads like a native writer wrote it. It removes AI-writing tells and English-translation patterns while keeping the meaning, facts and the author's voice.

[อ่านภาษาไทย](README.md)

## Example

A LINE message to a coworker. (Thai original; the English gloss is below each block.)

**Before**

> สวัสดีครับพี่เมย์ ผมหวังว่าพี่จะสบายดีนะครับ ผมต้องการที่จะขอความช่วยเหลือจากพี่ในเรื่องหนึ่งครับ เนื่องจากในวันเสาร์ที่ 7 นี้ ผมมีความจำเป็นต้องเดินทางกลับต่างจังหวัดเพื่อไปร่วมงานบวชของน้องชาย ดังนั้น ผมจึงอยากสอบถามว่าพี่จะสามารถช่วยเข้ากะแทนผมในช่วงเวลา 13.00–21.00 น. ได้หรือไม่ครับ ทั้งนี้ ผมยินดีที่จะเข้ากะแทนพี่ในวันอื่นเป็นการตอบแทนครับ ขอบคุณพี่มากๆ สำหรับการพิจารณาครับ 🙏

*Gloss: "Hello P'May, I hope you are well. I would like to request your assistance on one matter. Due to the fact that this Saturday the 7th I am required to travel upcountry to attend my brother's ordination, therefore I would like to inquire whether you would be able to cover my shift... Furthermore, I am willing to cover your shift on another day in return. Thank you for your consideration."*

**After**

> พี่เมย์ครับ ขอรบกวนหน่อย เสาร์ที่ 7 นี้ผมต้องกลับต่างจังหวัดไปงานบวชน้องชาย พี่พอจะเข้ากะแทนผมช่วง 13.00–21.00 น. ได้ไหมครับ เดี๋ยวผมเข้ากะแทนพี่วันอื่นคืนให้ ขอบคุณมากครับ

*Gloss: "P'May, could I ask a favor? This Saturday the 7th I have to go home for my brother's ordination. Could you cover my 13:00–21:00 shift? I'll cover one of yours in return. Thanks a lot."*

The emoji at the end is removed. Numbers, names and the writer's polite particle "ครับ" are unchanged, and the text is less than half as long. More in [examples/](examples/).

## Why an English humanizer doesn't work for Thai

Existing humanizers (for example blader/humanizer) match English patterns. Thai differs in ways those rules cannot see:

- **Grammar:** Thai has no tense or articles, drops the subject freely, and marks politeness through particles instead of word choice. "Translated" Thai shows up as `ได้ทำการ`, `ถูก...โดย` (passive) and `ซึ่ง...ซึ่ง...` chains, not as English tells like "delve" or "tapestry".
- **Register:** Thai schools teach five register levels, from intimate to ceremonial, and readers notice when the wrong one is used. AI text often uses one register for every channel, such as government-letter Thai in a LINE message.
- **Particles and pronouns:** `ครับ`/`ค่ะ` carry the writer's gender, and putting them on every sentence, or switching between them, is itself a tell. Overusing `คุณ` ("you") is another.
- **Spacing and punctuation:** Thai uses spaces, not commas and full stops, to separate phrases and sentences. English-style punctuation is a tell, and so are emoji and "!", which Thai writers do not tack onto the end of messages.

## Features

**Three modes**

| Mode | Example request | Output |
|---|---|---|
| ตรวจ (check) | "Check which parts look AI-written" | List of findings with pattern codes and reasons. Does not edit. |
| เขียนใหม่ (rewrite, default) | "Rewrite this to sound natural" | Full new text plus a short summary of changes |
| แก้เฉพาะจุด (fix spots) | "Just fix the stiff parts" | Targeted fixes, original structure kept |

Mode and register names are in Thai because that is what the skill writes in its output.

**Four registers**, named after the register levels taught in Thai schools (the fifth, ceremonial, is out of scope):

| Register | Used for |
|---|---|
| กันเอง (intimate) | Chat with friends, family, close people |
| ไม่เป็นทางการ (informal) | Social posts, blogs, chat with a boss or coworkers |
| กึ่งทางการ (semi-formal) | Everyday work email, customer messages |
| ทางการ (formal) | Reports, official letters, academic writing |

If you don't say, the skill infers one and tells you which.

**What the skill never touches**

- Facts, numbers, dates, names, brands and prices never change.
- Quoted speech, links, code and proper nouns are left alone.
- No information is added that the original doesn't contain.
- The writer's `ครับ`/`ค่ะ` is preserved, never swapped.
- If the text already reads naturally, the skill says so and changes as little as possible.

## Install

### Claude.ai (zip upload)

1. Download `humanizer-th.zip` from [Releases](https://github.com/inatbalthazar/humanizer-th/releases), or build it with `scripts/build_zip.sh`.
2. Go to Settings → Capabilities → Skills and upload the zip.
3. Enable the skill and start a conversation.

### Claude Code

Copy the skill folder into `~/.claude/skills/`:

```bash
git clone https://github.com/inatbalthazar/humanizer-th.git
cp -r humanizer-th/skills/humanizer-th ~/.claude/skills/
```

## Usage

Paste Thai text with a request. Requests can be in Thai or English.

```text
Rewrite this naturally, informal register, for a Facebook post.
[paste text]
```

```text
Check which parts of this look AI-written.
[paste text]
```

## Patterns

29 patterns (TH01–TH29) in five categories: sentences, words, tone and register, structure and format, spacing and punctuation. Each has a code, why it reads as AI, a before/after, and **when not to fix it**. Most of them are what Thai grammar classes call ประโยคฟุ่มเฟือย (redundant sentences) and สำนวนต่างประเทศ (foreign-style phrasing); the rest are chatbot habits such as emoji and "!". Sources are listed at the end of patterns.md. See [patterns.md](skills/humanizer-th/references/patterns.md), [registers.md](skills/humanizer-th/references/registers.md) and [word-swaps.md](skills/humanizer-th/references/word-swaps.md).

## What this is not

**This skill is for making Thai easier to read. It is not an AI-detector evasion tool.** It is not designed to avoid detection, and it will never deliberately insert spelling or grammar mistakes to look human.

It is also not a translator; English-to-Thai translation is a different task.

## Limitations

- Thai text only.
- It is guidance Claude follows, not a program with deterministic output. Review the result before using it.
- What counts as "natural" depends on the writer and reader. Some patterns are matters of taste, so each one lists exceptions.
- There is no automated test suite yet (see [CHANGELOG](CHANGELOG.md)).

## Contributing

To propose a new pattern or a fix, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
