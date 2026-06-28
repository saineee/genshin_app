# Genshin Impact Build Tracker

A personal Genshin Impact character build tracker that pulls live data from the enka.network API, stores it in a PostgreSQL database, and displays it as a card-based web UI.

## Current Features

- Pulls live character data via enka.network API
- UID input form: fetch any player's showcase on demand from the browser
- Player profile card displaying nickname, AR, World Level, signature, achievements, Spiral Abyss floor/stars, Imaginarium Theater act/stars, and Stygian Onslaught difficulty/time
- Stores full character stats (HP, ATK, DEF, Crit Rate, Crit DMG, EM, ER, DMG Bonus)
- Tracks weapon name and refinement level
- Tracks talent levels with constellation bonus offsets applied
- Tracks constellation level and friendship level
- Full artifact data per character (set, slot, main stat, all substats)
- PostgreSQL relational database with SQLAlchemy ORM (characters + artifacts tables)
- Upsert logic: refreshes existing characters and artifacts on each fetch
- Modular pipeline: `enka_client` → `parsers` → `db_ops`, orchestrated by `sync`
- Character display order stabilized by insertion ID
- Flask web view with three-column card layout: character portrait, stats panel, artifact mini-cards
- Tailwind CSS with custom dark theme (void-bg, abyss-card, electro palette) and Rajdhani font
- Robust error handling for network failures, missing fetterInfo, empty affixMap, missing substats, empty showcases, and new accounts
- pytest unit tests for parsers and DB operations
- Pydantic validation on API response data

## Planned Features

- Pandas-powered artifact optimizer for maximum DPS
- Docker + AWS deployment
- Homepage with navigation

## Tech Stack

- Python 3
- PostgreSQL + psycopg2
- SQLAlchemy 2.0 (ORM)
- Flask 3.1
- Jinja2 templating
- Tailwind CSS
- Requests
- python-dotenv
- pytest
- Pydantic
- Pandas

## Project Structure

```
genshin_app/
├── app.py                  # Flask routes and web views
├── sync.py                 # Pipeline orchestrator (CLI entry point)
├── enka_client.py          # enka.network API calls
├── parsers.py              # Data extraction and transformation
├── db_ops.py               # Database insert/upsert operations
├── db.py                   # SQLAlchemy engine and session
├── models.py               # ORM models (Character, Artifact)
├── schemas.py              # Pydantic validation schemas
├── logger.py               # Root logger configuration
├── data/
│   ├── game_data.py        # Loads loc.json and character_skills.json
│   ├── character_skills.json
│   ├── loc.json
│   ├── stat_keys.py
│   └── stat_names.py
├── templates/
│   └── characters.html     # Character card UI
└── tests/
    ├── conftest.py
    ├── test_parsers.py
    └── fixtures/
        ├── sample_character.json
        └── edge_case_character.json
```

## Setup

1. Clone the repo and create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your PostgreSQL credentials:
   ```
   DB_HOST=localhost
   DB_NAME=your_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   ```
4. Run the Flask app: `python app.py`
5. Navigate to `http://localhost:5000/characters/view` and enter a Genshin UID

## Data Source

Live character data is pulled from the [enka.network](https://enka.network/) API. A custom `User-Agent` header is required per their usage guidelines.

## Known Issues

- Newer characters and weapons (Zibai, Nicole, Skirk's weapon, Furina's weapon) display as "Unknown" due to an outdated `loc.json` from the enka repo

## License

MIT
