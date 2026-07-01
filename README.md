# ED Deep Species Planner

A lightweight desktop planner for Elite Dangerous species scouting and payout estimation.

The application helps a player narrow down compatible species from telemetry filters, identify likely genera for each signal slot, and generate a simple scouting plan with route guidance and payout estimates.

## What this project does

- Loads species data from JSON files
- Filters species using telemetry-style inputs such as:
  - atmosphere
  - composition
  - gravity
  - temperature range
  - volcanism severity/type
- Lets the user assign a genus to each signal slot
- Estimates potential payout ranges or values
- Produces a planning log with:
  - eligible species information
  - terrain-based pathing guidance
  - landing-zone suggestions

## Project files

- [species_planner.py](species_planner.py) — Main Tkinter desktop application
- [exobiology_species.json](exobiology_species.json) — Primary species database
- [species_data.json](species_data.json) — Legacy fallback species database
- [run_planner.pyw](run_planner.pyw) — Optional wrapper for launching the planner without a console window

## Requirements

- Python 3.9+
- Tkinter (usually included with Python on Windows)

## Running the planner

### Windows

From the project folder, run:

```powershell
.venv\Scripts\python.exe species_planner.py
```

Or launch the wrapper:

```powershell
.venv\Scripts\python.exe run_planner.pyw
```

### General usage

1. Open the planner.
2. Set the scan telemetry filters.
3. Click "INITIALIZE MATRIX".
4. Choose the genus for each signal slot.
5. Review the payout estimate and planning log.

## How the code is organized

The core logic is implemented in [species_planner.py](species_planner.py) and follows a simple flow:

1. Load species data from JSON
2. Normalize records into a consistent internal shape
3. Apply the telemetry filters
4. Build a list of compatible genera
5. Let the user select genera for each slot
6. Calculate payout estimates and produce a planning report

## Data format notes

The planner supports two species data formats:

- a richer structured format from [exobiology_species.json](exobiology_species.json)
- a legacy flat-list format from [species_data.json](species_data.json)

The normalization layer keeps the rest of the program consistent regardless of which source file is used.

## Suggested future improvements

The following enhancements would make the planner more powerful and user-friendly:

- Save/load planner sessions so users can revisit a previous setup
- Export reports to plain text, CSV, or Markdown
- Add support for weighted probability estimates rather than simple ranges
- Add a more advanced pathing engine with multi-zone route optimization
- Support user-defined custom terrain or scouting heuristics
- Add a dark/light theme toggle or more polished UI themes
- Add species sorting by value, rarity, or compatibility score
- Add a search/filter box for genera or species names
- Add per-genera confidence indicators based on how many species remain eligible
- Add unit tests for filtering, normalization, and estimate calculation

## Notes for contributors

If you plan to modify the planner:

- Keep the filtering and normalization logic separate from the UI code where possible
- Preserve the existing JSON compatibility layer
- Prefer small, well-named helper functions over large blocks of logic
- Keep the output log readable and explainable for users who are not programmers
