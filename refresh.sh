#!/usr/bin/env bash
# codemap refresh — re-extract code graphs (free, no LLM) + rebuild global graph
# Usage: ./refresh.sh   (run from D:/Ailab/codemap)
set -e
G=./venv/Scripts/graphify.exe
REPOS=(
  "D:/Work/Ai Dev/Company/Business APP/business-erp"
  "D:/Work/Ai Dev/revanmo"
  "D:/Work/Ai Dev/Wiz-Wi"
  "D:/Oracles/github.com/Soul-Brews-Studio/arra-oracle-v3"
  "D:/Oracles/github.com/xaxixak/fleet-monitor"
  "D:/Oracles/.oracle/mqtt-channel"
  "C:/Users/xaxix/.claude/plugins/cache/claude-plugins-official/discord/0.0.4"
)
GRAPHS=()
for R in "${REPOS[@]}"; do
  echo "== $R"
  "$G" update "$R" --no-cluster | grep -E 'Rebuilt|error' || true
  GRAPHS+=("$R/graphify-out/graph.json")
done
"$G" merge-graphs "${GRAPHS[@]}" --out global/graph.json
echo "done: global/graph.json"
