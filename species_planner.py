import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, scrolledtext


def _split_csv(value):
    if not value:
        return []
    if isinstance(value, list):
        return [piece.strip() for piece in value if piece and str(piece).strip()]
    return [piece.strip() for piece in str(value).replace(";", ",").split(",") if piece.strip()]


def _parse_volcanism_tags(value):
    tags = []
    if not value:
        return tags

    parts = [part.strip() for part in str(value).replace(";", ",").split(",") if part.strip()]
    pending_intensity = None

    for part in parts:
        segment = part.strip()
        lower = segment.lower()

        if any(token in lower for token in ("no volcanism", "none", "nil")):
            tags.append("None")
            pending_intensity = None
            continue
        if "insignificant" in lower or "low (tolerance" in lower or "low" in lower:
            tags.append("Insignificant")
            pending_intensity = None
            continue

        intensity = None
        if "major" in lower:
            intensity = "Major"
            segment = segment.replace("major", "", 1).strip()
        elif "minor" in lower:
            intensity = "Minor"
            segment = segment.replace("minor", "", 1).strip()

        if intensity:
            pending_intensity = intensity

        cleaned = segment
        cleaned = cleaned.replace("magma", "").replace("geyser", "").replace("geysers", "")
        cleaned = cleaned.replace("/", " ")
        cleaned = cleaned.strip()
        cleaned = cleaned.replace("(tolerance, not preference)", "")
        cleaned = cleaned.replace("and", " ").replace("or", " ")

        if not cleaned and pending_intensity:
            continue

        for candidate in [item.strip() for item in cleaned.split() if item.strip()]:
            lowered = candidate.lower()
            if lowered in {"and", "or", "of", "the"}:
                continue
            if lowered in {"carbon", "dioxide"}:
                substance = "Carbon Dioxide"
            elif lowered in {"methane"}:
                substance = "Methane"
            elif lowered in {"nitrogen"}:
                substance = "Nitrogen"
            elif lowered in {"ammonia"}:
                substance = "Ammonia"
            elif lowered in {"water"}:
                substance = "Water"
            elif lowered in {"silicate", "silicate-based", "silicate/vapor", "vapour", "vapor"}:
                substance = "Silicate"
            elif lowered in {"rocky"}:
                substance = "Rocky"
            elif lowered in {"metallic"}:
                substance = "Metallic"
            elif lowered in {"sulphur", "sulfur"}:
                substance = "Sulphur Dioxide"
            elif lowered in {"oxygen"}:
                substance = "Oxygen"
            elif lowered in {"argon"}:
                substance = "Argon"
            elif lowered in {"helium"}:
                substance = "Helium"
            elif lowered in {"neon"}:
                substance = "Neon"
            else:
                continue
            intensity_to_use = pending_intensity if pending_intensity and not intensity else (intensity or pending_intensity)
            tags.append(f"{intensity_to_use} {substance}" if intensity_to_use else substance)

        if intensity:
            pending_intensity = None

    return sorted(set(tags))


