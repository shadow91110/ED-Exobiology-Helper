import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, scrolledtext


# ---------------------------------------------------------------------------
# Data file resolution
# ---------------------------------------------------------------------------
# The planner now targets the richer "exobiology_species.json" schema
# (genus/species/value_credits/atmosphere/gravity{min_g,max_g}/volcanism/
# description/location/min_distance_between_genetic_samples_m/temperature_k,
# wrapped in a {"metadata": ..., "species": [...]} envelope). It will still
# happily load the older flat-list "species_data.json" format if that's all
# that's available, so nothing breaks if you swap files around.

NEW_FILENAME = "exobiology_species.json"
LEGACY_FILENAME = "species_data.json"


def resolve_data_file():
    search_dirs = [Path(__file__).resolve().parent]

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        search_dirs.append(exe_dir)
        if hasattr(sys, "_MEIPASS"):
            search_dirs.append(Path(sys._MEIPASS))

    candidates = []
    for directory in search_dirs:
        candidates.append(directory / NEW_FILENAME)
    for directory in search_dirs:
        candidates.append(directory / LEGACY_FILENAME)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Default to the new filename even if it doesn't exist yet, so the
    # error message / empty state points at the right place.
    return candidates[0]


DATA_FILE = resolve_data_file()


# ---------------------------------------------------------------------------
# Terrain / DSS-zone heuristics
# ---------------------------------------------------------------------------
# The new JSON schema doesn't carry a per-species "terrain" / "dss_visual_zone"
# field (it focuses on atmosphere, gravity, volcanism, value, temperature and
# colonial sample-distance instead). The pathing/advice engine below still
# wants a terrain label per species, so we derive one from genus-level field
# notes (and a couple of well-documented species-level exceptions), based on
# the in-game/Canonn lore describing where each genus is "regularly found".

TERRAIN_TO_ZONE = {
    "Plains": "Lowland Plains / Flatlands",
    "Deserts": "Lowland Plains / Flatlands",
    "Geothermal Vents": "Geothermal / Active Fields",
    "Hills": "Rugged Terrain / Foothills",
    "Rocky Fields": "Rugged Terrain / Foothills",
    "Valleys": "Rugged Terrain / Foothills",
    "Badlands": "Rugged Terrain / Foothills",
    "Glaciers": "Ice Sheets / Highland Caps",
    "Mountains": "Highlands / Mountain Ridges",
    "Canyons": "Deep Chasms / Canyons",
    "Craters": "Impact Basins / Craters",
}

GENUS_TERRAIN_DEFAULT = {
    "Recepta": "Plains",        # favour flattish, slightly undulating or gently sloping terrain
    "Bacterium": "Plains",      # preference for flat or slightly undulating terrain
    "Fonticulua": "Plains",     # mostly favour gently undulating plains
    "Frutexa": "Hills",         # colonise most terrain from plains to low mountains
    "Stratum": "Plains",        # mainly favour open, flattish terrain
    "Tussock": "Plains",        # clump grasses requiring a solid, mostly flat surface
    "Fungoida": "Mountains",    # preference for mountainous areas / mountain sides and peaks
    "Osseus": "Rocky Fields",   # found exclusively on rocky areas
    "Aleoida": "Plains",        # see species overrides below for the hillier/mountain species
    "Fumerola": "Geothermal Vents",  # located in regions with active fumaroles
    "Electricae": "Glaciers",   # extremely cold ice worlds near frozen lakes
    "Concha": "Valleys",        # excel in valleys at the foot of hills/mountains
    "Cactoida": "Plains",       # see species override for Peperatis
    "Clypeus": "Plains",        # rock-strewn plains and low hillside terrain
    "Tubus": "Plains",          # prefer open plains, tolerant of light undulation
}

SPECIES_TERRAIN_OVERRIDES = {
    # (genus, species) -> terrain  (documented exceptions to the genus default)
    ("Aleoida", "Coronamus"): "Hills",
    ("Aleoida", "Laminiae"): "Hills",
    ("Aleoida", "Spica"): "Mountains",
    ("Cactoida", "Peperatis"): "Hills",
    ("Fonticulua", "Digitos"): "Canyons",
}


def terrain_for(genus, species_name):
    override = SPECIES_TERRAIN_OVERRIDES.get((genus, species_name))
    if override:
        return override
    return GENUS_TERRAIN_DEFAULT.get(genus, "Plains")


def zone_for(terrain):
    return TERRAIN_TO_ZONE.get(terrain, "Rugged Terrain / Foothills")


# ---------------------------------------------------------------------------
# Record normalization
# ---------------------------------------------------------------------------

