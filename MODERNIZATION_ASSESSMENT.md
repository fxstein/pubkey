# Pubkey Repository Modernization Assessment

## Guiding Principles

### 1. **Zero or Minimal External Dependencies**
- **Primary Goal**: Build for Python 3.10, 3.11+ with **ZERO external dependencies** if possible
- **Fallback**: If zero dependencies is not feasible, minimize to the absolute minimum
- **Rationale**: Reduce supply chain risk, simplify installation, improve security posture

### 2. **Simplicity First**
- Clean, readable implementation without unnecessary complexity
- Prefer stdlib solutions over external libraries when functionality is equivalent
- Avoid over-engineering and feature creep
- Keep the core use case simple: serve a public key over HTTP

### 3. **Dependency Analysis Required**
Current dependencies (2015):
- **asyncio** >= 3.4.0 → ✅ **Built into Python 3.4+** (stdlib, no external dep)
- **aiohttp** >= 0.17.0 → ❓ **Evaluate**: Can we use `http.server` + `asyncio` instead?
- **cement** >= 2.6.0 → ❓ **Can replace with**: `argparse` (stdlib) for CLI
- **colorlog** >= 2.6.0 → ❓ **Can replace with**: `logging` (stdlib) for output

**Target**: Reduce from 3 external dependencies → **0-1 external dependencies**

### 4. **Modern Python Features**
- Use Python 3.10+ features where they simplify code
- Type hints for clarity and maintainability
- Modern async/await syntax (not old `@asyncio.coroutine`)

### 5. **Don't Compromise Core Functionality**
- Async HTTP server for concurrent requests
- Simple REST API (GET / and GET /json)
- Auto-detect local IP functionality
- Request limits and timeouts

## Current State (2015-era codebase)

### Critical Issues
- **Python Version**: Requires Python 3.4/3.5 (EOL since 2017/2020)
- **CI/CD**: Using Travis CI (.travis.yml) - outdated
- **Packaging**: Old setup.py format, no pyproject.toml
- **Dependencies**: All from 2015, severely outdated:
  - asyncio >= 3.4.0
  - aiohttp >= 0.17.0 (current is 3.9+)
  - cement >= 2.6.0
  - colorlog >= 2.6.0
- **Testing**: Minimal smoke tests only, no pytest
- **Code Quality**: Basic flake8, no type hints, no pre-commit hooks
- **Documentation**: Missing CONTRIBUTING.md, CODE_OF_CONDUCT.md
- **Security**: No security scanning, no dependabot

### Project Files
- `setup.py` - Old-style packaging (needs pyproject.toml)
- `.travis.yml` - Travis CI config (needs GitHub Actions)
- `pubkey/__init__.py` - Version 0.9.7dev
- `tests/id_rsa.pub` - Single test fixture
- `README.md` - Has Travis CI badge
- `DESCRIPTION.rst` - Package description

### Dependency Evaluation for Minimization

#### Current Usage Analysis
1. **asyncio** (stdlib) - Used for:
   - Event loop management
   - Async HTTP server
   - ✅ **Keep**: Essential, no external dependency

2. **aiohttp** (external) - Used for:
   - `web.Application()` - Web framework
   - `web.Response()` - HTTP responses
   - HTTP routing
   - 🔍 **Evaluate**: Could use `http.server` + `asyncio` or `asyncio` streams directly
   - **Trade-off**: aiohttp is mature but adds dependency; stdlib approach more complex

3. **cement** (external) - Used for:
   - CLI argument parsing (can use `argparse`)
   - Logging framework (can use `logging`)
   - Config management (can use `configparser`)
   - Application lifecycle hooks (can implement directly)
   - ✅ **Replace**: All functionality available in stdlib

4. **colorlog** (external) - Used for:
   - Colored console output
   - ✅ **Replace**: Standard `logging` is sufficient; colors are nice-to-have

#### Recommended Approach
- **Phase 1**: Replace cement → argparse + logging (removes 2 deps)
- **Phase 2**: Evaluate aiohttp alternatives (potentially remove last dep)
- **Target**: 0-1 external dependencies total

