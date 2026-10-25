# humanizer-th

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg) ![version](https://img.shields.io/badge/version-0.3.0-green.svg)

A set of Thai-language [Agent Skills](https://agentskills.io). Translate subtitles, games, apps and websites into Thai that doesn't read like a translation, write and polish dialogue for AI-generated short dramas and Thai AI voice-over, and edit AI-written Thai so it reads like a native writer wrote it.

Works with Claude, ChatGPT, Gemini, Codex, GitHub Copilot, Cursor and any tool that supports Agent Skills. Tools without skill support can use a single bundled prompt file instead.

[อ่านภาษาไทย](README.md)

## The skills

| Skill | What it does | Example request |
|---|---|---|
| **localize-th** | English to Thai for subtitles, dubbing scripts, app and website strings, and games | "แปลซับนี้เป็นไทย" / "Translate this strings file into Thai" |
| **script-th** | Writes and polishes Thai dialogue for AI short dramas, per-shot video prompts, and TTS-ready voice scripts | "เขียนบทละครสั้นเรื่อง..." / "Polish this script" |
| **humanizer-th** | Edits AI-written Thai posts, emails and chat messages | "เกลาให้หน่อย" / "Make this sound natural" |

Install once and the agent picks the right skill for each request.

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

Examples: [SRT subtitles](examples/localize-th/01-subtitle-srt.md), [app JSON](examples/localize-th/02-app-ui-json.md), [game CSV](examples/localize-th/03-game-dialogue-csv.md).

## script-th: AI short dramas and Thai voice-over

Four modes: write a script from an idea, polish an existing script without changing the story, turn it into per-shot prompts for AI video tools, and prepare a voice script that Thai TTS reads correctly (numbers as words, unambiguous spellings, pauses and voice direction).

- Character sheets with fixed English visual descriptions, copied verbatim into every shot prompt for consistency.
- Lines sized to the clip length using a syllable estimate, with long lines split across shots.
- Twelve AI-dialogue tells (SC01–SC12), such as characters naming their feelings, exposition dumps, stock lines from short dramas and everyone sounding the same.
- Three ways to add Thai speech (native audio from the video model, separate TTS with lip-sync, or narration and subtitles), because many video models still speak Thai poorly.

Examples: [write from an idea](examples/script-th/01-write-short-drama.md), [polish an AI script](examples/script-th/02-polish-ai-script.md), [shot prompts and voice script](examples/script-th/03-shot-prompts-and-voice.md).

## humanizer-th: AI-written Thai

Three modes (ตรวจ check, เขียนใหม่ rewrite, แก้เฉพาะจุด fix spots) across the four registers taught in Thai schools: กันเอง (intimate), ไม่เป็นทางการ (informal), กึ่งทางการ (semi-formal) and ทางการ (formal). It checks 29 patterns (TH01–TH29), most of which Thai grammar classes call ประโยคฟุ่มเฟือย (redundant sentences) and สำนวนต่างประเทศ (foreign-style phrasing). See [patterns.md](shared/patterns.md) and [examples/humanizer-th/](examples/humanizer-th/).

### Why English humanizers don't work for Thai

- **Grammar:** Thai has no tense or articles, drops subjects freely, and marks politeness with particles. Translated Thai shows up as `ได้ทำการ`, `ถูก...โดย` (passive) and `ซึ่ง...ซึ่ง...` chains, not as "delve" or "tapestry".
- **Register:** readers notice the wrong register immediately, such as government-letter Thai in a LINE message.
- **Particles and pronouns:** `ครับ`/`ค่ะ` carry the writer's gender. Putting one on every sentence, or mixing them, is a tell, and so is overusing `คุณ` ("you").
- **Punctuation:** Thai separates phrases with spaces, not commas and full stops. English punctuation, emoji and "!" are tells.

**None of the skills change** facts, numbers, dates, names, brands, links, code or the writer's `ครับ`/`ค่ะ`, and none add information that isn't in the source.

## Install

### Claude Code

Installs all three skills:

```text
/plugin marketplace add inatbalthazar/humanizer-th
/plugin install humanizer-th@humanizer-th
```

### Codex

```bash
npx skills add inatbalthazar/humanizer-th --global --agent codex
```

### Other agents

```bash
npx skills add inatbalthazar/humanizer-th --global --agent '*'
```

This installs for every agent the [Skills CLI](https://github.com/vercel-labs/skills) supports, including Gemini CLI, GitHub Copilot, Cursor and Windsurf. Leave off `--global` to install only in the current project, and add `--skill localize-th` (for example) to pick one skill.

Without Node.js, use the install script (macOS or Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/inatbalthazar/humanizer-th/main/install.sh | bash
```

It installs all three skills into `~/.agents/skills/`, plus Claude Code, Gemini CLI and GitHub Copilot if it finds them. Run it again to update. Use `| bash -s -- --skill localize-th` for one skill and `| bash -s -- --uninstall` to remove them.

### Claude.ai and Claude Desktop

Download the zip for each skill you want from [Releases](https://github.com/inatbalthazar/humanizer-th/releases) (`localize-th.zip`, `script-th.zip`, `humanizer-th.zip`) and upload them one at a time under Settings → Capabilities → Skills.

### ChatGPT, Gemini and other AI tools

Download the bundled prompt for each skill from [Releases](https://github.com/inatbalthazar/humanizer-th/releases) (`localize-th-prompt.md`, `script-th-prompt.md`, `humanizer-th-prompt.md`):

- **ChatGPT:** one GPT per skill. Upload the file under Knowledge and set Instructions to "ทำตามคำสั่งในไฟล์ [file name] ทุกข้อ" (Instructions is capped at 8,000 characters, too short for the whole file).
- **Gemini:** create a Gem and paste the whole file into its instructions, or attach it.
- **API:** use the whole file as the system prompt.
- **Any chat:** attach the file and ask the model to follow it.

The bundles are 48,000 to 85,000 characters. Thai uses more tokens than English, so sending one on every API call adds up.

### Manual install

Copy the folders in `skills/` into the agent's skills folder:

| Tool | All projects | One project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot in VS Code | `~/.copilot/skills/` | `.github/skills/` |

Agents not in the table mostly read `.agents/skills/`. To build the zips and prompt bundles from source, run `bash scripts/build.sh`; output goes to `dist/`.

## What this is not

- **Not an AI-detector evasion tool.** The goal is text that is easier for Thai readers, and the skills never insert deliberate mistakes.
- **No scripts that put words in real people's mouths** for AI video, unless the user is that person or has permission, and no deceptive content such as fake news or scam clips.
- **English source only** for translation for now.

## Limitations

- The skills are guidance the model follows, not deterministic programs. Review the output, and have a native Thai reader check translations before publishing.
- Tested in depth with Claude only. Results with other models depend on how well they handle Thai.
- Shot prompts and voice scripts have not yet been run through real video and TTS tools. The syllables-per-second figure is an estimate to calibrate on the first shot. See [tests/manual-test-v0.3.md](tests/manual-test-v0.3.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
