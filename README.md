# The Complete Obsidian Mastery Guide

The most detailed, comprehensive guide to mastering [Obsidian](https://obsidian.md) and using it to run your entire life — knowledge, tasks, projects, health, finance, relationships, home, creativity, and self-reflection. Written against **Obsidian 1.13** (2026): Bases, the CLI, Keychain, Web Clipper + Interpreter, iOS Share Sheet, and the current plugin ecosystem.

**38 chapters · ~84,000 words · hundreds of copy-ready Bases, Dataview, Templater, Tasks, CSS and CLI snippets.**

- 🌐 **Web edition:** https://gorg667.github.io/obsidian-guide/
- 📄 **Single-file edition:** [`GUIDE.md`](GUIDE.md) (auto-generated from `docs/`)
- 📚 **Chapters:** [`docs/`](docs/)

## Contents

| Part | Chapters |
| --- | --- |
| I — Foundations | Philosophy & mental model · Setup, settings & interface · Markdown & editing · Links, backlinks, graph & canvas · Properties, tags & metadata design · Search |
| II — Systems & methodology | PKM methodologies compared (Zettelkasten, Evergreen, LYT, PARA, CODE, GTD, Johnny.Decimal) · Vault architecture — the reference design |
| III — Core tools mastery | Core plugins · Bases · Templates & Templater · Dataview · Tasks & time · Essential community plugins |
| IV — Obsidian for everything in life | Daily notes & journaling · Tasks, projects & goals · Knowledge & learning · Academic research · Work & career · Health, fitness & food · Finance · Home & life admin · Relationships & people · Creativity, writing & media · Mind & self |
| V — Power user | Sync, backup & security · Mobile · Customization (themes/CSS) · Automation & integrations (URI, CLI, Shell, REST, Web Clipper) · AI in your vault · Publishing & sharing · Performance, maintenance & troubleshooting · Migration · Plugin development primer |
| VI — Reference | Mastery roadmap (30/60/90 days, 1 year) · Templates library · Cheat sheets · Glossary & resources |

## Build locally

```bash
pip install -r requirements.txt
python scripts/build_guide.py   # regenerates GUIDE.md from docs/
mkdocs serve                    # http://127.0.0.1:8000
mkdocs gh-deploy --force        # publish to the gh-pages branch
```

Built with MkDocs Material; deployed to GitHub Pages from the `gh-pages` branch. An optional GitHub Actions workflow is provided in `deploy-templates/` if you prefer CI builds (move it to `.github/workflows/`).

## Contributing / feedback

Open an issue or PR. Chapters are plain Markdown in `docs/`; the site nav is in `mkdocs.yml`; `PROGRESS.md` documents the design decisions.

## License

Content may be freely shared and adapted with attribution (CC BY 4.0). Code snippets are MIT.
