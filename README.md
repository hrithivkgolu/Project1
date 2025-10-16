# GitHub repo creator API (FastAPI) — Vercel-ready

This project provides a tiny FastAPI app that can be deployed to Vercel. It exposes a single POST endpoint `/api/create-repo` which accepts a JSON payload describing a GitHub repository to create and the files to add.

Environment
- Set `GITHUB_TOKEN` in Vercel environment variables (or locally) to a personal access token with `repo` scope (or `org` scope for organization repos).

Deploy
- Push this repository to Git (or connect to Vercel) and deploy. Vercel will detect the Python function at `api/create_repo.py`.

Example payload

{
  "name": "my-app",
  "description": "Created by API",
  "private": true,
  "init_readme": true,
  "files": {"app.py": "print(\"hello\")"}
}

Security notes
- Don't commit secrets. Use Vercel's dashboard to add `GITHUB_TOKEN`.
- The API will create repositories under the token owner's account or in an organization if `org` is provided.
