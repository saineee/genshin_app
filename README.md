# Genshin Impact Build Tracker

A personal Genshin Impact character build tracker that pulls live data from the enka.network API and stores it in a PostgreSQL database. Inspired by enka.network, this project aims to be a full-featured character build viewer and DPS optimizer.

## Current Features
- Pulls live character data via enka.network API
- Stores full character stats (HP, ATK, DEF, Crit Rate, Crit DMG, EM, ER)
- Tracks weapon name and refinement level
- Tracks talent levels (including constellation bonuses)
- Tracks constellation level and friendship level
- Full artifact data per character (set, slot, main stat, all substats)
- PostgreSQL relational database (characters + artifacts tables)
- Error handling with try/except for robust data pipeline

## Planned Features
- Flask web view — character cards with full build details
- SQLAlchemy ORM integration
- Artifact pool — stores all artifacts across characters
- Pandas-powered artifact optimizer for maximum DPS
- DPS / damage calculator
- Support for multiple UIDs
- Live hosting via AWS

## Tech Stack
- Python
- PostgreSQL
- psycopg2
- Flask (coming soon)
- SQLAlchemy (coming soon)
- Pandas (coming soon)

## Project Structure
genshin_app/

├── test_api.py          # Main pipeline - fetches API data and inserts to DB

├── artifact_parser.py   # Parses artifact data from API response

└── data/

├── avatar_names.py  # Avatar ID → character name lookup

├── weapon_names.py  # Weapon ID → weapon name lookup

├── artifact_sets.py # Set ID → artifact set name lookup

├── stat_keys.py     # Stat code → fightPropMap key lookup

└── stat_names.py    # Stat prop ID → readable name lookup

## Data Source
Live character data is pulled from the [enka.network](https://enka.network) API.
