#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# read mem.log from devices
# output overview.csv and detail.csv


import os
import sys
import re


info = {
    "Pid": -1,
    "Process": "",
    "VmPeak": 0,
    "VmSize": 0,
    "VmHWM": 0,
    "VmRSS": 0,
    "Perm": "",
    "Path": "",
    "Size": 0,
    "Rss": 0,
    "Pss": 0,
    "total": {
        "text": 0, "data": 0, "rodata": 0, "heap": 0,
        "stack": 0, "other": 0, "VmPSS": 0
    }
}

tmp = info.copy()
tmp["total"] = (info["total"]).copy()


detail = ["Pid", "Process", "Perm", "Path", "Size", "Rss", "Pss"]
overview = ["Pid", "Process", "VmPeak", "VmSize", "VmHWM", "VmRSS"]
total = [key for key in info["total"]]


f_detail = open("detail.csv", "w")
cols = detail
line = f"{cols[0]}"
for n in range(1, len(cols)):
    line = f"{line},{cols[n]}"
line = f"{line}\n"
f_detail.write(line)


f_overview = open("overview.csv", "w")
cols = overview + total
line = f"{cols[0]}"
for n in range(1, len(cols)):
    line = f"{line},{cols[n]}"
line = f"{line}\n"
f_overview.write(line)


def output_detail(output, data):
    if (data["Perm"] == ""):
        return
    cols = detail
    line = f"{data[cols[0]]}"
    for n in range(1, len(cols)):
        value = str(data[cols[n]])
        if (value.startswith("-")):
            value = f"FH:{value}"
        line = f"{line},{value}"
    line = f"{line}\n"
    output.write(line)


def output_overview(output, data):
    if (data["Process"] == ""):
        return
    cols = overview
    line = f"{data[cols[0]]}"
    for n in range(1, len(cols)):
        value = str(data[cols[n]])
        if (value.startswith("-")):
            value = f"FH:{value}"
        line = f"{line},{value}"
    cols = total
    data = data["total"]
    for n in range(0, len(cols)):
        value = str(data[cols[n]])
        if (value.startswith("-")):
            value = f"FH:{value}"
        line = f"{line},{data[cols[n]]}"
    line = f"{line}\n"
    output.write(line)


with open("mem.log") as fin:
    for line in fin:
        line = line.rstrip("\n")
        if re.match(r'^[0-9a-fA-F]+[-][0-9a-fA-F]+', line):
            output_detail(f_detail, tmp)
            fields = line.split()
            if (len(fields) < 6):
                path = "anonymous"
            else:
                path = fields[5]
                for n in range(6, len(fields)):
                    path = f"{path}_{fields[n]}"
            tmp["Perm"] = fields[1]
            tmp["Path"] = path
        else:
            fields = line.split()
            key = (fields[0]).rstrip(":")
            value = fields[1]

            if (key not in info):
                continue

            if (key == "Process"):
                output_detail(f_detail, tmp)
                output_overview(f_overview, tmp)
                tmp = info.copy()
                tmp["total"] = (info["total"]).copy()
            else:
                value = int(value)

            tmp[key] = value

            if (key == "Rss"):
                if (tmp["Path"] == "[heap]"):
                    tmp["total"]["heap"] += value
                elif (tmp["Path"] == "[stack]"):
                    tmp["total"]["stack"] += value
                elif (tmp["Perm"] == "r-xp"):
                    tmp["total"]["text"] += value
                elif (tmp["Perm"] == "rw-p"):
                    tmp["total"]["data"] += value
                elif (tmp["Perm"] == "r--p"):
                    tmp["total"]["rodata"] += value
                else:
                    tmp["total"]["other"] += value
            elif (key == "Pss"):
                tmp["total"]["VmPSS"] += value

output_detail(f_detail, tmp)
output_overview(f_overview, tmp)
f_detail.close()
f_overview.close()
