// --- SPECIES DATABASE MAPPED TO VISUAL DSS HEATMAP OVERLAYS ---
const SPECIES_DB = [
    // --- FONTICULUA (Scan Distance: 500m) ---
    { genus: "Fonticulua", species: "digitos", base_value: 1804100, scan_dist: 500, min_gravity: 0.0, max_gravity: 0.27, atmospheres: ["Methane", "Methane-rich"], compositions: ["Icy", "Rocky"], terrain: "Fissures", dss_visual_zone: "Fractured / Tectonic Zones" },
    { genus: "Fonticulua", species: "campestris", base_value: 1000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Argon", "Argon-rich"], compositions: ["Icy", "Rocky"], terrain: "Geothermal Vents", dss_visual_zone: "Geothermal / Active Fields" },
    { genus: "Fonticulua", species: "upupam", base_value: 6835100, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Argon-rich"], compositions: ["Icy", "Rocky"], terrain: "Fissures", dss_visual_zone: "Fractured / Tectonic Zones" },
    { genus: "Fonticulua", species: "segmentatus", base_value: 19010800, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Neon-rich"], compositions: ["Icy"], terrain: "Geothermal Vents", dss_visual_zone: "Geothermal / Active Fields" },
    { genus: "Fonticulua", species: "lapida", base_value: 3111000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Nitrogen"], compositions: ["Icy", "Rocky"], terrain: "Glaciers", dss_visual_zone: "Ice Sheets / Highland Caps" },
    { genus: "Fonticulua", species: "fluctus", base_value: 20000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 0.20, atmospheres: ["Carbon Dioxide"], compositions: ["Icy"], terrain: "Canyons", dss_visual_zone: "Deep Chasms / Canyons" },

    // --- STRATUM (Scan Distance: 100m) ---
    { genus: "Stratum", species: "tectonicas", base_value: 19010800, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Carbon Dioxide-rich", "Oxygen", "Ammonia", "Water", "Water-rich", "Sulfur Dioxide"], compositions: ["Metal"], terrain: "Flat Fields", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "cucumisis", base_value: 16202800, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Carbon Dioxide-rich", "Sulfur Dioxide"], compositions: ["Rocky"], terrain: "Lowlands", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "excrescens", base_value: 16104400, scan_dist: 100, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Sulfur Dioxide"], compositions: ["Metal", "Rocky"], terrain: "Flat Fields", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "paleas", base_value: 2341200, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Nitrogen", "Ammonia", "Water", "Water-rich", "Carbon Dioxide", "Carbon Dioxide-rich"], compositions: ["Icy", "Rocky"], terrain: "Lowlands", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "laminamus", base_value: 4934500, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Ammonia"], compositions: ["Rocky", "Metal"], terrain: "Badlands", dss_visual_zone: "Rugged Terrain / Foothills" },
    { genus: "Stratum", species: "excutitus", base_value: 2710100, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Sulfur Dioxide"], compositions: ["Rocky"], terrain: "Dunes", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "limaxus", base_value: 2314500, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Sulfur Dioxide"], compositions: ["Rocky", "Metal"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Stratum", species: "frigus", base_value: 3200800, scan_dist: 100, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Carbon Dioxide-rich"], compositions: ["Icy"], terrain: "Glaciers", dss_visual_zone: "Ice Sheets / Highland Caps" },

    // --- BACTERIUM (Scan Distance: 500m) ---
    { genus: "Bacterium", species: "bullaris", base_value: 1152500, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Methane", "Methane-rich"], compositions: ["Icy", "Rocky", "Metal"], terrain: "Flat Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "vesicula", base_value: 1000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Argon", "Argon-rich"], compositions: ["Icy", "Rocky", "Metal"], terrain: "Smooth Basins", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "informem", base_value: 8418000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Nitrogen"], compositions: ["Icy", "Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "acies", base_value: 1000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Neon", "Neon-rich"], compositions: ["Icy", "Rocky", "Metal"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "volu", base_value: 7774700, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Oxygen"], compositions: ["Rocky", "Metal"], terrain: "Flat Basins", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "alcyoneum", base_value: 1658500, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Ammonia"], compositions: ["Rocky", "Metal"], terrain: "Lowlands", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "aurasus", base_value: 1000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Carbon Dioxide", "Carbon Dioxide-rich"], compositions: ["Rocky", "Metal"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "nebulus", base_value: 5289900, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Helium"], compositions: ["Icy"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "omentum", base_value: 4638900, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Neon", "Neon-rich"], compositions: ["Metal", "Rocky"], terrain: "Volcanic fields", dss_visual_zone: "Geothermal / Active Fields" },
    { genus: "Bacterium", species: "scopulum", base_value: 4934500, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Neon", "Neon-rich"], compositions: ["Rocky"], terrain: "Chasms", dss_visual_zone: "Deep Chasms / Canyons" },
    { genus: "Bacterium", species: "verrata", base_value: 3897000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Neon", "Neon-rich"], compositions: ["Icy", "Rocky"], terrain: "Smooth Basins", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "tela", base_value: 1949000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Nitrogen", "Methane", "Water"], compositions: ["Icy", "Rocky", "Metal"], terrain: "Fields", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Bacterium", species: "cerbrus", base_value: 1689800, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Sulfur Dioxide"], compositions: ["Rocky", "Metal"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    // --- FRUTEXA (Scan Distance: 150m) ---
    { genus: "Frutexa", species: "acus", base_value: 7774700, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.45, atmospheres: ["Carbon Dioxide"], compositions: ["Rocky"], terrain: "Mountains", dss_visual_zone: "Highlands / Mountain Ridges" },
    { genus: "Frutexa", species: "collum", base_value: 1639800, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.50, atmospheres: ["Carbon Dioxide-rich", "Sulfur Dioxide"], compositions: ["Rocky", "Metal"], terrain: "Rocky Slopes", dss_visual_zone: "Rugged Terrain / Foothills" },
    { genus: "Frutexa", species: "fera", base_value: 1632500, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Argon-rich", "Methane-rich"], compositions: ["Icy"], terrain: "Hills", dss_visual_zone: "Rugged Terrain / Foothills" },
    { genus: "Frutexa", species: "flabellum", base_value: 1808900, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Nitrogen"], compositions: ["Icy", "Rocky"], terrain: "Canyons", dss_visual_zone: "Deep Chasms / Canyons" },

    // --- RECEPTA (Scan Distance: 150m) ---
    { genus: "Recepta", species: "condylasis", base_value: 15309200, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.35, atmospheres: ["Oxygen", "Water"], compositions: ["Rocky", "Metal"], terrain: "Rough Ridges", dss_visual_zone: "Highlands / Mountain Ridges" },
    { genus: "Recepta", species: "delta", base_value: 8418000, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Sulfur Dioxide"], compositions: ["Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },

    // --- TUSSOCK (Scan Distance: 200m) ---
    { genus: "Tussock", species: "capillum", base_value: 7411200, scan_dist: 200, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Argon", "Argon-rich", "Methane", "Methane-rich"], compositions: ["Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Tussock", species: "propagito", base_value: 5000000, scan_dist: 200, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Nitrogen"], compositions: ["Rocky", "Metal"], terrain: "Fields", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Tussock", species: "catena", base_value: 1766600, scan_dist: 200, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Sulfur Dioxide"], compositions: ["Rocky"], terrain: "Lowlands", dss_visual_zone: "Lowland Plains / Flatlands" },

    // --- FUNGOIDA (Scan Distance: 300m) ---
    { genus: "Fungoida", species: "bullarum", base_value: 5000000, scan_dist: 300, min_gravity: 0.0, max_gravity: 0.30, atmospheres: ["Argon", "Argon-rich"], compositions: ["Icy", "Rocky"], terrain: "Mountains", dss_visual_zone: "Highlands / Mountain Ridges" },
    { genus: "Fungoida", species: "setisis", base_value: 4320100, scan_dist: 300, min_gravity: 0.0, max_gravity: 0.25, atmospheres: ["Methane", "Methane-rich"], compositions: ["Rocky"], terrain: "Highlands", dss_visual_zone: "Highlands / Mountain Ridges" },

    // --- OSSEUS (Scan Distance: 500m) ---
    { genus: "Osseus", species: "pumice", base_value: 4000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Argon", "Argon-rich", "Methane", "Methane-rich"], compositions: ["Rocky", "Metal"], terrain: "Rocky Fields", dss_visual_zone: "Rugged Terrain / Foothills" },
    { genus: "Osseus", species: "spiralis", base_value: 2404700, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.00, atmospheres: ["Sulfur Dioxide"], compositions: ["Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },

    // --- ALEOIDA (Scan Distance: 150m) ---
    { genus: "Aleoida", species: "coroniformis", base_value: 14000000, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.80, atmospheres: ["Carbon Dioxide", "Carbon Dioxide-rich"], compositions: ["Rocky", "Metal"], terrain: "Craters", dss_visual_zone: "Impact Basins / Craters" },

    // --- FUMEROLA (Scan Distance: 100m) ---
    { genus: "Fumerola", species: "carbofila", base_value: 6500000, scan_dist: 100, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Carbon Dioxide"], compositions: ["Metal"], terrain: "Geothermal Fields", dss_visual_zone: "Geothermal / Active Fields" },

    // --- ELECTRICAE (Scan Distance: 1000m) ---
    { genus: "Electricae", species: "segmentatus", base_value: 15000000, scan_dist: 1000, min_gravity: 0.0, max_gravity: 0.15, atmospheres: ["Neon-rich"], compositions: ["Icy"], terrain: "Glaciers", dss_visual_zone: "Ice Sheets / Highland Caps" },
    { genus: "Electricae", species: "radialem", base_value: 15000000, scan_dist: 1000, min_gravity: 0.0, max_gravity: 0.20, atmospheres: ["Argon", "Methane"], compositions: ["Icy", "Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands" },

    // --- CONCHA (Scan Distance: 150m) ---
    { genus: "Concha", species: "bivalvis", base_value: 12400000, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.60, atmospheres: ["Carbon Dioxide"], compositions: ["Rocky"], terrain: "Shorelines", dss_visual_zone: "Impact Basins / Craters" },

    // --- CACTOIDA (Scan Distance: 300m) ---
    { genus: "Cactoida", species: "cortex", base_value: 18000000, scan_dist: 300, min_gravity: 0.0, max_gravity: 0.90, atmospheres: ["Carbon Dioxide", "Oxygen"], compositions: ["Rocky", "Metal"], terrain: "Valleys", dss_visual_zone: "Rugged Terrain / Foothills" },

    // --- TUBUS (Scan Distance: 800m) ---
    { genus: "Tubus", species: "cavas", base_value: 59366000, scan_dist: 800, min_gravity: 0.0, max_gravity: 0.50, atmospheres: ["Nitrogen"], compositions: ["Rocky"], terrain: "Deserts", dss_visual_zone: "Lowland Plains / Flatlands" },
    { genus: "Tubus", species: "compagibus", base_value: 38873500, scan_dist: 800, min_gravity: 0.0, max_gravity: 0.50, atmospheres: ["Methane"], compositions: ["Rocky"], terrain: "Canyons", dss_visual_zone: "Deep Chasms / Canyons" },

    // --- CLYPEUS (Scan Distance: 150m) ---
    { genus: "Clypeus", species: "lacrimam", base_value: 11000000, scan_dist: 150, min_gravity: 0.0, max_gravity: 0.70, atmospheres: ["Water", "Water-rich"], compositions: ["Metal"], terrain: "Basins", dss_visual_zone: "Impact Basins / Craters" }
];

let filteredValidSpecies = [];
let signalCountTarget = 0;
function calculateEstimate() {
    const atmos = document.getElementById("atmos").value;
    const composition = document.getElementById("composition").value;
    const gravity = parseFloat(document.getElementById("gravity").value);
    signalCountTarget = parseInt(document.getElementById("signal_count").value);

    const logBox = document.getElementById("output_box");
    logBox.textContent = `[Telemetry Scan Initialized]\nAtmos: ${atmos}\nComposition: ${composition}\nGravity: ${gravity} G\nTarget Signals: ${signalCountTarget}\n\n`;

    filteredValidSpecies = SPECIES_DB.filter(s => {
        return s.atmospheres.includes(atmos) && 
               s.compositions.includes(composition) && 
               gravity >= s.min_gravity && 
               gravity <= s.max_gravity;
    });

    const dropContainer = document.getElementById("dropdown_container");
    const p2Btn = document.getElementById("calc_p2_btn");
    const label = document.getElementById("estimate_label");

    if (filteredValidSpecies.length === 0) {
        logBox.textContent += `[ERROR] Environmental parameters yield 0 viable baseline species.\nTelemetry profiles mismatch. Relocate landing zone.`;
        dropContainer.innerHTML = `<p style="color: #ff4757; font-size: 0.85rem; text-align: center;">Matrix Exception: No viable Genus matches current telemetry.</p>`;
        p2Btn.disabled = true;
        label.textContent = "Incompatible Environment Matrix";
        label.style.color = "#ff4757";
        return;
    }

    const viableGenera = [...new Set(filteredValidSpecies.map(s => s.genus))];
    
    logBox.textContent += `[Scan Success] Found ${filteredValidSpecies.length} total compatible species variations across ${viableGenera.length} unique Genera.\n`;
    viableGenera.forEach(g => {
        const sample = filteredValidSpecies.find(s => s.genus === g);
        logBox.textContent += ` -> Viable Genus: ${g.toUpperCase()} | Required Scan Colony Separation: ${sample.scan_dist}m\n`;
    });

    dropContainer.innerHTML = "";
    for (let i = 1; i <= signalCountTarget; i++) {
        const row = document.createElement("div");
        row.className = "slot-row";
        
        const labelEl = document.createElement("label");
        labelEl.textContent = `Signal Slot #${i}:`;
        
        const selectEl = document.createElement("select");
        selectEl.id = `slot_genus_${i}`;
        
        const defaultOpt = document.createElement("option");
        defaultOpt.value = "";
        defaultOpt.textContent = "-- Select Identified Genus --";
        selectEl.appendChild(defaultOpt);

        viableGenera.forEach(g => {
            const opt = document.createElement("option");
            opt.value = g;
            opt.textContent = g;
            selectEl.appendChild(opt);
        });

        row.appendChild(labelEl);
        row.appendChild(selectEl);
        dropContainer.appendChild(row);
    }

    p2Btn.disabled = false;
    label.textContent = "Matrix Online - Assign Detected Genus Slots";
    label.style.color = "var(--accent)";
}
function optimizeAndValue() {
    const logBox = document.getElementById("output_box");
    const label = document.getElementById("estimate_label");
    logBox.textContent += `\n[Evaluating Field Identification Profiles...]\n`;

    let selectedGenera = [];
    for (let i = 1; i <= signalCountTarget; i++) {
        const val = document.getElementById(`slot_genus_${i}`).value;
        if (val) { selectedGenera.push(val); }
    }

    if (selectedGenera.length === 0) {
        logBox.textContent += `[Warning] No target genera assigned to slots. Calculations halted.\n`;
        alert("Please assign at least one detected genus to a slot.");
        return;
    }

    let overallTotalBaseValue = 0;
    let itemsToRoute = [];

    selectedGenera.forEach((gen, index) => {
        const choices = filteredValidSpecies.filter(s => s.genus === gen);
        if (choices.length > 0) {
            choices.sort((a, b) => b.base_value - a.base_value);
            const optimalSpecies = choices[0]; // Resolves index mapping issue safely
            
            overallTotalBaseValue += optimalSpecies.base_value;
            itemsToRoute.push(optimalSpecies);

            logBox.textContent += `Slot #${index+1} Resolved -> ${optimalSpecies.genus} ${optimalSpecies.species} | Area: ${optimalSpecies.terrain} | Value: ${optimalSpecies.base_value.toLocaleString()} CR\n`;
        }
    });

    // --- VISUAL HEATMAP COMPILATION ENGINE ---
    logBox.textContent += `\n[COMPILING FLIGHT ROUTING MATRIX...]`;
    
    let visualOverlayGroups = {};
    itemsToRoute.forEach(item => {
        if (!visualOverlayGroups[item.dss_visual_zone]) {
            visualOverlayGroups[item.dss_visual_zone] = [];
        }
        visualOverlayGroups[item.dss_visual_zone].push({
            name: `${item.genus} ${item.species}`,
            dist: item.scan_dist,
            micro: item.terrain
        });
    });

    logBox.textContent += `\n=======================================================\n`;
    logBox.textContent += `🛰️ ORBITAL DSS HEATMAP TARGET GUIDE (VISUAL DROPZONES):\n`;
    logBox.textContent += `=======================================================\n`;

    let dropZoneCounter = 1;
    for (const [dssZone, speciesList] of Object.entries(visualOverlayGroups)) {
        logBox.textContent += `🟢 VISUAL DSS ZONE #${dropZoneCounter} -> [${dssZone.toUpperCase()}]\n`;
        logBox.textContent += `   Aim your glide path down toward these visual surface areas.\n`;
        
        speciesList.forEach(sp => {
            logBox.textContent += `   👉 ${sp.name} [Requires ${sp.dist}m separation | Found in micro-terrain: ${sp.micro}]\n`;
        });
        logBox.textContent += `\n`;
        dropZoneCounter++;
    }

    // --- SEPARATED GAME PAYOUT CALCULATIONS ---
    const totalFirstFootfallPayout = overallTotalBaseValue * 5;

    logBox.textContent += `-------------------------------------------------------\n`;
    logBox.textContent += `📊 ECONOMIC EXPLORATION REWARD ESTIMATES:\n`;
    logBox.textContent += `-------------------------------------------------------\n`;
    logBox.textContent += `Standard System (Total Base Value): ${overallTotalBaseValue.toLocaleString()} CR\n`;
    logBox.textContent += `Pristine System (Total First Footfall): ${totalFirstFootfallPayout.toLocaleString()} CR\n`;
    logBox.textContent += `=======================================================\n`;
    
    logBox.scrollTop = logBox.scrollHeight;

    label.textContent = `Pristine Est: ${totalFirstFootfallPayout.toLocaleString()} CR`;
    label.style.color = "var(--success)";
}
