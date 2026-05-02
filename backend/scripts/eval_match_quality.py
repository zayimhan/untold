"""
Regression test for match quality.

Each test case specifies a user input and a set of acceptable archive IDs.
Pass = matcher's top-1 is in the acceptable set after evaluator re-ranking.

Usage:
    python -m scripts.eval_match_quality
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.theme_interpreter import interpret_theme
from app.matcher import find_matches
from app.evaluator import select_best_match
from app.config import TOP_K, QUALITY_THRESHOLD

CASES = [
    {
        "input": "i wish i could tell her i love her",
        "acceptable_ids": ["vl_005", "vl_020", "vl_024", "dy_007", "cc_008"],
        "label": "unspoken_love",
    },
    {
        "input": "dad i became strong because of you i miss you",
        "acceptable_ids": ["vl_030", "vl_018", "dy_007"],
        "label": "father_gratitude",
    },
    {
        "input": "i never forgave you",
        "acceptable_ids": ["vl_006", "cc_007", "cc_009", "cc_010"],
        "label": "unforgiveness",
    },
    {
        "input": "brother i'm sorry let me be your brother again",
        "acceptable_ids": ["cc_009", "vl_019", "cc_010"],
        "label": "reconciliation_attempt",
    },
    {
        "input": "i don't know who i am anymore",
        "acceptable_ids": ["vl_021", "cc_011", "vl_011"],
        "label": "identity_loss",
    },
]


def run() -> int:
    passed = 0
    failed = []
    for case in CASES:
        theme = interpret_theme(case["input"])
        candidates = find_matches(theme["search_query"], TOP_K)
        selected, history, score = select_best_match(
            case["input"], theme, candidates, QUALITY_THRESHOLD
        )
        ok = selected.id in case["acceptable_ids"]
        marker = "✓" if ok else "✗"
        print(f"{marker} [{case['label']}] → {selected.id} (score {score})")
        if not ok:
            print(f"    Expected one of: {case['acceptable_ids']}")
            print(f"    Got top-K: {[c.id for c in candidates]}")
            failed.append(case["label"])
        passed += int(ok)
    print(f"\n{passed}/{len(CASES)} passed")
    if failed:
        print(f"Failed: {failed}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
