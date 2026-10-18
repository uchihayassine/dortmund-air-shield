// Export the Air Shield model (inputs, assumptions, results) as CSV files.
// Runs the planner's own optimizer code from the built page, so the numbers match the app exactly.
// eval() only ever runs our own locally built file (app/air-shield-planner-en.html), never external input.
//   node tools/export_csv.js            -> writes data/export/*.csv
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "data", "export");
fs.mkdirSync(OUT, { recursive: true });

const html = fs.readFileSync(path.join(ROOT, "app", "air-shield-planner-en.html"), "utf8");
const js = html.split("<script>")[1].split("</script>")[0];
const core = js.slice(0, js.indexOf("// ---------- state ----------"));

// Same presets as in the planner (keep in sync with PRESETS in app/planner.template.html)
const DEFAULTS = { scenario: "EU", system: "auto", budget: 9, target: 4, missions: 8000, beta: 0.5, minGain: 0.4, peak: 3, block: 0.1, minSep: 1, allowAtc: true };
const PRESETS = [
  ["★ Recommended: 4 min · €9M", {}],
  ["Pilot 2027: €2.5M", { budget: 2.5 }],
  ["Phase 1: €4M", { budget: 4 }],
  ["Lean city-wide: €6M", { budget: 6 }],
  ["Faster: 3-minute response", { target: 3, budget: 12 }],
  ["Relaxed: 5-minute response", { target: 5 }],
  ["Major incident year: 20,000 missions", { missions: 20000, budget: 12 }],
  ["No sites near the airport", { allowAtc: false }],
  ["Benchmark: mixed suppliers", { scenario: "MX" }],
];

