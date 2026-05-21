# auh-realty-ontology — Project Blueprint

> Investor's analytical infrastructure for cross-jurisdictional real estate analysis.
> Active markets: Abu Dhabi → Tbilisi → Tirana.

This document is the project context for Claude Code. Commit it to the repository as `CLAUDE.md` so Claude Code uses it automatically when invoked in this directory.

---

## 0. Voice Principles (apply to ALL written outputs: README, docstrings, commit messages, comments, error messages)

- **Declarative, not comparative.** State facts; do not claim advantages.
- **Fact-enumeration, not advantage-claiming.** List what is; do not assert what is "better" or "best."
- **Empirical over methodological.** Concrete data, concrete decisions; not framework names.
- **Recognition over performance.** Earned recognition signals; no signaling for signaling's sake.
- **Cold-close moves.** No filler closers. End on the substance.
- **No exclamation marks. No emoji in technical content. No marketing adjectives** ("seamless", "powerful", "robust", "cutting-edge"). Strip them on sight.

These apply to anything Claude Code writes on this project.

---

## 1. Project Framing

This is **not** a portfolio piece. It is real analytical infrastructure for a real multi-jurisdictional real estate investing program.

The author (Marc Jichi) is an active investor in three markets:
- **Abu Dhabi** — primary, longstanding; chair of the Mamsha Saadiyat owners' association
- **Tbilisi, Georgia** — existing holdings
- **Tirana, Albania** — pre-investment due diligence

Existing consumer tools (Bayut, Property Finder, DLD portals) do not aggregate across jurisdictions, do not surface transacted prices alongside listing prices, and do not enable time-series or cohort analysis. This repository fills that gap for personal use; the ontology and methods are reusable for any heterogeneous-source real estate market.

The repository surfaces the author's analytical thinking as a side benefit. It is also referenced in conversations with potential employers and partners. Both functions reinforce each other only if the work is honest and the README is truthful.

---

## 2. Problem Statement (current canonical version — paste into README)

