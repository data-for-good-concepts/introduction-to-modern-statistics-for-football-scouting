"""Derive small analysis-ready CSVs from StatsBomb open event data.

Source: https://github.com/statsbomb/open-data (CC BY-NC-SA 4.0, StatsBomb).

Downloads match lists and per-match event files (cached in the scratchpad,
~500MB transient), extracts shot events, and writes compact CSVs into
data/derived/ that the book's R examples and the tutor's exercises read.
Raw StatsBomb JSON never enters this repo.

Usage: python3 scripts/derive_statsbomb_tables.py <cache_dir>
"""

import csv
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW_BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPETITIONS = {
    "wc2022": (43, 106),      # FIFA World Cup, 2022
    "weuro2025": (53, 315),   # UEFA Women's Euro, 2025
}

SHOT_FIELDS = [
    "competition", "match_id", "match_date", "stage", "team", "opponent",
    "player", "position", "period", "minute", "second", "play_pattern",
    "shot_type", "body_part", "technique", "first_time", "under_pressure",
    "one_on_one", "statsbomb_xg", "outcome", "goal",
]


def fetch_matches(competition_id: int, season_id: int, cache_dir: Path) -> list[dict]:
    cached = cache_dir / f"matches-{competition_id}-{season_id}.json"
    if not cached.exists():
        urllib.request.urlretrieve(
            f"{RAW_BASE}/matches/{competition_id}/{season_id}.json", cached
        )
    return json.loads(cached.read_text())


def fetch_events(match_id: int, cache_dir: Path) -> list[dict]:
    cached = cache_dir / f"{match_id}.json"
    if not cached.exists():
        urllib.request.urlretrieve(f"{RAW_BASE}/events/{match_id}.json", cached)
    return json.loads(cached.read_text())


def shots_for_match(comp: str, match: dict, cache_dir: Path) -> list[dict]:
    events = fetch_events(match["match_id"], cache_dir)
    home, away = match["home_team"]["home_team_name"], match["away_team"]["away_team_name"]
    rows = []
    for ev in events:
        if ev.get("type", {}).get("name") != "Shot":
            continue
        shot = ev.get("shot", {})
        team = ev["team"]["name"]
        rows.append({
            "competition": comp,
            "match_id": match["match_id"],
            "match_date": match["match_date"],
            "stage": match["competition_stage"]["name"],
            "team": team,
            "opponent": away if team == home else home,
            "player": ev.get("player", {}).get("name"),
            "position": ev.get("position", {}).get("name"),
            "period": ev.get("period"),
            "minute": ev.get("minute"),
            "second": ev.get("second"),
            "play_pattern": ev.get("play_pattern", {}).get("name"),
            "shot_type": shot.get("type", {}).get("name"),
            "body_part": shot.get("body_part", {}).get("name"),
            "technique": shot.get("technique", {}).get("name"),
            "first_time": bool(shot.get("first_time", False)),
            "under_pressure": bool(ev.get("under_pressure", False)),
            "one_on_one": bool(shot.get("one_on_one", False)),
            "statsbomb_xg": shot.get("statsbomb_xg"),
            "outcome": shot.get("outcome", {}).get("name"),
            "goal": shot.get("outcome", {}).get("name") == "Goal",
        })
    return rows


def match_table(comp: str, matches: list[dict]) -> list[dict]:
    rows = []
    for m in matches:
        hs, as_ = m["home_score"], m["away_score"]
        rows.append({
            "competition": comp,
            "match_id": m["match_id"],
            "match_date": m["match_date"],
            "stage": m["competition_stage"]["name"],
            "home_team": m["home_team"]["home_team_name"],
            "away_team": m["away_team"]["away_team_name"],
            "home_score": hs,
            "away_score": as_,
            "result": "home" if hs > as_ else ("away" if as_ > hs else "draw"),
        })
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cache_dir = Path(sys.argv[1])
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir = REPO / "data/derived"
    for comp, (competition_id, season_id) in COMPETITIONS.items():
        matches = fetch_matches(competition_id, season_id, cache_dir)
        with ThreadPoolExecutor(max_workers=8) as pool:
            per_match = list(pool.map(lambda m: shots_for_match(comp, m, cache_dir), matches))
        shots = [r for rows in per_match for r in rows]
        write_csv(out_dir / f"{comp}_shots.csv", shots, SHOT_FIELDS)
        write_csv(out_dir / f"{comp}_matches.csv", match_table(comp, matches),
                  ["competition", "match_id", "match_date", "stage", "home_team",
                   "away_team", "home_score", "away_score", "result"])
        print(f"{comp}: {len(matches)} matches, {len(shots)} shots")


if __name__ == "__main__":
    main()
