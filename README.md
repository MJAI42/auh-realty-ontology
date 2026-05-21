# auh-realty-ontology

Building an ontology of UAE real estate data from heterogeneous public sources.

Started 05/21/2026.

## Problem

I am an active investor in real estate across three markets: Abu Dhabi, Tbilisi, and Tirana. Each market has heterogeneous public data sources — listings on consumer portals, transaction registers, developer announcements — none of which share a schema, none of which cross jurisdictions, and most of which report listing prices rather than transacted prices.
The decisions this affects are real: where to deploy the next capital allocation, whether a listing in a known neighborhood is mispriced relative to recent transactions, how Tirana entry prices compare to Tbilisi at the same property class, when to exit a position in Abu Dhabi.
Existing tools don't answer these questions. This repository ingests listings and transactions from heterogeneous public sources, structures them as a cross-jurisdictional property ontology, and surfaces (1) current and historical prices on a map, (2) comparative analysis across neighborhoods and markets, and (3) anomaly detection on listings that diverge from local patterns.

## Data sources

- **Bayut** — listings (Saadiyat scope, initial)
- **Property Finder** — listings (Saadiyat scope, initial)
- **DLD** — Dubai weekly transactions (cross-emirate extension)
- **Future** — ADREC Abu Dhabi data, scrapeable developer sites

## Ontology

Entities, relationships, properties — designed iteratively as the data shape
becomes clear.

Current draft:
- **Property** — villa, apartment, plot, townhouse
- **Listing** — a snapshot of a Property at a point in time (price, agent, source)
- **Agent**
- **Developer**
- **Neighborhood**

## Status

Active build. Week 1 focus: ingestion from Bayut + Property Finder for Saadiyat,
schema reconciliation, duplicate detection across sources.

## Notes

Future work: private-channel ingestion via WhatsApp Business API for personal
use, separate from this public ontology.