def _canonical_volcanism_severity(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    lowered = text.lower()
    if lowered in {"any", "all"}:
        return "Any"
    if lowered in {"none", "no volcanism", "nil"}:
        return "None"
    if lowered in {"low", "insignificant", "low (tolerance, not preference)"}:
        return "Low"
    if lowered in {"minor"}:
        return "Minor"
    if lowered in {"major"}:
        return "Major"
    return text


def _canonical_volcanism_type(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    lowered = text.lower()
    if lowered in {"any", "all"}:
        return "Any"
    if lowered in {"none", "no volcanism", "nil"}:
        return "None"
    return text


def _parse_volcanism_components(value):
    if not value:
        return []

    components = []
    for tag in _parse_volcanism_tags(value):
        if tag.lower() in {"none", "insignificant"}:
            components.append(("None" if tag.lower() == "none" else "Low", None))
            continue
        parts = tag.split(" ", 1)
        if len(parts) == 2:
            severity = _canonical_volcanism_severity(parts[0])
            volcanism_type = _canonical_volcanism_type(parts[1])
            components.append((severity, volcanism_type))
        else:
            components.append((_canonical_volcanism_severity(tag), None))
    return components


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

def _parse_temperature_limit(value):
    text = str(value).strip()
    if not text or text.lower() in {"any", "all"}:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def normalize_new_record(raw):
    """Map an exobiology_species.json entry onto the field names the rest
    of the app expects to work with."""
    genus = raw.get("genus", "")
    species_name = raw.get("species", "")
    gravity = raw.get("gravity", {}) or {}
    terrain = terrain_for(genus, species_name)

    volcanism_text = raw.get("volcanism", "")
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
        "volcanism": volcanism_text,
        "volcanism_tags": _parse_volcanism_tags(volcanism_text),
        "volcanism_components": _parse_volcanism_components(volcanism_text),
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
    record["volcanism_tags"] = _parse_volcanism_tags(record.get("volcanism", ""))
    record["volcanism_components"] = _parse_volcanism_components(record.get("volcanism", ""))
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
        self.atmos_var = tk.StringVar(value="Any")
        self.composition_var = tk.StringVar(value="Rocky")
        gravity_values = [self._format_gravity_value(item["max_gravity"]) for item in SPECIES_DB]
        unique_gravity_values = sorted(set(gravity_values), key=lambda value: float(value)) if gravity_values else ["1.0"]
        self.gravity_var = tk.StringVar(value="Any")
        self.temp_min_var = tk.StringVar(value="0")
        self.temp_max_var = tk.StringVar(value="1000")
        self.volcanism_severity_var = tk.StringVar(value="Any")
        self.volcanism_type_var = tk.StringVar(value="Any")

        row1 = ttk.Frame(telemetry)
        row1.pack(fill="x")

        ttk.Label(row1, text="Signals:").pack(side="left", padx=(0, 8))
        ttk.Spinbox(row1, from_=1, to=15, textvariable=self.signal_count_var, width=8).pack(side="left")

        ttk.Label(row1, text="Atmosphere:").pack(side="left", padx=(18, 8))
        atmos_values = sorted({"Any", *{item for species in SPECIES_DB for item in species["atmospheres"]}})
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
        gravity_choices = ["Any"] + unique_gravity_values
        self.gravity_cb = ttk.Combobox(row1, textvariable=self.gravity_var, values=gravity_choices, state="readonly", width=10)
        self.gravity_cb.pack(side="left")
        self.gravity_cb.configure(font=("Courier New", 10, "bold"))
        self.gravity_cb.configure(style="TCombobox")

        row2 = ttk.Frame(telemetry)
        row2.pack(fill="x", pady=(10, 0))

        ttk.Label(row2, text="Temp (K):").pack(side="left", padx=(0, 8))
        ttk.Spinbox(row2, from_=0, to=1000, textvariable=self.temp_min_var, width=8).pack(side="left")
        ttk.Label(row2, text="to").pack(side="left", padx=(6, 6))
        ttk.Spinbox(row2, from_=0, to=1000, textvariable=self.temp_max_var, width=8).pack(side="left")

        ttk.Label(row2, text="Volcanism Severity:").pack(side="left", padx=(18, 8))
        severity_values = ["Any", "None", "Low", "Insignificant", "Minor", "Major"]
        self.volcanism_severity_cb = ttk.Combobox(row2, textvariable=self.volcanism_severity_var, values=severity_values, state="readonly", width=12)
        self.volcanism_severity_cb.pack(side="left")
        self.volcanism_severity_cb.configure(font=("Courier New", 10, "bold"))
        self.volcanism_severity_cb.configure(style="TCombobox")

        ttk.Label(row2, text="Type:").pack(side="left", padx=(8, 8))
        volcanism_types = ["Any"] + sorted({component[1] for species in SPECIES_DB for component in species.get("volcanism_components", []) if component[1]})
        self.volcanism_type_cb = ttk.Combobox(row2, textvariable=self.volcanism_type_var, values=volcanism_types, state="readonly", width=18)
        self.volcanism_type_cb.pack(side="left")
        self.volcanism_type_cb.configure(font=("Courier New", 10, "bold"))
        self.volcanism_type_cb.configure(style="TCombobox")

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

        gravity_limit = float(gravity_class) if gravity_class and gravity_class != "Any" else None
        temp_min = _parse_temperature_limit(self.temp_min_var.get())
        temp_max = _parse_temperature_limit(self.temp_max_var.get())
        volcanism_severity = self.volcanism_severity_var.get()
        volcanism_type = self.volcanism_type_var.get()

        self.filtered_valid_species = [
            species for species in SPECIES_DB
            if self._atmosphere_matches(species["atmospheres"], atmosphere)
            and composition in species["compositions"]
            and (gravity_limit is None or species["max_gravity"] <= gravity_limit)
            and self._temperature_matches(species.get("temperature_k"), temp_min, temp_max)
            and self._volcanism_matches(species, volcanism_severity, volcanism_type)
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
        auto_genus = viable_genera[0] if len(viable_genera) == 1 else ""

        for idx in range(1, self.signal_count_target + 1):
            row = ttk.Frame(self.slot_container)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"Slot #{idx}:", width=8).pack(side="left")
            slot_var = tk.StringVar(value=auto_genus)
            combo = ttk.Combobox(row, textvariable=slot_var, values=viable_genera, state="readonly", width=combo_width)
            combo.pack(side="left")
            combo.bind("<<ComboboxSelected>>", lambda event: self.update_payout_display())
            value_label = ttk.Label(
                row,
                text="—",
                width=24,
                anchor="w",
                foreground="#2ecc71",
                font=("Courier New", 10, "bold"),
            )
            value_label.pack(side="left", padx=(6, 0))
            self.slot_boxes.append((slot_var, combo, value_label))
            self.slot_value_labels.append(value_label)

        self.update_payout_display()

    def _atmosphere_matches(self, atmospheres, selected):
        if not selected or selected == "Any":
            return True
        return selected in atmospheres

    def _temperature_matches(self, temp_range, temp_min, temp_max):
        if temp_min is None and temp_max is None:
            return True
        if not temp_range:
            return True
        lo = temp_range.get("min")
        hi = temp_range.get("max")
        if lo is None or hi is None:
            return True
        if temp_min is not None and hi < temp_min:
            return False
        if temp_max is not None and lo > temp_max:
            return False
        return True

    def _volcanism_matches(self, species, severity_selected, type_selected):
        severity_choice = _canonical_volcanism_severity(severity_selected)
        type_choice = _canonical_volcanism_type(type_selected)
        components = species.get("volcanism_components", [])

        if severity_choice in {None, "Any"} and type_choice in {None, "Any"}:
            return True

        if severity_choice == "None":
            return any(_canonical_volcanism_severity(component[0]) == "None" for component in components)

        if severity_choice in {None, "Any"}:
            return any(
                component[1] is not None and _canonical_volcanism_type(component[1]).lower() == type_choice.lower()
                for component in components
            )

        if type_choice in {None, "Any"}:
            return any(
                _canonical_volcanism_severity(component[0]).lower() == severity_choice.lower()
                for component in components
            )

        return any(
            _canonical_volcanism_severity(component[0]).lower() == severity_choice.lower()
            and component[1] is not None
            and _canonical_volcanism_type(component[1]).lower() == type_choice.lower()
            for component in components
        )

    def _get_global_value_range(self):
        values = [species["base_value"] for species in self.filtered_valid_species]
        if not values:
            return None
        return min(values), max(values)

    def _get_genus_value_range(self, genus):
        if not genus:
            return None
        choices = [species for species in self.filtered_valid_species if species["genus"] == genus]
        if not choices:
            return None
        values = [species["base_value"] for species in choices]
        return min(values), max(values)

    def _format_value_range(self, low, high):
        if low is None or high is None:
            return "—"
        if low == high:
            return f"{low:,.0f} CR"
        return f"{low:,.0f} - {high:,.0f} CR"

    def update_payout_display(self):
        if not self.is_system_initialized:
            return

        for slot_var, _, value_label in self.slot_boxes:
            genus = slot_var.get()
            if value_label is not None:
                if genus:
                    value_range = self._get_genus_value_range(genus)
                    if value_range is not None:
                        value_label.configure(text=self._format_value_range(*value_range))
                    else:
                        value_label.configure(text="—")
                else:
                    value_label.configure(text="—")

        self.optimize_and_value()

    def optimize_and_value(self):
        if not self.is_system_initialized:
            return

        multiplier = 5 if self.first_footfall_var.get() else 1
        global_range = self._get_global_value_range()
        if not global_range:
            self.estimate_var.set("No compatible species found.")
            return

        overall_min_total = 0
        overall_max_total = 0
        items_to_route = []

        for slot in self.slot_boxes:
            slot_var = slot[0] if len(slot) > 0 else None
            genus = slot_var.get() if slot_var is not None else ""
            if genus:
                value_range = self._get_genus_value_range(genus) or global_range
                choices = [species for species in self.filtered_valid_species if species["genus"] == genus]
                best = max(choices, key=lambda item: item["base_value"]) if choices else None
                if best is not None:
                    item = dict(best)
                    item["value_range"] = value_range
                    item["species_options"] = [species["species"] for species in choices]
                    item["description"] = self.get_species_description(genus, choices)
                    items_to_route.append(item)
            else:
                value_range = global_range

            overall_min_total += value_range[0]
            overall_max_total += value_range[1]

        if overall_min_total == overall_max_total:
            self.estimate_var.set(f"Est. Value: {overall_min_total * multiplier:,.0f} CR")
        else:
            self.estimate_var.set(f"Est. Range: {overall_min_total * multiplier:,.0f} - {overall_max_total * multiplier:,.0f} CR")
        unresolved_slots = max(0, self.signal_count_target - len(items_to_route))
        self.generate_optimized_path(items_to_route, unresolved_slots=unresolved_slots)

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
        self.atmos_var.set("Any")
        self.composition_var.set("Rocky")
        self.gravity_var.set(self.gravity_var.get() or "Any")
        self.temp_min_var.set("0")
        self.temp_max_var.set("1000")
        self.volcanism_severity_var.set("Any")
        self.volcanism_type_var.set("Any")
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

    def generate_optimized_path(self, items, unresolved_slots=0):
        zones = [[], [], []]
        for item in items:
            zones[self.get_terrain_zone(item.get("dss_visual_zone"))].append(item)

        output = "🚀 SURFACE EXPLORATION CHAINING PROTOCOL:\n\n"
        output += "--- SPECIES IDENTIFIERS ---\n"
        if not items:
            output += "No genera selected yet. The current estimate reflects the full range of compatible species under the active filters.\n"
        else:
            for item in items:
                value_range = item.get("value_range")
                if value_range:
                    line = f"• {item['genus']} — {self._format_value_range(*value_range)}"
                else:
                    line = f"• {item['genus']} ({item['species']}) — {item['base_value']:,.0f} CR base"
                if item.get("species_options"):
                    options = ", ".join(item["species_options"][:8])
                    if len(item["species_options"]) > 8:
                        options += ", ..."
                    line += f"\n    ↳ Eligible species: {options}"
                output += line + "\n"
                description = item.get("description")
                if description:
                    output += f"    ↳ {description}\n"

        output += "\n"
        for left_idx in range(2):
            if zones[left_idx] and zones[left_idx + 1]:
                output += f">>> OPTIMAL LANDING ZONE: [{self._zone_label(left_idx)}]\n"
                output += "    Strategy: Target the boundary line between adjacent terrain clusters. This allows a one-trip collection cycle with minimal re-entry travel.\n\n"

        output += "--- EXECUTION PATH (Descending) ---\n"
        active_zones = [idx for idx in range(2, -1, -1) if zones[idx]]
        step = 1
        for idx in active_zones:
            if not zones[idx]:
                continue
            output += f"{step}. [Zone: {['PLAINS', 'FOOTHILLS', 'MOUNTAINS'][idx]}]\n"
            terrains = sorted({item["terrain"] for item in zones[idx]})
            for terrain in terrains:
                matches = [item["genus"] for item in zones[idx] if item["terrain"] == terrain]
                output += f"   - {terrain.upper()}: {', '.join(matches)}\n"
                output += f"     Pilot Cue: {self.get_terrain_advice(terrain)}\n\n"
            if len(active_zones) <= 1:
                output += "   -> End condition: Single sample identified; collect it and complete the mission.\n\n"
            elif idx == active_zones[-1]:
                output += "   -> End condition: Sample collection complete.\n\n"
            else:
                output += "   -> Transit: Descending slope to next cluster.\n\n"
            step += 1

        if unresolved_slots:
            global_range = self._get_global_value_range()
            if global_range:
                output += f"Unresolved slots: {unresolved_slots}\n"
                output += f"Potential payout for unresolved slots: {self._format_value_range(global_range[0], global_range[1])}\n"

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
