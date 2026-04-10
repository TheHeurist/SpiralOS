#!/bin/bash

# Navigate to the repo
cd /mnt/e/_Dev_/SpiralOS

# Stage all changes (including sitemap.xml and fixed files)
git add .

# Commit the changes
commit_message="Fix docs sitemap generation and unblock GitHub Pages Jekyll parsing"
git commit -m "$commit_message"

# Push to a new branch
branch_name="fix-docs-sitemap-$(date +%Y%m%d%H%M%S)"
git checkout -b "$branch_name"
git push --set-upstream origin "$branch_name"

# Create a Pull Request using GitHub CLI
gh pr create \
  --title "$commit_message" \
  --body "This PR fixes:
  - YAML front matter syntax errors in markdown files.
  - UTF-8 encoding issues in non-compliant files.
  - Adds/updates sitemap.xml for GitHub Pages.
  - Ensures Jekyll can build the site without errors." \
  --base main \
  --head "$branch_name"

echo "Pull Request created! Check it at: https://github.com/TheHeurist/SpiralOS/pulls"
