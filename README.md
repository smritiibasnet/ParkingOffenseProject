# Parking Tickets Interactive Dashboard

The project is separated into two notebooks:
1. Data cleaning notebook: shows all cleaning, merging, null handling, column renaming, and saving the clean CSV.
2. Machine learning notebook: loads the cleaned CSV, trains predictive models, and evaluates performance.

## Features
- Big-picture summary metrics
- Tickets by district
- Tickets by month
- Top streets by ticket count
- Top offense types
- Interactive filters for district, street, state, and offense description
- Ticket location map
- Detailed ticket table

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py