function csv(name, header, rows) {
  const esc = v => {
    if (v === null || v === undefined) return "";
    const s = typeof v === "number" ? String(Math.round(v * 10000) / 10000) : String(v);
    return /[",;\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const text = [header.join(","), ...rows.map(r => r.map(esc).join(","))].join("\n") + "\n";
  fs.writeFileSync(path.join(OUT, name), "﻿" + text, "utf8");   // BOM so Excel reads UTF-8
  console.log(`${name}: ${rows.length} rows`);
}

eval(core + `
const pOf = o => ({ scenario: o.scenario, budget: o.budget, target: o.target, missions: o.missions, beta: o.beta, minGain: o.minGain, peak: o.peak, block: o.block, allowAtc: o.allowAtc, minSep: o.minSep });
const solve = o => o.system === "auto" ? bestFor(o.scenario, pOf(o), new Set()) : optimize(SYSTEMS.find(s => s.id === o.system), pOf(o), new Set());

// ---------- base (recommended) run ----------
const B = { ...DEFAULTS };
const res = solve(B), ev = res.ev, sys = res.sys;
const worst = robustness(res, pOf(B));
const siteInfo = new Map(ev.perSite.map(x => [x.j, x]));

// 1. demand cells
csv("cells.csv",
  ["cell_id", "lat", "lon", "district_nr", "district", "city_district", "population", "weight", "hotspot", "stations_in_reach", "best_response_min", "covered", "redundant"],
  cells.map((c, i) => { const d = DATA.districts[c.d]; return [i, c.lat, c.lon, d.nr, d.name, d.sb, c.pop, c.w, c.hot || "", ev.cnt[i],
    ev.cnt[i] ? ev.best[i] : "", ev.cnt[i] ? 1 : 0, ev.cnt[i] > 1 ? 1 : 0]; }));

// 2. districts with coverage
const dAgg = DATA.districts.map(d => ({ d, cells: 0, pop: 0, cov: 0, dbl: 0, tw: 0 }));
cells.forEach((c, i) => { const a = dAgg[c.d]; a.cells++; a.pop += c.pop; if (ev.cnt[i]) { a.cov += c.pop; a.tw += ev.best[i] * c.pop; } if (ev.cnt[i] > 1) a.dbl += c.pop; });
csv("districts.csv",
  ["district_nr", "district", "city_district", "population_2023", "hexagons", "covered_pct", "redundant_pct", "avg_response_min"],
  dAgg.map(a => [a.d.nr, a.d.name, a.d.sb, a.d.pop, a.cells, a.pop ? 100 * a.cov / a.pop : 0, a.pop ? 100 * a.dbl / a.pop : 0, a.cov ? a.tw / a.cov : ""]));

// 3. candidate sites + selection
csv("candidate_sites.csv",
  ["site_id", "name", "type", "ward", "lat", "lon", "km_to_airport", "airport_area", "selected", "docks", "missions_per_year", "peak_erlang_load", "hexagons_in_reach"],
  cands.map(k => { const s = siteInfo.get(k.j); return [k.j, k.name, k.kind, k.ward || "", k.lat, k.lon, k.apKm, k.atc ? 1 : 0,
    s ? 1 : 0, s ? s.docks : 0, s ? s.missions : 0, s ? s.a : "", res.plan.lists[k.j].length]; }));

// 4. hospitals and hotspots
csv("hospitals.csv", ["name", "lat", "lon"], DATA.hospitals.map(h => [h.name, h.lat, h.lon]));
csv("hotspots.csv", ["name", "lat", "lon", "extra_weight", "status"], DATA.hotspots.map(h => [h.name, h.lat, h.lon, h.w, "estimate"]));

// 5. drone systems and special drones
csv("drone_systems.csv",
  ["id", "name", "maker", "origin", "group", "type", "hover_capable", "speed_m_s", "range_km", "launch_s", "endurance_min", "recharge_min", "thermal", "ip_rating", "dock_price_eur", "opex_per_dock_eur_year", "bvlos_note", "status"],
  SYSTEMS.map(s => [s.id, s.name, s.maker, s.origin, s.grp, s.kind, s.hover ? 1 : 0, s.speed, s.radius, s.launch, s.endurance, s.recharge, s.thermal ? 1 : 0, s.ip, s.dock, s.opex, s.bvlos, "estimate"]));
csv("special_drones.csv", ["scenario", "name", "role", "origin", "count", "unit_price_eur", "status"],
  Object.entries(SPECIAL).flatMap(([sc, list]) => list.map(x => [sc === "EU" ? "EU only" : "Mixed", x.name, x.role, x.origin, x.n, x.price, "estimate"])));

// 6. missions and cost split
csv("missions.csv", ["mission", "users", "sensors", "priority", "platform", "share_of_missions", "status"],
  MISSIONS.map(m => [m[0], m[1], m[2], "P" + m[3], m[4], m[5], "assumption"]));
csv("cost_split.csv", ["organisation", "share", "missions_per_year", "cost_eur_per_year", "status"],
  SPLIT.map(([n, sh]) => [n, sh, B.missions * sh, (ev.capex / C.YEARS + ev.opex) * sh, "assumption"]));

// 7. assumptions / parameters
const A = [
  ["scenario_input", "suppliers", "EU / EEA / CH only", "", "brief requirement"],
  ["scenario_input", "capital_budget", B.budget * 1e6, "EUR", "choice"],
  ["scenario_input", "target_response_time", B.target, "min", "choice"],
  ["scenario_input", "missions_per_year", B.missions, "missions", "estimate"],
  ["scenario_input", "backup_weight_beta", B.beta, "", "choice"],
  ["scenario_input", "minimum_gain_per_station", B.minGain, "% of total weight", "choice"],
  ["scenario_input", "peak_factor", B.peak, "x average hour", "estimate"],
  ["scenario_input", "max_overflow_at_peak", B.block, "share of alerts", "choice"],
  ["scenario_input", "minimum_station_spacing", B.minSep, "km", "choice"],
  ["scenario_input", "airport_sites_allowed", B.allowAtc ? "yes" : "no", "", "choice"],
  ["model_constant", "detour_factor", C.ROUTE, "x straight line", "estimate"],
  ["model_constant", "time_on_scene", C.ONSCENE, "min", "estimate"],
  ["model_constant", "site_preparation", C.SITE, "EUR per site", "estimate"],
  ["model_constant", "airport_coordination", C.ATC, "EUR per airport-area site", "estimate"],
  ["model_constant", "airport_near_zone_radius", C.ATC_KM, "km", "estimate (schematic)"],
  ["model_constant", "airport_ctr_radius_display", C.CTR_KM, "km", "estimate (schematic)"],
  ["model_constant", "control_centre_integration", C.LEITSTAND_CAPEX, "EUR one-off", "estimate"],
  ["model_constant", "software_utm_data", C.SOFTWARE, "EUR per year", "estimate"],
  ["model_constant", "remote_pilot_cost", C.FTE, "EUR per FTE per year", "estimate"],
  ["model_constant", "fte_per_24_7_seat", C.SEAT_FTE, "FTE", "estimate"],
  ["model_constant", "flights_per_pilot", C.DRONES_PER_PILOT, "simultaneous flights", "estimate"],
  ["model_constant", "minimum_seats", 2, "seats", "choice"],
  ["model_constant", "insurance", C.INSUR, "EUR per dock per year", "estimate"],
  ["model_constant", "special_drone_upkeep", 0.12, "share of value per year", "estimate"],
  ["model_constant", "depreciation_period", C.YEARS, "years", "choice"],
  ["model_constant", "hexagon_area", 0.36, "km2", "choice"],
  ["model_constant", "hexagon_circumradius", DATA.meta.hex_r_km, "km", "derived"],
  ["model_constant", "auto_choice_tolerance", 0.5, "% coverage", "choice"],
  ["model_constant", "fee_model_availability_share", 0.6, "share", "assumption"],
  ["model_constant", "fee_model_per_mission_share", 0.4, "share", "assumption"],
];
csv("assumptions.csv", ["category", "parameter", "value", "unit", "status"], A);

// 8. data sources
csv("data_sources.csv", ["item", "source", "dataset_or_url", "status"], [
  ["District boundaries (62)", "Stadt Dortmund open data", "fb62-statistischebezirke", "sourced"],
  ["Population 2023 per district", "Stadt Dortmund open data", "ds-bevolkerung-nach-geschlecht-und-migrationshintergrund-2023", "sourced"],
  ["Fire brigade sites", "Stadt Dortmund open data", "feuerwehr", "sourced"],
  ["Police sites", "Stadt Dortmund open data", "polizei", "sourced"],
  ["Hospitals", "Stadt Dortmund open data", "krankenhaus", "sourced"],
  ["Street map", "OpenStreetMap contributors", "tile.openstreetmap.org zoom 13", "sourced"],
  ["Geozones", "dipul.de", "not imported; airport zone schematic", "to verify"],
  ["Drone specs and prices", "team estimate", "", "estimate"],
  ["Mission volume, cost rates, cost split", "team estimate", "", "estimate"],
]);

// 9. recommended scenario: cost breakdown and KPIs
const sp = SPECIAL.EU, spCap = sp.reduce((a, x) => a + x.n * x.price, 0);
csv("recommended_costs.csv", ["type", "item", "quantity", "unit_cost_eur", "total_eur"], [
  ["investment", "Docks incl. drone (" + sys.name + ")", ev.docks, sys.dock, ev.docks * sys.dock],
  ["investment", "Site preparation", res.plan.sel.length, C.SITE, res.plan.sel.length * C.SITE],
  ["investment", "Airport coordination", ev.atcSites, C.ATC, ev.atcSites * C.ATC],
  ["investment", "Special drones", "", "", spCap],
  ["investment", "Control-centre integration", 1, C.LEITSTAND_CAPEX, C.LEITSTAND_CAPEX],
  ["investment", "TOTAL investment", "", "", ev.capex],
  ["operations_per_year", "Dock maintenance, licences, spares", ev.docks, sys.opex, ev.docks * sys.opex],
  ["operations_per_year", "Insurance", ev.docks, C.INSUR, ev.docks * C.INSUR],
  ["operations_per_year", "Remote pilots (" + ev.seats + " seats x " + C.SEAT_FTE + " FTE)", ev.seats * C.SEAT_FTE, C.FTE, ev.staff],
  ["operations_per_year", "Software / UTM / data", 1, C.SOFTWARE, C.SOFTWARE],
  ["operations_per_year", "Special drones upkeep (12%)", "", "", spCap * 0.12],
  ["operations_per_year", "TOTAL operations per year", "", "", ev.opex],
  ["summary", "5-year TCO", "", "", ev.tco],
  ["summary", "Annual cost (investment/5 + operations)", "", "", ev.capex / C.YEARS + ev.opex],
  ["summary", "Cost per mission", B.missions, "", ev.costPerMission],
]);

// 10. scenarios (inputs + outputs)
const scenRows = PRESETS.map(([name, o]) => {
  const p = { ...DEFAULTS, ...o }; const r = solve(p); const w = robustness(r, pOf(p));
  return [name, p.scenario === "EU" ? "EU only" : "Mixed", p.budget * 1e6, p.target, p.missions, p.beta, p.minGain, p.peak, p.block, p.minSep, p.allowAtc ? "yes" : "no",
    r.sys.name, r.plan.r, r.plan.sel.length, r.ev.docks, 100 * r.ev.covPop / POP, 100 * r.ev.dblPop / POP, r.ev.avgT, r.ev.capex, r.ev.opex, r.ev.tco,
    r.ev.capex / C.YEARS + r.ev.opex, r.ev.costPerMission, r.ev.seats, 100 * w.loss / POP, cands[w.j].name];
});
csv("scenarios.csv", ["scenario", "suppliers", "budget_eur", "target_min", "missions_per_year", "beta", "min_gain_pct", "peak_factor", "max_overflow", "min_spacing_km", "airport_sites",
  "system", "reach_km", "sites", "docks", "coverage_pct", "redundant_pct", "avg_response_min", "investment_eur", "operations_eur_year", "tco_5y_eur", "annual_cost_eur",
  "cost_per_mission_eur", "control_seats", "worst_failure_loss_pct", "worst_failure_site"], scenRows);

// 11. cost of sovereignty
const eu = bestFor("EU", pOf(B), new Set()), mx = bestFor("MX", pOf({ ...B, scenario: "MX" }), new Set());
csv("cost_of_sovereignty.csv", ["variant", "system", "sites", "docks", "coverage_pct", "investment_eur", "tco_5y_eur"], [
  ["EU only", eu.sys.name, eu.plan.sel.length, eu.ev.docks, 100 * eu.ev.covPop / POP, eu.ev.capex, eu.ev.tco],
  ["Mixed", mx.sys.name, mx.plan.sel.length, mx.ev.docks, 100 * mx.ev.covPop / POP, mx.ev.capex, mx.ev.tco],
  ["Difference (EU - mixed)", "", "", "", 100 * (eu.ev.covPop - mx.ev.covPop) / POP, eu.ev.capex - mx.ev.capex, eu.ev.tco - mx.ev.tco],
  ["Per resident per year", "", "", "", "", "", (eu.ev.tco - mx.ev.tco) / POP / C.YEARS],
]);

// 10b. stations chosen in every scenario
const scenSt = [];
for (const [name, o] of PRESETS) {
  const p = { ...DEFAULTS, ...o }; const r = solve(p); const ps = new Map(r.ev.perSite.map(x => [x.j, x]));
  for (const j of r.plan.sel) { const k = cands[j], s = ps.get(j); scenSt.push([name, r.sys.name, j, k.name, k.kind, k.lat, k.lon, s ? s.docks : 0, s ? s.missions : 0]); }
}
csv("scenario_stations.csv", ["scenario", "system", "site_id", "name", "type", "lat", "lon", "docks", "missions_per_year"], scenSt);

// 10c. reach matrix: every hexagon-site pair within the recommended reach (distance and response time)
const reach = [];
for (let j = 0; j < NK; j++) for (const i of res.plan.lists[j]) {
  const d = DIST[i * NK + j];
  reach.push([i, j, cands[j].name, d, respMin(sys, d), res.plan.sel.includes(j) ? 1 : 0]);
}
csv("reach_matrix.csv", ["cell_id", "site_id", "site_name", "distance_km", "response_min", "site_selected"], reach);

// 10d. full distance matrix in long format (all 769 x 48 pairs)
const dm = [];
for (let i = 0; i < NC; i++) for (let j = 0; j < NK; j++) dm.push([i, j, DIST[i * NK + j]]);
csv("distance_matrix.csv", ["cell_id", "site_id", "distance_km"], dm);

// 10e. geometries as WKT (opens in QGIS / Excel / Power BI)
const ring = r => "(" + r.map(c => c[0] + " " + c[1]).join(", ") + ")";
csv("district_geometry.csv", ["district_nr", "district", "city_district", "wkt"],
  DATA.districts.map(d => [d.nr, d.name, d.sb, d.geom.length > 1 ? "MULTIPOLYGON(" + d.geom.map(p => "(" + p.map(ring).join(", ") + ")").join(", ") + ")" : "POLYGON(" + d.geom[0].map(ring).join(", ") + ")"]));
const HR = DATA.meta.hex_r_km, KXc = 111.32 * Math.cos(51.51 * Math.PI / 180), KYc = 110.57;
csv("hexagon_geometry.csv", ["cell_id", "wkt"], cells.map((c, i) => {
  const v = [30, 90, 150, 210, 270, 330, 30].map(a => [c.lon + HR * Math.cos(a * Math.PI / 180) / KXc, c.lat + HR * Math.sin(a * Math.PI / 180) / KYc]);
  return [i, "POLYGON((" + v.map(p => p[0].toFixed(6) + " " + p[1].toFixed(6)).join(", ") + "))"];
}));

// 12. sensitivity (one change at a time from recommended)
const tests = [["target_response_time", "target", [3, 5, 6]], ["capital_budget_MEUR", "budget", [4, 6, 12]], ["missions_per_year", "missions", [4000, 20000]],
  ["backup_weight_beta", "beta", [0, 1]], ["minimum_gain_pct", "minGain", [0.1, 1]], ["peak_factor", "peak", [1.5, 5]], ["max_overflow", "block", [0.05, 0.2]],
  ["minimum_spacing_km", "minSep", [0, 2]], ["airport_sites", "allowAtc", [false]]];
const sens = [];
for (const [label, key, vals] of tests) for (const v of vals) {
  const p = { ...B, [key]: v }; const r = solve(p);
  sens.push([label, v, r.sys.name, r.plan.sel.length, r.ev.docks, 100 * r.ev.covPop / POP, 100 * r.ev.dblPop / POP, r.ev.capex, r.ev.tco, r.ev.costPerMission]);
}
csv("sensitivity.csv", ["changed_parameter", "value", "system", "sites", "docks", "coverage_pct", "redundant_pct", "investment_eur", "tco_5y_eur", "cost_per_mission_eur"], sens);
`);
