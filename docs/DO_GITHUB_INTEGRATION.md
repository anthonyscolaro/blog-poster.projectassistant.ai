# Digital Ocean GitHub Integration Guide

## Best Solution: Use DO's Native GitHub Integration

Instead of managing DIGITALOCEAN_ACCESS_TOKEN in every repository, you can connect GitHub directly to Digital Ocean. This is the cleanest approach for personal accounts.

## Method 1: Direct GitHub Integration (Recommended)

### Step 1: Connect GitHub to Digital Ocean
1. Log into Digital Ocean: https://cloud.digitalocean.com/
2. Go to **Apps** → **Create App**
3. Choose **GitHub** as the source
4. Click **Manage Access** or **Connect to GitHub**
5. Authorize DigitalOcean to access your repositories
6. Select which repositories DO can access (you can grant access to all or specific ones)

### Step 2: Deploy Without Secrets
Once connected, you can:
- Deploy directly from GitHub without needing DIGITALOCEAN_ACCESS_TOKEN
- DO automatically deploys when you push to specified branches
- No GitHub Actions needed for basic deployments

### Step 3: Create App from GitHub
```bash
# Using doctl with GitHub integration
doctl apps create --spec .do/app-staging.yaml

# Or through the DO dashboard:
# 1. Go to Apps
# 2. Click "Create App"
# 3. Select your GitHub repo
# 4. DO will auto-detect app.yaml
```

## Method 2: Shared Secrets Script (For Multiple Repos)

If you prefer to keep using GitHub Actions, use the provided script:

```bash
# Run the setup script
./scripts/setup-do-secrets.sh

# This will:
# 1. Store your DO token securely locally
# 2. Let you add it to multiple repos easily
# 3. List which repos have the token
```

## Method 3: Environment Variables (For Local Development)

Store DO credentials in your shell profile:

```bash
# Add to ~/.zshrc or ~/.bashrc
export DIGITALOCEAN_ACCESS_TOKEN="dop_v1_xxxxx"

# For GitHub Actions, add programmatically:
gh secret set DIGITALOCEAN_ACCESS_TOKEN --body "$DIGITALOCEAN_ACCESS_TOKEN"
```

## Method 4: 1Password CLI Integration (If You Use 1Password)

If you use 1Password, you can integrate it with GitHub:

```bash
# Install 1Password CLI
brew install 1password-cli

# Store secret in 1Password
op item create --category=password --title="DO GitHub Token" --vault="Development" password="your-token"

# Reference in GitHub Actions
# Use 1Password's GitHub Action to inject secrets
```

## Comparison of Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **DO GitHub Integration** | No token needed, automatic | Less control over deployment | Simple deployments |
| **Shared Script** | Reusable across repos, secure | Need to run for each repo | Multiple personal projects |
| **Environment Variables** | Simple, works everywhere | Less secure on shared machines | Solo developers |
| **1Password** | Very secure, centralized | Requires 1Password subscription | Teams/security-focused |

## Recommended Approach

For personal projects where you own both the GitHub and Digital Ocean accounts:

1. **Use DO's native GitHub integration** for deployment
2. **Keep other secrets (API keys) in GitHub Secrets** per repository
3. **Use the script** for quickly adding API keys to multiple repos

This way:
- DO handles its own authentication
- You only manage API keys in GitHub
- Deployment is simpler and more secure

## Security Best Practices

1. **Never commit tokens** to repositories
2. **Rotate tokens regularly** (every 90 days)
3. **Use read-only tokens** where possible
4. **Limit token scope** to specific resources
5. **Use different tokens** for dev/staging/production

## Quick Setup for This Project

Since you own both accounts, the easiest approach:

1. **Connect GitHub to DO** (one-time setup):
   ```bash
   # In Digital Ocean dashboard
   Apps → Create → GitHub → Authorize
   ```

2. **Deploy without secrets**:
   ```bash
   # DO will use its GitHub integration
   doctl apps create --spec .do/app-staging.yaml
   ```

3. **Add only API keys to GitHub**:
   ```bash
   # Just add the API keys, not DO token
   gh secret set ANTHROPIC_API_KEY
   gh secret set JINA_API_KEY
   gh secret set WP_USERNAME
   gh secret set WP_APP_PASSWORD
   ```

This eliminates the need to manage DIGITALOCEAN_ACCESS_TOKEN entirely!