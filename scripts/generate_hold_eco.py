#!/usr/bin/env python3
import re, sys, os

def generate_hold_eco_script(hold_report_path, output_tcl_path):
    if not os.path.exists(hold_report_path):
        print(f"Report '{hold_report_path}' not found.")
        return
    with open(hold_report_path, 'r') as f:
        content = f.read()
    paths = re.split(r'Startpoint:\s*', content)[1:]
    eco_commands = []
    for i, raw_path in enumerate(paths, start=1):
        slack_match = re.search(r'slack\s*\([^\)]+\)\s*([-\d\.]+)', raw_path, re.IGNORECASE)
        if not slack_match:
            continue
        slack = float(slack_match.group(1))
        if slack < 0:
            ep_match = re.search(r'Endpoint:\s*([^\s]+)', raw_path)
            endpoint = ep_match.group(1) if ep_match else "Unknown"
            net_match = re.findall(r'([^\s]+)\s+\(net\)', raw_path)
            target_net = net_match[-1] if net_match else f"net_to_{endpoint}"
            buf_cell = "sky130_fd_sc_hd__dlygate4sd3_1"
            tcl_cmd = f"insert_buffer {target_net} {buf_cell} hold_eco_buf_{i}"
            eco_commands.append((target_net, slack, tcl_cmd))
    with open(output_tcl_path, 'w') as out_f:
        out_f.write("# ===================================================\n")
        out_f.write("# AUTOMATICALLY GENERATED HOLD TIMING ECO DECK\n")
        out_f.write("# Target Process: SkyWater 130nm\n")
        out_f.write("# ===================================================\n\n")
        if eco_commands:
            for _, _, cmd in eco_commands:
                out_f.write(f"{cmd}\n")
            out_f.write("\ndetailed_placement\nestimate_parasitics -placement\nreport_checks -path_delay min\n")
        else:
            out_f.write("# Zero hold violations detected! Design is Hold-Clean.\n")

if __name__ == '__main__':
    generate_hold_eco_script('designs/riscv32/runs/eco_fixed_45/reports/signoff/31-rcx_sta.min.rpt', 'designs/riscv32/fix_hold_eco.tcl')
