"""Generate a synthetic but plausible dataset for SiKupingBesar.

The generated file follows the PRD schema and contains the 36 UCL clubs plus a
few domestic-only opponents, so every UCL club has a domestic schedule:
domestic league matches for 2023/24, 2024/25, and the played part of 2025/26,
plus the 2025/26 UCL league phase with the first five matchdays played and the
remaining three left empty so the simulator has something to simulate.

Usage:
    python generate_sample_data.py
    python generate_sample_data.py --out data/matches_sample.csv --seed 7
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

BASE_GOALS = 1.02
HOME_ADVANTAGE = 1.12
LAST_PLAYED_DATE = date(2025, 11, 26)

# name: (domestic competition, attack, defence) - a larger defence value is weaker.
TEAMS: dict[str, tuple[str, float, float]] = {
    "Arsenal": ("Premier League", 1.45, 0.82),
    "Liverpool": ("Premier League", 1.52, 0.90),
    "Manchester City": ("Premier League", 1.55, 0.88),
    "Chelsea": ("Premier League", 1.30, 0.95),
    "Newcastle United": ("Premier League", 1.18, 1.00),
    "Tottenham Hotspur": ("Premier League", 1.26, 1.06),
    "Real Madrid": ("La Liga", 1.55, 0.85),
    "Barcelona": ("La Liga", 1.62, 0.92),
    "Atletico Madrid": ("La Liga", 1.24, 0.82),
    "Athletic Club": ("La Liga", 1.10, 0.96),
    "Villarreal": ("La Liga", 1.16, 1.00),
    "Bayern Munich": ("Bundesliga", 1.70, 0.80),
    "Bayer Leverkusen": ("Bundesliga", 1.35, 0.93),
    "Borussia Dortmund": ("Bundesliga", 1.30, 0.98),
    "Eintracht Frankfurt": ("Bundesliga", 1.20, 1.02),
    "Inter": ("Serie A", 1.40, 0.85),
    "Napoli": ("Serie A", 1.25, 0.88),
    "Juventus": ("Serie A", 1.15, 0.90),
    "Atalanta": ("Serie A", 1.35, 0.98),
    "Paris Saint-Germain": ("Ligue 1", 1.60, 0.84),
    "Monaco": ("Ligue 1", 1.22, 1.00),
    "Marseille": ("Ligue 1", 1.15, 1.02),
    "PSV": ("Eredivisie", 1.35, 0.95),
    "Ajax": ("Eredivisie", 1.15, 1.05),
    "Benfica": ("Primeira Liga", 1.25, 0.95),
    "Sporting CP": ("Primeira Liga", 1.30, 0.92),
    "Club Brugge": ("Pro League", 1.10, 1.00),
    "Galatasaray": ("Super Lig", 1.20, 1.05),
    "Slavia Praha": ("Czech First League", 1.05, 0.98),
    "Olympiacos": ("Super League Greece", 1.10, 1.00),
    "Bodo/Glimt": ("Eliteserien", 1.15, 1.08),
    "FC Copenhagen": ("Superliga", 1.00, 1.02),
    "Celtic": ("Scottish Premiership", 1.05, 1.10),
    "Kairat Almaty": ("Kazakh Premier League", 0.85, 1.30),
    "Qarabag": ("Azerbaijan Premier League", 0.85, 1.25),
    "Pafos": ("Cypriot First Division", 0.90, 1.20),
}

UCL_MATCHDAYS = [
    date(2025, 9, 16),
    date(2025, 9, 30),
    date(2025, 10, 21),
    date(2025, 11, 4),
    date(2025, 11, 25),
    date(2025, 12, 9),
    date(2026, 1, 20),
    date(2026, 1, 28),
]
PLAYED_UCL_ROUNDS = 5

# Domestic opponents that are not in the UCL field. They only exist so every
# UCL club has a domestic schedule in the demo data; the UCL rules still see
# exactly 36 teams.
FILLERS: dict[str, list[tuple[str, float, float]]] = {
    "Ligue 1": [
        ("Lyon", 1.05, 1.05),
        ("Lille", 1.08, 1.00),
        ("Nice", 1.00, 1.03),
    ],
    "Eredivisie": [
        ("Feyenoord", 1.25, 0.98),
        ("AZ Alkmaar", 1.10, 1.03),
    ],
    "Primeira Liga": [
        ("Porto", 1.20, 0.96),
        ("Braga", 1.05, 1.02),
    ],
    "Pro League": [
        ("Anderlecht", 0.98, 1.05),
        ("Genk", 1.02, 1.02),
        ("Gent", 0.95, 1.08),
    ],
    "Super Lig": [
        ("Fenerbahce", 1.15, 1.00),
        ("Besiktas", 1.05, 1.05),
        ("Trabzonspor", 1.00, 1.06),
    ],
    "Czech First League": [
        ("Sparta Praha", 1.08, 0.98),
        ("Viktoria Plzen", 1.00, 1.02),
        ("Banik Ostrava", 0.92, 1.08),
    ],
    "Super League Greece": [
        ("Panathinaikos", 1.08, 0.98),
        ("AEK Athens", 1.05, 1.00),
        ("PAOK", 1.02, 1.03),
    ],
    "Eliteserien": [
        ("Molde", 1.05, 1.02),
        ("Rosenborg", 0.98, 1.05),
        ("Brann", 1.00, 1.04),
    ],
    "Superliga": [
        ("Midtjylland", 1.05, 1.00),
        ("Brondby", 1.02, 1.03),
        ("Nordsjaelland", 0.96, 1.06),
    ],
    "Scottish Premiership": [
        ("Rangers", 1.08, 1.02),
        ("Hearts", 0.95, 1.06),
        ("Aberdeen", 0.92, 1.08),
    ],
    "Kazakh Premier League": [
        ("Astana", 0.95, 1.08),
        ("Aktobe", 0.90, 1.12),
        ("Tobol", 0.88, 1.14),
    ],
    "Azerbaijan Premier League": [
        ("Neftci Baku", 0.94, 1.10),
        ("Sabah", 0.92, 1.10),
        ("Zira", 0.88, 1.14),
    ],
    "Cypriot First Division": [
        ("APOEL", 0.98, 1.05),
        ("Omonia", 0.96, 1.06),
        ("AEK Larnaca", 0.94, 1.08),
    ],
}

DOMESTIC_STARTS = {
    "2023/24": date(2023, 8, 12),
    "2024/25": date(2024, 8, 10),
    "2025/26": date(2025, 8, 9),
}
DOMESTIC_ROUND_DAYS = 14


BYE = "__bye__"


def circle_rounds(teams: list[str], rounds: int) -> list[list[tuple[str, str]]]:
    """Round-robin pairing by the circle method, without repeated opponents.

    An odd number of teams is padded with a bye so the rotation still works.
    """
    rotation = list(teams)
    if len(rotation) % 2:
        rotation.append(BYE)
    n = len(rotation)
    schedule: list[list[tuple[str, str]]] = []
    for _ in range(rounds):
        pairs = []
        for i in range(n // 2):
            first, second = rotation[i], rotation[n - 1 - i]
            if BYE not in (first, second):
                pairs.append((first, second))
        schedule.append(pairs)
        rotation = [rotation[0], rotation[-1], *rotation[1:-1]]
    return schedule


def balance_home_games(
    rounds: list[list[tuple[str, str]]], rng: np.random.Generator
) -> list[list[tuple[str, str]]]:
    """Orient each pairing so every team ends with four home matches."""
    target = 4
    home_count: dict[str, int] = {
        team: 0 for pairs in rounds for pair in pairs for team in pair
    }
    oriented: list[list[tuple[str, str]]] = []

    for pairs in rounds:
        row: list[tuple[str, str]] = []
        for first, second in pairs:
            if home_count[first] < home_count[second]:
                home, away = first, second
            elif home_count[second] < home_count[first]:
                home, away = second, first
            else:
                home, away = (first, second) if rng.random() < 0.5 else (second, first)
            home_count[home] += 1
            row.append((home, away))
        oriented.append(row)

    while True:
        over = [team for team, count in home_count.items() if count > target]
        if not over:
            break
        under = {team for team, count in home_count.items() if count < target}

        edges: dict[str, list[tuple[int, int]]] = {team: [] for team in home_count}
        for round_index, row in enumerate(oriented):
            for pair_index, (home, _) in enumerate(row):
                edges[home].append((round_index, pair_index))

        repaired = False
        for start in over:
            parent: dict[str, tuple[str, int, int] | None] = {start: None}
            queue = [start]
            end = None
            for team in queue:
                if end is not None:
                    break
                for round_index, pair_index in edges[team]:
                    opponent = oriented[round_index][pair_index][1]
                    if opponent in parent:
                        continue
                    parent[opponent] = (team, round_index, pair_index)
                    if opponent in under:
                        end = opponent
                        break
                    queue.append(opponent)

            if end is None:
                continue

            team = end
            while parent[team] is not None:
                previous, round_index, pair_index = parent[team]
                home, away = oriented[round_index][pair_index]
                oriented[round_index][pair_index] = (away, home)
                home_count[home] -= 1
                home_count[away] += 1
                team = previous
            repaired = True
            break

        if not repaired:
            break

    return oriented


def poisson_goals(
    rng: np.random.Generator, lam_home: float, lam_away: float
) -> tuple[int, int]:
    return int(rng.poisson(lam_home)), int(rng.poisson(lam_away))


def _team_table() -> dict[str, tuple[str, float, float]]:
    """UCL clubs plus the domestic-only opponents used for filler fixtures."""
    table = dict(TEAMS)
    for competition, fillers in FILLERS.items():
        for name, attack, defence in fillers:
            table[name] = (competition, attack, defence)
    return table


def build_domestic(rng: np.random.Generator) -> list[dict[str, object]]:
    table = _team_table()
    leagues: dict[str, list[str]] = defaultdict(list)
    for team, (competition, _, _) in table.items():
        leagues[competition].append(team)

    rows: list[dict[str, object]] = []
    for season, start in DOMESTIC_STARTS.items():
        for competition, teams in leagues.items():
            if len(teams) < 2:
                continue
            ordered = sorted(teams)
            rng.shuffle(ordered)
            first_leg = circle_rounds(ordered, len(ordered) - 1)
            fixture_rounds = first_leg + [
                [(away, home) for home, away in pairs] for pairs in first_leg
            ]

            for round_index, pairs in enumerate(fixture_rounds):
                match_date = start + timedelta(days=DOMESTIC_ROUND_DAYS * round_index)
                if match_date > LAST_PLAYED_DATE:
                    continue
                for home, away in pairs:
                    _, attack_home, defence_home = table[home]
                    _, attack_away, defence_away = table[away]
                    lam_home = BASE_GOALS * HOME_ADVANTAGE * attack_home * defence_away
                    lam_away = BASE_GOALS * attack_away * defence_home
                    home_goals, away_goals = poisson_goals(rng, lam_home, lam_away)
                    rows.append(
                        {
                            "date": match_date,
                            "home": home,
                            "away": away,
                            "home_goals": home_goals,
                            "away_goals": away_goals,
                            "competition": competition,
                        }
                    )
    return rows


def build_ucl(rng: np.random.Generator) -> list[dict[str, object]]:
    teams = sorted(TEAMS)
    rounds = balance_home_games(circle_rounds(teams, len(UCL_MATCHDAYS)), rng)

    rows: list[dict[str, object]] = []
    for round_index, pairs in enumerate(rounds):
        match_date = UCL_MATCHDAYS[round_index]
        played = round_index < PLAYED_UCL_ROUNDS
        for home, away in pairs:
            row: dict[str, object] = {
                "date": match_date,
                "home": home,
                "away": away,
                "home_goals": np.nan,
                "away_goals": np.nan,
                "competition": "UCL",
            }
            if played:
                _, attack_home, defence_home = TEAMS[home]
                _, attack_away, defence_away = TEAMS[away]
                lam_home = BASE_GOALS * HOME_ADVANTAGE * attack_home * defence_away
                lam_away = BASE_GOALS * attack_away * defence_home
                row["home_goals"], row["away_goals"] = poisson_goals(
                    rng, lam_home, lam_away
                )
            rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", default="data/matches_sample.csv", help="Output CSV path"
    )
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    rows = build_domestic(rng) + build_ucl(rng)
    matches = pd.DataFrame(rows).sort_values(
        ["date", "competition", "home"], ignore_index=True
    )
    matches["date"] = pd.to_datetime(matches["date"]).dt.date

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(out, index=False, na_rep="")

    ucl = matches[matches["competition"] == "UCL"]
    played = matches.dropna(subset=["home_goals", "away_goals"])
    domestic = matches[matches["competition"] != "UCL"]
    ucl_teams = sorted(set(ucl["home"]) | set(ucl["away"]))
    domestic_appearances = pd.concat([domestic["home"], domestic["away"]]).value_counts()
    without_domestic = [team for team in ucl_teams if domestic_appearances.get(team, 0) == 0]

    print(f"Wrote {len(matches)} matches to {out}")
    print(f"  domestic: {len(domestic)} | UCL: {len(ucl)}")
    print(
        f"  played: {len(played)} | scheduled UCL: "
        f"{len(ucl) - len(played[played['competition'] == 'UCL'])}"
    )
    print(f"  UCL teams: {len(ucl_teams)}")
    print(f"  domestic competitions: {domestic['competition'].nunique()}")
    print(f"  UCL teams without domestic matches: {len(without_domestic)}")
    print(f"  last played date: {played['date'].max()}")


if __name__ == "__main__":
    main()
