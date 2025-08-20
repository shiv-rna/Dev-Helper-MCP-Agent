# Git Cheatsheet & Best Practices

## Table of Contents
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Conventions](#commit-message-conventions)
- [Tagging Strategy](#tagging-strategy)
- [Workflow Commands](#workflow-commands)
- [Phase-Based Development](#phase-based-development)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Troubleshooting](#troubleshooting)

---

## Branch Naming Conventions

### Feature Branches
```
feature/phase-{version}-{description}
```

**Examples:**
- `feature/phase-1.1-dynamic-query-formation`
- `feature/phase-1.2-enhanced-search-integration`
- `feature/phase-2.1-github-trending-integration`
- `feature/phase-3.1-langsmith-integration`
- `feature/phase-4.1-mcp-server-implementation`

### Other Branch Types
```
hotfix/{description}           # Critical bug fixes
bugfix/{description}           # Regular bug fixes
docs/{description}             # Documentation updates
chore/{description}            # Maintenance tasks
refactor/{description}         # Code refactoring
test/{description}             # Test-related changes
```

---

## Commit Message Conventions

### Conventional Commits Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types
| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: implement Serper API integration` |
| `fix` | Bug fix | `fix: resolve search query formation issue` |
| `docs` | Documentation | `docs: update PRD with Phase 1.2 details` |
| `style` | Code style changes | `style: format code according to PEP8` |
| `refactor` | Code refactoring | `refactor: extract query builder logic` |
| `test` | Adding tests | `test: add unit tests for search integration` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `perf` | Performance improvements | `perf: optimize search response time` |
| `ci` | CI/CD changes | `ci: add GitHub Actions workflow` |
| `build` | Build system changes | `build: update pyproject.toml` |

### Examples
```bash
# Feature commits
git commit -m "feat: implement Phase 1.1 - Dynamic Query Formation"
git commit -m "feat(search): add Serper API as fallback search provider"

# Bug fixes
git commit -m "fix: resolve query classification accuracy issue"
git commit -m "fix(search): handle API rate limiting gracefully"

# Documentation
git commit -m "docs: update PRD with Phase 1.2 acceptance criteria"
git commit -m "docs: add API integration examples"

# Maintenance
git commit -m "chore: update .gitignore with comprehensive patterns"
git commit -m "chore: bump dependencies to latest versions"

# Tests
git commit -m "test: add integration tests for Serper API"
git commit -m "test: cover query builder edge cases"
```

---

## Tagging Strategy

### Semantic Versioning Tags
```
v{major}.{minor}.{patch}
```

**Examples:**
- `v1.0.0` - Initial release
- `v1.1.0` - Phase 1.1 completion
- `v1.2.0` - Phase 1.2 completion
- `v1.2.1` - Bug fix after Phase 1.2

### Phase Completion Tags
```
phase-{version}-{description}
```

**Examples:**
- `phase-1.1-dynamic-query-formation`
- `phase-1.2-enhanced-search-integration`
- `phase-2.1-github-trending-integration`

### Creating Tags
```bash
# Annotated tag (recommended)
git tag -a v1.1.0 -m "Release Phase 1.1 - Dynamic Query Formation"
git tag -a phase-1.1-dynamic-query-formation -m "Complete Phase 1.1 implementation"

# Lightweight tag
git tag v1.1.0

# Push tags
git push origin v1.1.0
git push origin --tags  # Push all tags
```

---

## Workflow Commands

### Starting a New Phase
```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create new phase branch
git checkout -b feature/phase-1.2-enhanced-search-integration

# 3. Cherry-pick any needed commits from previous phase
git cherry-pick <commit-hash>

# 4. Start development
# ... make changes ...
git add .
git commit -m "feat: implement Serper API integration"
```

### Daily Development Workflow
```bash
# Start of day
git checkout feature/phase-1.2-enhanced-search-integration
git pull origin main  # Get latest main changes

# During development
git add .
git commit -m "feat: add hybrid search strategy"
git push origin feature/phase-1.2-enhanced-search-integration

# End of day
git push origin feature/phase-1.2-enhanced-search-integration
```

### Merging Phase Completion
```bash
# 1. Create Pull Request on GitHub
# 2. After approval and merge
git checkout main
git pull origin main

# 3. Create release tag
git tag -a v1.2.0 -m "Release Phase 1.2 - Enhanced Search Integration"
git push origin v1.2.0

# 4. Clean up feature branch
git branch -d feature/phase-1.2-enhanced-search-integration
git push origin --delete feature/phase-1.2-enhanced-search-integration
```

---

## Phase-Based Development

### Phase Workflow Template
```bash
# Phase X.Y: {Description}
# Week X: {Focus Area}

# 1. Create phase branch
git checkout -b feature/phase-X.Y-{description}

# 2. Development commits
git commit -m "feat: implement {specific feature}"
git commit -m "test: add tests for {feature}"
git commit -m "docs: update documentation for {feature}"

# 3. Phase completion
git commit -m "feat: complete Phase X.Y - {description}"
git tag -a phase-X.Y-{description} -m "Complete Phase X.Y implementation"
git push origin phase-X.Y-{description}

# 4. Create PR and merge
# 5. Tag release
git tag -a vX.Y.0 -m "Release Phase X.Y - {description}"
```

### Phase Status Tracking
```bash
# Check phase progress
git log --oneline feature/phase-1.2-enhanced-search-integration

# Compare with main
git log main..feature/phase-1.2-enhanced-search-integration --oneline

# Check phase tags
git tag --list "phase-*"
```

---

## Pull Request Guidelines

### PR Title Format
```
feat: Phase X.Y - {Description}
```

**Examples:**
- `feat: Phase 1.2 - Enhanced Search Integration`
- `fix: Phase 1.1 - Query Classification Bug Fix`
- `docs: Phase 2.1 - Update GitHub Integration Docs`

### PR Description Template
```markdown
## Phase X.Y: {Description}

### Changes Made
- [ ] Feature 1: {description}
- [ ] Feature 2: {description}
- [ ] Tests: {description}
- [ ] Documentation: {description}

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

### Related Issues
Closes #123
Related to #456

### Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

---

## Troubleshooting

### Common Issues & Solutions

#### Cherry-picking Conflicts
```bash
# If cherry-pick fails due to conflicts
git cherry-pick --abort  # Cancel cherry-pick
git cherry-pick --continue  # After resolving conflicts
```

#### Undoing Last Commit
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes, undo commit
git reset --hard HEAD~1
```

#### Moving Commits Between Branches
```bash
# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Move last commit to different branch
git checkout <target-branch>
git cherry-pick <source-branch>
git checkout <source-branch>
git reset --hard HEAD~1
```

#### Fixing Commit Messages
```bash
# Fix last commit message
git commit --amend -m "New commit message"

# Interactive rebase to fix multiple commits
git rebase -i HEAD~3
```

#### Branch Cleanup
```bash
# Delete local branch
git branch -d feature/phase-1.1-dynamic-query-formation

# Delete remote branch
git push origin --delete feature/phase-1.1-dynamic-query-formation

# Clean up merged branches
git branch --merged main | grep -v main | xargs git branch -d
```

---

## Best Practices Summary

### ✅ Do's
- Use conventional commit messages
- Create descriptive branch names
- Tag releases and phase completions
- Keep commits atomic and focused
- Write clear PR descriptions
- Test before pushing
- Update documentation with changes

### ❌ Don'ts
- Commit directly to main
- Use vague commit messages
- Mix multiple features in one commit
- Skip testing
- Forget to update documentation
- Use generic branch names
- Leave feature branches unmerged

### 📋 Checklist for Each Phase
- [ ] Branch follows naming convention
- [ ] Commits follow conventional format
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] PR created with proper description
- [ ] Code reviewed and approved
- [ ] Phase tag created after merge
- [ ] Release tag created
- [ ] Feature branch cleaned up

---

## Quick Reference

### Essential Commands
```bash
# Branch management
git checkout -b feature/phase-X.Y-description
git branch -d feature/phase-X.Y-description

# Committing
git add .
git commit -m "type: description"

# Tagging
git tag -a vX.Y.Z -m "Release description"
git push origin vX.Y.Z

# Phase workflow
git checkout main && git pull
git checkout -b feature/phase-X.Y-description
# ... development ...
git push origin feature/phase-X.Y-description
# ... PR and merge ...
git tag -a phase-X.Y-description -m "Complete Phase X.Y"
```

This cheatsheet ensures consistent Git practices across all phases of your project and can be used as a reference for future projects as well. 