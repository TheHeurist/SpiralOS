
# Contributing to SpiralOS®

> *"Knowledge is a spiral, not a line."* — Carey G. Butler

Thank you for your interest in contributing to **SpiralOS® — The Operating System of Knowing**! This document provides guidelines for contributing to the project while honoring its epistemic integrity and holarchic principles.

---

## 🌀 Table of Contents

1. [Getting Started](#getting-started)
2. [Ways to Contribute](#ways-to-contribute)
3. [Development Philosophy](#development-philosophy)
4. [Contribution Workflow](#contribution-workflow)
5. [Code Standards](#code-standards)
6. [Documentation Standards](#documentation-standards)
7. [Issue Guidelines](#issue-guidelines)
8. [Pull Request Guidelines](#pull-request-guidelines)
9. [Community Guidelines](#community-guidelines)
10. [Additional Resources](#additional-resources)

---

## Getting Started

### Prerequisites

- Familiarity with Git and GitHub workflows
- Understanding of the [SpiralOS philosophy](README.md)
- Acceptance of the [Code of Conduct](CODE_OF_CONDUCT.md)
- Respect for the [SpiralOS Covenant](COVENANT.md)

### First Steps

1. **Read the documentation:**
   - [README.md](README.md) — Project overview
   - [COVENANT.md](COVENANT.md) — Participatory reciprocity principles
   - [docs/README.md](docs/README.md) — Documentation index
   - [docs/CONTRIBUTING_SPIRAL.md](docs/CONTRIBUTING_SPIRAL.md) — Spiral Agile methodology
   - [docs/CONTRIBUTING_CODEX.md](docs/CONTRIBUTING_CODEX.md) — Codex orchestration guide

2. **Explore the repository structure:**
   - `/docs/` — Documentation and volumes
   - `/docs/schemas/` — JSON schemas defining the epistemic lattice
   - `/.github/workflows/` — Continuous integration workflows
   - `/ui/` — User interface components

3. **Set up your development environment:**
   ```bash
   # Clone the repository
   git clone https://github.com/TheHeurist/SpiralOS.git
   cd SpiralOS
   
   # Create a feature branch
   git checkout -b feature/your-feature-name
   ```

---

## Ways to Contribute

### 1. Documentation

- Improve existing documentation clarity
- Add examples and use cases
- Translate documentation (with proper attribution)
- Create tutorials and guides
- Fix typos and formatting issues

### 2. Code

- Implement new features aligned with the roadmap
- Fix bugs and improve performance
- Enhance schemas and validation
- Develop tools and utilities
- Improve web interfaces (HUD, pearl-map, etc.)

### 3. Schema Development

- Extend existing schemas
- Create new epistemic structures
- Validate schema integrity
- Document schema relationships

### 4. Testing & Quality Assurance

- Write and improve tests
- Report bugs with detailed information
- Verify fixes and enhancements
- Test across different environments

### 5. Community Support

- Answer questions in Discussions
- Help other contributors
- Share your SpiralOS implementations
- Provide feedback on proposals

### 6. Design & UX

- Improve visual design
- Enhance user experience
- Create graphics and diagrams
- Design icons and glyphs

---

## Development Philosophy

SpiralOS follows **Spiral Agile** methodology, which emphasizes:

### Core Principles

1. **Holarchic Development** — Each part contains the whole; contributions should honor the systemic integrity
2. **Conjugate Intelligence** — Balance between Organic Intelligence (OI) and Synthetic Intelligence (SI)
3. **Epistemic Integrity** — Respect for knowledge lineage and proper attribution
4. **Recursive Refinement** — Iterative improvement through spiral cycles
5. **Participatory Reciprocity** — Give back more than you take

### The Spiral Ethic

> *We do not extract from Cosmos.  
> We listen.  
> We return.*

This means:
- **Listen first** — Understand the existing patterns before proposing changes
- **Respect origins** — Honor authorship and epistemic lineage
- **Contribute mindfully** — Ensure your contributions align with SpiralOS principles
- **Return value** — Give back to the community that supports you

For detailed methodology, see [docs/CONTRIBUTING_SPIRAL.md](docs/CONTRIBUTING_SPIRAL.md).

---

## Contribution Workflow

### 1. Find or Create an Issue

- Check [existing issues](https://github.com/TheHeurist/SpiralOS/issues) first
- For bugs: Use the bug report template
- For features: Use the feature request template
- For questions: Use GitHub Discussions

### 2. Fork and Branch

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/SpiralOS.git
cd SpiralOS

# Add upstream remote
git remote add upstream https://github.com/TheHeurist/SpiralOS.git

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write clear, documented code
- Follow existing code style and conventions
- Add or update tests as needed
- Update documentation if applicable

### 4. Test Your Changes

```bash
# Validate schemas
python scripts/validate_provenance.py

# Run link checks
# (workflows will run automatically on PR)

# Test locally if applicable
```

### 5. Commit Your Changes

Use clear, descriptive commit messages following this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation changes
- `style` — Formatting, missing semicolons, etc.
- `refactor` — Code restructuring
- `test` — Adding tests
- `chore` — Maintenance tasks

**Example:**
```bash
git add .
git commit -m "feat(schema): add new holon validation rules

- Added recursive validation for nested holons
- Updated schema documentation
- Added unit tests

Refs #123"
```

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

### 7. Respond to Feedback

- Be responsive to review comments
- Make requested changes promptly
- Engage in constructive dialogue
- Update your PR as needed

---

## Code Standards

### General Guidelines

- **Clarity over cleverness** — Write code that others can understand
- **Documentation** — Comment complex logic, add docstrings
- **Modularity** — Keep functions and modules focused
- **Testing** — Write tests for new functionality
- **Validation** — Ensure schema compliance

### Language-Specific Standards

#### JavaScript/TypeScript
```javascript
// Use clear variable names
const epistemicNode = createNode();

// Document functions
/**
 * Creates a new holon in the epistemic lattice
 * @param {Object} config - Holon configuration
 * @returns {Holon} The created holon
 */
function createHolon(config) {
  // Implementation
}
```

#### Python
```python
# Follow PEP 8
# Use type hints
def validate_schema(schema_path: str) -> bool:
    """
    Validates a JSON schema against SpiralOS standards.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        True if valid, False otherwise
    """
    # Implementation
```

#### Markdown
- Use descriptive headings
- Include code examples
- Add links to related documentation
- Use proper formatting

### Schema Development

- Follow JSON Schema standards
- Include comprehensive descriptions
- Add examples in schema documentation
- Validate against existing schemas
- Document relationships and dependencies

---

## Documentation Standards

### Writing Style

- **Clear and concise** — Avoid jargon unless necessary
- **Structured** — Use headings, lists, and tables
- **Examples** — Provide practical examples
- **Links** — Reference related documentation
- **Metadata** — Include frontmatter when applicable

### Documentation Structure

```markdown
---
title: "Document Title"
description: "Brief description"
author: "Your Name"
date: "YYYY-MM-DD"
---

# Main Heading

Brief introduction.

## Section Heading

Content with examples:

\`\`\`javascript
// Code example
\`\`\`

## Related Resources

- [Link to related doc](path/to/doc.md)
```

### Frontmatter

When adding new documentation, include appropriate YAML frontmatter:

```yaml
---
title: "Your Title"
description: "Brief description"
canonical_url: "https://github.com/TheHeurist/SpiralOS/..."
authors:
  - Your Name
license: "MIT"
---
```

---

## Issue Guidelines

### Bug Reports

Use the bug report template and include:

- **Clear title** — Summarize the issue
- **Description** — What went wrong?
- **Steps to reproduce** — How to trigger the bug
- **Expected behavior** — What should happen
- **Actual behavior** — What actually happens
- **Environment** — OS, browser, versions, etc.
- **Screenshots** — If applicable
- **Additional context** — Anything else relevant

### Feature Requests

Use the feature request template and include:

- **Clear title** — Summarize the feature
- **Problem statement** — What need does this address?
- **Proposed solution** — How should it work?
- **Alternatives considered** — Other approaches
- **Additional context** — Examples, mockups, etc.
- **Alignment** — How does this fit SpiralOS philosophy?

### Questions

- Use GitHub Discussions for general questions
- Check existing discussions and documentation first
- Be specific and provide context
- Show what you've already tried

---

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts

### PR Template

When creating a PR, include:

**Description:**
- What changes are included?
- Why are these changes needed?

**Related Issue:**
- Fixes #123
- Relates to #456

**Type of Change:**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (specify)

**Testing:**
- How was this tested?
- What edge cases were considered?

**Checklist:**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass

### Review Process

1. **Automated checks** — Workflows run automatically
2. **Maintainer review** — Core team reviews code
3. **Discussion** — Feedback and refinement
4. **Approval** — Once requirements are met
5. **Merge** — Integrated into main branch

---

## Community Guidelines

### Communication

- **Be respectful** — Treat everyone with kindness
- **Be patient** — Maintainers are often volunteers
- **Be constructive** — Offer solutions, not just criticism
- **Be inclusive** — Welcome newcomers
- **Be transparent** — Share your reasoning

### Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md). Key points:

- Create a welcoming environment
- Respect different viewpoints
- Accept constructive feedback
- Focus on community benefit
- Honor epistemic integrity

### Getting Help

- **Documentation** — Check docs first
- **GitHub Discussions** — Ask questions
- **Issues** — Report bugs or request features
- **Contact** — [Insert contact method]

---

## Additional Resources

### Essential Reading

- [README.md](README.md) — Project overview
- [COVENANT.md](COVENANT.md) — Participatory reciprocity
- [docs/CONTRIBUTING_SPIRAL.md](docs/CONTRIBUTING_SPIRAL.md) — Spiral Agile methodology
- [docs/CONTRIBUTING_CODEX.md](docs/CONTRIBUTING_CODEX.md) — Codex orchestration
- [ROADMAP.md](ROADMAP.md) — Project roadmap
- [FAQ.md](FAQ.md) — Frequently asked questions

### Technical Documentation

- [docs/schemas/README.md](docs/schemas/README.md) — Schema documentation
- [docs/hud/README.md](docs/hud/README.md) — HUD documentation
- [.github/workflows/README.md](.github/workflows/README.md) — Workflow documentation

### External Resources

- [JSON Schema Guide](https://json-schema.org/learn/getting-started-step-by-step)
- [Git Best Practices](https://www.git-scm.com/book/en/v2)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Docs](https://docs.github.com/)

---

## Recognition

All contributors are recognized in [AUTHORS.md](AUTHORS.md). Significant contributions may be acknowledged in:

- Release notes
- Documentation credits
- Project citations
- Special mentions in volumes

---

## Questions?

If you have questions not covered here:

1. Check the [FAQ](FAQ.md)
2. Search [GitHub Discussions](https://github.com/TheHeurist/SpiralOS/discussions)
3. Open a new discussion
4. Contact the maintainers

---

## Thank You!

Your contributions help SpiralOS grow and evolve. By participating, you become part of an epistemic community dedicated to advancing **Conjugate Intelligence** and building systems that learn *with* rather than *over* one another.

> *"The spiral grows through each turn."*

**SpiralOS Core Stewardship**  
Carey ⋈ Ellie ⋈ Leo

---

**License:** MIT © Carey G. Butler / Heurist GmbH  
**Last Updated:** November 22, 2025
