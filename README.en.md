# humanizer-th

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg) ![version](https://img.shields.io/badge/version-0.5.0-green.svg)

A set of Thai-language [Agent Skills](https://agentskills.io). Translate subtitles, games, apps and websites into Thai that doesn't read like a translation, write and polish dialogue for AI-generated short dramas and Thai AI voice-over, and edit AI-written Thai so it reads like a native writer wrote it.

Works with Claude, ChatGPT, Gemini, Codex, GitHub Copilot, Cursor and any tool that supports Agent Skills. Tools without skill support can use a single bundled prompt file instead.

[อ่านภาษาไทย](README.md)

## The skills

| Skill | What it does | Example request |
|---|---|---|
| **localize-th** | English to Thai for subtitles, dubbing scripts, app and website strings, and games | "แปลซับนี้เป็นไทย" / "Translate this strings file into Thai" |
| **script-th** | Writes and polishes Thai dialogue for AI short dramas, per-shot video prompts, and TTS-ready voice scripts | "เขียนบทละครสั้นเรื่อง..." / "Polish this script" |
| **humanizer-th** | Edits AI-written Thai posts, emails and chat messages, and writes in the user's own voice from samples of their past writing | "เกลาให้หน่อย" / "เขียนให้เหมือนที่เราเขียน" |

Install once and the agent picks the right skill for each request.

```bash
npx humanizer-th
```

No terminal, or using ChatGPT or Gemini? See [Install](#install).

## If you don't read Thai

- **Ask in English.** The Thai output stays Thai, and everything that explains it (translation notes, change summaries, questions) comes back in English. Thai words quoted in the notes get their meaning in brackets.
- **Back-translations.** For short jobs, up to about 30 lines, subtitle blocks or strings, the agent adds a table that says in plain English what the Thai actually says, so you can check the meaning. For longer files, ask for one. Back-translations never go into the translated file.
- **Example:** [game menu strings for a developer who doesn't read Thai](examples/localize-th/04-english-speaker.md).
- **Still get a native review.** Have a Thai speaker read anything you publish.

## localize-th: subtitles, games, apps and websites

| Source | Typical machine translation | localize-th |
|---|---|---|
| Oh no. (subtitle) | โอ้ไม่ ("oh no", literal) | ซวยแล้ว ("I'm in trouble") |
| Payment failed. (app) | การชำระเงินล้มเหลว ("the payment has failed") | ชำระเงินไม่สำเร็จ ("payment didn't go through") |
| Your cart (app) | ตะกร้าของคุณ ("your cart") | ตะกร้า ("cart"; Thai UI drops "your") |
| No haggling, my back can't take it. (game) | literal joke that falls flat | ห้ามต่อนะ ข้าแก่แล้ว เถียงไม่ไหว ("no haggling, I'm too old to argue") |

- **Files stay valid:** subtitle timings and block numbers, keys, placeholders (`{name}`, `%s`, `[PlayerName]`, ICU plurals) and tags are kept exactly.
- **Readable subtitles:** at most 35 characters per line, 2 lines, about 20 characters per second, line breaks on word boundaries (Thai has no spaces between words). The defaults follow Netflix's Thai timed-text guide and can be overridden.
- **Characters sound like people:** pronouns and particles are chosen per relationship and kept consistent. English "I" and "you" have a dozen Thai equivalents.
- **Consistent terms:** follows your glossary, or a built-in glossary of standard Thai UI and game terms with Royal Institute spellings.
- **Checker script:** `skills/localize-th/scripts/check_translation.py` compares a translation with its source (SRT, VTT, ASS, JSON, ARB, PO, XLIFF, `.strings`, Android XML, CSV) and reports broken timings, missing keys or placeholders, long lines and reading speed. Agents that can run commands run it themselves.

```bash
python3 skills/localize-th/scripts/check_translation.py en.srt th.srt
```

Examples: [SRT subtitles](examples/localize-th/01-subtitle-srt.md), [app JSON](examples/localize-th/02-app-ui-json.md), [game CSV](examples/localize-th/03-game-dialogue-csv.md), [for a developer who doesn't read Thai](examples/localize-th/04-english-speaker.md).

## script-th: AI short dramas and Thai voice-over

Four modes: write a script from an idea, polish an existing script without changing the story, turn it into per-shot prompts for AI video tools, and prepare a voice script that Thai TTS reads correctly (numbers as words, unambiguous spellings, pauses and voice direction).

- Character sheets with fixed English visual descriptions, copied verbatim into every shot prompt for consistency.
- Lines sized to the clip length using a syllable estimate, with long lines split across shots.
- Twelve AI-dialogue tells (SC01–SC12), such as characters naming their feelings, exposition dumps, stock lines from short dramas and everyone sounding the same.
- Three ways to add Thai speech (native audio from the video model, separate TTS with lip-sync, or narration and subtitles), because many video models still speak Thai poorly.

Examples: [write from an idea](examples/script-th/01-write-short-drama.md), [polish an AI script](examples/script-th/02-polish-ai-script.md), [shot prompts and voice script](examples/script-th/03-shot-prompts-and-voice.md).

## humanizer-th: AI-written Thai

Four modes (ตรวจ check, เขียนใหม่ rewrite, แก้เฉพาะจุด fix spots, เลียนสไตล์ match style) across the four registers taught in Thai schools: กันเอง (intimate), ไม่เป็นทางการ (informal), กึ่งทางการ (semi-formal) and ทางการ (formal). It checks 29 patterns (TH01–TH29), most of which Thai grammar classes call ประโยคฟุ่มเฟือย (redundant sentences) and สำนวนต่างประเทศ (foreign-style phrasing). See [patterns.md](shared/patterns.md) and [examples/humanizer-th/](examples/humanizer-th/).

### Writing in your own voice (เลียนสไตล์)

Natural Thai is not the same as your Thai. Send three or more pieces you wrote yourself, plus an AI draft or just a brief, and the skill builds a style profile: what you call yourself, where you put `ครับ`/`ค่ะ`, how often you break lines, how you open and close, how you write times and prices. It then writes the new text that way.

- Content comes only from the draft or brief. Nothing is lifted from the samples, and nothing is invented to fit the style; the skill asks instead.
- It copies habits only as often as they appear in the samples, never copies misspellings, and never copies translationese like `ได้ทำการ` even if the writer uses it.
- The profile can be saved and pasted next time instead of the samples.
- The same profile method works in `localize-th` (continue a translation in the style of earlier episodes or app versions) and `script-th` (write a new episode in the style of earlier ones).

Full example with the profile: [examples/humanizer-th/07-match-style.md](examples/humanizer-th/07-match-style.md).

### Why English humanizers don't work for Thai

- **Grammar:** Thai has no tense or articles, drops subjects freely, and marks politeness with particles. Translated Thai shows up as `ได้ทำการ`, `ถูก...โดย` (passive) and `ซึ่ง...ซึ่ง...` chains, not as "delve" or "tapestry".
- **Register:** readers notice the wrong register immediately, such as government-letter Thai in a LINE message.
- **Particles and pronouns:** `ครับ`/`ค่ะ` carry the writer's gender. Putting one on every sentence, or mixing them, is a tell, and so is overusing `คุณ` ("you").
- **Punctuation:** Thai separates phrases with spaces, not commas and full stops. English punctuation, emoji and "!" are tells.

**None of the skills change** facts, numbers, dates, names, brands, links, code or the writer's `ครับ`/`ค่ะ`, and none add information that isn't in the source.

## Install

### One command

Open Terminal (Mac) or PowerShell (Windows) and run

```bash
npx humanizer-th
```

It installs all three skills for Claude Code, Codex, Gemini CLI and GitHub Copilot, whichever you have. Restart your tool once, then just ask.

- Needs Node.js 18 or later, from [nodejs.org](https://nodejs.org). Most Claude Code and Codex users already have it.
- If it asks `Ok to proceed?`, press `y`.
- Update with `npx humanizer-th@latest`, remove with `npx humanizer-th uninstall`, pick one skill with `--skill localize-th`, or install into the current project only with `--project`.

### Without a terminal

**Claude.ai and Claude Desktop:** download the zip for each skill you want from [Releases](https://github.com/inatbalthazar/humanizer-th/releases/latest) (`localize-th.zip`, `script-th.zip`, `humanizer-th.zip`) and upload them one at a time under Settings → Capabilities → Skills.

**ChatGPT, Gemini and other AI tools:** download the bundled prompt for each skill from [Releases](https://github.com/inatbalthazar/humanizer-th/releases/latest) (`localize-th-prompt.md`, `script-th-prompt.md`, `humanizer-th-prompt.md`):

- **ChatGPT:** one GPT per skill. Upload the file under Knowledge and set Instructions to "Follow every instruction in [file name]." (Instructions is capped at 8,000 characters, too short for the whole file).
- **Gemini:** create a Gem and paste the whole file into its instructions, or attach it.
- **API:** use the whole file as the system prompt.
- **Any chat:** attach the file and ask the model to follow it.

The bundles are 59,000 to 94,000 characters. Thai uses more tokens than English, so sending one on every API call adds up.

<details>
<summary><strong>Other ways</strong> (Claude Code plugin, Skills CLI, no Node.js, manual)</summary>

**Claude Code plugin:** run inside Claude Code

```text
/plugin marketplace add inatbalthazar/humanizer-th
/plugin install humanizer-th@humanizer-th
```

**Skills CLI:** installs for every agent the [Skills CLI](https://github.com/vercel-labs/skills) supports, including Cursor and Windsurf

```bash
npx skills add inatbalthazar/humanizer-th --global --agent '*'
```

**No Node.js (macOS or Linux):**

```bash
curl -fsSL https://raw.githubusercontent.com/inatbalthazar/humanizer-th/main/install.sh | bash
```

Use `| bash -s -- --skill localize-th` for one skill and `| bash -s -- --uninstall` to remove them.

**Manual:** copy the folders in `skills/` into the agent's skills folder

| Tool | All projects | One project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot in VS Code | `~/.copilot/skills/` | `.github/skills/` |

Agents not in the table mostly read `.agents/skills/`. To build the zips and prompt bundles from source, run `bash scripts/build.sh`; output goes to `dist/`.

</details>

## What this is not

- **Not an AI-detector evasion tool.** The goal is text that is easier for Thai readers, and the skills never insert deliberate mistakes.
- **No writing as someone else.** Style matching is for your own writing, or ghostwriting the person knows about (a page admin posting for the shop owner). It won't fake messages from other people.
- **No scripts that put words in real people's mouths** for AI video, unless the user is that person or has permission, and no deceptive content such as fake news or scam clips.
- **English source only** for translation for now.

## Limitations

- The skills are guidance the model follows, not deterministic programs. Review the output, and have a native Thai reader check translations before publishing.
- Tested in depth with Claude only. Results with other models depend on how well they handle Thai.
- Shot prompts and voice scripts have not yet been run through real video and TTS tools. The syllables-per-second figure is an estimate to calibrate on the first shot. See [tests/manual-test-v0.3.md](tests/manual-test-v0.3.md).
- Style matching has been tested on one made-up set of samples, not yet on real writers' work. See [tests/manual-test-v0.4.md](tests/manual-test-v0.4.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
