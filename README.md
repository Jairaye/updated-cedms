# Updated CEDMS

A Streamlit-based Dealer Management System for tournament scheduling, employee management, and more. Built for modularity, scalability, and ease of use.

### 🧠 Dealer Forecast Parser

This module parses the WSOP tournament schedule and generates dealer forecasts based on:

- Forward-filling floating date header rows
- Cleaning column aliases (`Buy-in`, `Projection`, `Event #`)
- Identifying table format (Hold'em vs. Mixed)
- Estimating dealer needs using player projections and handedness
- Flagging restart rounds based on name, number, or buy-in notes

Cleaned data is used across dashboard components to power summary views and forecasting analysis.