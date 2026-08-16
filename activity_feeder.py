"""Fleet activity feeder — makes the codemap viewer GLOW where agents work.

Polls fleet-monitor /api/fleet (existing heartbeats, no new infra), maps each
live agent's cwd to a repo from repos.txt, and POSTs agent-activity events to
the viewer's existing SSE pipe (/api/agent-activity -> browser glow).

Pilot v1 (Sage 2026-08-17): repo-level glow for busy agents. File-level comes
from the typing-v1.1 hook family later.
"""
import json
import os
import time
import urllib.request

VIEWER = os.environ.get("CODEMAP_VIEWER_URL", "http://127.0.0.1:47800")
FLEET_API = "https://fleet-monitor.xaxixak.workers.dev/api/fleet"
TOKEN_FILE = os.path.expanduser("~/.claude/oracle-token-sage")
REPOS_TXT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repos.txt")
POLL_SECONDS = 20


def load_repos():
    repos = []
    with open(REPOS_TXT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                norm = line.replace("\\", "/").rstrip("/")
                repos.append((norm.lower(), os.path.basename(norm)))
    return repos


def repo_for_cwd(cwd, repos):
    if not cwd:
        return None
    c = cwd.replace("\\", "/").lower()
    for prefix, name in repos:
        if c.startswith(prefix):
            return name
    return None


def post_activity(payload):
    req = urllib.request.Request(
        VIEWER + "/api/agent-activity",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        r.read()


def main():
    token = open(TOKEN_FILE).read().strip()
    repos = load_repos()
    print(f"[feeder] {len(repos)} repos, viewer={VIEWER}, poll={POLL_SECONDS}s")
    while True:
        try:
            # custom UA required: Cloudflare 403s the default Python-urllib agent
            req = urllib.request.Request(FLEET_API, headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "codemap-feeder/1.0",
            })
            with urllib.request.urlopen(req, timeout=15) as r:
                fleet = json.load(r)
            sent = 0
            for o in fleet.get("oracles", []):
                status = o.get("live_status")
                for s in o.get("live_sessions") or []:
                    repo = repo_for_cwd(s.get("cwd", ""), repos)
                    if repo and status in ("busy", "idle"):
                        post_activity({
                            "tool": status,
                            "focus": repo,
                            "args": {"agent": o.get("name"), "emoji": o.get("ack_emoji", "")},
                        })
                        sent += 1
            print(f"[feeder] tick: {sent} activity events")
        except Exception as e:
            print(f"[feeder] error: {e}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
