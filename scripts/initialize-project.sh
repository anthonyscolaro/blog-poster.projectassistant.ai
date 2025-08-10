#!/bin/bash

# ============================================================================
# Project Initialization Script for Context Engineering Projects
# ============================================================================
# This script sets up a new project from the context-engineering-template
# Including git workflow, project structure, and initial configuration
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${2}${1}${NC}\n"
}

# Function to print section headers
print_header() {
    echo ""
    print_color "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "$CYAN"
    print_color "  $1" "$CYAN"
    print_color "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "$CYAN"
    echo ""
}

# ASCII Art Banner
show_banner() {
    print_color "╔══════════════════════════════════════════════════════════════╗" "$BLUE"
    print_color "║                                                              ║" "$BLUE"
    print_color "║     Context Engineering Project Initialization              ║" "$BLUE"
    print_color "║     Enhanced Template with LocalDocs Integration            ║" "$BLUE"
    print_color "║                                                              ║" "$BLUE"
    print_color "╚══════════════════════════════════════════════════════════════╝" "$BLUE"
    echo ""
}

# Function to get project information
get_project_info() {
    print_header "Project Information"
    
    # Get project name
    read -p "Enter project name (lowercase, hyphens allowed): " PROJECT_NAME
    while [[ ! "$PROJECT_NAME" =~ ^[a-z0-9-]+$ ]]; do
        print_color "Invalid name. Use lowercase letters, numbers, and hyphens only." "$RED"
        read -p "Enter project name: " PROJECT_NAME
    done
    
    # Get project description
    read -p "Enter project description: " PROJECT_DESCRIPTION
    
    # Get project type
    print_color "\nSelect project type:" "$YELLOW"
    echo "1) Web Application (Next.js, React, Vue)"
    echo "2) API Service (FastAPI, Express, etc.)"
    echo "3) NPM Package/CLI Tool"
    echo "4) Mobile Application"
    echo "5) Monorepo"
    echo "6) Other/Generic"
    
    read -p "Enter choice (1-6): " PROJECT_TYPE_CHOICE
    
    case $PROJECT_TYPE_CHOICE in
        1) PROJECT_TYPE="web" ;;
        2) PROJECT_TYPE="api" ;;
        3) PROJECT_TYPE="npm" ;;
        4) PROJECT_TYPE="mobile" ;;
        5) PROJECT_TYPE="monorepo" ;;
        *) PROJECT_TYPE="web" ;;
    esac
    
    print_color "\n✓ Project: $PROJECT_NAME" "$GREEN"
    print_color "✓ Type: $PROJECT_TYPE" "$GREEN"
    print_color "✓ Description: $PROJECT_DESCRIPTION" "$GREEN"
}

# Function to initialize git repository
init_git_repo() {
    print_header "Git Repository Setup"
    
    if [ -d ".git" ]; then
        print_color "Git repository already exists" "$YELLOW"
    else
        print_color "Initializing git repository..." "$YELLOW"
        git init
        print_color "✓ Git repository initialized" "$GREEN"
    fi
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << 'EOF'
# Dependencies
node_modules/
venv/
env/
*.pyc
__pycache__/

# Environment
.env
.env.local
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Build outputs
dist/
build/
*.egg-info/
.next/
out/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/
.coverage
.pytest_cache/

# LocalDocs
docs/.localdocs-cache/

# Research (sensitive data)
research/**/*.json
research/**/*-api-key*
research/**/*-secret*
EOF
        print_color "✓ .gitignore created" "$GREEN"
    fi
}

# Function to setup git workflow using LocalDocs
setup_git_workflow() {
    print_header "Git Workflow Setup"
    
    print_color "Setting up git branches..." "$YELLOW"
    
    # Create branches
    local current_branch=$(git branch --show-current || echo "main")
    
    # Create dev branch if it doesn't exist
    if ! git show-ref --verify --quiet refs/heads/dev; then
        git checkout -b dev
        print_color "✓ dev branch created" "$GREEN"
    else
        print_color "✓ dev branch exists" "$GREEN"
    fi
    
    # Create staging branch if it doesn't exist
    if ! git show-ref --verify --quiet refs/heads/staging; then
        git checkout -b staging
        print_color "✓ staging branch created" "$GREEN"
    else
        print_color "✓ staging branch exists" "$GREEN"
    fi
    
    # Return to main/original branch
    git checkout main 2>/dev/null || git checkout "$current_branch"
    
    # Create .github directory
    mkdir -p .github
    
    # Create PR template
    print_color "Creating PR template..." "$YELLOW"
    cat > .github/pull_request_template.md << 'EOF'
## Description
Brief description of changes

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change)
- [ ] ✨ New feature (non-breaking change)
- [ ] 💥 Breaking change
- [ ] 📝 Documentation update
- [ ] ♻️ Refactoring
- [ ] ✅ Test update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated

## Related Issues
Closes #
EOF
    
    print_color "✓ Git workflow configured" "$GREEN"
    print_color "  Note: To get the full workflow documentation, run:" "$CYAN"
    print_color "  npx github:anthonyscolaro/localdocs export .github --include git-workflow" "$CYAN"
}

