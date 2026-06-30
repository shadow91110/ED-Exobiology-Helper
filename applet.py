import tkinter as tk
from tkinter import ttk, scrolledtext


SPECIES_DB = [
    {"genus": "Fonticulua", "species": "digitos", "base_value": 1804100, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 0.27, "atmospheres": ["Methane", "Methane-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Fissures", "dss_visual_zone": "Fractured / Tectonic Zones"},
    {"genus": "Fonticulua", "species": "campestris", "base_value": 1000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Argon", "Argon-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Geothermal Vents", "dss_visual_zone": "Geothermal / Active Fields"},
    {"genus": "Fonticulua", "species": "upupam", "base_value": 6835100, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Argon-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Fissures", "dss_visual_zone": "Fractured / Tectonic Zones"},
    {"genus": "Fonticulua", "species": "segmentatus", "base_value": 19010800, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Neon-rich"], "compositions": ["Icy"], "terrain": "Geothermal Vents", "dss_visual_zone": "Geothermal / Active Fields"},
    {"genus": "Fonticulua", "species": "lapida", "base_value": 3111000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Nitrogen"], "compositions": ["Icy", "Rocky"], "terrain": "Glaciers", "dss_visual_zone": "Ice Sheets / Highland Caps"},
    {"genus": "Fonticulua", "species": "fluctus", "base_value": 20000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 0.20, "atmospheres": ["Carbon Dioxide"], "compositions": ["Icy"], "terrain": "Canyons", "dss_visual_zone": "Deep Chasms / Canyons"},

    {"genus": "Stratum", "species": "tectonicas", "base_value": 19010800, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Carbon Dioxide-rich", "Oxygen", "Ammonia", "Water", "Water-rich", "Sulfur Dioxide"], "compositions": ["Metal"], "terrain": "Flat Fields", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "cucumisis", "base_value": 16202800, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Carbon Dioxide-rich", "Sulfur Dioxide"], "compositions": ["Rocky"], "terrain": "Lowlands", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "excrescens", "base_value": 16104400, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 0.40, "atmospheres": ["Sulfur Dioxide"], "compositions": ["Metal", "Rocky"], "terrain": "Flat Fields", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "paleas", "base_value": 2341200, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Nitrogen", "Ammonia", "Water", "Water-rich", "Carbon Dioxide", "Carbon Dioxide-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Lowlands", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "laminamus", "base_value": 4934500, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Ammonia"], "compositions": ["Rocky", "Metal"], "terrain": "Badlands", "dss_visual_zone": "Rugged Terrain / Foothills"},
    {"genus": "Stratum", "species": "excutitus", "base_value": 2710100, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Sulfur Dioxide"], "compositions": ["Rocky"], "terrain": "Dunes", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "limaxus", "base_value": 2314500, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Sulfur Dioxide"], "compositions": ["Rocky", "Metal"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Stratum", "species": "frigus", "base_value": 3200800, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Carbon Dioxide-rich"], "compositions": ["Icy"], "terrain": "Glaciers", "dss_visual_zone": "Ice Sheets / Highland Caps"},

    {"genus": "Bacterium", "species": "bullaris", "base_value": 1152500, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Methane", "Methane-rich"], "compositions": ["Icy", "Rocky", "Metal"], "terrain": "Flat Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "vesicula", "base_value": 1000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Argon", "Argon-rich"], "compositions": ["Icy", "Rocky", "Metal"], "terrain": "Smooth Basins", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "informem", "base_value": 8418000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Nitrogen"], "compositions": ["Icy", "Rocky"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "acies", "base_value": 1000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Neon", "Neon-rich"], "compositions": ["Icy", "Rocky", "Metal"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "volu", "base_value": 7774700, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Oxygen"], "compositions": ["Rocky", "Metal"], "terrain": "Flat Basins", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "alcyoneum", "base_value": 1658500, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Ammonia"], "compositions": ["Rocky", "Metal"], "terrain": "Lowlands", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "aurasus", "base_value": 1000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Carbon Dioxide", "Carbon Dioxide-rich"], "compositions": ["Rocky", "Metal"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "nebulus", "base_value": 5289900, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Helium"], "compositions": ["Icy"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "omentum", "base_value": 4638900, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Neon", "Neon-rich"], "compositions": ["Metal", "Rocky"], "terrain": "Volcanic fields", "dss_visual_zone": "Geothermal / Active Fields"},
    {"genus": "Bacterium", "species": "scopulum", "base_value": 4934500, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Neon", "Neon-rich"], "compositions": ["Rocky"], "terrain": "Chasms", "dss_visual_zone": "Deep Chasms / Canyons"},
    {"genus": "Bacterium", "species": "verrata", "base_value": 3897000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Neon", "Neon-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Smooth Basins", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "tela", "base_value": 1949000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Nitrogen", "Methane", "Water"], "compositions": ["Icy", "Rocky", "Metal"], "terrain": "Fields", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Bacterium", "species": "cerbrus", "base_value": 1689800, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Sulfur Dioxide"], "compositions": ["Rocky", "Metal"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},

    {"genus": "Frutexa", "species": "acus", "base_value": 7774700, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.45, "atmospheres": ["Carbon Dioxide"], "compositions": ["Rocky"], "terrain": "Mountains", "dss_visual_zone": "Highlands / Mountain Ridges"},
    {"genus": "Frutexa", "species": "collum", "base_value": 1639800, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.50, "atmospheres": ["Carbon Dioxide-rich", "Sulfur Dioxide"], "compositions": ["Rocky", "Metal"], "terrain": "Rocky Slopes", "dss_visual_zone": "Rugged Terrain / Foothills"},
    {"genus": "Frutexa", "species": "fera", "base_value": 1632500, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.40, "atmospheres": ["Argon-rich", "Methane-rich"], "compositions": ["Icy"], "terrain": "Hills", "dss_visual_zone": "Rugged Terrain / Foothills"},
    {"genus": "Frutexa", "species": "flabellum", "base_value": 1808900, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.40, "atmospheres": ["Nitrogen"], "compositions": ["Icy", "Rocky"], "terrain": "Canyons", "dss_visual_zone": "Deep Chasms / Canyons"},

    {"genus": "Recepta", "species": "condylasis", "base_value": 15309200, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.35, "atmospheres": ["Oxygen", "Water"], "compositions": ["Rocky", "Metal"], "terrain": "Rough Ridges", "dss_visual_zone": "Highlands / Mountain Ridges"},
    {"genus": "Recepta", "species": "delta", "base_value": 8418000, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.40, "atmospheres": ["Sulfur Dioxide"], "compositions": ["Rocky"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},

    {"genus": "Tussock", "species": "capillum", "base_value": 7411200, "scan_dist": 200, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Argon", "Argon-rich", "Methane", "Methane-rich"], "compositions": ["Rocky"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Tussock", "species": "propagito", "base_value": 5000000, "scan_dist": 200, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Nitrogen"], "compositions": ["Rocky", "Metal"], "terrain": "Fields", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Tussock", "species": "catena", "base_value": 1766600, "scan_dist": 200, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Sulfur Dioxide"], "compositions": ["Rocky"], "terrain": "Lowlands", "dss_visual_zone": "Lowland Plains / Flatlands"},

    {"genus": "Fungoida", "species": "bullarum", "base_value": 5000000, "scan_dist": 300, "min_gravity": 0.0, "max_gravity": 0.30, "atmospheres": ["Argon", "Argon-rich"], "compositions": ["Icy", "Rocky"], "terrain": "Mountains", "dss_visual_zone": "Highlands / Mountain Ridges"},
    {"genus": "Fungoida", "species": "setisis", "base_value": 4320100, "scan_dist": 300, "min_gravity": 0.0, "max_gravity": 0.25, "atmospheres": ["Methane", "Methane-rich"], "compositions": ["Rocky"], "terrain": "Highlands", "dss_visual_zone": "Highlands / Mountain Ridges"},

    {"genus": "Osseus", "species": "pumice", "base_value": 4000000, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Argon", "Argon-rich", "Methane", "Methane-rich"], "compositions": ["Rocky", "Metal"], "terrain": "Rocky Fields", "dss_visual_zone": "Rugged Terrain / Foothills"},
    {"genus": "Osseus", "species": "spiralis", "base_value": 2404700, "scan_dist": 500, "min_gravity": 0.0, "max_gravity": 1.00, "atmospheres": ["Sulfur Dioxide"], "compositions": ["Rocky"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},

    {"genus": "Aleoida", "species": "coroniformis", "base_value": 14000000, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.80, "atmospheres": ["Carbon Dioxide", "Carbon Dioxide-rich"], "compositions": ["Rocky", "Metal"], "terrain": "Craters", "dss_visual_zone": "Impact Basins / Craters"},

    {"genus": "Fumerola", "species": "carbofila", "base_value": 6500000, "scan_dist": 100, "min_gravity": 0.0, "max_gravity": 0.40, "atmospheres": ["Carbon Dioxide"], "compositions": ["Metal"], "terrain": "Geothermal Fields", "dss_visual_zone": "Geothermal / Active Fields"},

    {"genus": "Electricae", "species": "segmentatus", "base_value": 15000000, "scan_dist": 1000, "min_gravity": 0.0, "max_gravity": 0.15, "atmospheres": ["Neon-rich"], "compositions": ["Icy"], "terrain": "Glaciers", "dss_visual_zone": "Ice Sheets / Highland Caps"},
    {"genus": "Electricae", "species": "radialem", "base_value": 15000000, "scan_dist": 1000, "min_gravity": 0.0, "max_gravity": 0.20, "atmospheres": ["Argon", "Methane"], "compositions": ["Icy", "Rocky"], "terrain": "Plains", "dss_visual_zone": "Lowland Plains / Flatlands"},

    {"genus": "Concha", "species": "bivalvis", "base_value": 12400000, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.60, "atmospheres": ["Carbon Dioxide"], "compositions": ["Rocky"], "terrain": "Shorelines", "dss_visual_zone": "Impact Basins / Craters"},

    {"genus": "Cactoida", "species": "cortex", "base_value": 18000000, "scan_dist": 300, "min_gravity": 0.0, "max_gravity": 0.90, "atmospheres": ["Carbon Dioxide", "Oxygen"], "compositions": ["Rocky", "Metal"], "terrain": "Valleys", "dss_visual_zone": "Rugged Terrain / Foothills"},

    {"genus": "Tubus", "species": "cavas", "base_value": 59366000, "scan_dist": 800, "min_gravity": 0.0, "max_gravity": 0.50, "atmospheres": ["Nitrogen"], "compositions": ["Rocky"], "terrain": "Deserts", "dss_visual_zone": "Lowland Plains / Flatlands"},
    {"genus": "Tubus", "species": "compagibus", "base_value": 38873500, "scan_dist": 800, "min_gravity": 0.0, "max_gravity": 0.50, "atmospheres": ["Methane"], "compositions": ["Rocky"], "terrain": "Canyons", "dss_visual_zone": "Deep Chasms / Canyons"},

    {"genus": "Clypeus", "species": "lacrimam", "base_value": 11000000, "scan_dist": 150, "min_gravity": 0.0, "max_gravity": 0.70, "atmospheres": ["Water", "Water-rich"], "compositions": ["Metal"], "terrain": "Basins", "dss_visual_zone": "Impact Basins / Craters"}
]


class SpeciesPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ED Deep Species Planner")
        self.root.geometry("900x720")
        self.root.minsize(860, 680)
        self.root.configure(bg="#111111")

        self.root.resizable(False, False)

        self.filtered_valid_species = []
        self.signal_count_target = 0
        self.is_system_initialized = False
        self.slot_boxes = []

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

        telemetry = ttk.LabelFrame(self.root, text="Phase 1: Scan Telemetry", padding=12)
        telemetry.pack(fill="x", padx=12, pady=8)

        self.signal_count_var = tk.StringVar(value="3")
        self.atmos_var = tk.StringVar(value="Carbon Dioxide")
        self.composition_var = tk.StringVar(value="Rocky")
        self.gravity_var = tk.StringVar(value="high")

        row1 = ttk.Frame(telemetry)
        row1.pack(fill="x")

        ttk.Label(row1, text="Signals:").pack(side="left", padx=(0, 8))
        ttk.Spinbox(row1, from_=1, to=15, textvariable=self.signal_count_var, width=8).pack(side="left")

        ttk.Label(row1, text="Atmosphere:").pack(side="left", padx=(18, 8))
        atmos_values = sorted({item for species in SPECIES_DB for item in species["atmospheres"]})
        self.atmos_cb = ttk.Combobox(row1, textvariable=self.atmos_var, values=atmos_values, state="readonly", width=18)
        self.atmos_cb.pack(side="left")

        ttk.Label(row1, text="Composition:").pack(side="left", padx=(18, 8))
        comp_values = sorted({item for species in SPECIES_DB for item in species["compositions"]})
        self.comp_cb = ttk.Combobox(row1, textvariable=self.composition_var, values=comp_values, state="readonly", width=14)
        self.comp_cb.pack(side="left")

        ttk.Label(row1, text="Gravity:").pack(side="left", padx=(18, 8))
        gravity_values = ["low", "high"]
        self.gravity_cb = ttk.Combobox(row1, textvariable=self.gravity_var, values=gravity_values, state="readonly", width=10)
        self.gravity_cb.pack(side="left")

        init_btn = ttk.Button(telemetry, text="INITIALIZE MATRIX", command=self.calculate_estimate)
        init_btn.pack(pady=(12, 4), fill="x")

        self.estimate_var = tk.StringVar(value="System Offline")
        ttk.Label(telemetry, textvariable=self.estimate_var, foreground="#2ecc71", font=("Courier New", 11, "bold")).pack(pady=(6, 0))

        slots = ttk.LabelFrame(self.root, text="Phase 2: Genus Identification", padding=12)
        slots.pack(fill="x", padx=12, pady=8)
        self.slot_container = ttk.Frame(slots)
        self.slot_container.pack(fill="x")

        logs = ttk.LabelFrame(self.root, text="Logs & Pathing", padding=12)
        logs.pack(fill="x", padx=12, pady=(0, 12))

        self.output_box = scrolledtext.ScrolledText(logs, height=1, bg="#080808", fg="#2ecc71", font=("Courier New", 10, "bold"), wrap="word")
        self.output_box.pack(fill="x")
        self.output_box.insert(tk.END, "Terminal core online...\n")
        self._fit_text_height(self.output_box)

        self.advice_box = scrolledtext.ScrolledText(logs, height=1, bg="#191919", fg="#f1c40f", font=("Courier New", 10), wrap="word")
        self.advice_box.pack(fill="x", pady=(8, 0))

    def calculate_estimate(self):
        atmosphere = self.atmos_var.get()
        composition = self.composition_var.get()
        gravity_class = self.gravity_var.get()
        self.signal_count_target = int(self.signal_count_var.get())

        self.filtered_valid_species = [
            species for species in SPECIES_DB
            if atmosphere in species["atmospheres"]
            and composition in species["compositions"]
            and ((gravity_class == "low" and species["max_gravity"] <= 0.27) or (gravity_class == "high" and species["max_gravity"] > 0.27))
        ]

        self._clear_slot_rows()
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "[Processing Identification...]\n")
        self._fit_text_height(self.output_box)
        self.advice_box.delete("1.0", tk.END)
        self._fit_text_height(self.advice_box)

        if not self.filtered_valid_species:
            self.estimate_var.set("No compatible species found.")
            self.is_system_initialized = False
            return

        self.is_system_initialized = True

        viable_genera = sorted({species["genus"] for species in self.filtered_valid_species})
        self.slot_boxes = []

        for idx in range(1, self.signal_count_target + 1):
            row = ttk.Frame(self.slot_container)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"Slot #{idx}:", width=12).pack(side="left")
            slot_var = tk.StringVar(value="")
            combo = ttk.Combobox(row, textvariable=slot_var, values=viable_genera, state="readonly", width=36)
            combo.pack(side="left", fill="x", expand=True)
            combo.bind("<<ComboboxSelected>>", lambda event: self.update_payout_display())
            self.slot_boxes.append((slot_var, combo))

        self.update_payout_display()

    def update_payout_display(self):
        if not self.is_system_initialized:
            return

        multiplier = 5 if self.first_footfall_var.get() else 1
        selected_genera = [slot_var.get() for slot_var, _ in self.slot_boxes if slot_var.get()]

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

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "[Processing Identification...]\n")
        self._fit_text_height(self.output_box)

        for idx, (slot_var, _) in enumerate(self.slot_boxes, start=1):
            genus = slot_var.get()
            if genus:
                choices = [species for species in self.filtered_valid_species if species["genus"] == genus]
                if choices:
                    best = max(choices, key=lambda item: item["base_value"])
                    overall_total += best["base_value"]
                    items_to_route.append(best)
                    self.output_box.insert(tk.END, f"Slot #{idx}: {best['genus']} - {best['base_value']:,.0f} CR\n")

        final_payout = overall_total * multiplier
        self.output_box.insert(tk.END, f"\nTotal Projected: {final_payout:,.0f} CR")
        self._fit_text_height(self.output_box)
        self.estimate_var.set(f"Projected: {final_payout:,.0f} CR")
        self.generate_optimized_path(items_to_route)

    def _clear_slot_rows(self):
        for widget in self.slot_container.winfo_children():
            widget.destroy()
        self.slot_boxes = []

    def reset_form(self):
        self.first_footfall_var.set(False)
        self._clear_slot_rows()
        self.filtered_valid_species = []
        self.is_system_initialized = False
        self.signal_count_var.set("3")
        self.atmos_var.set("Carbon Dioxide")
        self.composition_var.set("Rocky")
        self.gravity_var.set("high")
        self.estimate_var.set("System Offline")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "System reset. Standing by for survey data...\n")
        self._fit_text_height(self.output_box)
        self.advice_box.delete("1.0", tk.END)
        self._fit_text_height(self.advice_box)

    def generate_optimized_path(self, items):
        zones = [[], [], []]
        for item in items:
            zones[self.get_terrain_zone(item["dss_visual_zone"])].append(item)

        output = "🚀 SURFACE EXPLORATION CHAINING PROTOCOL:\n\n"
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
        self._fit_text_height(self.advice_box)

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
        }
        return advice_map.get(terrain, "Perform a high-intensity surface sweep; no specialized terrain markers identified.")

    def _zone_label(self, index):
        return "PLAINS/FOOTHILLS" if index == 0 else "FOOTHILLS/MOUNTAINS"

    def _fit_text_height(self, widget, max_height=10):
        content = widget.get("1.0", tk.END)
        lines = max(1, len(content.splitlines()))
        widget.configure(height=min(max_height, lines))


def main():
    root = tk.Tk()
    app = SpeciesPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
