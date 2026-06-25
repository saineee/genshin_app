# Genshin Impact Build Tracker

A personal Genshin Impact character build tracker that pulls live data from the
enka.network API, stores it in a PostgreSQL database, and displays it as a
card-based web UI.

## Current Features

- Pulls live character data via enka.network API
- Stores full character stats (HP, ATK, DEF, Crit Rate, Crit DMG, EM, ER, DMG Bonus)
- Tracks weapon name and refinement level
- Tracks talent levels including constellation bonuses
- Tracks constellation level and friendship level
- Full artifact data per character (set, slot, main stat, all substats)
- PostgreSQL relational database with SQLAlchemy ORM (characters + artifacts tables)
- Modular pipeline: enka_client → parsers → db_ops → sync orchestrator
- Flask web view with card-based UI (character portrait, stats, artifact mini-cards)
- Tailwind CSS styling with custom color palette and Rajdhani font
- Robust error handling across network, DB, and parsing layers

## Planned Features

- UID input on the page — fetch any player's showcase without hardcoding
- Player profile card (AR, world level, Spiral Abyss, Imaginarium Theater)
- Upsert logic — refresh existing characters instead of skipping duplicates
- Pandas-powered artifact optimizer for maximum DPS
- pytest unit tests for parsers and DB operations
- Pydantic validation on API response data
- AWS deployment

## Tech Stack

- Python 3
- PostgreSQL + psycopg2
- SQLAlchemy 2.0 (ORM)
- Flask 3.1
- Jinja2 templating
- Tailwind CSS
- Requests
- python-dotenv
- Pandas (planned)

## Project Structure

## Project Structure
```
genshin_app/
├── app.py                  # Flask routes and web views
├── sync.py                 # Pipeline
├── enka_client.py          # enka.network API calls
├── parsers.py              # Data extraction and transformation
├── db_ops.py               # Database insert operations
├── db.py                   # SQLAlchemy engine and session
├── models.py               # ORM models (Character, Artifact)
├── templates/
│   └── characters.html     # Character card UI
└── data/
├── game_data.py        # Loads loc.json and character_skills.json
├── character_skills.json
├── loc.json
├── stat_keys.py
└── stat_names.py
```

## Data Source

Live character data is pulled from the [enka.network](https://enka.network/) API.
A custom `User-Agent` header is required per their usage guidelines.

## Issues

- Newer characters and weapons (Zibai, Nicole, Skirk's weapon, Furina's weapon)
  display as "Unknown" due to an outdated `loc.json` from the enka repo
