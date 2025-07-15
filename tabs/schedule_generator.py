import streamlit as st
import pandas as pd
from datetime import date, timedelta

def generate_matrix_schedule(dealer_df, forecast_df, date_range):
    # ✅ Fix Excel float-format EE# issues by extracting digits only
    dealer_df["ee_number"] = (
        dealer_df["ee_number"]
        .astype(str)
        .str.extract(r"(\d+)")
        .fillna("0")
        .astype("int64")
    )

    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"], errors="coerce")
    forecast_df["Dealer Forecast"] = pd.to_numeric(
        forecast_df["Dealer Forecast"], errors="coerce"
    ).fillna(0).astype(int)

    forecast_df = forecast_df[
        (forecast_df["Date"].notnull()) &
        (forecast_df["Date"].dt.date >= date_range[0]) &
        (forecast_df["Date"].dt.date <= date_range[1])
    ]

    all_dates = sorted(forecast_df["Date"].dt.date.unique())
    schedule_map = {}
    debug_logs = []

    for date_obj in all_dates:
        date_str = str(date_obj)
        weekday_col = f"AVAIL-{pd.to_datetime(date_obj).strftime('%a').upper()}"

        if weekday_col not in dealer_df.columns:
            st.warning(f"Missing availability column: {weekday_col}")
            continue

        forecast_total = int(forecast_df[forecast_df["Date"].dt.date == date_obj]["Dealer Forecast"].sum())
        if forecast_total == 0:
            continue

        available_pool = dealer_df[dealer_df[weekday_col] == True].copy()
        available_pool = available_pool.sort_values("ee_number")
        assigned = available_pool.head(forecast_total)
        assigned_keys = set(assigned["ee_number"].tolist())

        for _, dealer in dealer_df.iterrows():
            key = dealer["ee_number"]
            if key not in schedule_map:
                schedule_map[key] = {
                    "Last Name": dealer.get("last_name", ""),
                    "First Name": dealer.get("first_name", ""),
                    "FT/PT": dealer.get("ft_pt", ""),
                    "EE#": key
                }
            schedule_map[key][date_str] = "ON" if key in assigned_keys else "OFF"

        debug_logs.append({
            "Date": date_str,
            "Forecasted": forecast_total,
            "Available": len(available_pool),
            "Assigned": len(assigned),
            "Sample EE#s": sorted(list(assigned_keys))[:10]
        })

    matrix_rows = []
    for key, profile in schedule_map.items():
        row = {
            "Last Name": profile["Last Name"],
            "First Name": profile["First Name"],
            "FT/PT": profile["FT/PT"],
            "EE#": profile["EE#"]
        }
        for date_obj in all_dates:
            row[str(date_obj)] = profile.get(str(date_obj), "OFF")
        matrix_rows.append(row)

    matrix_df = pd.DataFrame(matrix_rows).sort_values(["Last Name", "First Name"])
    matrix_df.reset_index(drop=True, inplace=True)

    debug_df = pd.DataFrame(debug_logs)

    st.success(f"✅ Schedule generated for {len(matrix_df)} dealers across {len(all_dates)} days.")
    st.markdown("### 📊 Assignment Log")
    st.dataframe(debug_df, use_container_width=True)

    st.markdown("### 📁 Download Full Dealer Schedule")
    csv_data = matrix_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Schedule as CSV",
        data=csv_data,
        file_name="dealer_schedule.csv",
        mime="text/csv"
    )

    return matrix_df

def render_schedulegen_tab():
    st.title("📆 Dealer Series Scheduler (Simplified & Exportable)")
    st.markdown("Assign dealers based on forecast totals and daily availability. Use the button below to download the full schedule.")

    dealer_df = st.session_state.get("dealer_master_list")
    forecast_df = st.session_state.get("parsed_df")

    if dealer_df is None or forecast_df is None:
        st.warning("Upload both Dealer Master List and Tournament Forecast.")
        return

    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"], errors="coerce")
    unique_dates = sorted(forecast_df["Date"].dropna().dt.date.unique())

    if not unique_dates:
        st.error("No valid tournament dates found.")
        return

    min_date = min(unique_dates)
    max_date = max(unique_dates)

    st.markdown("#### 📅 Select Tournament Range")
    selected_range = st.date_input(
        "Date Range",
        (min_date, min_date + timedelta(days=6)),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        if (selected_range[1] - selected_range[0]).days > 6:
            st.warning("⚠️ Max 7-day range.")
            return

        if st.button("🧪 Generate Schedule"):
            matrix_df = generate_matrix_schedule(dealer_df, forecast_df, selected_range)
            if not matrix_df.empty:
                st.markdown("### 📋 Schedule Matrix Preview")
                st.dataframe(matrix_df, use_container_width=True)
            else:
                st.info("🚫 No schedule generated. Check availability and forecast columns.")
    else:
        st.info("Please select both start and end dates.")