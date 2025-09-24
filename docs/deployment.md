# Deployment Guide

This document explains how to deploy the project in different environments: local development, staging, and production.

## 1. Prerequisites

Before deploying, ensure you have the following installed:

- **Node.js** (LTS recommended)
- **npm** or **yarn**
- **Git**
- **Docker** (optional for containerized deployment)
- **Supabase account** ([https://supabase.com](https://supabase.com))

## 2. Environment Setup

All environment variables are stored in a `.env` file (not committed to Git).

**Example `.env`:**

```env
# Server
PORT=3000
NODE_ENV=development

# Supabase
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
```

⚠️ **Never commit `.env` files to version control.** Instead, use environment-specific configs or CI/CD secrets management.

## 3. Local Deployment

Clone the repository:

```sh
git clone https://github.com/your-org/your-project.git
cd your-project
```

Install dependencies:

```sh
npm install
```

Create a `.env` file (as shown above).

Start the server:

```sh
npm run dev
```

Access the API at:

```sh
http://localhost:3000
```

## 4. Supabase Setup

- Create a new Supabase project.
- Copy the Project URL and Anon Key from the dashboard.
- Paste them into your `.env` file under `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
- (Optional) For backend-only operations, also use the `SUPABASE_SERVICE_ROLE_KEY`.
- Set up your database schema in Supabase via SQL editor or migrations.

## 5. Production Deployment Options

### Option A: Deploy on Railway.app

- Connect your GitHub repository.
- Add environment variables in the Railway dashboard.
- Railway will auto-build and deploy on pushes to main.

### Option B: Deploy on Render.com

- Create a new Web Service.
- Connect your GitHub repo.
- Add environment variables in Render dashboard.
- Deploy service.

### Option C: Deploy with Docker

Build Docker image:

```sh
docker build -t my-app .
```

Run container:

```sh
docker run -d -p 3000:3000 --env-file .env my-app
```

## 6. CI/CD Setup (Optional)

Configure GitHub Actions, GitLab CI, or other CI/CD to:

- Run tests on push.
- Deploy automatically on main branch.
- Store `.env` values in your CI/CD secret manager.

## 7. Post Deployment

- Monitor logs:

  ```sh
  npm run logs
  ```

- Health check endpoint: `/health`
- Secure your environment variables.
- Rotate Supabase service keys regularly.