> I am an active investor in real estate across three markets: Abu Dhabi (where I chair the Mamsha Saadiyat owners' association), Tbilisi, and Tirana (pre-investment due diligence). Each market has heterogeneous public data sources — listings on consumer portals, transaction registers, developer announcements — none of which share a schema, none of which cross jurisdictions, and most of which report listing prices rather than transacted prices.
>
> The decisions this affects are real: where to deploy the next capital allocation, whether a listing in a known neighborhood is mispriced relative to recent transactions, how Tirana entry prices compare to Tbilisi at the same property class, when to exit a position in Abu Dhabi.
>
> Existing tools don't answer these questions. This repository ingests listings and transactions from heterogeneous public sources, structures them as a cross-jurisdictional property ontology, and surfaces (1) current and historical prices on a map, (2) comparative analysis across neighborhoods and markets, and (3) anomaly detection on listings that diverge from local patterns.

---

## 3. Current Focus — Phase 1 (Sub-phase A): Saadiyat Island, Abu Dhabi

Build the smallest end-to-end loop. Ship before optimizing.

### Week 1 deliverable

One Jupyter notebook (`notebooks/01_saadiyat_ingestion.ipynb`) that:

1. Pulls N≥30 listings from Bayut for Saadiyat Island
2. Pulls M≥30 listings from Property Finder for Saadiyat Island
3. Parses both into Pandas DataFrames with a reconciled schema
4. Detects duplicates (same property listed on both sources at different prices)
5. Writes a unified CSV (`data/processed/saadiyat_unified.csv`)
6. Includes a short markdown narrative in the notebook explaining decisions made and why

**Do not** build the map, the ontology graph, the anomaly detection, or any UI in week 1. The smallest thing that works beats the most beautiful thing that's two weeks from working.

### Fallback if scraping stalls

Bayut and Property Finder both have anti-bot measures. If scraping consumes more than 4 hours without working data flowing:

**Switch immediately to DLD Dubai weekly transactions** (public CSV downloads, no scraping required). Get to a working ETL on *any* data source before optimizing the data source choice. Geographic rename of the repo description to "UAE Real Estate Ontology" — the Abu Dhabi version becomes the second deliverable.

---

## 4. Architecture

### Tech stack (locked for phase 1)

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11+ | Author has Python practice and the 42 piscine foundation |
| Data manipulation | Pandas | Standard for tabular data; lets author show fluency |
| Entity validation | Pydantic v2 | Typed entities = the "ontology" in code form |
| Storage (phase 1) | SQLite via stdlib `sqlite3` or DuckDB | No infrastructure; upgrade path is DuckDB → Postgres if needed |
| HTTP scraping | `requests` + `BeautifulSoup4` first; Playwright if needed | Try simple before heavy |
| Mapping (phase 2) | Folium | Simpler than Plotly for geographic; HTML output |
| Notebooks | Jupyter | Phase 1 exploration; migrate patterns to `src/` as they stabilize |
| Testing | pytest | Standard |
| Dependency mgmt | `uv` (preferred) or `pip` + `pyproject.toml` | `uv` is fast and modern; either works |
| Code style | `ruff` for lint and format | One tool, fast, opinionated |
| Type checking | `mypy` (optional, light) | Don't slow down phase 1 with strict typing |

### Directory structure

```
auh-realty-ontology/
├── README.md                   # public-facing, follows problem statement above
├── CLAUDE.md                   # this file — Claude Code project context
├── pyproject.toml              # dependencies and tooling config
├── .gitignore                  # ignore data/raw/, data/processed/, .env, etc.
├── .env.example                # template for any env vars (no secrets in git)
├── notebooks/
│   ├── 01_saadiyat_ingestion.ipynb     # week 1 deliverable
│   └── (subsequent numbered explorations)
├── src/
│   └── auh_realty/
│       ├── __init__.py
│       ├── ontology/
│       │   ├── __init__.py
│       │   └── entities.py     # Pydantic models for Property, Listing, Transaction, Agent, etc.
│       ├── ingest/
│       │   ├── __init__.py
│       │   ├── bayut.py        # Bayut scraper / parser
│       │   ├── property_finder.py
│       │   └── dld.py          # Dubai Land Department CSV ingestion (fallback)
│       ├── normalize/
│       │   ├── __init__.py
│       │   ├── schema.py       # cross-source schema reconciliation
│       │   └── dedup.py        # duplicate detection across sources
│       └── analysis/
│           ├── __init__.py
│           ├── price.py        # current/historical price logic
│           └── anomaly.py      # anomaly detection (phase 2+)
├── data/
│   ├── raw/                    # gitignored — scraped HTML/JSON, do not commit
│   ├── processed/              # gitignored — normalized CSVs, do not commit
│   └── samples/                # small committed sample for tests
├── tests/
│   ├── test_ontology.py
│   ├── test_ingest_bayut.py
│   └── test_normalize.py
└── docs/
    ├── ontology.md             # entity-relationship documentation
    └── decisions.md            # architecture decision log (one paragraph per decision)
```

### Ontology — initial entity design

Pydantic models in `src/auh_realty/ontology/entities.py`. The ontology evolves as real data lands; this is the starting design, not the final one.

```python
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Literal
from uuid import UUID, uuid4
from decimal import Decimal


Jurisdiction = Literal["AUH", "DXB", "TBS", "BUS", "TIA"]
# AUH=Abu Dhabi, DXB=Dubai, TBS=Tbilisi, BUS=Batumi, TIA=Tirana

PropertyType = Literal["villa", "apartment", "townhouse", "plot", "commercial"]

Currency = Literal["AED", "USD", "EUR", "GEL", "ALL"]


class Neighborhood(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    jurisdiction: Jurisdiction
    # boundary: optional GeoJSON polygon — add when needed


class Developer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    jurisdiction: Jurisdiction


class Agent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    agency: str | None = None


class Property(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    property_type: PropertyType
    neighborhood_id: UUID
    developer_id: UUID | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    size_sqft: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    completion_year: int | None = None
    jurisdiction: Jurisdiction


class Listing(BaseModel):
    """A snapshot of a Property at a point in time, from one source."""
    id: UUID = Field(default_factory=uuid4)
    property_id: UUID
    source: Literal["bayut", "property_finder", "dld", "manual"]
    source_url: str | None = None
    listed_price: Decimal
    currency: Currency
    listed_date: date
    agent_id: UUID | None = None
    status: Literal["active", "sold", "withdrawn", "unknown"] = "unknown"
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class Transaction(BaseModel):
    """An actual transacted price from a government register (e.g., DLD)."""
    id: UUID = Field(default_factory=uuid4)
    property_id: UUID
    transacted_price: Decimal
    currency: Currency
    transacted_date: date
    source: Literal["dld", "adrec", "georgian_register", "albanian_register", "private"]
```

### Relationships

- `Property` → `Neighborhood` (many-to-one)
- `Property` → `Developer` (many-to-one, nullable)
- `Listing` → `Property` (many-to-one)
- `Listing` → `Agent` (many-to-one, nullable)
- `Transaction` → `Property` (many-to-one)

Stored as foreign keys in the SQLite/DuckDB schema. The "ontology graph" is the relationships *expressed* through these models — not a separate graph database.

### Key design principles

1. **Property is the canonical entity.** Listings and Transactions are events against a Property. Multiple Listings for the same Property is the duplicate-detection problem.
2. **Property identity is the hardest problem.** Two listings on different sources for the same physical unit need to resolve to the same `Property` row. Phase 1 will use heuristic matching (address + size + bedrooms); phase 2 may evolve.
3. **Currency stays per-entity.** Do not normalize to a base currency in storage. Normalize at query time. Exchange rates are time-series; baking them in is lossy.
4. **Source-of-truth is preserved.** Always keep the raw source URL and the scrape timestamp. The README explains why.

---

## 5. Future phases (do NOT build yet — context only)

### Sub-phase B (autumn 2026): Tbilisi + Batumi

- New ingestion modules for Georgian listing portals (myhome.ge, ss.ge)
- Schema reconciliation extends to GEL currency, Georgian neighborhood structures
- Cross-jurisdictional comparable analysis becomes the headline feature
- Map extends to Georgia

### Sub-phase C (mid-2027): Tirana

- Albanian portals (still being researched)
- Pre-investment DD module — what would inform a real Albania allocation decision
- Cross-comparison Tbilisi vs Tirana entry pricing

### Possible later: Private channel ingestion

- WhatsApp Business API + email — agent communications, deal flow
- **MUST be a separate private repository.** Never in this public repo.
- Privacy / consent / IP issues with agent communications are real.

---

## 6. README narrative guide

The public README is the document a screener (or future investor, or partner) reads in 60 seconds. It is also the document that turns the repo from "code" into "credible evidence."

### Structure (for the public README, not this CLAUDE.md)

```
# auh-realty-ontology

[Problem Statement — three paragraphs from section 2 above]

## Status

Active build, started [date]. Current focus: [current sub-phase].

## Data sources

- **Bayut** — listings (Saadiyat scope, initial)
- **Property Finder** — listings (Saadiyat scope, initial)
- **DLD (Dubai Land Department)** — weekly transactions (CSV downloads)
- **Future** — ADREC Abu Dhabi; Georgian portals (myhome.ge, ss.ge); Albanian portals

## Ontology

Entities, relationships, properties — see [`docs/ontology.md`](docs/ontology.md). Designed iteratively as the data shape becomes clear.

Current entities:
- Property (the physical unit — canonical entity)
- Listing (a snapshot from one source at one time)
- Transaction (an actual transacted price from a government register)
- Agent
- Developer
- Neighborhood

## Repository layout

[brief tree, link to relevant docs]

## Future work

Private-channel ingestion (WhatsApp Business API for agent communications) is intentionally kept out of this public repo. The ontology and methods here are designed to be reusable for any heterogeneous-source real estate market.
```

### Once data is flowing, add an "Example" section

A concrete deployment story is worth more than ten features. Once at least one real anomaly or insight has been surfaced, add:

```
## Example

[Two-paragraph concrete story: "In [date] I was evaluating two listings...
The tool flagged X. On inspection, Y. Without it I'd have evaluated as Z.
With it, I treated them as separate data points."]
```

This is the difference between "tool that lists features" and "tool that changes decisions."

---

## 7. Privacy and Legal Constraints

Non-negotiable:

1. **No real agent communications in this repository.** WhatsApp messages, private emails, direct chats — these contain personal data and confidential listing IP that agents did not consent to publicizing. Use synthetic / anonymized data only.
2. **Do not commit scraped data to the repo.** `data/raw/` and `data/processed/` are gitignored. Small sample data in `data/samples/` is okay if anonymized.
3. **Respect `robots.txt` and rate limits.** Bayut and Property Finder have terms of service. Scrape responsibly: low request rates, identifiable User-Agent, no circumvention of explicit blocks. If a source blocks the IP, stop — don't escalate. Move to DLD.
4. **No personal data of agents.** Agent names are fine in aggregate; agent phone numbers / emails / personal addresses are not. Strip on ingestion.
5. **License the code openly.** MIT or Apache 2.0. Add a LICENSE file.

---

## 8. Don't-Do List (boundaries for Claude Code in phase 1)

- ❌ Don't build a web app, dashboard, or any frontend in phase 1. Notebooks only.
- ❌ Don't use a heavy ORM (SQLAlchemy etc.) — direct SQLite or DuckDB queries are fine.
- ❌ Don't add Postgres / cloud infrastructure / Docker / CI/CD in phase 1.
- ❌ Don't add machine learning or LLM features for "smart" anything in phase 1. Statistics and joins solve the actual problems.
- ❌ Don't write tutorials, blog posts, or marketing-style content in the README.
- ❌ Don't add emoji, exclamation marks, or AI-marketing adjectives anywhere.
- ❌ Don't generate fake data and present it as real. If a section needs example data, label it `synthetic`.
- ❌ Don't bypass the privacy constraints in section 7 even if it would "make the example richer."
- ❌ Don't refactor the ontology before there is real data motivating the refactor. Premature ontology is the failure mode.

---

## 9. Conventions

### Git

- `main` is the only long-lived branch in phase 1. No PR workflow needed yet — this is solo work.
- Commit messages: imperative present-tense, short subject line, body if needed. No conventional-commits boilerplate.
  - Good: `add bayut listing parser for saadiyat`
  - Bad: `feat(ingest): implement bayut listing parser ✨🚀`
- Squash messy WIP commits before pushing if you remember; if not, fine.

### Code

- Type hints on function signatures and class attributes. Inside-function types optional.
- Docstrings on public functions, classes, and modules. One-line for simple, paragraph for non-obvious.
- Module names lowercase, no underscores if avoidable.
- Tests live in `tests/` mirroring `src/` structure.
- One module = one responsibility. Split when a file gets past ~300 lines.

### Notebooks

- Numbered prefix (`01_`, `02_`, ...) for ordering.
- Markdown cells explain decisions, not just labels.
- Clear all outputs before committing (avoid bloating the repo with rendered figures).
- Migrate stable patterns out of notebooks into `src/` modules.

---

## 10. Suggested First Prompts for Claude Code Tonight

These are starter prompts to paste into Claude Code in this repo's directory. Each one is scoped to one task.

### 1. Project scaffold

```
Set up the auh-realty-ontology project scaffold per CLAUDE.md section 4.
- Create pyproject.toml with the locked tech stack
- Create the directory structure exactly as specified
- Create .gitignore for Python + data/raw/ + data/processed/ + .env
- Create empty __init__.py files where needed
- Create the Pydantic entities in src/auh_realty/ontology/entities.py exactly as specified in section 4 of CLAUDE.md
- Do NOT create the ingest, normalize, or analysis modules yet — only ontology
- Do NOT install dependencies — just scaffold the files
Confirm with `tree -L 3` output when done.
```

### 2. First ingestion — Bayut, Saadiyat

```
Build the Bayut ingestion module per CLAUDE.md section 3.
Target: extract listings for Saadiyat Island, Abu Dhabi.
Approach:
- Inspect Bayut's Saadiyat search URL structure
- Use requests + BeautifulSoup for initial scrape; switch to Playwright only if anti-bot blocks the basic approach
- Parse each listing into the Listing Pydantic model defined in src/auh_realty/ontology/entities.py
- Create Property records as a side effect (one Property per unique listing; address+size+beds as identity heuristic for phase 1)
- Write outputs to data/raw/bayut_saadiyat_<timestamp>.json
- Respect robots.txt; rate-limit to one request per 2 seconds; identifiable User-Agent
- If Bayut blocks the IP, STOP, document the block in docs/decisions.md, and fall back to DLD per CLAUDE.md section 3
Goal: pull at least 30 listings successfully and save as JSON.
Do not build the Property Finder module yet.
```

### 3. Cross-source reconciliation

```
With Bayut ingestion working, build the Property Finder ingestion module mirroring the Bayut approach.
Then build src/auh_realty/normalize/schema.py to reconcile the two source schemas into the canonical Listing + Property ontology.
Then build src/auh_realty/normalize/dedup.py to detect cross-source duplicates: same Property listed on both Bayut and Property Finder at different prices.
Heuristic for phase 1: match on (address string normalized, bedrooms, size_sqft within 5%).
Output: unified data/processed/saadiyat_unified.csv with one row per Listing and a `duplicate_group_id` column where applicable.
```

### 4. Week 1 notebook

```
Create notebooks/01_saadiyat_ingestion.ipynb that:
1. Imports the ingest, normalize, and ontology modules
2. Runs the full pipeline end-to-end: scrape Bayut → scrape Property Finder → reconcile → dedupe → write unified CSV
3. Displays summary statistics: total listings, by source, duplicate count, price range, bedroom distribution
4. Includes 3-5 markdown cells narrating the key decisions made and any data-quality issues encountered
5. Ends with a "Next steps" markdown cell listing what week 2 should add
Style follows CLAUDE.md voice principles (section 0): no exclamation marks, no emoji, declarative.
```

### 5. README and ontology docs

```
Write README.md per CLAUDE.md section 6.
Use the canonical problem statement from CLAUDE.md section 2 verbatim.
Write docs/ontology.md describing each entity, its fields, and its relationships (referencing src/auh_realty/ontology/entities.py).
Write docs/decisions.md as an empty file with a header explaining its purpose — to log one-paragraph rationales for non-obvious architectural decisions.
Voice per CLAUDE.md section 0.
```

---

## 11. Success criteria for end of Week 1

By the end of one week of evening work:

- [ ] Repo scaffolded per section 4
- [ ] At least 30 listings each from Bayut and Property Finder for Saadiyat, in unified CSV
- [ ] Duplicate detection working: at least one cross-source duplicate identified and flagged
- [ ] Notebook `01_saadiyat_ingestion.ipynb` runs end-to-end from a clean clone
- [ ] README.md committed with the canonical problem statement
- [ ] At least one entry in `docs/decisions.md` documenting a real choice you made
- [ ] All commits in clean voice per section 0

If scraping is blocked: the same checklist applies, but DLD Dubai data substitutes for Bayut + Property Finder Saadiyat. The end-to-end loop is what matters; the specific source is replaceable.

---

## 12. Anti-goals

What this project is NOT:

- Not a real estate marketplace
- Not a Zillow / Bayut competitor
- Not a SaaS product
- Not optimized for other people's use
- Not "AI-powered" in any meaningful sense (the LLM does not write decisions; the investor does)
- Not a portfolio piece designed to impress

It is operational analytical infrastructure for one investor's actual decisions, made public so the methods are credible and the ontology is reusable.

---

*Last updated: [author to date on commit]. This file is the canonical project context for Claude Code. Update it when the project's framing or constraints change.*
