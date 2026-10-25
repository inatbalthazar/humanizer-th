#!/usr/bin/env node
// Install the Thai skills (humanizer-th, localize-th, script-th) into every
// AI tool found on this machine.
//
//   npx humanizer-th                      install all three skills
//   npx humanizer-th --skill localize-th  install one skill (repeatable)
//   npx humanizer-th --project            install into the current folder only
//   npx humanizer-th --target DIR         install into DIR/<skill>
//   npx humanizer-th uninstall            remove the skills
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const ALL_SKILLS = ["humanizer-th", "localize-th", "script-th"];
const SRC = path.join(__dirname, "..", "skills");
const VERSION = require("../package.json").version;

const HELP = `humanizer-th ${VERSION}

  npx humanizer-th                      ติดตั้งทั้งสาม skill / install all three skills
  npx humanizer-th --skill localize-th  ติดตั้งบางตัว / install one skill (repeatable)
  npx humanizer-th --project            ติดตั้งเฉพาะโฟลเดอร์นี้ / this folder only
  npx humanizer-th --target DIR         ติดตั้งลง DIR / install into DIR
  npx humanizer-th uninstall            ลบออก / remove

Skills: ${ALL_SKILLS.join(", ")}`;

function fail(message) {
  console.error(message);
  process.exit(1);
}

function parseArgs(argv) {
  const opts = { command: "install", skills: [], target: "", project: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "install" || arg === "uninstall") opts.command = arg;
    else if (arg === "--skill") opts.skills.push(argv[++i] || fail("--skill needs a name"));
    else if (arg === "--target") opts.target = argv[++i] || fail("--target needs a folder");
    else if (arg === "--project") opts.project = true;
    else if (arg === "-h" || arg === "--help" || arg === "help") opts.command = "help";
    else if (arg === "-v" || arg === "--version") opts.command = "version";
    else fail(`Unknown option: ${arg}\n\n${HELP}`);
  }
  if (opts.skills.length === 0) opts.skills = ALL_SKILLS;
  for (const s of opts.skills) {
    if (!ALL_SKILLS.includes(s)) fail(`Unknown skill: ${s} (choose from ${ALL_SKILLS.join(", ")})`);
  }
  return opts;
}

// Skill folders to install into, with the tool each one serves.
// .agents/skills is shared by Codex and other tools that follow the Agent
// Skills standard, so it is always used. The rest only when the tool exists.
function destinations(opts) {
  if (opts.target) return [{ dir: path.resolve(opts.target), tool: opts.target }];
  if (opts.project) {
    const cwd = process.cwd();
    return [
      { dir: path.join(cwd, ".agents", "skills"), tool: "Codex and others" },
      { dir: path.join(cwd, ".claude", "skills"), tool: "Claude Code" },
    ];
  }
  const home = os.homedir();
  const dests = [{ dir: path.join(home, ".agents", "skills"), tool: "Codex and others" }];
  const optional = [
    [".claude", "Claude Code"],
    [".gemini", "Gemini CLI"],
    [".copilot", "GitHub Copilot"],
  ];
  for (const [folder, tool] of optional) {
    if (fs.existsSync(path.join(home, folder))) dests.push({ dir: path.join(home, folder, "skills"), tool });
  }
  return dests;
}

function install(opts) {
  for (const s of opts.skills) {
    if (!fs.existsSync(path.join(SRC, s, "SKILL.md"))) fail(`${s}/SKILL.md is missing from this package`);
  }
  const dests = destinations(opts);
  for (const { dir } of dests) {
    fs.mkdirSync(dir, { recursive: true });
    for (const s of opts.skills) {
      const to = path.join(dir, s);
      fs.rmSync(to, { recursive: true, force: true });
      fs.cpSync(path.join(SRC, s), to, { recursive: true });
    }
  }
  console.log(`humanizer-th ${VERSION}: ${opts.skills.join(", ")}`);
  for (const { dir, tool } of dests) console.log(`  ${dir}  (${tool})`);
  console.log(`
เสร็จแล้ว ถ้าเปิดโปรแกรม AI อยู่ ให้ปิดแล้วเปิดใหม่ก่อน แล้วลองพิมพ์
  "แปลซับนี้เป็นไทย" แล้วแนบไฟล์ซับ
  "เขียนบทละครสั้นเรื่อง..."
  "เกลาให้หน่อย" ตามด้วยข้อความภาษาไทย

Done. Restart your AI tool, then just ask, e.g. "Translate this subtitle file into Thai".
อัปเดตเวอร์ชันใหม่ / update: npx humanizer-th@latest`);
}

function uninstall(opts) {
  let removed = 0;
  for (const { dir } of destinations(opts)) {
    for (const s of opts.skills) {
      const to = path.join(dir, s);
      if (fs.existsSync(to)) {
        fs.rmSync(to, { recursive: true, force: true });
        console.log(`Removed ${to}`);
        removed++;
      }
    }
  }
  if (removed === 0) console.log("ไม่พบ skill ที่ติดตั้งไว้ / Nothing to remove");
}

const opts = parseArgs(process.argv.slice(2));
if (opts.command === "help") console.log(HELP);
else if (opts.command === "version") console.log(VERSION);
else if (opts.command === "uninstall") uninstall(opts);
else install(opts);
