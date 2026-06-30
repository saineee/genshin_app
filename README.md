# Genshin Build Tracker

## About

Genshin Build Tracker is a full-stack web app that fetches a player's showcased characters from the enka.network API and
displays their stats, weapons, and artifacts. A built-in artifact optimizer scores and ranks artifacts per slot based on
a selected build type, returning the best combination for that character.

Inspired by enka.network and akasha.cv after six years of playing Genshin Impact. I wanted to build something of my own
around a game I actually care about.

## Live Demo

> [Live App](http://44.204.214.240:5000)

## Features

- Card-based UI
- UID Lookup
- Showcase character details
- Showcase equipped artifacts and weapon
- Built-in artifact optimizer
- Data synced from enka.network API
- PostgreSQL persistence, all data stored across sessions
- Pydantic validation on all incoming API data
- Deployed on AWS ECS with RDS PostgreSQL backend

## Tech Stack

- **PostgreSQL**: production-ready database with support for concurrent reads/writes and native AWS RDS compatibility.
- **SQLAlchemy ORM**: maps Python models directly to database tables, handling inserts and upserts without writing raw
  SQL.
- **Pandas**: vectorized scoring across all artifacts at once, applying build formulas to entire DataFrames in a single
  operation.
- **Flask**: lightweight web framework, no unnecessary overhead for a project of this scope.
- **Pydantic**: validates and enforces types on raw API data from enka.network before it touches the database.
- **Docker**: containerizes the app for consistent local development and seamless AWS deployment.
- **AWS (ECR, ECS, RDS)**: managed cloud infrastructure. ECR stores the image, ECS with Fargate runs the container, RDS
  hosts the production database. No server management required.
- **pytest**: unit tests covering parsers and schema validation to catch bad API data early.
- **Jinja2**: server-side templating for dynamic rendering of character and artifact data.

## Running Locally

1. Clone the repo

```bash
git clone https://github.com/saineee/genshin_app.git
cd genshin_app
```

2. Create a `.env` file in the project root with your own credentials

```env
DATABASE_URL=postgresql://your_user:your_password@db:5432/your_dbname
```

> The your_user, your_password, and your_dbname can be anything. Docker will create the database using these credentials on first run.

3. Run with Docker

```bash
docker compose up --build
```

4. Visit `http://localhost:5000`

## Screenshots

### Homepage

![Homepage](screenshots/homepage.png)

### Character View

![Character View](screenshots/character_view.png)

### Optimizer

![Optimizer](screenshots/optimizer.png)