## Modernization Plan

Reference repository: https://github.com/fxstein/ascii-guard

**⚠️ IMPORTANT:** The ascii-guard repository uses `.cursor/rules/` to automate the entire release process. These cursor rules guide AI agents through version management, GitHub Actions workflows, and PyPI publishing. This is a critical component to adopt.

### Task Categories (41 total tasks)

**Note**: Task priorities have been adjusted to emphasize dependency minimization per guiding principles. Task #41 added specifically to evaluate zero-dependency feasibility.

#### 1. Assessment (3 tasks)
- Audit current dependencies
- Review ascii-guard best practices
- Document package versions

#### 2. Modernization (5 tasks)
- Python 3.11+ support
- Modern pyproject.toml
- Type hints
- Updated asyncio/aiohttp syntax
- Modern shebang

#### 3. Environment Setup (3 tasks)
- Virtual environment (venv)
- .python-version file
- setup.sh script

#### 4. CI/CD (4 tasks)
- GitHub Actions workflows
- Testing pipeline
- Release automation
- PyPI publishing

#### 5. Dependencies (3 tasks) **[CRITICAL - ZERO DEPENDENCY GOAL]**
- **Evaluate zero-dependency implementation feasibility** (task #41)
- Replace cement/colorlog with stdlib (argparse, logging)
- Document final dependency decisions and trade-offs

#### 6. Code Quality (3 tasks)
- Pre-commit hooks
- Ruff linting
- Mypy type checking

#### 7. Testing (4 tasks)
- Pytest framework
- Comprehensive test suite
- Code coverage (codecov)
- PyPI test installation

#### 8. Security (2 tasks)
- Security scanning (bandit, safety)
- Dependabot configuration

#### 9. Documentation (8 tasks)
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- Modern README
- Badges
- docs/ directory
- Usage examples
- Migration guide
- License update

#### 10. Packaging (2 tasks)
- MANIFEST.in review
- Package classifiers

#### 11. Project Structure (2 tasks)
- Modern .gitignore
- **Cursor rules for release automation** (CRITICAL)

#### 12. Cleanup (1 task)
- Remove .travis.yml

## Next Steps (Prioritized for Simplicity)

1. **Assessment & Dependency Analysis** (#1-3, #8)
   - CRITICAL: Evaluate zero-dependency feasibility
   - Document trade-offs for each dependency
   - Decision: Keep aiohttp or move to stdlib?

2. **Dependency Reduction Implementation** (#7, #8)
   - Replace cement with argparse + logging (stdlib)
   - Replace colorlog with logging (stdlib)
   - Evaluate aiohttp alternatives

3. **Environment Setup** (#5, #18, #19)
   - Virtual environment (venv)
   - Modern development workflow

4. **Modernization** (#4, #22-23, #39)
   - Create simple pyproject.toml
   - Add type hints
   - Update to modern async/await syntax

5. **CI/CD & Testing** (#6, #9-11, #21, #27)
   - GitHub Actions workflows
   - Pytest framework
   - Code coverage

6. **Code Quality** (#12-14)
   - Pre-commit hooks
   - Ruff linting
   - Mypy type checking

7. **Documentation** (#15-17, #28-29, #34-35, #38)
   - Contributing guidelines
   - Modern README emphasizing simplicity

8. **Security & Final Steps** (#24-25, #36-37)

## Benefits of Modernization

- 🎯 **Simplicity**: Zero or minimal dependencies, clean stdlib-based implementation
- 🔒 **Security**: Minimal supply chain risk, reduced attack surface
- ⚡ **Performance**: No dependency overhead, faster installation
- ✅ **Maintainability**: Type hints, modern tooling, automated checks
- 🧪 **Reliability**: Comprehensive tests, CI/CD automation
- 👥 **Developer Experience**: One-step setup, easy to understand codebase
- 📦 **Distribution**: Modern PyPI packaging, automated releases
- 🌍 **Community**: Contributing guidelines, code of conduct

