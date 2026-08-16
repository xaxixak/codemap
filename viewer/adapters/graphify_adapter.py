"""Graphify Adapter — feeds codemap graphs (graphify graph.json) into the WI viewer.

Sources:
  graphify:global      -> D:/Ailab/codemap/global/graph.json (merged, ids carry <repo>:: prefix)
  graphify:<repo-name> -> <repo>/graphify-out/graph.json (per-repo, from repos.txt)

Lifted-and-wired by Sage 2026-08-17 per Kong's pilot (compose, don't fuse):
graphify stays stock; this file only READS its output.
"""
import json
import os
from pathlib import Path
from typing import List

from .base import BaseAdapter, GraphSource, UniversalGraph

CODEMAP = Path("D:/Ailab/codemap")
REPOS_TXT = CODEMAP / "repos.txt"
GLOBAL_GRAPH = CODEMAP / "global" / "graph.json"


def _repo_list():
    repos = []
    if REPOS_TXT.exists():
        for line in REPOS_TXT.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                repos.append(Path(line))
    return repos


def _tier_for(label: str, source_file: str) -> str:
    base = os.path.basename(source_file or "")
    if label == base and base:
        return "macro"          # file node
    if label.startswith(".") and label.endswith("()"):
        return "micro"          # method stub
    return "meso"


class GraphifyAdapter(BaseAdapter):
    def list_sources(self) -> List[GraphSource]:
        sources = []
        if GLOBAL_GRAPH.exists():
            size_kb = GLOBAL_GRAPH.stat().st_size // 1024
            sources.append(GraphSource(
                id="graphify:global",
                name="🗺️ Fleet Global (all repos)",
                adapter="graphify",
                description=f"Merged code map ({size_kb} KB)",
                group="Codemap",
                config={"path": str(GLOBAL_GRAPH)},
            ))
        for repo in _repo_list():
            gpath = repo / "graphify-out" / "graph.json"
            if gpath.exists():
                sources.append(GraphSource(
                    id=f"graphify:{repo.name}",
                    name=repo.name,
                    adapter="graphify",
                    description=str(repo),
                    group="Codemap repos",
                    config={"path": str(gpath)},
                ))
        return sources

    def load_graph(self, source_id: str) -> UniversalGraph:
        src = None
        for s in self.list_sources():
            if s.id == source_id:
                src = s
                break
        if src is None:
            raise ValueError(f"Unknown graphify source: {source_id}")

        with open(src.config["path"], "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_nodes = data.get("nodes", [])
        raw_edges = data.get("links", data.get("edges", []))

        nodes = []
        for n in raw_nodes:
            nid = str(n.get("id", ""))
            label = n.get("label", nid)
            sf = n.get("source_file", "") or ""
            # merged ids carry "<repo>::" prefix — surface as a tag so the
            # viewer can filter per folder/job
            repo_tag = nid.split("::", 1)[0] if "::" in nid else ""
            node = {
                "id": nid,
                "type": n.get("file_type", "code"),
                "name": label,
                "tier": _tier_for(label, sf),
                "metadata": {
                    "source_file": sf,
                    "loc": n.get("source_location") or "",
                    "community": n.get("community", ""),
                },
            }
            if repo_tag:
                node["tags"] = [repo_tag]
            if n.get("community") not in (None, ""):
                node["categories"] = [str(n.get("community"))]
            nodes.append(node)

        conf_map = {"EXTRACTED": 1.0, "INFERRED": 0.5, "AMBIGUOUS": 0.2}
        edges = []
        for e in raw_edges:
            conf = e.get("confidence", "EXTRACTED")
            if isinstance(conf, str):
                conf = conf_map.get(conf.upper(), 0.5)
            edges.append({
                "source_id": str(e.get("source", e.get("source_id", ""))),
                "target_id": str(e.get("target", e.get("target_id", ""))),
                "type": e.get("relation", e.get("type", "connects")),
                "weight": float(conf),
                "confidence": conf,
            })

        edge_types = sorted({e["type"] for e in edges})
        caps = {
            "hierarchy": any(e["type"] == "contains" for e in edges),
            "categories": True,
            "edge_types": edge_types,
            "graph_name": src.name,   # Fafa spec #1: always know which graph you look at
        }
        return UniversalGraph(src, nodes, edges, caps)
