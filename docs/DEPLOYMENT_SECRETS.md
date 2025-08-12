# Deployment Secrets Configuration Guide

## GitHub Secrets Required

To enable automated deployment to Digital Ocean, you need to configure the following secrets in your GitHub repository:

### 1. Navigate to GitHub Repository Settings
1. Go to your repository: https://github.com/anthonyscolaro/blog-poster
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### 2. Required GitHub Secrets

Add each of these secrets:

#### `DIGITALOCEAN_ACCESS_TOKEN` (Required)
- **Description**: Your Digital Ocean API token for deployment
- **How to get it**:
  1. Log into Digital Ocean
  2. Go to **API** → **Tokens/Keys**
  3. Click **Generate New Token**
  4. Name it "blog-poster-deployment"
  5. Select **Write** scope
  6. Copy the token (you won't see it again!)

#### `ANTHROPIC_API_KEY` (Required for article generation)
- **Description**: Claude API key for content generation
- **How to get it**:
  1. Go to https://console.anthropic.com/
  2. Navigate to **API Keys**
  3. Create a new key or use existing
  4. Copy the key starting with `sk-ant-`

#### `OPENAI_API_KEY` (Optional - fallback)
- **Description**: OpenAI API key as fallback
- **How to get it**:
  1. Go to https://platform.openai.com/api-keys
  2. Create new secret key
  3. Copy the key starting with `sk-`

#### `JINA_API_KEY` (Required for web scraping)
- **Description**: Jina AI key for competitor monitoring
- **How to get it**:
  1. Go to https://jina.ai/
  2. Sign up/login
  3. Go to API section
  4. Generate API key
  5. Copy the key starting with `jina_`

#### `WP_USERNAME` (Required for WordPress)
- **Description**: WordPress admin username
- **Value**: Your WordPress admin username

#### `WP_APP_PASSWORD` (Required for WordPress)
- **Description**: WordPress application password
- **How to get it**:
  1. Log into WordPress admin
  2. Go to **Users** → **Profile**
  3. Scroll to **Application Passwords**
  4. Enter name: "blog-poster"
  5. Click **Add New Application Password**
  6. Copy the generated password (spaces included)

## Digital Ocean App Platform Secrets

After the app is created, you'll need to set these in the DO dashboard:

### 1. Navigate to App Settings
1. Go to https://cloud.digitalocean.com/apps
2. Click on your app: **blog-poster-staging**
3. Go to **Settings** tab
4. Click on **App-Level Environment Variables**

### 2. Add Secret Environment Variables

Click **Edit** and add these as **Encrypted** (secret) variables:

```yaml
ANTHROPIC_API_KEY: sk-ant-api03-...
OPENAI_API_KEY: sk-...
JINA_API_KEY: jina_...
WP_USERNAME: your-wordpress-username
WP_APP_PASSWORD: xxxx xxxx xxxx xxxx xxxx xxxx
API_ENCRYPTION_KEY: (generate a random 32-char string)
```

### 3. Generate API Encryption Key
```bash
# Generate a secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Workflow

### Automatic Deployment (GitHub Actions)

Once secrets are configured:

1. **Push to `dev` branch** → Automatically deploys to staging
2. **Push to `main` branch** → Automatically deploys to production (if configured)

The GitHub Action will:
- Run tests
- Build Docker image
- Push to DO Container Registry
- Deploy to App Platform
- Run smoke tests

### Manual Deployment (CLI)

If you prefer manual deployment:

```bash
# Using doctl CLI
doctl apps create --spec .do/app-staging.yaml

# Update existing app
APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "blog-poster-staging" | awk '{print $1}')
doctl apps update $APP_ID --spec .do/app-staging.yaml
```

## Verification Checklist

After setting up secrets, verify:

- [ ] GitHub Actions tab shows green checkmark after push
- [ ] Digital Ocean Apps dashboard shows "Deployed"
- [ ] Health check passes: `curl https://your-app.ondigitalocean.app/health`
- [ ] Can access dashboard: `https://your-app.ondigitalocean.app/dashboard`
- [ ] Pipeline status works: `https://your-app.ondigitalocean.app/pipeline`
- [ ] WordPress connection test passes

## Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs
2. Verify all secrets are set correctly
3. Check DO App Platform logs: `doctl apps logs <app-id>`

### Database Connection Issues
- DATABASE_URL is automatically set by DO
- Check if database is running: DO Dashboard → Databases

### WordPress Connection Fails
- Verify WP_APP_PASSWORD is correct (include spaces)
- Check WP_VERIFY_SSL setting (may need `false` for staging)
- Ensure WordPress URL is accessible

### API Key Issues
- Verify keys are active in respective dashboards
- Check rate limits haven't been exceeded
- Ensure billing is active on API accounts

## Security Best Practices

1. **Rotate secrets regularly** (every 90 days)
2. **Use different keys for staging/production**
3. **Never commit secrets to repository**
4. **Use encrypted variables in DO**
5. **Restrict API key permissions** where possible
6. **Monitor usage** for unusual activity

## Cost Monitoring

Estimated monthly costs:
- Digital Ocean App (staging): $11/month
  - App: $4/month (basic-xxs)
  - Database: $7/month (dev tier)
- API Usage (varies):
  - Anthropic: ~$0.50-2.00 per article
  - Jina: Free tier usually sufficient
  - OpenAI: ~$0.30-1.00 per article (if used)

Set up billing alerts in each service to avoid surprises!