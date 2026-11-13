# fast-api

REST API for posts, users and votes with JWT authentication, built with FastAPI and PostgreSQL. It also holds the full delivery path: tests in CI, a Docker image, and AWS infrastructure defined with Terraform and Packer.

## Features

- Users, posts and votes with their CRUD endpoints (`/users`, `/posts`, `/votes`) and login (`/login`)
- JWT authentication (OAuth2 password flow) and password hashing with bcrypt
- Database models with SQLModel and migrations with Alembic
- Tests with pytest (`tests/`)
- CI with GitHub Actions: runs the tests against a PostgreSQL service and publishes the Docker image to Docker Hub from `main`
- Golden AMI pattern: Packer builds an Ubuntu image with Docker, the AWS CLI and a systemd unit; Terraform deploys it on EC2, creates the SSM parameters for the app settings and gives the instance a role to read them

## Stack

| Layer | Technology |
|---|---|
| API | Python 3.13, FastAPI, SQLModel |
| Database | PostgreSQL, Alembic |
| Tests | pytest |
| Container | Docker, Docker Compose |
| CI/CD | GitHub Actions, Docker Hub |
| Infrastructure | Terraform (EC2, security group, IAM role, SSM parameters), Packer |

## Requirements

- Python 3.13 and a PostgreSQL database, or Docker with Compose

## Setup and usage

```bash
git clone https://github.com/netfoor/fast-api.git
cd fast-api
cp .env.example .env   # fill in the database URL and the JWT settings
docker compose -f docker-compose-dev.yml up --build
```

The API listens on port 8000, and FastAPI serves the interactive docs at `/docs`.

Without Docker:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tests:

```bash
pytest tests/
```

## Deployment

- CI runs the tests on every push and pull request. Publishing the image to Docker Hub and triggering the Render deploy run only when the workflow is started manually (`workflow_dispatch`), and need the `DOCKER_USERNAME`, `DOCKER_ACCESS_TOKEN` and `DEPLOY_HOOK_URL` secrets.
- `docker-compose-prod.yml` runs the image published by that job.
- `infra/packer/` builds the base image and `infra/envs/dev/` deploys it with Terraform. The Terraform code expects an AMI that Packer already built.

## Notes

- `DOCUMENTATION.MD` holds study notes about Python, async and FastAPI.
- `requirements.txt` is saved as UTF-16; some tools may need it converted to UTF-8.

## Status

Learning project. It has no active deployment: the Render service that used it is suspended.

## License

MIT
