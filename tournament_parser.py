"""
WSOP Tournament Schedule Parser

Processes raw Excel sheets containing event schedules, cleans formatting artifacts,
and produces enriched tournament entries with:

- Valid dates from input rows
- Standardized column names and missing value patches
- Dealer forecast logic based on player projections and handedness
- Restart flagging for multi-day events

Designed for use in Streamlit dashboards and schedule visualizations.
"""

import pandas as pd
import re

def parse_format(event_name):
    name = str(event_name).lower()
    if any(term in name for term in ["omaha", "razz", "stud", "mixed", "horse", "badugi", "triple draw"]):
        return "Mixed"
    return "Holdem"

def parse_handedness(event_name, format_type):
    name = str(event_name)
    match = re.search(r"(\d+)-Handed", name)
    if match:
        return int(match.group(1))
    return 9 if format_type == "Holdem" else 8

def forecast_dealers(players, handed):
    try:
        base = players / handed
        full = round(base * 1.20)
        fallback = round(base * 1.15)
        return full if full else fallback
    except:
        return None

def is_restart(row):
    return (
        "restart" in str(row.get("Buy-in Amount", "")).lower()
        or "restart" in str(row.get("Event Name", "")).lower()
        or "-D" in str(row.get("Event Number", "")).upper()
    )

def clean_raw_schedule(raw_df):
    df = raw_df.copy()

    # 🔄 Column Aliases
    column_aliases = {
        "Projection": "Player Projection",
        "Buy-in": "Buy-in Amount",
        "Buy-In": "Buy-in Amount",
        "Event #": "Event Number"
    }
    df.rename(columns=column_aliases, inplace=True)

    # 🔧 Ensure required columns
    required_cols = ["Date", "Time", "Event Number", "Event Name", "Buy-in Amount", "Player Projection"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # 🗓️ Parse dates directly
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").apply(
        lambda d: d.replace(year=2026).date() if pd.notnull(d) else None
    )

    # 🕒 Parse start time with fallback
    df["Raw_Time"] = df["Time"].astype(str)
    df["StartHour"] = pd.to_datetime(df["Raw_Time"], format="%I:%M %p", errors="coerce").dt.hour
    df["StartHour"] = df["StartHour"].fillna(9)

    # 🔢 Normalize projections
    df["Player Projection"] = pd.to_numeric(df["Player Projection"], errors="coerce").fillna(0).astype(int)

    # 🔮 Enrich features
    df["Format"] = df["Event Name"].apply(parse_format)
    df["Handed"] = df.apply(lambda r: parse_handedness(r["Event Name"], r["Format"]), axis=1)
    df["Dealer Forecast"] = df.apply(lambda r: forecast_dealers(r["Player Projection"], r["Handed"]), axis=1)
    df["Restart_Flag"] = df.apply(is_restart, axis=1)

    # ✅ Filter complete tournament rows
    df = df[df["Event Number"].notnull() & df["Event Name"].notnull()].copy()

    return df.reset_index(drop=True)