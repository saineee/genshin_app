# Genshin Build Tracker

## About

Genshin Build Tracker is a full-stack web app that fetches a player's showcased characters from the enka.network API and
displays their stats, weapons, and artifacts. A built-in artifact optimizer scores and ranks artifacts per slot based on
a selected build type, returning the best combination for that character.

Inspired by enka.network and akasha.cv after six years of playing Genshin Impact. I wanted to build something of my own
around a game I actually care about.

The app itself is finished, but the infrastructure layer is continuously updated. 

## Live Demo

> [Live App](http://13.218.149.143:5000)

The task runs on Fargate with a public IP and no load balancer in front of it, so that address changes every time the
service redeploys. If the link is dead, the screenshots below are the same thing. Putting an ALB in front would solve the issue, as would an elastic ip, but the cost is not worth it.

## Features

- Card-based UI
- UID lookup
- Showcase character details
- Showcase equipped artifacts and weapon
- Built-in artifact optimizer
- Data synced from the enka.network API
- PostgreSQL persistence, all data stored across sessions
- Deployed on AWS ECS Fargate with an RDS PostgreSQL backend
- Infrastructure managed in Terraform
- CI/CD on every merge to master, with automatic rollback on a failed deployment

## Tech Stack

- **PostgreSQL**: production-ready database with support for concurrent reads/writes and native AWS RDS compatibility.
- **SQLAlchemy ORM**: maps Python models directly to database tables, handling all inserts and upserts without raw SQL.
- **Pandas**: vectorized scoring across all artifacts at once, applying build formulas to entire DataFrames instantly.
- **Flask**: lightweight web framework, no unnecessary overhead for a project of this size.
- **Gunicorn**: the actual WSGI server in front of Flask.
- **Pydantic**: validates and enforces types on raw API data.
- **Docker**: containerizes the app for consistent local development and seamless AWS deployment.
- **Terraform**: every AWS resource this project owns is defined in code.
- **AWS (ECR, ECS, RDS, SSM, CloudWatch)**: managed cloud infrastructure. ECR stores the image, ECS with Fargate runs the
  container, RDS hosts the production database, Parameter Store holds the database credentials, CloudWatch holds the
  logs.
- **pytest**: unit tests covering parsers and schema validation to catch bad API data early.
- **Jinja2**: server-side templating for dynamic rendering of character and artifact data.
- **GitHub Actions**: tests and Terraform plans on every pull request, ships to ECS on merge to master. It logs into AWS
  with OIDC, so there are no AWS keys sitting in the repo or in GitHub secrets.

## Infrastructure

Fourteen resources in Terraform, with S3 remote state and native S3 locking. The state bucket was created by manually, 
because Terraform cannot manage the bucket that stores its own state.

Terraform doesn't own the task definition. The pipeline registers a new revision on every deploy, so if Terraform
managed it, every deploy would show up as drift. The ECS service is managed with `ignore_changes` on that one field:
Terraform owns everything except which revision is currently deployed.

`DATABASE_URL` is not in the task definition. It lives in SSM Parameter Store as a SecureString and is injected
into the container at startup. It is not in the repo, not in the task definition, and not in Terraform state. The
password is set with a write-only argument, so Terraform sends it to AWS without storing it.

There are three IAM roles, each doing exactly one job. `GHAuth` is used by the deploy job on master and can only push
to this one ECR repo and update this one ECS service. `genshin-task-exec-role` is used by the running container and can
only read `/genshin/*` from Parameter Store and write logs. `ciPlanRole` is used by the plan job on pull requests and
can only read.

The task execution role is dedicated rather than the account-wide `ecsTaskExecutionRole`, because that shared role is
also used by another project, and adding the secret read permission to it would have let an unrelated app read this database's
password.

The database is not reachable from the internet. It has no public IP, and its security group accepts traffic on 5432
only from the application's security group, by identity rather than by address, so Fargate's changing IPs do not matter.
Storage is also encrypted at rest.

The container runs as an unprivileged user and cannot write to its own application directory.

## CI/CD

Merging to `master` deploys the app on its own.

1. **Compile and test**: `compileall` parses every Python file, then pytest runs. The compile step exists because nothing
   imports `app.py` in tests, so a syntax error there would otherwise reach prod.
2. **Authenticate**: the runner asks GitHub for a signed token and trades it to AWS for credentials that expire in an
   hour.
3. **Build and push**: the image goes up to ECR tagged with the commit SHA, so I can always tell exactly which code is
   running in a container. A lifecycle policy expires everything past the last ten images.
4. **Deploy**: it pulls the live task definition, swaps in the new image, registers it as a new revision, and points the
   service at it.

A failed deployment rolls itself back. The container has a health check, and the service has a deployment circuit
breaker with rollback enabled. A container that starts but cannot serve fails its check, fails the deployment, and ECS
returns the service to the previous working revision.

Pull requests run the tests and a `terraform plan`, so an infrastructure change shows its full diff in the checks before
anyone merges it. There is deliberately no `terraform apply` in the CI. Applying would require permission to create IAM roles, and a
role that can create IAM roles can grant itself anything.

The AWS trust policies are pinned to the OIDC subject claim, so the deploy role only accepts tokens from master and the
plan role only accepts tokens from pull requests. Neither can be assumed from anywhere else on GitHub.

Merges that only touch the README/Docs, Terraform, or the compose file skip the build entirely, since there is nothing new to
put in an image.

## Running Locally

1. Clone the repo

```bash
git clone https://github.com/saineee/genshin_app.git
cd genshin_app
```

2. Copy the example environment file and fill it in

```bash
cp .env.example .env
```

`POSTGRES_PASSWORD` can be anything; Docker creates the local database with it on first run. `DATABASE_URL` is only
needed if you want to run pytest or `sync.py` directly on your machine rather than through Compose.

3. Run with Docker

```bash
docker compose up --build
```

4. Visit `http://localhost:5000`

To load data, enter a Genshin UID with a public character showcase.

## Screenshots

### Homepage

![Homepage](screenshots/homepage.png)

### Character View

![Character View](screenshots/character_view.png)

### Optimizer

![Optimizer](screenshots/optimizer.png)

## Cost

All the infra runs in us-east-1 and costs about 13 dollars a month.

Fargate is most of it, roughly 9 dollars for a 0.25 vCPU task with 0.5 GB of memory running 24/7. The task's public IP is
another $3.65. ECR storage is almost nothing and stays low because of the lifecycle policy. CloudWatch Logs is
under a megabyte with 14-day retention. Parameter Store's standard tier and the AWS-managed encryption keys are free.

The database is a db.t3.micro with 20 GB, which would run about 15 dollars on its own but is free for the first year, so the
real cost is closer to 28 dollars once the free tier expires.

If this ever had real users, the first two things I would change are a load balancer in front of the task instead of
a public IP on it, and a schedule that shuts the service down overnight.

## Known Limitations

These are deliberate or known, not undiscovered.

- Pydantic only validates the CLI path. `sync.py` validates through `schemas.py`. the web route at `/characters`
  doesn't. The two write paths differ on purpose (the CLI inserts and skips duplicates, the web route upserts), but
  only one of them is validated.
- Nothing imports `app.py` in tests. It calls `create_all` at import, so it cannot be imported without a live
  database, which means the web entrypoint has no test coverage at all. The `compileall` step in CI catches syntax
  errors there and nothing more.
- No database migrations. Schema is created with `create_all` at startup, so changing a model on an existing
  database needs manual DDL.
- The optimizer ignores set bonuses. It picks the highest-scoring artifact per slot independently, which is not the
  same as the best five-piece combination.
- One task, so no load balancer. The public IP changes on every deployment, and a deployment is a brief interruption.
- The health check only proves the app is serving users, not that the database is reachable. The route it hits renders a
  static template.

## License

**MIT**
