# codemap 🗺️

แผนที่โค้ดของ fleet (Kong's X3K) — สร้างด้วย [graphify](https://github.com/Graphify-Labs/graphify) เฉพาะ**ส่วนฟรี** (tree-sitter code graph, ไม่มี LLM cost)

## สิ่งที่ตั้งไว้ (2026-08-16 โดย Sage 🪞 ตามคำสั่ง Kong)

- `venv/` — graphifyy 0.9.44 + [sql,mcp] extras (isolated ไม่แตะ global python)
- `global/graph.json` — แผนที่รวมข้าม repo (merge จาก per-repo graphs)
- `refresh.sh` — สแกนใหม่ทุก repo + rebuild global (ฟรี ~1 นาที)
- **MCP**: ลงทะเบียน user-scope ชื่อ `graphify` → agent ทุกตัวบนเครื่องนี้ถาม `query_graph`/`get_neighbors`/`shortest_path`/`affected` ฯลฯ ได้
- **Hook บังคับ (ฉบับเรา)**: PreToolUse ใน `~/.claude/settings.json` เรียก `graphify hook-guard search|read` — nudge ให้ดูแผนที่ก่อน grep/read **เฉพาะ repo ที่มีแผนที่สด** (fail-open, ไม่ block, self-gate)

## ⚠️ กติกาสำคัญ

- **ห้ามรัน `graphify install` เด็ดขาด** — installer ของมันเขียนทับ `~/.claude/CLAUDE.md` + settings ของทุก agent (เราจึง wire ทุกอย่างเองแบบ manual)
- อย่าเปิด `graphify watch` บน Windows (rebuild lock เป็น no-op) — ใช้ `refresh.sh` หรือ git post-commit hook แทน
- repo เป้าหมายมี `graphify-out/` เกิดขึ้นข้างใน — ignore ผ่าน `.git/info/exclude` แล้ว (local-only)

## เพิ่ม repo ใหม่เข้าแผนที่

แก้ array `REPOS` ใน `refresh.sh` แล้วรัน

## ที่มาการตัดสินใจ

การศึกษาเต็ม 2 ฉบับ: `sage-oracle/ψ/learn/graphify-2026-08/{fit,arch}-report.md`
— ใช้เฉพาะ code graph (ฟรี), ไม่ให้ LLM กิน ψ brain (ไทยพังฝั่ง query + สมองเราเป็น append-only)
