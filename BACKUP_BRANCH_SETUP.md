# 🔒 Backup Branch Setup

## Quick Status
- Fixed the workflow so it creates the `backups` branch on first run.
- Backups go to the `backups` branch under `backups/YYYY-MM-DD_HH-MM-SS/`.
- Your local `main` ignores `backups/` so you won’t be forced to pull them.

## How it works now
- The workflow:
  - Fetches `origin/backups` (or creates it if missing).
  - Creates a worktree for the `backups` branch.
  - Downloads `.enc` files into a timestamped folder.
  - Commits and pushes only to `backups` (never touches `main`).
  - Cleans up 30+ day old folders in `backups`.

## View your backups
- In GitHub: switch to the `backups` branch and browse `backups/`.
- Locally: you can fetch and check the branch without affecting `main`:
  ```bash
  git fetch origin backups
  git log --oneline origin/backups
  git show origin/backups:backups/2025-10-15_14-19-46/backup_manifest.json
  ```

## If you still get “couldn’t find remote ref”
- Make sure `RAILWAY_APP_URL` is set in GitHub secrets.
- Re-run the workflow manually; it will create the branch on first push.

## Want to mirror backups elsewhere?
- I can add a step to upload the downloaded set to a private S3 bucket or another remote.

- Implemented:
  - Secure download endpoint: `/api/download-file/<filename>` (`.enc` only, no traversal).
  - Workflow downloads files and pushes to `backups` branch.
  - Local `.gitignore` ignores `backups/` so you won’t pull them on `main`.
  - Fixed branch creation logic to avoid “invalid reference” errors.

- Next run should succeed and create `origin/backups` with your encrypted files.