def _split_csv(value):
    if not value:
        return []
    return [piece.strip() for piece in value.split(",") if piece.strip()]


def normalize_new_record(raw):
    """Map an exobiology_species.json entry onto the field names the rest
    of the app expects to work with."""
    genus = raw.get("genus", "")
    species_name = raw.get("species", "")
    gravity = raw.get("gravity", {}) or {}
    terrain = terrain_for(genus, species_name)

    return {
        "genus": genus,
        "species": species_name,
        "base_value": raw.get("value_credits", 0),
        "scan_dist": raw.get("min_distance_between_genetic_samples_m", 0),
        "min_gravity": gravity.get("min_g", 0.0),
        "max_gravity": gravity.get("max_g", 1.0),
        "atmospheres": _split_csv(raw.get("atmosphere", "")),
        "compositions": _split_csv(raw.get("location", "")),
        "terrain": terrain,
        "dss_visual_zone": zone_for(terrain),
        "description": raw.get("description", ""),
        "volcanism": raw.get("volcanism", ""),
        "temperature_k": raw.get("temperature_k", {}) or {},
    }


def normalize_legacy_record(raw):
    """Pass an old-style flat species_data.json record through, filling in
    the newer optional fields (volcanism / temperature_k) if missing."""
    record = dict(raw)
    record.setdefault("volcanism", "")
    record.setdefault("temperature_k", {})
    record.setdefault("atmospheres", [])
    record.setdefault("compositions", [])
    record.setdefault("terrain", "Plains")
    record.setdefault("dss_visual_zone", zone_for(record["terrain"]))
    return record


def load_species_db():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    # New schema: {"metadata": {...}, "species": [ {...}, ... ]}
    if isinstance(data, dict) and "species" in data:
        return [normalize_new_record(item) for item in data["species"]]

    # Legacy schema: a bare list of flat records.
    if isinstance(data, list):
        return [normalize_legacy_record(item) for item in data]

    return []


SPECIES_DB = load_species_db()


def format_temperature(temp_range):
    if not temp_range:
        return None
    lo = temp_range.get("min")
    hi = temp_range.get("max")
    if lo is None or hi is None:
        return None
    return f"{lo:.0f}K - {hi:.0f}K"


class SpeciesPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ED Deep Species Planner")
        self.root.geometry("940x780")
        self.root.minsize(780, 560)
        self.root.configure(bg="#0d0d0d")

        self.root.resizable(True, True)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", background="#0d0d0d", foreground="#d9d9d9")
        style.configure("TFrame", background="#0d0d0d")
        style.configure("TLabelframe", background="#0d0d0d", foreground="#b8b8b8")
        style.configure("TLabelframe.Label", background="#0d0d0d", foreground="#b8b8b8")
        style.configure("TButton", background="#4f5f70", foreground="#f2f2f2")
        style.map("TButton", background=[("active", "#5f6f81"), ("disabled", "#2b2b2b")])
        style.configure("TCombobox", fieldbackground="#f5f5f5", background="#f5f5f5", foreground="#111111", selectbackground="#c7d8ff", selectforeground="#111111", arrowcolor="#111111")
        style.map("TCombobox", fieldbackground=[("readonly", "#f5f5f5")], foreground=[("readonly", "#111111")], selectbackground=[("readonly", "#c7d8ff")], selectforeground=[("readonly", "#111111")])
        style.configure("TEntry", fieldbackground="#f5f5f5", foreground="#111111")
        style.configure("TCheckbutton", background="#0d0d0d", foreground="#d9d9d9")

        self.filtered_valid_species = []
        self.signal_count_target = 0
        self.is_system_initialized = False
        self.slot_boxes = []
        self.slot_value_labels = []
        self.output_box = None

        self._build_ui()

    def _build_ui(self):
        header = ttk.Frame(self.root, padding=(16, 12, 16, 6))
        header.pack(fill="x")

        title = ttk.Label(header, text="🚀 ED DEEP SPECIES PLANNER", font=("Courier New", 16, "bold"), foreground="#e67e22")
        title.pack(side="left")

        self.first_footfall_var = tk.BooleanVar(value=False)
        toggle = ttk.Checkbutton(header, text="First Footfall", variable=self.first_footfall_var, command=self.update_payout_display)
        toggle.pack(side="right")

        reset_btn = ttk.Button(header, text="RESET", command=self.reset_form)
        reset_btn.pack(side="right", padx=(0, 12))

        if not SPECIES_DB:
            warn = ttk.Label(
                header,
                text=f"⚠ No species data loaded (looked for {DATA_FILE.name})",
                foreground="#e74c3c",
            )
            warn.pack(side="left", padx=(16, 0))

        telemetry = ttk.LabelFrame(self.root, text="Phase 1: Scan Telemetry", padding=12)
        telemetry.pack(fill="x", padx=12, pady=8)

        self.signal_count_var = tk.StringVar(value="3")
        self.atmos_var = tk.StringVar(value="Carbon Dioxide")
        self.composition_var = tk.StringVar(value="Rocky")
        gravity_values = [self._format_gravity_value(item["max_gravity"]) for item in SPECIES_DB]
        unique_gravity_values = sorted(set(gravity_values), key=lambda value: float(value)) if gravity_values else ["1.0"]
        self.gravity_var = tk.StringVar(value=unique_gravity_values[-1] if unique_gravity_values else "1.0")

        row1 = ttk.Frame(telemetry)
        row1.pack(fill="x")

        ttk.Label(row1, text="Signals:").pack(side="left", padx=(0, 8))
        ttk.Spinbox(row1, from_=1, to=15, textvariable=self.signal_count_var, width=8).pack(side="left")

        ttk.Label(row1, text="Atmosphere:").pack(side="left", padx=(18, 8))
        atmos_values = sorted({item for species in SPECIES_DB for item in species["atmospheres"]})
        if "Carbon Dioxide" not in atmos_values and atmos_values:
            self.atmos_var.set(atmos_values[0])
        self.atmos_cb = ttk.Combobox(row1, textvariable=self.atmos_var, values=atmos_values, state="readonly", width=18)
        self.atmos_cb.pack(side="left")
        self.atmos_cb.configure(font=("Courier New", 10, "bold"))
        self.atmos_cb.configure(style="TCombobox")

        ttk.Label(row1, text="Composition:").pack(side="left", padx=(18, 8))
        comp_values = sorted({item for species in SPECIES_DB for item in species["compositions"]})
        if "Rocky" not in comp_values and comp_values:
            self.composition_var.set(comp_values[0])
        self.comp_cb = ttk.Combobox(row1, textvariable=self.composition_var, values=comp_values, state="readonly", width=18)
        self.comp_cb.pack(side="left")
        self.comp_cb.configure(font=("Courier New", 10, "bold"))
        self.comp_cb.configure(style="TCombobox")

        ttk.Label(row1, text="Gravity:").pack(side="left", padx=(18, 8))
        self.gravity_cb = ttk.Combobox(row1, textvariable=self.gravity_var, values=unique_gravity_values, state="readonly", width=10)
        self.gravity_cb.pack(side="left")
        self.gravity_cb.configure(font=("Courier New", 10, "bold"))
        self.gravity_cb.configure(style="TCombobox")

        init_btn = ttk.Button(telemetry, text="INITIALIZE MATRIX", command=self.calculate_estimate)
        init_btn.pack(pady=(12, 4), fill="x")

        self.estimate_var = tk.StringVar(value="System Offline")
        ttk.Label(telemetry, textvariable=self.estimate_var, foreground="#2ecc71", font=("Courier New", 11, "bold")).pack(pady=(6, 0))

        slots = ttk.LabelFrame(self.root, text="Phase 2: Genus Identification", padding=12)
        slots.pack(fill="x", padx=12, pady=8)
        self.slot_container = ttk.Frame(slots)
        self.slot_container.pack(fill="x")

        logs = ttk.LabelFrame(self.root, text="Logs & Pathing", padding=12)
        logs.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log_frame = ttk.Frame(logs)
        self.log_frame.pack(fill="both", expand=True)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        self.advice_box = scrolledtext.ScrolledText(
            self.log_frame,
            height=10,
            bg="#0f0f0f",
            fg="#FFD36A",
            insertbackground="#FFD36A",
            selectbackground="#4a3b1a",
            selectforeground="#ffffff",
            font=("Courier New", 9),
            wrap="word",
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground="#3a3a3a",
            highlightcolor="#FFD36A"
        )
        self.advice_box.grid(row=0, column=0, sticky="nsew")
        self._fit_text_box(self.advice_box)

    def calculate_estimate(self):
        atmosphere = self.atmos_var.get()
        composition = self.composition_var.get()
        gravity_class = self.gravity_var.get()
        self.signal_count_target = int(self.signal_count_var.get())

        gravity_limit = float(gravity_class) if gravity_class else 1.0
        self.filtered_valid_species = [
            species for species in SPECIES_DB
            if atmosphere in species["atmospheres"]
            and composition in species["compositions"]
            and species["max_gravity"] <= gravity_limit
        ]

        self._clear_slot_rows()
        self.advice_box.delete("1.0", tk.END)
        self._fit_text_box(self.advice_box)

        if not self.filtered_valid_species:
            self.estimate_var.set("No compatible species found.")
            self.is_system_initialized = False
            return

        self.is_system_initialized = True

        viable_genera = sorted({species["genus"] for species in self.filtered_valid_species})
        combo_width = self._get_combo_width(viable_genera)
        self.slot_boxes = []
        self.slot_value_labels = []

        for idx in range(1, self.signal_count_target + 1):
            row = ttk.Frame(self.slot_container)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"Slot #{idx}:", width=8).pack(side="left")
            slot_var = tk.StringVar(value="")
            combo = ttk.Combobox(row, textvariable=slot_var, values=viable_genera, state="readonly", width=combo_width)
            combo.pack(side="left")
            combo.bind("<<ComboboxSelected>>", lambda event: self.update_payout_display())
            value_label = ttk.Label(row, text="—", width=12, foreground="#2ecc71", font=("Courier New", 10, "bold"))
            value_label.pack(side="left", padx=(6, 0))
            self.slot_boxes.append((slot_var, combo, value_label))
            self.slot_value_labels.append(value_label)

        self.update_payout_display()

    def update_payout_display(self):
        if not self.is_system_initialized:
            return

        multiplier = 5 if self.first_footfall_var.get() else 1
        selected_genera = [slot_var.get() for slot_var, _, _ in self.slot_boxes if slot_var.get()]

        for slot_var, _, value_label in self.slot_boxes:
            genus = slot_var.get()
            if genus:
                choices = [species for species in self.filtered_valid_species if species["genus"] == genus]
                if choices:
                    best = max(choices, key=lambda item: item["base_value"])
                    value_label.configure(text=f"{best['base_value']:,.0f} CR")
                else:
                    value_label.configure(text="—")
            else:
                value_label.configure(text="—")

        if not selected_genera:
            values = [species["base_value"] for species in self.filtered_valid_species]
            if values:
                minimum = min(values) * multiplier
                maximum = max(values) * multiplier
                self.estimate_var.set(f"Est. Range: {minimum:,.0f} - {maximum:,.0f} CR")
            else:
                self.estimate_var.set("No compatible species found.")
            return

        self.optimize_and_value()

    def optimize_and_value(self):
        if not self.is_system_initialized:
            return

        multiplier = 5 if self.first_footfall_var.get() else 1
        overall_total = 0
        items_to_route = []

        for _, slot_var, _ in self.slot_boxes:
            genus = slot_var.get()
            if genus:
                choices = [species for species in self.filtered_valid_species if species["genus"] == genus]
                if choices:
                    best = max(choices, key=lambda item: item["base_value"])
                    overall_total += best["base_value"]
                    best_item = dict(best)
                    best_item["description"] = self.get_species_description(genus, choices)
                    items_to_route.append(best_item)

        final_payout = overall_total * multiplier
        self.estimate_var.set(f"Projected: {final_payout:,.0f} CR")
        self.generate_optimized_path(items_to_route)

    def _clear_slot_rows(self):
        for widget in self.slot_container.winfo_children():
            widget.destroy()
        self.slot_boxes = []
        self.slot_value_labels = []

    def reset_form(self):
        self.first_footfall_var.set(False)
        self._clear_slot_rows()
        self.filtered_valid_species = []
        self.is_system_initialized = False
        self.signal_count_var.set("3")
        self.atmos_var.set("Carbon Dioxide")
        self.composition_var.set("Rocky")
        self.gravity_var.set(self.gravity_var.get() or "1.0")
        self.estimate_var.set("System Offline")
        self.advice_box.delete("1.0", tk.END)
        self._fit_text_box(self.advice_box)

    def get_species_description(self, genus, choices=None):
        if choices:
            for item in choices:
                description = item.get("description")
                if description:
                    return description
        return ""

    def generate_optimized_path(self, items):
        zones = [[], [], []]
        for item in items:
            zones[self.get_terrain_zone(item["dss_visual_zone"])].append(item)

        output = "🚀 SURFACE EXPLORATION CHAINING PROTOCOL:\n\n"
        output += "--- SPECIES IDENTIFIERS ---\n"
        for item in items:
            line = f"• {item['genus']} ({item['species']}) — {item['base_value']:,.0f} CR base"
            extras = []
            if item.get("volcanism"):
                extras.append(f"volcanism: {item['volcanism']}")
            temp_str = format_temperature(item.get("temperature_k"))
            if temp_str:
                extras.append(f"temp: {temp_str}")
            if extras:
                line += f"  [{'; '.join(extras)}]"
            output += line + "\n"
            description = item.get("description")
            if description:
                output += f"    ↳ {description}\n"
        output += "\n"
        for left_idx in range(2):
            if zones[left_idx] and zones[left_idx + 1]:
                output += f">>> OPTIMAL LANDING ZONE: [{self._zone_label(left_idx)}]\n"
                output += "    Strategy: Target the boundary line between biomes. This allows for a 'one-trip' collection cycle without orbital re-entry.\n\n"

        output += "--- EXECUTION PATH (Descending) ---\n"
        step = 1
        for idx in range(2, -1, -1):
            if zones[idx]:
                output += f"{step}. [Zone: {['PLAINS', 'FOOTHILLS', 'MOUNTAINS'][idx]}]\n"
                terrains = sorted({item["terrain"] for item in zones[idx]})
                for terrain in terrains:
                    matches = [item["genus"] for item in zones[idx] if item["terrain"] == terrain]
                    output += f"   - {terrain.upper()}: {', '.join(matches)}\n"
                    output += f"     Pilot Cue: {self.get_terrain_advice(terrain)}\n\n"
                output += f"   -> Transit: {idx > 0 and 'Descending slope to next cluster.' or 'Mission complete.'}\n\n"
                step += 1

        self.advice_box.delete("1.0", tk.END)
        self.advice_box.insert(tk.END, output)
        self._fit_text_box(self.advice_box)

    def get_terrain_zone(self, dss_zone):
        mapping = {
            "Lowland Plains / Flatlands": 0,
            "Geothermal / Active Fields": 1,
            "Rugged Terrain / Foothills": 1,
            "Ice Sheets / Highland Caps": 1,
            "Highlands / Mountain Ridges": 2,
            "Deep Chasms / Canyons": 2,
            "Fractured / Tectonic Zones": 2,
            "Impact Basins / Craters": 2,
        }
        return mapping.get(dss_zone, 1)

    def get_terrain_advice(self, terrain):
        advice_map = {
            "Mountains": "Check high-altitude rock formations. Look for clusters clinging to vertical cliff faces or tucked into the deep, shadowed pockets of craggy peaks.",
            "Craters": "Survey the central 'uplift' spike in the middle of the crater or the transition zone where the smooth basin floor meets the steep interior rim.",
            "Canyons": "Navigate the canyon floor, focusing on the interface between the bottom sediment and the lower vertical walls. Watch for light-catching textures.",
            "Plains": "Look for low-contrast color shifts on the flat ground. These species often blend into the terrain texture; use your ship's scanner while in low-hover to spot them.",
            "Hills": "Scan the gentle, upward-sloping sides. Avoid the peaks themselves; species here prefer the 'sheltered' middle elevation where wind erosion creates small gullies.",
            "Rocky Fields": "Scan for small, distinctive silhouettes between larger boulders. Your scanner range will be restricted by terrain clutter; move slowly with the SRV.",
            "Geothermal Vents": "Look for gas plumes on your HUD. High-yield clusters are usually found in the immediate, slightly cooler perimeter of the vent site.",
            "Glaciers": "Focus on the spiderweb fissures and deep ice-cracks. These species tend to grow where the ice sheet has fractured, providing grip for root systems.",
            "Badlands": "Carefully navigate the eroded, uneven ground. Prioritize the deep basins between ridges where moisture/sediment collects.",
            "Deserts": "Search the dunes, but keep your eyes on the 'leeward' side of the ridges. Look for high-contrast color patterns that break the uniform sand texture.",
            "Valleys": "Drop into the low ground between hills or mountains — these colonies tend to cluster densely right at the foot of the surrounding slopes.",
        }
        return advice_map.get(terrain, "Perform a high-intensity surface sweep; no specialized terrain markers identified.")

    def _zone_label(self, index):
        return "PLAINS/FOOTHILLS" if index == 0 else "FOOTHILLS/MOUNTAINS"

    def _format_gravity_value(self, value):
        return f"{value:.2f}".rstrip("0").rstrip(".") or "0"

    def _get_combo_width(self, values):
        if not values:
            return 10
        longest = max(values, key=len)
        return max(10, len(longest) + max(1, len(longest) // 3))

    def _fit_text_box(self, widget, min_height=4, max_height=28):
        content = widget.get("1.0", tk.END).rstrip("\n")
        line_count = max(1, len(content.splitlines()))
        widget.configure(height=min(max_height, max(min_height, line_count + 1)))


def main():
    root = tk.Tk()
    app = SpeciesPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
