#!/usr/bin/env python3
"""Benchmark live ERDDAP HFR endpoints with short subsets; standard library only."""
from __future__ import annotations
import argparse, csv, io, json, re, time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = "https://erddap.hfrnode.eu/erddap/griddap"
SITES = {
    "IZOL": "EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3",
    "PIRA": "EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3",
}
DIMS = "[(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]"

def fetch(url, timeout):
    req = Request(url, headers={"User-Agent": "RheoMarine-HFR-audit/1.0"})
    t0 = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as response:
            body = response.read()
            return body, round(time.perf_counter() - t0, 3), response.status
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"{type(exc).__name__}: {exc}; elapsed={time.perf_counter()-t0:.2f}s") from exc

def das(site, dataset, timeout):
    url = f"{BASE}/{dataset}.das"
    body, elapsed, status = fetch(url, timeout)
    raw = body.decode("utf-8", "replace")
    fields = {}
    for key in ("time_coverage_start", "time_coverage_end", "date_created",
                "date_modified", "last_calibration_date", "testOutOfDate",
                "update_interval", "institution"):
        m = re.search(r'(?:String|Float64)\s+' + re.escape(key) + r'\s+"?([^";\n]+)"?;', raw)
        if m:
            fields[key] = m.group(1).strip()
    return {"site": site, "url": url, "http_status": status,
            "elapsed_seconds": elapsed, "bytes": len(body), "metadata": fields}

def subset(site, dataset, days, timeout):
    # data feed lags real time by ~1-2 h; requesting 'now' as the end
    # makes ERDDAP return 404, so clamp the window end backwards
    end = (datetime.now(timezone.utc) - timedelta(hours=3)
           ).replace(microsecond=0)
    start = end - timedelta(days=days)
    s = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    e = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    dims = f"[({s}):1:({e})]" + DIMS
    query = ",".join(name + dims for name in ("EWCT", "NSCT", "QCflag"))
    # this ERDDAP rejects unencoded brackets/parens -> encode everything
    url = f"{BASE}/{dataset}.csv0?{quote(query, safe='')}"
    body, elapsed, status = fetch(url, timeout)
    # csv0 has NO header row; columns are time,depth,lat,lon then the
    # requested vars in order (EWCT, NSCT, QCflag)
    rdr = csv.reader(io.StringIO(body.decode("utf-8-sig", "replace")))
    rows = [r for r in rdr if r]
    if not rows:
        raise RuntimeError("HTTP response contained no CSV data rows")
    times = [r[0] for r in rows if len(r) > 0 and r[0]]
    def col(i):
        return [r[i] for r in rows if len(r) > i]
    ewct, nsct, qcf = col(4), col(5), col(6)
    def valid(vals):
        return sum(v not in ("", "NaN", "nan", "-32.767", "-127")
                   for v in vals)
    flags = {}
    for v in qcf:
        flags[v] = flags.get(v, 0) + 1
    return {"site": site, "window_days": days, "requested_start_utc": s,
            "requested_end_utc": e, "http_status": status,
            "elapsed_seconds": elapsed, "bytes": len(body), "data_rows": len(rows),
            "first_returned_time": min(times) if times else None,
            "last_returned_time": max(times) if times else None,
            "EWCT_valid": valid(ewct), "NSCT_valid": valid(nsct),
            "QCflag_counts": flags, "request_url": url}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", nargs="+", type=int, default=[1, 7])
    p.add_argument("--timeout", type=int, default=120)
    a = p.parse_args()
    if any(d < 1 or d > 31 for d in a.days):
        p.error("days must be between 1 and 31")
    report = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
              "note": "Short subsets only; no multi-year archive requested.",
              "metadata": [], "tests": [], "errors": []}
    for site, dataset in SITES.items():
        try:
            report["metadata"].append(das(site, dataset, a.timeout))
        except Exception as exc:
            report["errors"].append({"site": site, "stage": "metadata", "error": str(exc)})
        for days in a.days:
            try:
                report["tests"].append(subset(site, dataset, days, a.timeout))
            except Exception as exc:
                report["errors"].append({"site": site, "stage": f"{days}d_subset", "error": str(exc)})
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["errors"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