# Function to customize project files
customize_project_files() {
    print_header "Customizing Project Files"
    
    # Update README.md
    if [ -f "README.md" ]; then
        print_color "Updating README.md..." "$YELLOW"
        
        # Create a new README with project info
        cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESCRIPTION

## 🚀 Quick Start

This project was created from the [Context Engineering Template Enhanced](https://github.com/anthonyscolaro/context-engineering-template-enhanced).

### Setup

\`\`\`bash
# Install dependencies (if applicable)
npm install  # or pip install -r requirements.txt

# Start development
npm run dev  # or your start command
\`\`\`

## 📁 Project Structure

\`\`\`
$PROJECT_NAME/
├── .claude/          # Claude AI configuration
├── PRPs/            # Product Requirement Prompts
├── research/        # Jina-scraped documentation
├── docs/           # LocalDocs collections
├── memory/         # Project knowledge base
└── .github/        # Git workflow and templates
\`\`\`

## 🌳 Git Workflow

This project follows a standardized git workflow:
- **main** - Production/stable code
- **staging** - Pre-production testing
- **dev** - Active development

See \`.github/GIT_WORKFLOW.md\` for complete details.

## 📚 Documentation

- **CLAUDE.md** - AI assistant instructions
- **RESEARCH_GUIDE.md** - Research workflow
- **LOCALDOCS_GUIDE.md** - LocalDocs usage
- **PORT_ALLOCATION_STRATEGY.md** - Port management

## 🤝 Contributing

1. Create feature branch from \`dev\`
2. Make changes with conventional commits
3. Submit PR following template
4. See \`.github/GIT_WORKFLOW.md\` for details

---

Created with Context Engineering Template Enhanced
EOF
        print_color "✓ README.md updated" "$GREEN"
    fi
    
    # Update CLAUDE.md with project name
    if [ -f "CLAUDE.md" ]; then
        sed -i.bak "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || \
        sed -i '' "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || true
        rm -f CLAUDE.md.bak
        print_color "✓ CLAUDE.md customized" "$GREEN"
    fi
    
    # Create initial project configuration
    cat > project.config.json << EOF
{
  "name": "$PROJECT_NAME",
  "type": "$PROJECT_TYPE",
  "description": "$PROJECT_DESCRIPTION",
  "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "template": "context-engineering-template-enhanced",
  "version": "1.0.0",
  "git": {
    "workflow": "main-staging-dev",
    "conventionalCommits": true
  },
  "localdocs": {
    "enabled": true,
    "collections": []
  }
}
EOF
    print_color "✓ project.config.json created" "$GREEN"
}

# Function to setup LocalDocs
setup_localdocs() {
    print_header "LocalDocs Configuration"
    
    print_color "Setting up LocalDocs for documentation management..." "$YELLOW"
    
    # Create LocalDocs directories
    mkdir -p docs/api-collections
    mkdir -p docs/deployment-workflows
    mkdir -p docs/infrastructure-guides
    
    # Update or create localdocs.config.json
    cat > localdocs.config.json << EOF
{
  "project": "$PROJECT_NAME",
  "collections": {
    "api-docs": {
      "path": "docs/api-collections",
      "format": "claude"
    },
    "deployment": {
      "path": "docs/deployment-workflows",
      "format": "standard"
    },
    "infrastructure": {
      "path": "docs/infrastructure-guides",
      "format": "standard"
    }
  },
  "export": {
    "defaultFormat": "claude",
    "includeMetadata": true
  }
}
EOF
    
    print_color "✓ LocalDocs configured" "$GREEN"
    print_color "  Use 'npx github:anthonyscolaro/localdocs' to manage docs" "$CYAN"
}

# Function to create initial commit
create_initial_commit() {
    print_header "Creating Initial Commit"
    
    print_color "Staging all files..." "$YELLOW"
    git add -A
    
    print_color "Creating initial commit..." "$YELLOW"
    git commit -m "feat: initialize $PROJECT_NAME from context engineering template

- Set up project structure
- Configure git workflow (main/staging/dev)
- Initialize LocalDocs integration
- Add project documentation
- Configure Claude AI instructions

Project type: $PROJECT_TYPE
Template: context-engineering-template-enhanced"
    
    print_color "✓ Initial commit created" "$GREEN"
}

# Function to show next steps
show_next_steps() {
    print_header "✅ Setup Complete!"
    
    print_color "Your project '$PROJECT_NAME' has been initialized!" "$GREEN"
    echo ""
    print_color "Next steps:" "$YELLOW"
    echo ""
    print_color "1. Review and customize:" "$CYAN"
    echo "   - .github/GIT_WORKFLOW.md (git workflow)"
    echo "   - CLAUDE.md (AI instructions)"
    echo "   - RESEARCH_GUIDE.md (research process)"
    echo ""
    print_color "2. Set up remote repository:" "$CYAN"
    echo "   git remote add origin <your-repo-url>"
    echo "   git push -u origin main"
    echo "   git push --all origin"
    echo ""
    print_color "3. Configure branch protection in GitHub/GitLab" "$CYAN"
    echo ""
    print_color "4. Start development:" "$CYAN"
    echo "   git checkout dev"
    echo "   git checkout -b feature/your-first-feature"
    echo ""
    print_color "5. Add documentation with LocalDocs:" "$CYAN"
    echo "   npx github:anthonyscolaro/localdocs add <doc-url>"
    echo ""
    print_color "Happy coding! 🚀" "$MAGENTA"
}

# Main execution
main() {
    clear
    show_banner
    
    # Check if we're in the template directory (should not run here)
    if [ -f "QUICKSTART.md" ] && grep -q "context-engineering-template-enhanced" README.md 2>/dev/null; then
        print_color "⚠️  Warning: This appears to be the template repository itself!" "$YELLOW"
        print_color "This script should be run in a NEW project created from the template." "$YELLOW"
        echo ""
        read -p "Continue anyway? (y/N): " CONTINUE
        if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
            print_color "Initialization cancelled." "$RED"
            exit 0
        fi
    fi
    
    # Run initialization steps
    get_project_info
    init_git_repo
    setup_git_workflow
    customize_project_files
    setup_localdocs
    create_initial_commit
    show_next_steps
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi