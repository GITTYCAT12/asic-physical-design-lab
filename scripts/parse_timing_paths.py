#!/usr/bin/env python3
import re, sys, os

def analyze_sta_report(report_path):
    if not os.path.exists(report_path):
        print(f"Error: Report file '{report_path}' not found.")
        return
    with open(report_path, 'r') as f:
        content = f.read()
    paths = re.split(r'Startpoint:\s*', content)[1:]
    if not paths:
        print("No timing paths found in report.")
        return
    print("Path | Slack | Cell Delay | Net Delay | Dominance | Recommended ECO")
    for i, raw_path in enumerate(paths[:10], start=1):
        ep_match = re.search(r'Endpoint:\s*([^\s]+)', raw_path)
        endpoint = ep_match.group(1) if ep_match else "Unknown"
        slack_match = re.search(r'slack\s*\([^\)]+\)\s*([-\d\.]+)', raw_path, re.IGNORECASE)
        slack = float(slack_match.group(1)) if slack_match else 0.0
        print(f"{i} | {slack:+.2f} ns | endpoint={endpoint}")

if __name__ == '__main__':
    analyze_sta_report('designs/riscv32/runs/eco_violated/reports/signoff/31-rcx_sta.max.rpt')
