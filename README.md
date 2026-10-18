# Dortmund Air Shield

City-wide drone network planner for police, fire brigade, THW, and the city of Dortmund. Built by Team Pilots for the DO-Data-Hackathon 2026 (challenge by Morpheus Logistik GmbH).

The recommended plan places 27 docked stations on existing fire and police sites and reaches 97.3% of residents within 4 minutes.

## What's in this repo

- `app/` — interactive planner (`air-shield-planner-en.html`)
- `data/` — open data, model outputs, and CSV exports
- `presentation/` — pitch deck source and notes
- `tools/` — rebuild scripts
- `PROJECT_NOTES.md` — decisions, model, and results
- `CALCULATION_METHODS.md` — formulas
- `ARTIFACTS.md` — how to open and export the planner and deck

## Open the planner

Open `app/air-shield-planner-en.html` in a browser. The map and data are embedded; a network connection is only needed for D3.js and Google Fonts.

## Rebuild

```bash
python tools/build_data.py
python tools/build_app.py
node tools/export_csv.js
python tools/export_raw_csv.py
```

Edit `app/planner.template.html`, then rebuild. Do not edit the generated HTML by hand.
