#!/usr/bin/env python3
"""OpenRouter model catalog builder.

Outputs:
- data/openrouter/generated/model-routing-matrix.csv
- data/openrouter/generated/model-routing-matrix.json
- data/openrouter/generated/model-router.generated.json

The seed mode is bootstrap-only. The snapshot mode fetches live OpenRouter metadata.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "openrouter" / "generated"
BASE = "https://openrouter.ai/api/v1"
FIELDS = [
    "snapshot_date","model_id","name","family","is_free","context_length","max_completion_tokens",
    "input_modalities","output_modalities","supports_tools","supports_structured_output","supports_reasoning",
    "pricing_prompt_per_mtok","pricing_completion_per_mtok","price_doc_per_mtok","price_code_per_mtok",
    "price_review_per_mtok","price_agent_per_mtok","weekly_rank","weekly_tokens","intelligence_index",
    "coding_index","agentic_index","task_tags","strength_tags","weakness_tags","coding_role",
    "documentation_role","testing_role","frontend_role","backend_role","architecture_role","planning_role",
    "reasoning_role","local_dev_role","production_role","trust_tier","routing_notes","source_urls"
]
ROLES = {"primary","fallback","high_reasoning","cheap","free","avoid","unknown","candidate"}
MIX = {
    "documentation": (0.85, 0.15),
    "coding": (0.55, 0.45),
    "testing": (0.60, 0.40),
    "review": (0.90, 0.10),
    "agent": (0.50, 0.50),
    "planning": (0.70, 0.30),
}
SEED = [
    {"id":"z-ai/glm-5.2","name":"Z.ai: GLM 5.2","description":"1M context reasoning model for long-horizon agent workflows and project-level software engineering.","context_length":1048576,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},"pricing":{"prompt":"0.00000093","completion":"0.000003"},"top_provider":{"max_completion_tokens":32768},"supported_parameters":["reasoning","reasoning_effort","response_format","structured_outputs","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":51.1,"coding_index":68.8,"agentic_index":43.1}},"reasoning":{}},
    {"id":"moonshotai/kimi-k2.7-code","name":"MoonshotAI: Kimi K2.7 Code","description":"Coding-focused model built for end-to-end programming tasks over long contexts.","context_length":262144,"architecture":{"input_modalities":["text","image"],"output_modalities":["text"]},"pricing":{"prompt":"0.00000074","completion":"0.0000035"},"top_provider":{"max_completion_tokens":16384},"supported_parameters":["reasoning","reasoning_effort","response_format","structured_outputs","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":41.9,"coding_index":60.8,"agentic_index":29.6}},"reasoning":{}},
    {"id":"anthropic/claude-sonnet-5","name":"Anthropic: Claude Sonnet 5","description":"Frontier Sonnet-class model for coding, agents, and professional work with adaptive thinking.","context_length":1000000,"architecture":{"input_modalities":["text","image","file"],"output_modalities":["text"]},"pricing":{"prompt":"0.000002","completion":"0.00001"},"top_provider":{"max_completion_tokens":128000},"supported_parameters":["reasoning","response_format","structured_outputs","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":53.4,"coding_index":71.5,"agentic_index":46.7}},"reasoning":{}},
    {"id":"anthropic/claude-fable-5","name":"Anthropic: Claude Fable 5","description":"Premium autonomous knowledge work and coding model with text, image, and file inputs.","context_length":1000000,"architecture":{"input_modalities":["text","image","file"],"output_modalities":["text"]},"pricing":{"prompt":"0.00001","completion":"0.00005"},"top_provider":{"max_completion_tokens":128000},"supported_parameters":["reasoning","response_format","structured_outputs","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":59.9,"coding_index":76.5,"agentic_index":52.8}},"reasoning":{}},
    {"id":"qwen/qwen3.7-plus","name":"Qwen: Qwen3.7 Plus","description":"Cost-effective Qwen model with text/image input, long context, reasoning, tools, and structured outputs.","context_length":1000000,"architecture":{"input_modalities":["text","image"],"output_modalities":["text"]},"pricing":{"prompt":"0.00000032","completion":"0.00000128"},"top_provider":{"max_completion_tokens":65536},"supported_parameters":["reasoning","response_format","structured_outputs","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":39.0,"coding_index":55.9,"agentic_index":20.8}},"reasoning":{}},
    {"id":"nex-agi/nex-n2-mini","name":"Nex AGI: Nex-N2-Mini","description":"Cheap agentic MoE model for coding and tool use.","context_length":262144,"architecture":{"input_modalities":["text","image"],"output_modalities":["text"]},"pricing":{"prompt":"0.000000025","completion":"0.0000001"},"top_provider":{"max_completion_tokens":262144},"supported_parameters":["reasoning","response_format","structured_outputs","tool_choice","tools"],"reasoning":{}},
    {"id":"poolside/laguna-xs-2.1:free","name":"Poolside: Laguna XS 2.1 (free)","description":"Free coding agent model.","context_length":262144,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},"pricing":{"prompt":"0","completion":"0"},"top_provider":{"max_completion_tokens":32768},"supported_parameters":["reasoning","tool_choice","tools"],"reasoning":{}},
    {"id":"cohere/north-mini-code:free","name":"Cohere: North Mini Code (free)","description":"Free agentic coding model.","context_length":256000,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},"pricing":{"prompt":"0","completion":"0"},"top_provider":{"max_completion_tokens":64000},"supported_parameters":["reasoning","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"coding_index":36.5}},"reasoning":{}},
    {"id":"nvidia/nemotron-3-ultra-550b-a55b:free","name":"NVIDIA: Nemotron 3 Ultra (free)","description":"Free open frontier-reasoning and orchestration model with 1M context.","context_length":1000000,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},"pricing":{"prompt":"0","completion":"0"},"top_provider":{"max_completion_tokens":65536},"supported_parameters":["reasoning","tool_choice","tools"],"benchmarks":{"artificial_analysis":{"intelligence_index":37.8,"coding_index":49.3,"agentic_index":27.4}},"reasoning":{}},
    {"id":"tencent/hy3:free","name":"Tencent: Hy3 (free)","description":"Free MoE reasoning and agentic workflow model.","context_length":262144,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},"pricing":{"prompt":"0","completion":"0"},"top_provider":{"max_completion_tokens":262144},"supported_parameters":["reasoning","structured_outputs","tool_choice","tools"],"expiration_date":"2026-07-21","reasoning":{}},
]


def f(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def i(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def mtok(model: dict[str, Any], key: str) -> float:
    return f((model.get("pricing") or {}).get(key)) * 1_000_000


def weighted(prompt: float, completion: float, kind: str) -> float:
    a, b = MIX[kind]
    return prompt * a + completion * b


def params(model: dict[str, Any]) -> set[str]:
    return set(model.get("supported_parameters") or [])


def mods(model: dict[str, Any], key: str) -> list[str]:
    return list(((model.get("architecture") or {}).get(key)) or [])


def has(model: dict[str, Any], feature: str) -> bool:
    p = params(model)
    if feature == "tools":
        return "tools" in p or "tool_choice" in p
    if feature == "structured":
        return "response_format" in p or "structured_outputs" in p
    if feature == "reasoning":
        return bool(model.get("reasoning")) or "reasoning" in p
    if feature == "files":
        return "file" in mods(model, "input_modalities")
    return False


def family(model_id: str, name: str) -> str:
    text = f"{model_id} {name}".lower()
    families = {
        "claude": ["claude", "anthropic"],
        "gpt": ["gpt", "openai"],
        "gemini": ["gemini", "google"],
        "qwen": ["qwen"],
        "glm": ["glm", "z-ai"],
        "kimi": ["kimi", "moonshot"],
        "nemotron": ["nemotron", "nvidia"],
        "poolside": ["poolside", "laguna"],
        "cohere": ["cohere", "north"],
        "tencent": ["tencent", "hy3"],
        "nex": ["nex-agi"],
    }
    for label, needles in families.items():
        if any(needle in text for needle in needles):
            return label
    return "unknown"


def bench(model: dict[str, Any], key: str) -> float:
    return f(((model.get("benchmarks") or {}).get("artificial_analysis") or {}).get(key))


def tags(model: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    model_id = str(model.get("id") or "")
    text = f"{model_id} {model.get('name','')} {model.get('description','')}".lower()
    task, strengths, weaknesses = set(), set(), set()
    if any(x in text for x in ["code", "coding", "programming", "software"]):
        task.add("coding")
    if any(x in text for x in ["reasoning", "thinking", "agentic"]):
        task.add("reasoning")
    if i(model.get("context_length")) >= 128_000:
        task.add("long_context")
    if model_id.endswith(":free") or (mtok(model, "prompt") == 0 and mtok(model, "completion") == 0):
        task.add("free")
    if mtok(model, "prompt") <= 0.5 and mtok(model, "completion") <= 2.0:
        task.add("cheap")
    if has(model, "tools"):
        task.add("tools"); strengths.add("tool_use")
    if has(model, "structured"):
        task.add("structured_output"); strengths.add("structured_output")
    if has(model, "reasoning"):
        task.add("reasoning"); strengths.add("reasoning")
    if bench(model, "coding_index") >= 60:
        strengths.add("coding_benchmark_high")
    if i(model.get("context_length")) >= 1_000_000:
        strengths.add("very_long_context")
    if model.get("expiration_date"):
        weaknesses.add("expiration_date_set")
    if not has(model, "tools"):
        weaknesses.add("no_tool_support_detected")
    return sorted(task), sorted(strengths), sorted(weaknesses)


def score(model: dict[str, Any], kind: str, cost: float) -> float:
    quality = max(bench(model, "coding_index"), bench(model, "intelligence_index"), bench(model, "agentic_index")) / 100
    if quality == 0 and has(model, "reasoning"):
        quality = 0.45
    tagset = set(tags(model)[0])
    fit = 0.0
    if kind in {"coding", "testing", "frontend", "backend"}:
        fit += 0.35 if "coding" in tagset else 0
        fit += 0.25 if has(model, "tools") else 0
        fit += 0.15 if has(model, "structured") else 0
        fit += 0.15 if i(model.get("context_length")) >= 128_000 else 0
        fit += 0.10 if has(model, "reasoning") else 0
    else:
        fit += 0.35 if has(model, "reasoning") else 0
        fit += 0.25 if i(model.get("context_length")) >= 128_000 else 0
        fit += 0.20 if has(model, "tools") else 0
        fit += 0.20 if "reasoning" in tagset else 0
    cost_score = 1.0 if cost <= 0 else 1 / (1 + math.log1p(cost))
    context_score = 0 if i(model.get("context_length")) <= 0 else min(1, math.log2(i(model.get("context_length"))) / math.log2(1_048_576))
    reliability = 0.25 if model.get("expiration_date") else 0.35
    return quality * 0.40 + fit * 0.20 + cost_score * 0.20 + context_score * 0.08 + reliability * 0.12


def role(model: dict[str, Any], kind: str, cost: float) -> str:
    is_free = str(model.get("id", "")).endswith(":free") or "free" in tags(model)[0]
    current_score = score(model, kind, cost)
    if kind == "production" and is_free:
        return "avoid"
    if kind == "local_dev" and is_free:
        return "free"
    if is_free and kind in {"coding", "testing", "frontend", "backend", "documentation"}:
        return "cheap"
    if is_free and kind in {"architecture", "planning", "reasoning"}:
        return "fallback" if has(model, "reasoning") and current_score >= 0.55 else "avoid"
    if kind == "documentation" and cost < 0.75:
        return "cheap"
    if kind in {"architecture", "reasoning"} and has(model, "reasoning") and current_score >= 0.55:
        return "high_reasoning"
    if current_score >= 0.62:
        return "primary"
    if current_score >= 0.40:
        return "fallback"
    if cost < 0.50:
        return "cheap"
    return "unknown"


def build_rows(models: list[dict[str, Any]], snapshot_date: str) -> list[dict[str, Any]]:
    output = []
    for model in models:
        prompt, completion = mtok(model, "prompt"), mtok(model, "completion")
        doc, code = weighted(prompt, completion, "documentation"), weighted(prompt, completion, "coding")
        test, review = weighted(prompt, completion, "testing"), weighted(prompt, completion, "review")
        agent, planning = weighted(prompt, completion, "agent"), weighted(prompt, completion, "planning")
        task_tags, strength_tags, weakness_tags = tags(model)
        row = {
            "snapshot_date": snapshot_date,
            "model_id": model["id"],
            "name": model.get("name", model["id"]),
            "family": family(model["id"], model.get("name", "")),
            "is_free": str(model["id"].endswith(":free") or (prompt == 0 and completion == 0)).lower(),
            "context_length": i(model.get("context_length")),
            "max_completion_tokens": i((model.get("top_provider") or {}).get("max_completion_tokens")),
            "input_modalities": "|".join(mods(model, "input_modalities")),
            "output_modalities": "|".join(mods(model, "output_modalities")),
            "supports_tools": str(has(model, "tools")).lower(),
            "supports_structured_output": str(has(model, "structured")).lower(),
            "supports_reasoning": str(has(model, "reasoning")).lower(),
            "pricing_prompt_per_mtok": round(prompt, 6),
            "pricing_completion_per_mtok": round(completion, 6),
            "price_doc_per_mtok": round(doc, 6),
            "price_code_per_mtok": round(code, 6),
            "price_review_per_mtok": round(review, 6),
            "price_agent_per_mtok": round(agent, 6),
            "weekly_rank": "",
            "weekly_tokens": 0,
            "intelligence_index": bench(model, "intelligence_index"),
            "coding_index": bench(model, "coding_index"),
            "agentic_index": bench(model, "agentic_index"),
            "task_tags": "|".join(task_tags),
            "strength_tags": "|".join(strength_tags),
            "weakness_tags": "|".join(weakness_tags),
            "coding_role": role(model, "coding", code),
            "documentation_role": role(model, "documentation", doc),
            "testing_role": role(model, "testing", test),
            "frontend_role": role(model, "frontend", code),
            "backend_role": role(model, "backend", code),
            "architecture_role": role(model, "architecture", agent),
            "planning_role": role(model, "planning", planning),
            "reasoning_role": role(model, "reasoning", agent),
            "local_dev_role": role(model, "local_dev", agent),
            "production_role": role(model, "production", agent),
            "trust_tier": "free" if model["id"].endswith(":free") else ("premium" if agent >= 10 else "paid"),
            "routing_notes": "bootstrap metadata-only; promote after live snapshot and evals",
            "source_urls": "https://openrouter.ai/api/v1/models",
        }
        output.append(row)
    output.sort(key=lambda row: (-f(row["coding_index"]), f(row["price_agent_per_mtok"]), row["model_id"]))
    return output


def write_outputs(model_rows: list[dict[str, Any]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "model-routing-matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(model_rows)
    (OUT / "model-routing-matrix.json").write_text(json.dumps(model_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    mapping = {
        "coding": "coding_role",
        "documentation": "documentation_role",
        "testing": "testing_role",
        "frontend": "frontend_role",
        "backend": "backend_role",
        "architecture": "architecture_role",
        "planning": "planning_role",
        "reasoning": "reasoning_role",
        "local_dev": "local_dev_role",
        "production": "production_role",
    }
    buckets: dict[str, dict[str, list[str]]] = {}
    order = ["primary", "high_reasoning", "cheap", "free", "fallback", "candidate", "unknown", "avoid"]
    for use_case, column in mapping.items():
        buckets[use_case] = {item: [] for item in order}
        for row in model_rows:
            bucket = row[column] if row[column] in buckets[use_case] else "unknown"
            if len(buckets[use_case][bucket]) < 8:
                buckets[use_case][bucket].append(row["model_id"])
    payload = {"schema_version": "0.1", "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "buckets": buckets}
    (OUT / "model-router.generated.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def fetch_live(sort: str) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"sort": sort, "output_modalities": "text"})
    req = urllib.request.Request(f"{BASE}/models?{query}", headers={"Accept": "application/json", "User-Agent": "architectonic-models/0.1"})
    with urllib.request.urlopen(req, timeout=45) as response:
        payload = json.loads(response.read().decode("utf-8"))
    raw_dir = ROOT / "data" / "openrouter" / "raw" / dt.date.today().isoformat()
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "models.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return list(payload.get("data") or [])


def validate() -> list[str]:
    path = OUT / "model-routing-matrix.csv"
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path}"]
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        data = list(reader)
    if reader.fieldnames != FIELDS:
        errors.append("CSV columns do not match schema")
    if not data:
        errors.append("matrix has no rows")
    ids = [row["model_id"] for row in data]
    if len(ids) != len(set(ids)):
        errors.append("duplicate model_id rows")
    for line_number, row in enumerate(data, start=2):
        for column in [field for field in FIELDS if field.endswith("_role")]:
            if row[column] not in ROLES:
                errors.append(f"line {line_number}: invalid {column}={row[column]}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and validate the OpenRouter model routing catalog.")
    parser.add_argument("command", choices=["seed", "snapshot", "validate"])
    parser.add_argument("--sort", default="top-weekly")
    parser.add_argument("--snapshot-date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    if args.command == "seed":
        write_outputs(build_rows(SEED, args.snapshot_date))
    elif args.command == "snapshot":
        write_outputs(build_rows(fetch_live(args.sort), args.snapshot_date))
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        sys.exit(1)
    print("valid matrix", OUT / "model-routing-matrix.csv")


if __name__ == "__main__":
    main()
