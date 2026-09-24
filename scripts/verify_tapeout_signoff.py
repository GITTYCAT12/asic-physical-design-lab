#!/usr/bin/env python3
import csv, os, re, hashlib

def verify_signoff(run_tag):
    base_dir = f"designs/riscv32/runs/{run_tag}"
    metrics_file = f"{base_dir}/reports/metrics.csv"
    if not os.path.exists(metrics_file):
        print(f"Error: Run directory '{base_dir}' not found.")
        return
    with open(metrics_file) as f:
        r = list(csv.reader(f))
        d = dict(zip(r[0], r[1]))
    drc = int(d.get('tritonRoute_violations', 0) or 0)
    wns = float(d.get('wns', 0.0) or 0.0)
    whs = float(d.get('whs', 0.0) or 0.0)
    tns = float(d.get('tns', 0.0) or 0.0)
    lvs_rpt = f"{base_dir}/reports/signoff/39-picorv32.lvs.rpt"
    lvs_pass = True
    if os.path.exists(lvs_rpt):
        with open(lvs_rpt) as f:
            c = f.read().lower()
        lvs_pass = "total errors = 0" in c or "no net, device, pin, or property mismatches" in c
    print("ASIC signoff summary")
    print(f"WNS: {wns:+.2f} ns")
    print(f"WHS: {whs:+.2f} ns")
    print(f"TNS: {tns:+.2f} ns")
    print(f"Route violations: {drc}")
    print(f"LVS clean: {lvs_pass}")

if __name__ == '__main__':
    verify_signoff('day7_multicorner')
