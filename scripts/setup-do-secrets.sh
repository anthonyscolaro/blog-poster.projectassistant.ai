#!/bin/bash

# Setup Digital Ocean secrets for GitHub repositories
# This script helps manage DO credentials across multiple repos

# Store your DO token in a secure location
DO_SECRETS_FILE="$HOME/.config/digitalocean/github-secrets"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🔐 Digital Ocean GitHub Secrets Manager"
echo "======================================="
echo ""

# Function to store secrets securely
store_secrets() {
    mkdir -p "$HOME/.config/digitalocean"
    chmod 700 "$HOME/.config/digitalocean"
    
    echo "Setting up your Digital Ocean credentials..."
    echo ""
    
    # Check if secrets file exists
    if [ -f "$DO_SECRETS_FILE" ]; then
        echo -e "${YELLOW}Existing credentials found. Loading...${NC}"
        source "$DO_SECRETS_FILE"
    else
        echo "Enter your Digital Ocean API Token:"
        read -s DO_TOKEN
        echo ""
        
        # Save to secure file
        cat > "$DO_SECRETS_FILE" << EOF
# Digital Ocean Credentials for GitHub Actions
export DIGITALOCEAN_ACCESS_TOKEN="$DO_TOKEN"
EOF
        chmod 600 "$DO_SECRETS_FILE"
        echo -e "${GREEN}✅ Credentials saved securely${NC}"
    fi
}

# Function to add secrets to a repository
add_to_repo() {
    local REPO=$1
    
    if [ -z "$REPO" ]; then
        echo "Usage: add_to_repo <owner/repo>"
        return 1
    fi
    
    # Load secrets
    if [ -f "$DO_SECRETS_FILE" ]; then
        source "$DO_SECRETS_FILE"
    else
        echo -e "${RED}No credentials found. Run 'store_secrets' first.${NC}"
        return 1
    fi
    
    echo "Adding DO token to repository: $REPO"
    
    # Use GitHub CLI to add secret
    echo "$DIGITALOCEAN_ACCESS_TOKEN" | gh secret set DIGITALOCEAN_ACCESS_TOKEN --repo "$REPO"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Secret added successfully to $REPO${NC}"
    else
        echo -e "${RED}❌ Failed to add secret to $REPO${NC}"
    fi
}

# Function to add secrets to multiple repos
add_to_multiple_repos() {
    echo "Enter repository names (one per line, format: owner/repo)"
    echo "Press Ctrl+D when done:"
    
    while IFS= read -r repo; do
        if [ ! -z "$repo" ]; then
            add_to_repo "$repo"
        fi
    done
}

# Function to list repos with the secret
list_repos_with_secret() {
    echo "Checking which of your repos have DIGITALOCEAN_ACCESS_TOKEN..."
    
    # Get all repos for the authenticated user
    gh repo list --limit 100 --json nameWithOwner -q '.[].nameWithOwner' | while read -r repo; do
        if gh secret list --repo "$repo" 2>/dev/null | grep -q "DIGITALOCEAN_ACCESS_TOKEN"; then
            echo -e "${GREEN}✓${NC} $repo"
        fi
    done
}

# Main menu
main_menu() {
    while true; do
        echo ""
        echo "What would you like to do?"
        echo "1) Store/Update DO credentials locally"
        echo "2) Add DO token to current repository"
        echo "3) Add DO token to specific repository"
        echo "4) Add DO token to multiple repositories"
        echo "5) List repositories with DO token"
        echo "6) Exit"
        echo ""
        read -p "Select option (1-6): " choice
        
        case $choice in
            1)
                store_secrets
                ;;
            2)
                # Get current repo from git
                if git remote -v 2>/dev/null | grep -q github.com; then
                    CURRENT_REPO=$(git remote -v | grep push | head -1 | sed 's/.*github.com[:/]\(.*\)\.git.*/\1/')
                    add_to_repo "$CURRENT_REPO"
                else
                    echo -e "${RED}Not in a GitHub repository${NC}"
                fi
                ;;
            3)
                read -p "Enter repository (format: owner/repo): " repo
                add_to_repo "$repo"
                ;;
            4)
                add_to_multiple_repos
                ;;
            5)
                list_repos_with_secret
                ;;
            6)
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
    done
}

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install it with: brew install gh"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI is not authenticated. Authenticating...${NC}"
    gh auth login
fi

# Run main menu
main_menu