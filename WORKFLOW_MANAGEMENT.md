# Workflow Management with LocalDocs

This template uses LocalDocs for centralized workflow management. Instead of storing workflows in each project, they're maintained centrally and exported as needed.

## 🎯 Philosophy

**Single Source of Truth**: All workflows (git, deployment, testing, etc.) are maintained in LocalDocs and exported to projects when needed. This ensures:
- Consistency across all projects
- Easy updates (update once, export everywhere)
- Version control of workflow evolution
- No duplication or drift between projects

## 📚 Available Workflows

These workflows are available via LocalDocs:

### Git Workflows
- **git-workflow-standard** - Main/staging/dev branching strategy
- **commit-conventions** - Conventional commits guide
- **pr-templates** - Pull request templates

### Deployment Workflows
- **docker-deployment** - Docker best practices
- **kubernetes-deployment** - K8s deployment guides
- **ci-cd-github** - GitHub Actions workflows

### Development Workflows
- **code-review** - Code review guidelines
- **testing-strategy** - Testing best practices
- **documentation-standards** - Documentation guidelines

## 🚀 Using Workflows

### 1. Add Workflows to LocalDocs (One-Time Setup)

First, add the workflow documents to your LocalDocs collection:

```bash
# Add git workflow documentation
npx github:anthonyscolaro/localdocs add \
  https://raw.githubusercontent.com/anthonyscolaro/servicedogus.org/main/temp-workflows/git-workflow-standard.md

# Add other workflows as needed
npx github:anthonyscolaro/localdocs add \
  https://example.com/workflows/docker-deployment.md \
  https://example.com/workflows/testing-strategy.md
```

### 2. Name and Tag Workflows

Organize your workflows in LocalDocs:

```bash
# Set meaningful names for workflows
npx github:anthonyscolaro/localdocs set a1b2c3d4 \
  -n "git-workflow-standard" \
  -d "Standardized git branching strategy" \
  -t "git,workflow,branching"

npx github:anthonyscolaro/localdocs set e5f6g7h8 \
  -n "commit-conventions" \
  -d "Conventional commits guide" \
  -t "git,commits,conventions"
```

### 3. Export to Projects

When setting up a new project or updating workflows:

```bash
# Export git workflow to project
npx github:anthonyscolaro/localdocs export .github \
  --include git-workflow-standard,commit-conventions \
  --format standard

# Export all workflows for reference
npx github:anthonyscolaro/localdocs export docs/workflows \
  --format toc
```

### 4. Update Workflows

When workflows change, update them centrally:

```bash
# Update specific workflow
npx github:anthonyscolaro/localdocs update a1b2c3d4

# Re-export to project
npx github:anthonyscolaro/localdocs export .github \
  --include git-workflow-standard \
  --overwrite
```

## 📋 Project Setup Flow

When initializing a new project from this template:

1. **Run initialization script** - Sets up branches and basic structure
2. **Export workflows from LocalDocs** - Get latest workflow docs
3. **Customize as needed** - Adjust for project-specific needs
4. **Commit workflow docs** - Include in project repository

Example:
```bash
# 1. Initialize project
./scripts/initialize-project.sh

# 2. Export workflows
npx github:anthonyscolaro/localdocs export .github \
  --include git-workflow-standard,pr-templates

# 3. Review and customize
cat .github/git-workflow-standard.md
# Edit if needed for project-specific requirements

# 4. Commit
git add .github/
git commit -m "docs: add workflow documentation from LocalDocs"
```

## 🔄 Keeping Workflows Updated

### For Individual Projects

```bash
# Check for updates
npx github:anthonyscolaro/localdocs list

# Update and re-export
npx github:anthonyscolaro/localdocs update
npx github:anthonyscolaro/localdocs export .github --overwrite
```

### For All Projects (Batch Update)

Create a script to update all projects:

```bash
#!/bin/bash
# update-all-workflows.sh

PROJECTS=(
  ~/apps/project1
  ~/apps/project2
  ~/apps/project3
)

for project in "${PROJECTS[@]}"; do
  echo "Updating workflows in $project"
  cd "$project"
  npx github:anthonyscolaro/localdocs export .github \
    --include git-workflow-standard \
    --overwrite
  git add .github/
  git commit -m "docs: update workflows from LocalDocs"
done
```

## 🎨 Customization

While workflows are standardized, projects may need customization:

1. **Export the base workflow** from LocalDocs
2. **Create project-specific overrides** in separate files
3. **Document the differences** clearly

Example structure:
```
.github/
├── git-workflow-standard.md    # From LocalDocs (don't edit)
├── git-workflow-overrides.md   # Project-specific changes
└── README.md                    # Explains the combination
```

## 🚨 Important Notes

### Don't Store Workflows in Templates

This template should NOT contain workflow documents. Instead:
- The initialization script sets up basic structure
- Users export workflows from LocalDocs after initialization
- This ensures everyone gets the latest versions

### LocalDocs as Source of Truth

All workflow updates should:
1. Be made in the source documents
2. Added/updated in LocalDocs
3. Exported to projects as needed

Never edit workflow docs directly in projects unless they're project-specific overrides.

### Version Control

While LocalDocs doesn't version documents, you can:
- Tag workflow updates with dates
- Keep a changelog in LocalDocs
- Use git history in the source repository

## 📚 Resources

- **LocalDocs**: https://github.com/anthonyscolaro/localdocs
- **Workflow Sources**: Store in a GitHub repository or Gist
- **Team Sharing**: Use shared LocalDocs config or export collections

## 💡 Best Practices

1. **Regular Updates**: Check for workflow updates monthly
2. **Team Alignment**: Ensure all team members use same workflows
3. **Documentation**: Keep workflows well-documented and current
4. **Automation**: Use scripts to automate workflow distribution
5. **Feedback Loop**: Update workflows based on team experience

---

**Remember**: Workflows are living documents. Use LocalDocs to keep them current and consistent across all projects!