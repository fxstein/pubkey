# Pubkey ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
- [ ] **#40** Adopt .cursor/rules/ structure from ascii-guard for release automation `#project-structure`
  > Copy .cursor/rules/ from ascii-guard. Key rules: release workflow automation, version management, PyPI publishing guidelines, GitHub Actions integration. These rules guide AI agents through the entire release process.
- [ ] **#39** Update shebang in pubkey script to modern Python `#modernization`
- [ ] **#38** Create migration guide for users upgrading from old version `#documentation`
- [ ] **#37** Verify all functionality works with updated dependencies `#testing`
- [ ] **#36** Test installation from PyPI test server `#testing`
- [ ] **#35** Add usage examples and tutorials `#documentation`
- [ ] **#34** Create docs/ directory structure `#documentation`
- [ ] **#33** Update package classifiers in pyproject.toml `#packaging`
- [ ] **#32** Review and update MANIFEST.in for package distribution `#packaging`
- [ ] **#31** Remove old .travis.yml file `#cleanup`
- [ ] **#30** Create .gitignore for Python/venv files `#project-structure`
  > Should exclude: __pycache__/, *.pyc, *.pyo, *.egg-info/, dist/, build/, .venv/, venv/, .pytest_cache/, .mypy_cache/
- [ ] **#29** Add badges to README (CI, coverage, PyPI) `#documentation`
- [ ] **#28** Update LICENSE.md copyright year `#documentation`
- [ ] **#27** Add code coverage reporting (codecov) `#testing`
- [ ] **#26** Create release workflow with version tagging `#ci-cd`
- [ ] **#25** Add dependabot configuration for dependency updates `#security`
- [ ] **#24** Add security scanning (bandit, safety) `#security`
- [ ] **#23** Review and update asyncio/aiohttp usage for modern syntax `#modernization`
  > Code uses old Python 3.4 asyncio syntax. Modern Python 3.11+ has better async/await patterns and updated aiohttp APIs
- [ ] **#22** Add type hints to existing code `#modernization`
- [ ] **#21** Create comprehensive test suite `#testing`
- [ ] **#20** Add development dependencies section to pyproject.toml `#dependencies`
- [ ] **#19** Create .python-version file `#environment`
- [ ] **#18** Add setup.sh script for one-step development setup `#environment`
  > See ascii-guard/setup.sh - Single script to setup venv, install deps, configure pre-commit, and run tests
- [ ] **#17** Update README.md with modern installation instructions `#documentation`
- [ ] **#16** Create CODE_OF_CONDUCT.md `#documentation`
- [ ] **#15** Create CONTRIBUTING.md based on ascii-guard `#documentation`
- [ ] **#14** Add mypy for type checking `#code-quality`
- [ ] **#13** Add ruff for linting (replace flake8) `#code-quality`
- [ ] **#12** Add pre-commit hooks configuration `#code-quality`
- [ ] **#11** Create GitHub Actions workflow for release/PyPI publish `#ci-cd`
- [ ] **#10** Create GitHub Actions workflow for testing `#ci-cd`
- [ ] **#9** Add proper testing framework (pytest) `#testing`
- [ ] **#8** Update dependency versions to latest compatible releases `#dependencies`
  > Current deps: asyncio>=3.4.0, aiohttp>=0.17.0, cement>=2.6.0, colorlog>=2.6.0 - All from 2015, need major updates
- [ ] **#7** Update Python version support (3.11+, drop 3.4/3.5) `#modernization`
- [ ] **#6** Migrate from Travis CI to GitHub Actions `#ci-cd`
  > Replace .travis.yml with .github/workflows/. See ascii-guard for examples: test.yml, release.yml workflows
- [ ] **#5** Set up Python virtual environment (venv) `#environment`
- [ ] **#4** Create modern pyproject.toml to replace setup.py `#modernization`
  > See ascii-guard/pyproject.toml as reference. Must include build-system, project metadata, dependencies, dev dependencies, and tool configs
- [ ] **#3** Review ascii-guard repo structure and best practices `#assessment`
  > Reference: https://github.com/fxstein/ascii-guard - Check pyproject.toml, .github/workflows/, setup.sh, .pre-commit-config.yaml, and ESPECIALLY .cursor/rules/ directory. The release process depends heavily on cursor rules for automation and workflow management.
- [ ] **#2** Document current package versions (asyncio, aiohttp, cement, colorlog) `#assessment`
- [ ] **#1** Assess current dependencies and Python version requirements `#assessment`

------------------

## Recently Completed

---

**Last Updated:** Fri Nov 21 18:34:42 CET 2025
**Repository:** https://github.com/fxstein/pubkey  
**Maintenance:** Use `todo.ai` script only

## Task Metadata

Task relationships and dependencies (managed by todo.ai tool).
View with: `./todo.ai show <task-id>`

<!-- TASK RELATIONSHIPS
-->
