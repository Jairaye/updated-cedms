import streamlit as st
import pandas as pd
import re
from collections import Counter

def render_manual_employee_tab():
    st.title("👥 Manual Dealer Entry")
    st.markdown("Save one dealer at a time. Choose to keep entering, or preview the batch and metrics.")

    # ✅ Flag to trigger form reset after Save & Add Next
    clear = st.session_state.get("clear_form", False)

    # 🧮 Sidebar
    with st.sidebar:
        st.subheader("📊 Dealer Master List")
        master_df = st.session_state.get("dealer_master_list", pd.DataFrame())
        total_saved = len(master_df)
        st.markdown(f"**Total Saved:** `{total_saved}`")

        if total_saved > 0:
            last_entry = master_df.iloc[-1]
            st.markdown(f"**Last Saved:** `{last_entry['first_name']} {last_entry['last_name']}`")

        if st.button("🔄 Reset Master List"):
            st.session_state.dealer_master_list = pd.DataFrame()
            st.success("Master list cleared.")

        if st.button("📤 Export Master List"):
            st.session_state.export_master = True

    if st.session_state.get("export_master"):
        st.download_button("⬇️ Download CSV",
                           data=st.session_state.dealer_master_list.to_csv(index=False),
                           file_name="dealer_master_list.csv",
                           mime="text/csv")
        st.session_state.export_master = False

    # 🧾 Dealer Form
    with st.form(key="dealer_entry_form"):
        row1 = st.columns([1, 1, 1])
        first_name = row1[0].text_input("First Name", value="" if clear else st.session_state.get("first_name", ""), key="first_name")
        last_name  = row1[1].text_input("Last Name", value="" if clear else st.session_state.get("last_name", ""), key="last_name")
        nametag    = row1[2].text_input("Nametag", value="" if clear else st.session_state.get("nametag_id", ""), key="nametag_id")

        row2 = st.columns([1, 2.5, 1.5])
        ee_number = row2[0].text_input("Employee # - 9 digits", value="" if clear else st.session_state.get("ee_number", ""), key="ee_number")
        email     = row2[1].text_input("Email", value="" if clear else st.session_state.get("email", ""), key="email")
        phone     = row2[2].text_input("Phone", value="" if clear else st.session_state.get("phone", ""), key="phone")

        row3 = st.columns([1.5, 1.5])
        ft_pt = row3[0].selectbox("FT/PT", ["FULL TIME", "PART TIME"], index=0 if clear else None, key="ft_pt")
        dealer_group = row3[1].selectbox("Dealer Group", ["Any", "Holdem", "Live"], index=0 if clear else None, key="dealer_group")

        avail_row = st.columns(7)
        availability = {}
        for idx, day in enumerate(["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]):
            availability[f"AVAIL-{day}"] = avail_row[idx].checkbox(day, value=False if clear else st.session_state.get(f"AVAIL-{day}", False), key=f"AVAIL-{day}")

        col_submit = st.columns([1, 1])
        save_add_next = col_submit[0].form_submit_button("✅ Save Dealer and Add Next")
        save_preview  = col_submit[1].form_submit_button("🔍 Save Dealer and Preview Master List")

    # Reset flag post-render
    if st.session_state.get("clear_form"):
        st.session_state.clear_form = False

    # 🚦 Save Logic
    if save_add_next or save_preview:
        if not first_name or not last_name:
            st.warning("First and Last name required.")
        else:
            entry = {
                "first_name": first_name,
                "last_name": last_name,
                "nametag_id": nametag,
                "ee_number": ee_number,
                "email": email,
                "phone": phone,
                "ft_pt": ft_pt,
                "dealer_group": dealer_group,
                **availability,
                "User_Added": True
            }

            if "dealer_master_list" not in st.session_state:
                st.session_state.dealer_master_list = pd.DataFrame([entry])
            else:
                st.session_state.dealer_master_list = pd.concat(
                    [st.session_state.dealer_master_list, pd.DataFrame([entry])],
                    ignore_index=True
                )

            st.success(f"✅ Saved {first_name} {last_name} to master list.")

            if save_add_next:
                st.session_state.clear_form = True
                st.rerun()

    # 📊 Metrics if Preview Button Used
    if save_preview and "dealer_master_list" in st.session_state:
        df = st.session_state.dealer_master_list
        st.markdown("## 🧾 Dealer Master Preview")
        st.dataframe(df, use_container_width=True)

        st.markdown("## 📈 Metrics Summary")
        st.markdown(f"**Total Dealers:** {len(df)}")

        type_counts = dict(Counter(df["ft_pt"].dropna()))
        st.markdown("**FT/PT Breakdown:**")
        for t, count in type_counts.items():
            st.markdown(f"- {t}: {count}")

        group_counts = dict(Counter(df["dealer_group"].dropna()))
        st.markdown("**Dealer Group:**")
        for g, count in group_counts.items():
            st.markdown(f"- {g}: {count}")

        st.markdown("**Availability by Day:**")
        for day in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]:
            col = f"AVAIL-{day}"
            if col in df.columns:
                st.markdown(f"- {day}: {df[col].sum()} Available")