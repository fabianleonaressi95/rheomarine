# Observational data contract — common schema for independent observations

**Purpose:** every external dataset destined for comparison with
RheoMarine-SLO model output must be expressible in this schema *before*
any metric is computed. The contract preserves provenance and forbids
silent repair of data.

## 1. Canonical record

One row per observation (CSV) or per grid point/trajectory fix
(NetCDF). Required fields:

| Field | Type | Unit / format | Required | Notes |
|---|---|---|---|---|
| `obs_id` | string | unique within dataset | yes | e.g. `NIB-01-bin03-t20261120T0600Z` |
| `dataset_id` | string | stable identifier | yes | links to provenance block |
| `instrument_id` | string | platform/sensor identifier | yes | mooring, buoy, drifter ID, radar site |
| `obs_type` | enum | see §3 | yes | determines which optional fields apply |
| `time_utc` | ISO-8601 | UTC, e.g. `2026-11-20T06:00:00Z` | yes | **observation time**; keep `time_original` + `tz_original` when source is not UTC |
| `time_original` | string | verbatim source timestamp | recommended | never discard the original representation |
| `tz_original` | string | e.g. `UTC+1`, `CET` | when `time_utc` was converted | document conversion |
| `longitude` | float | decimal degrees, EPSG:4326 | yes for geo-located obs | negative = W; verify datum before use |
| `latitude` | float | decimal degrees, EPSG:4326 | yes for geo-located obs | |
| `depth_m` | float | metres, positive **down** from sea surface | for profile obs | `depth_reference` required |
| `depth_reference` | enum | `below_surface` / `below_sea_level` / `above_bottom` / `pressure_dbar` | when `depth_m` present | conversion documented, never assumed |
| `u_east` | float | m s⁻¹, positive eastward | for velocity obs | NaN if not measured — **not** 0 |
| `v_north` | float | m s⁻¹, positive northward | for velocity obs | |
| `speed` | float | m s⁻¹ | optional | if supplied, keep; do not recompute silently |
| `direction` | float | degrees, convention stated | optional | `direction_convention` required if present |
| `direction_convention` | enum | `nautical_from_north_cw` / `oceanographic_from_east_ccw` / `math_rad` / `other` | when `direction` present | |
| `qc_flag` | int/string | source QC value **verbatim** | yes | map to meaning via source documentation; never renumber silently |
| `qc_meaning` | string | decoded meaning | recommended | e.g. `good_data` |
| `uncertainty` | float or string | stated units | when available | e.g. `±0.05 m/s` or `not_reported` |
| `avg_interval_s` | float | seconds the value averages over | recommended | distinguishes instantaneous vs averaged |
| `sample_interval_s` | float | nominal sampling cadence | recommended | |
| `missing_reason` | enum | `not_sampled` / `instrument_gap` / `qc_rejected` / `out_of_coverage` / `fill_value` / `unknown` | for missing records | distinguishes *no observation* from *bad observation* |
| `source_dataset` | string | e.g. `NIB-ADCP-PIRAN-2026`, URL or DOI | yes | provenance anchor |
| `source_file` | string | local/remote file name | when applicable | |
| `retrieved_utc` | ISO-8601 | when this copy was obtained | yes | audit trail |
| `licence` | string | usage terms | yes | e.g. `CC-BY-4.0`, `institutional agreement` |
| `raw_value` | string/float | verbatim source value if transcoded | when transcoded | e.g. direction+speed → u/v keeps both |

## 2. Hard rules

1. **Missing ≠ zero.** Absent observations are `NaN` with a
   `missing_reason`; fill values are flagged, never used as measurements.
2. **QC is preserved verbatim.** `qc_flag` stores the source code;
   `qc_meaning` is a documented decode. Downstream filtering happens in
   the comparison protocol, not by editing the file.
3. **No silent interpolation.** Gridding/collocation is a *comparison*
   step and must be reported as such.
4. **Units are explicit.** Velocity in m s⁻¹; depth positive down;
   direction convention declared; timestamps UTC with original retained.
5. **Depth compatibility is mandatory** for any current comparison —
   HFR measures the upper ~1–2 m; a 22 m ADCP bin is not the same
   observable.
6. **A drifter fix is a Lagrangian position**, not an Eulerian velocity
   at a point — it enters the schema with `obs_type=drifter_position`
   (or derived `drifter_velocity` only after a documented differentiation
   step, per protocol B).

## 3. `obs_type` vocabulary

| `obs_type` | Description | Required extras |
|---|---|---|
| `eulerian_point` | fixed-station single-depth velocity (current meter, ADCP bin, HF-radar pixel treated as point) | `depth_m` recommended |
| `current_profile` | vertical profile at one time (ADCP, AWAC) | `depth_m` per record |
| `drifter_position` | Lagrangian GPS fix | `obs_id` must carry drifter ID; positions only |
| `drifter_velocity` | derived Lagrangian velocity | must record differentiation method in `sample_interval_s`/notes field |
| `hfr_vector` | HF-radar analysed surface-current vector | grid cell coords are lon/lat of cell centre |
| `hfr_radial` | HF-radar radial component | bearing/site metadata in `instrument_id`/notes |
| `env_forcing` | wind, wave, sea-level, pressure | `depth_m` not applicable; variable name in `obs_id` or dedicated column set |
| `particle_sample` | microplastic count/concentration | `filtered_area_m2`/`filtered_volume_m3`, mesh size, count fields — **schema extension required before use; see §5** |

## 4. CSV template

`docs/validation/templates/observations_template.csv` ships with the
header row only — **no fabricated observations**. One file per dataset;
`dataset_id` constant within a file.

## 5. Particle-sample extension (for NIB-04 / Gajšt-type data)

When sample-level microplastic records arrive, add these columns rather
than overloading velocity fields:

`mesh_um`, `filtered_area_m2` or `filtered_volume_m3`,
`count_total`, `count_by_size_class` (JSON or repeated rows),
`tow_start_utc`, `tow_end_utc`, `vessel`, `blank_corrected` (bool),
`concentration_particles_per_m2` / `_per_m3` (computed, flagged as
derived).

Until the extension is implemented in the checker, particle files are
**ingestible but not comparable** — they feed the Tier-B/C benchmark
path only.

## 6. NetCDF inputs

No new NetCDF reader is implemented: the existing
`rheomarine_hfr.adapter.load_erddap_netcdf` already ingests ERDDAP
`griddap` subsets (vars `time/latitude/longitude/EWCT/NSCT/QCflag`)
with provenance and QC masking — **reuse it** for any HFR-family
NetCDF. For non-ERDDAP observational NetCDF (e.g. CMEMS INSITU), map
variables onto this schema at ingest time and record the mapping in
`source_dataset`; do not parse ad-hoc inside comparison scripts.

## 7. Validation check

`scripts/check_observation_file.py` validates a CSV against this
contract: required columns, enum vocabularies, ISO-8601 timestamps,
unit sanity (|u|,|v| plausibility bounds reported not enforced), QC
flag presence, and a coverage report (time range, spatial bbox,
missing fraction per `missing_reason`, obs_type counts). It **reports**;
it never repairs.
