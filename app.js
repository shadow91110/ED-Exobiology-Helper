const FALLBACK_SPECIES_DB = [
    { genus: "Fonticulua", species: "Digitos", base_value: 1804100, scan_dist: 500, min_gravity: 0.0, max_gravity: 0.27, atmospheres: ["Methane", "Methane-rich"], compositions: ["Icy", "Rocky"], terrain: "Canyons", dss_visual_zone: "Deep Chasms / Canyons", description: "A methane-adapted forest-like species that favours fractured terrain.", volcanism: "Insignificant", temperature_k: { min: 80, max: 260 } },
    { genus: "Fonticulua", species: "Campestris", base_value: 1000000, scan_dist: 500, min_gravity: 0.0, max_gravity: 1.0, atmospheres: ["Argon", "Argon-rich"], compositions: ["Icy", "Rocky"], terrain: "Geothermal Vents", dss_visual_zone: "Geothermal / Active Fields", description: "A broad-spectrum Fonticulua species associated with warm vent fields.", volcanism: "Low", temperature_k: { min: 90, max: 300 } },
    { genus: "Stratum", species: "Excrescens", base_value: 16104400, scan_dist: 100, min_gravity: 0.0, max_gravity: 0.40, atmospheres: ["Sulfur Dioxide"], compositions: ["Metal", "Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands", description: "A high-value Stratum species that clusters on stable metal-rich plains.", volcanism: "Low", temperature_k: { min: 130, max: 320 } },
    { genus: "Bacterium", species: "Acies", base_value: 1000000, scan_dist: 500, min_gravity: 0.26, max_gravity: 1.18, atmospheres: ["Neon", "Neon-rich"], compositions: ["Icy", "Rocky"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands", description: "A bright neon-adapted bacterium that thrives in cold, open landscapes.", volcanism: "Low", temperature_k: { min: 20, max: 138 } },
    { genus: "Recepta", species: "Conditivus", base_value: 14313700, scan_dist: 150, min_gravity: 0.04, max_gravity: 0.28, atmospheres: ["Sulfur Dioxide", "Carbon Dioxide"], compositions: ["Rocky", "Metal"], terrain: "Plains", dss_visual_zone: "Lowland Plains / Flatlands", description: "A Recepta species suspended within a translucent membrane, suited to low-gravity worlds.", volcanism: "Insignificant", temperature_k: { min: 132, max: 272 } },
    { genus: "Fungoida", species: "Bullarum", base_value: 5000000, scan_dist: 300, min_gravity: 0.0, max_gravity: 0.30, atmospheres: ["Argon", "Argon-rich"], compositions: ["Icy", "Rocky"], terrain: "Mountains", dss_visual_zone: "Highlands / Mountain Ridges", description: "A mountain-hugging Fungoida with strong affinities for argon-rich worlds.", volcanism: "Insignificant", temperature_k: { min: 120, max: 255 } },
    { genus: "Tubus", species: "Cavas", base_value: 59366000, scan_dist: 800, min_gravity: 0.0, max_gravity: 0.50, atmospheres: ["Nitrogen"], compositions: ["Rocky"], terrain: "Deserts", dss_visual_zone: "Lowland Plains / Flatlands", description: "A rare, high-paying Tubus species typically tied to arid, nitrogen-rich plains.", volcanism: "Insignificant", temperature_k: { min: 220, max: 380 } }
];

let SPECIES_DB = [];
let filteredValidSpecies = [];
let signalCountTarget = 0;
let isSystemInitialized = false;
let genusLookup = {};
let genusValueCache = {};
let globalValueRange = null;
let dataSourceLabel = "built-in fallback";

function initPlanner() {
    populateControls();
    window.addEventListener("DOMContentLoaded", () => {
        loadSpeciesDatabase().then(() => {
            populateControls();
            resetForm();
            document.getElementById("estimate_label").textContent = "Awaiting telemetry input…";
        });
    });
}

function populateControls() {
    if (!SPECIES_DB.length) {
        return;
    }
    const atmosphereSelect = document.getElementById("atmosphere");
    const compositionSelect = document.getElementById("composition");
    const gravitySelect = document.getElementById("gravity");
    const severitySelect = document.getElementById("volcanism_severity");
    const typeSelect = document.getElementById("volcanism_type");

    if (atmosphereSelect && atmosphereSelect.options.length === 0) {
        const atmosValues = ["Any", ...sortUnique(SPECIES_DB.flatMap((s) => s.atmospheres || []))];
        atmosphereSelect.innerHTML = atmosValues.map((value) => `<option value="${value}">${value}</option>`).join("");
        atmosphereSelect.value = "Any";
    }
    if (compositionSelect && compositionSelect.options.length === 0) {
        const compositionValues = ["Any", ...sortUnique(SPECIES_DB.flatMap((s) => s.compositions || []))];
        compositionSelect.innerHTML = compositionValues.map((value) => `<option value="${value}">${value}</option>`).join("");
        compositionSelect.value = "Any";
    }
    if (gravitySelect && gravitySelect.options.length === 0) {
        const gravityValues = ["Any", ...sortUnique(SPECIES_DB.map((s) => Number(s.max_gravity || 0)).map((value) => value.toFixed(2).replace(/0+$/, "").replace(/\.$/, "")))];
        gravitySelect.innerHTML = gravityValues.map((value) => `<option value="${value}">${value}</option>`).join("");
        gravitySelect.value = "Any";
    }
    if (severitySelect && severitySelect.options.length === 0) {
        const severityValues = ["Any", "None", "Low", "Insignificant", "Minor", "Major"];
        severitySelect.innerHTML = severityValues.map((value) => `<option value="${value}">${value}</option>`).join("");
        severitySelect.value = "Any";
    }
    if (typeSelect && typeSelect.options.length === 0) {
        const typeValues = ["Any", ...sortUnique(SPECIES_DB.flatMap((s) => getVolcanismTypes(s)).filter(Boolean))];
        typeSelect.innerHTML = typeValues.map((value) => `<option value="${value}">${value}</option>`).join("");
        typeSelect.value = "Any";
    }
}

function sortUnique(values) {
    return [...new Set(values.filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b)));
}

function normalizeSpecies(raw) {
    const genus = raw.genus || "";
    const speciesName = raw.species || "";
    const gravity = raw.gravity || {};
    const atmospheres = Array.isArray(raw.atmospheres) ? raw.atmospheres : splitCsv(raw.atmosphere || raw.atmospheres || "");
    const compositions = Array.isArray(raw.compositions) ? raw.compositions : splitCsv(raw.location || raw.compositions || "");
    const temperature = raw.temperature_k || raw.temperature || {};
    const volcanismText = raw.volcanism || "";
    const terrain = raw.terrain || terrainFor(genus, speciesName);
    return {
        genus,
        species: speciesName,
        base_value: raw.base_value ?? raw.value_credits ?? 0,
        scan_dist: raw.scan_dist ?? raw.min_distance_between_genetic_samples_m ?? 0,
        min_gravity: raw.min_gravity ?? gravity.min_g ?? gravity.min ?? 0,
        max_gravity: raw.max_gravity ?? gravity.max_g ?? gravity.max ?? 1,
        atmospheres: atmospheres.map((item) => String(item).trim()).filter(Boolean),
        compositions: compositions.map((item) => String(item).trim()).filter(Boolean),
        terrain,
        dss_visual_zone: raw.dss_visual_zone || zoneFor(terrain),
        description: raw.description || "",
        volcanism: volcanismText,
        volcanism_tags: parseVolcanismTags(volcanismText),
        volcanism_components: parseVolcanismComponents(volcanismText),
        temperature_k: normalizeTemperature(temperature)
    };
}

function splitCsv(value) {
    if (!value) {
        return [];
    }
    if (Array.isArray(value)) {
        return value;
    }
    return String(value).split(/[;,/]+/).map((item) => item.trim()).filter(Boolean);
}

function normalizeTemperature(temp) {
    if (!temp) {
        return {};
    }
    if (typeof temp === "object") {
        return {
            min: Number(temp.min ?? temp.min_k ?? 0),
            max: Number(temp.max ?? temp.max_k ?? 1000)
        };
    }
    return {};
}

function terrainFor(genus, speciesName) {
    const overrides = {
        "Aleoida:Coronamus": "Hills",
        "Aleoida:Laminiae": "Hills",
        "Aleoida:Spica": "Mountains",
        "Cactoida:Peperatis": "Hills",
        "Fonticulua:Digitos": "Canyons"
    };
    const key = `${genus}:${speciesName}`;
    if (overrides[key]) {
        return overrides[key];
    }
    const defaults = {
        Recepta: "Plains",
        Bacterium: "Plains",
        Fonticulua: "Plains",
        Frutexa: "Hills",
        Stratum: "Plains",
        Tussock: "Plains",
        Fungoida: "Mountains",
        Osseus: "Rocky Fields",
        Aleoida: "Plains",
        Fumerola: "Geothermal Vents",
        Electricae: "Glaciers",
        Concha: "Valleys",
        Cactoida: "Plains",
        Clypeus: "Plains",
        Tubus: "Plains"
    };
    return defaults[genus] || "Plains";
}

function zoneFor(terrain) {
    const mapping = {
        Plains: "Lowland Plains / Flatlands",
        "Geothermal Vents": "Geothermal / Active Fields",
        Hills: "Rugged Terrain / Foothills",
        Glaciers: "Ice Sheets / Highland Caps",
        Mountains: "Highlands / Mountain Ridges",
        Canyons: "Deep Chasms / Canyons",
        Valleys: "Impact Basins / Craters",
        "Rocky Fields": "Rugged Terrain / Foothills"
    };
    return mapping[terrain] || "Lowland Plains / Flatlands";
}

function parseVolcanismTags(text) {
    if (!text) {
        return [];
    }
    return String(text).split(/\s*,\s*/).filter(Boolean);
}

function parseVolcanismComponents(text) {
    if (!text) {
        return [];
    }
    return String(text).split(/\s*;\s*/).map((part) => part.trim()).filter(Boolean);
}

function getVolcanismTypes(species) {
    const components = species.volcanism_components || [];
    return components.map((entry) => {
        if (typeof entry === "string") {
            return entry.split(/\s*:\s*/).pop();
        }
        return entry[1] || entry.type || "";
    }).filter(Boolean);
}

function canonicalVolcanismSeverity(value) {
    if (!value || value === "Any") {
        return "Any";
    }
    const normalized = String(value).toLowerCase();
    if (normalized.includes("none")) {
        return "None";
    }
    if (normalized.includes("insignificant")) {
        return "Insignificant";
    }
    if (normalized.includes("minor")) {
        return "Minor";
    }
    if (normalized.includes("major")) {
        return "Major";
    }
    if (normalized.includes("low")) {
        return "Low";
    }
    return value;
}

function canonicalVolcanismType(value) {
    if (!value || value === "Any") {
        return "Any";
    }
    return String(value).toLowerCase();
}

async function loadSpeciesDatabase() {
    try {
        const response = await fetch("exobiology_species.json", { cache: "no-store" });
        if (!response.ok) {
            throw new Error("JSON not found");
        }
        const payload = await response.json();
        const records = Array.isArray(payload) ? payload : (payload && Array.isArray(payload.species) ? payload.species : []);
        SPECIES_DB = records.map(normalizeSpecies);
        dataSourceLabel = "shared JSON";
        document.getElementById("data_status").textContent = `Loaded ${SPECIES_DB.length} species from the shared JSON.`;
    } catch (error) {
        SPECIES_DB = FALLBACK_SPECIES_DB.map(normalizeSpecies);
        dataSourceLabel = "built-in fallback";
        document.getElementById("data_status").textContent = `Using ${dataSourceLabel} dataset (${SPECIES_DB.length} species).`;
    }
    populateControls();
}

function calculateEstimate() {
    const atmosphere = document.getElementById("atmosphere").value;
    const composition = document.getElementById("composition").value;
    const gravityValue = document.getElementById("gravity").value;
    const tempMin = Number(document.getElementById("temp_min").value || 0);
    const tempMax = Number(document.getElementById("temp_max").value || 1000);
    const volcanismSeverity = document.getElementById("volcanism_severity").value;
    const volcanismType = document.getElementById("volcanism_type").value;
    signalCountTarget = parseInt(document.getElementById("signal_count").value || "3", 10);

    filteredValidSpecies = SPECIES_DB.filter((species) => {
        const matchesAtmosphere = atmosphere === "Any" || (species.atmospheres || []).includes(atmosphere);
        const matchesComposition = composition === "Any" || (species.compositions || []).includes(composition);
        const matchesGravity = gravityValue === "Any" || Number(species.max_gravity || 0) <= Number(gravityValue);
        const matchesTemperature = temperatureMatches(species.temperature_k, tempMin, tempMax);
        const matchesVolcanism = volcanismMatches(species, volcanismSeverity, volcanismType);
        return matchesAtmosphere && matchesComposition && matchesGravity && matchesTemperature && matchesVolcanism;
    });

    genusLookup = {};
    genusValueCache = {};
    globalValueRange = null;

    if (filteredValidSpecies.length) {
        for (const species of filteredValidSpecies) {
            if (!genusLookup[species.genus]) {
                genusLookup[species.genus] = [];
            }
            genusLookup[species.genus].push(species);
        }
        Object.entries(genusLookup).forEach(([genus, choices]) => {
            const values = choices.map((entry) => Number(entry.base_value || 0));
            genusValueCache[genus] = [Math.min(...values), Math.max(...values)];
        });
        const values = filteredValidSpecies.map((entry) => Number(entry.base_value || 0));
        globalValueRange = [Math.min(...values), Math.max(...values)];
    }

    const dropContainer = document.getElementById("dropdown_container");
    const p2Btn = document.getElementById("calc_p2_btn");
    const label = document.getElementById("estimate_label");

    if (!filteredValidSpecies.length) {
        label.textContent = "No compatible species found.";
        label.style.color = "#ff6b6b";
        isSystemInitialized = false;
        p2Btn.disabled = true;
        dropContainer.innerHTML = "<p class='status'>No species matched the current telemetry filters.</p>";
        document.getElementById("output_box").textContent = "No compatible species found. Try relaxing one or more filters.";
        document.getElementById("pathing_advice").textContent = "Awaiting survey data…";
        return;
    }

    isSystemInitialized = true;
    p2Btn.disabled = false;
    const viableGenera = sortUnique(filteredValidSpecies.map((species) => species.genus));
    dropContainer.innerHTML = "";
    const autoGenus = viableGenera.length === 1 ? viableGenera[0] : "";

    for (let index = 1; index <= signalCountTarget; index += 1) {
        const row = document.createElement("div");
        row.className = "slot-row";
        row.innerHTML = `
            <label for="slot_genus_${index}">Slot #${index}</label>
            <select id="slot_genus_${index}" onchange="updatePayoutDisplay()">
                <option value="">-- Select Genus --</option>
                ${viableGenera.map((genus) => `<option value="${genus}" ${autoGenus === genus ? "selected" : ""}>${genus}</option>`).join("")}
            </select>
            <div class="value-label" id="slot_value_${index}">—</div>`;
        dropContainer.appendChild(row);
    }

    updatePayoutDisplay();
}

function temperatureMatches(tempRange, tempMin, tempMax) {
    if (!tempRange || (!tempMin && !tempMax)) {
        return true;
    }
    const lo = Number(tempRange.min ?? 0);
    const hi = Number(tempRange.max ?? 1000);
    if (!Number.isFinite(lo) || !Number.isFinite(hi)) {
        return true;
    }
    if (tempMin && hi < tempMin) {
        return false;
    }
    if (tempMax && lo > tempMax) {
        return false;
    }
    return true;
}

function volcanismMatches(species, severitySelected, typeSelected) {
    const severity = canonicalVolcanismSeverity(severitySelected);
    const type = canonicalVolcanismType(typeSelected);
    const components = species.volcanism_components || [];
    if (severity === "Any" && type === "Any") {
        return true;
    }
    if (severity === "None") {
        return components.some((component) => canonicalVolcanismSeverity(component) === "None");
    }
    if (severity === "Any") {
        return components.some((component) => canonicalVolcanismType(component).includes(type));
    }
    if (type === "Any") {
        return components.some((component) => canonicalVolcanismSeverity(component).toLowerCase() === severity.toLowerCase());
    }
    return components.some((component) => canonicalVolcanismSeverity(component).toLowerCase() === severity.toLowerCase() && canonicalVolcanismType(component).includes(type));
}

function formatValueRange(low, high) {
    if (low == null || high == null) {
        return "—";
    }
    if (low === high) {
        return `${Number(low).toLocaleString()} CR`;
    }
    return `${Number(low).toLocaleString()} - ${Number(high).toLocaleString()} CR`;
}

function updatePayoutDisplay() {
    if (!isSystemInitialized) {
        return;
    }
    const label = document.getElementById("estimate_label");
    const firstFootfall = document.getElementById("first_footfall_toggle").checked;
    const multiplier = firstFootfall ? 5 : 1;

    for (let index = 1; index <= signalCountTarget; index += 1) {
        const valueLabel = document.getElementById(`slot_value_${index}`);
        const select = document.getElementById(`slot_genus_${index}`);
        if (valueLabel && select) {
            const genus = select.value;
            const range = genus ? genusValueCache[genus] : null;
            valueLabel.textContent = range ? formatValueRange(...range) : "—";
        }
    }

    optimizeAndValue();
}

function optimizeAndValue() {
    if (!isSystemInitialized) {
        return;
    }
    const firstFootfall = document.getElementById("first_footfall_toggle").checked;
    const multiplier = firstFootfall ? 5 : 1;
    const label = document.getElementById("estimate_label");
    const logBox = document.getElementById("output_box");

    let overallMinTotal = 0;
    let overallMaxTotal = 0;
    const itemsToRoute = [];

    for (let index = 1; index <= signalCountTarget; index += 1) {
        const select = document.getElementById(`slot_genus_${index}`);
        if (!select || !select.value) {
            continue;
        }
        const genus = select.value;
        const range = genusValueCache[genus] || globalValueRange || [0, 0];
        const choices = genusLookup[genus] || [];
        const best = choices.slice().sort((a, b) => (b.base_value || 0) - (a.base_value || 0))[0];
        overallMinTotal += range[0] || 0;
        overallMaxTotal += range[1] || 0;
        if (best) {
            itemsToRoute.push({
                ...best,
                value_range: range,
                species_options: choices.map((entry) => entry.species).slice(0, 8),
                species_details: getSpeciesDetails(choices),
                description: best.description || ""
            });
        }
    }

    if (overallMinTotal === overallMaxTotal) {
        label.textContent = `Est. Value: ${(overallMinTotal * multiplier).toLocaleString()} CR`;
    } else {
        label.textContent = `Total Est. Range: ${(overallMinTotal * multiplier).toLocaleString()} - ${(overallMaxTotal * multiplier).toLocaleString()} CR`;
    }
    label.style.color = "#2ecc71";

    generateOptimizedPath(itemsToRoute, signalCountTarget - itemsToRoute.length);
}

function getSpeciesDetails(choices) {
    return (choices || []).map((item) => [item.species, item.description || "(no description available)"]).filter((entry) => entry[0]);
}

function generateOptimizedPath(items, unresolvedSlots) {
    const adviceBox = document.getElementById("pathing_advice");
    const zones = [[], [], []];
    items.forEach((item) => zones[getTerrainZone(item.dss_visual_zone)].push(item));

    let output = "🚀 SURFACE EXPLORATION CHAINING PROTOCOL\n\n";
    output += "--- SPECIES IDENTIFIERS ---\n";

    if (!items.length) {
        output += "No genera selected yet. The current estimate reflects the full range of compatible species under the active filters.\n";
    } else {
        items.forEach((item) => {
            const speciesOptions = item.species_options || [];
            output += `• ${item.genus} — ${formatValueRange(...(item.value_range || [0, 0]))}\n`;
            if (speciesOptions.length) {
                output += `    ↳ Eligible species: ${speciesOptions.join(", ")}\n`;
            }
            const speciesDetails = item.species_details || [];
            if (speciesDetails.length > 1) {
                output += `    ↳ Multiple species remain eligible under this genus (${speciesDetails.length} candidates).\n`;
            }
            speciesDetails.forEach(([speciesName, description]) => {
                if (speciesName || description) {
                    output += `    ↳ ${speciesName}: ${description}\n`;
                }
            });
        });
    }

    output += "\n";
    for (let index = 0; index < 2; index += 1) {
        if (zones[index].length && zones[index + 1].length) {
            output += `>>> OPTIMAL LANDING ZONE: [${index === 0 ? "PLAINS/FOOTHILLS" : "FOOTHILLS/MOUNTAINS"}]\n`;
            output += "    Strategy: Target the boundary line between adjacent terrain clusters to minimize re-entry travel.\n\n";
        }
    }

    output += "--- EXECUTION PATH (Descending) ---\n";
    const activeZones = [2, 1, 0].filter((zoneIndex) => zones[zoneIndex].length);
    activeZones.forEach((zoneIndex, stepIndex) => {
        const zoneLabel = ["PLAINS", "FOOTHILLS", "MOUNTAINS"][zoneIndex];
        const terrainSet = [...new Set(zones[zoneIndex].map((entry) => entry.terrain || "Plains"))];
        output += `${stepIndex + 1}. [Zone: ${zoneLabel}]\n`;
        terrainSet.forEach((terrain) => {
            const matches = zones[zoneIndex].filter((entry) => (entry.terrain || "Plains") === terrain).map((entry) => entry.genus);
            output += `   - ${terrain.toUpperCase()}: ${matches.join(", ")}\n`;
            output += `     Pilot Cue: ${getTerrainAdvice(terrain)}\n\n`;
        });
        output += `   -> Transit: ${zoneIndex > 0 ? "Descending slope to the next cluster." : "Mission complete."}\n\n`;
    });

    if (unresolvedSlots > 0) {
        output += `Unresolved slots: ${unresolvedSlots}\n`;
        output += `Potential payout for unresolved slots: ${formatValueRange(globalValueRange?.[0] || 0, globalValueRange?.[1] || 0)}\n`;
    }

    adviceBox.textContent = output;
}

function getTerrainZone(dssZone) {
    const mapping = {
        "Lowland Plains / Flatlands": 0,
        "Geothermal / Active Fields": 1,
        "Rugged Terrain / Foothills": 1,
        "Ice Sheets / Highland Caps": 1,
        "Highlands / Mountain Ridges": 2,
        "Deep Chasms / Canyons": 2,
        "Fractured / Tectonic Zones": 2,
        "Impact Basins / Craters": 2
    };
    return mapping[dssZone] ?? 1;
}

function getTerrainAdvice(terrain) {
    const adviceMap = {
        Mountains: "Check high-altitude rock formations and the shadowed pockets of cliff faces.",
        Craters: "Survey the central uplift spike and the transition between the floor and the rim.",
        Canyons: "Follow the canyon floor and the interfaces between sediment and vertical walls.",
        Plains: "Use low-hover sweeps and scan for subtle texture shifts across wide open ground.",
        Hills: "Focus on the sheltered middle slopes rather than the exposed ridgeline.",
        "Rocky Fields": "Move slowly across the boulder field with the SRV and scan between the larger rocks.",
        "Geothermal Vents": "Inspect the cooler perimeter of vent sites where dense colonies often cluster.",
        Glaciers: "Look for fissures and cracked surfaces that offer a firm foothold for growth.",
        Badlands: "Prioritize eroded basins between ridgelines where moisture collects.",
        Deserts: "Check the leeward side of dunes and ridges where color shifts stand out.",
        Valleys: "Drop into the low ground between hills or mountains where colonies cluster densely."
    };
    return adviceMap[terrain] || "Perform a high-intensity surface sweep; no specialized terrain markers were identified.";
}

function resetForm() {
    document.getElementById("first_footfall_toggle").checked = false;
    document.getElementById("dropdown_container").innerHTML = "";
    document.getElementById("output_box").textContent = "System reset. Standing by for survey data...";
    document.getElementById("pathing_advice").textContent = "Awaiting survey data…";
    document.getElementById("estimate_label").textContent = "Awaiting telemetry input…";
    document.getElementById("estimate_label").style.color = "#2ecc71";
    document.getElementById("calc_p2_btn").disabled = true;
    isSystemInitialized = false;
    filteredValidSpecies = [];
    genusLookup = {};
    genusValueCache = {};
    globalValueRange = null;
}

initPlanner();
