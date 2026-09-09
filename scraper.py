"""
Scrapes today's LHC cause list and merges it into combined_data.xlsx (repo root),
matching the schema/columns your lhc.py dashboard already expects.
Used by .github/workflows/daily_scrape.yml — no manual run needed once deployed.
"""
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import random
import os
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MASTER_FILE = "combined_data.xlsx"

LEGEND_MAP = {
    "#ff0000": "Old Cause List",
    "#ffff00": "Regular Cause List",
    "#90ee90": "Stay Matters",
    "#ffb6c1": "Part-heard Cases",
    "#ffdab9": "Judgement Reserved Cases",
}


def parse_bench_header(bench_text):
    bench_lines = [l.strip() for l in bench_text.split("\n") if l.strip()]
    hearing_date = bench_lines[0]
    hearing_day = datetime.datetime.strptime(hearing_date, "%d-%m-%Y").strftime("%A")
    bench_type_line = bench_lines[1]

    if "Regular Cause List" in bench_type_line:
        bench_type = bench_type_line.split("Regular Cause List")[0].strip()
        court_location = bench_type_line.split("Regular Cause List")[-1].strip(" []")
    else:
        bench_type = bench_type_line
        court_location = ""

    justice_lines = [l for l in bench_lines if "Justice" in l]
    justice = " | ".join(justice_lines) if justice_lines else ""
    court = next((l for l in bench_lines if "Court" in l or "Block" in l), "")

    return hearing_date, hearing_day, bench_type, justice, court, court_location


def fetch_cause_list(date_str=None):
    today = date_str or datetime.date.today().strftime("%Y-%m-%d")

    url = "https://data.lhc.gov.pk/dynamic/cause_list_regular_result.php"
    params = {
        "weekDay": today,
        "courtName": "All Courts",
        "color": "All",
        "location": "All",
        "bench": "",
        "caseNumber": "",
        "lawyerCode": "",
        "lawyerName": "",
        "partyName": "",
        "lawyer_cnic": "",
        "lawyer_mobile": "",
        "t": str(random.randint(1000000000000, 9999999999999)),
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://data.lhc.gov.pk/case_management/regular_cause_list",
        "X-Requested-With": "XMLHttpRequest",
    }

    session = requests.Session()
    retry = Retry(total=4, backoff_factor=5, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))

    resp = session.get(url, params=params, headers=headers, timeout=60)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    bench_tables = soup.find_all("table", attrs={"align": "center"})
    for bench_table in bench_tables:
        bench_text = bench_table.get_text("\n", strip=True)
        hearing_date, hearing_day, bench_type, justice, court, court_location = parse_bench_header(bench_text)

        next_sibling = bench_table.find_next_sibling()
        while next_sibling and not (next_sibling.name == "table" and next_sibling.get("align") == "center"):
            if next_sibling.name == "table":
                for tr in next_sibling.find_all("tr"):
                    cols = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                    if len(cols) == 6:
                        seq, category, case_no, title, lawyer, remarks = cols
                        legend = LEGEND_MAP.get(tr.get("bgcolor"), "Unknown")
                        rows.append([
                            hearing_date, hearing_day, bench_type, justice, court, court_location,
                            legend, seq, category, case_no, title, lawyer, remarks
                        ])
            next_sibling = next_sibling.find_next_sibling()

    columns = [
        "Hearing Date", "Hearing Day", "Bench Type", "Justice", "Court", "Court Location",
        "Legends", "Seq#", "Category", "Case#", "Title", "Lawyer", "Remarks"
    ]
    return pd.DataFrame(rows, columns=columns), today


def merge_into_master(daily_df, source_file_name):
    daily_df = daily_df.copy()
    daily_df['Original_Row_No'] = range(1, len(daily_df) + 1)
    daily_df['Source_File'] = source_file_name
    daily_df['File_Order'] = int(datetime.datetime.now().timestamp())

    if os.path.exists(MASTER_FILE):
        master_df = pd.read_excel(MASTER_FILE)
        master_df = master_df.drop(columns=['Sr_No'], errors='ignore')
        combined_df = pd.concat([master_df, daily_df], ignore_index=True)
    else:
        combined_df = daily_df

    data_columns = [c for c in combined_df.columns if c not in ['Sr_No', 'Original_Row_No', 'Source_File', 'File_Order']]
    combined_df = combined_df.drop_duplicates(subset=data_columns, keep='first')

    if 'Court Location' in combined_df.columns:
        combined_df['Court Location'] = combined_df['Court Location'].replace('', 'Lahore').fillna('Lahore')

    combined_df.insert(0, 'Sr_No', range(1, len(combined_df) + 1))
    return combined_df


if __name__ == "__main__":
    try:
        df, date_used = fetch_cause_list()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Could not reach LHC site (network/blocked): {e}")
        print("Leaving combined_data.xlsx untouched. Will retry on next scheduled run.")
        sys.exit(0)  # exit 0 so the workflow shows as passed, not failed, on a blocked/down source

    if df.empty:
        print(f"⚠️ No rows scraped for {date_used}. Site may be down/unchanged. Leaving {MASTER_FILE} untouched.")
    else:
        combined = merge_into_master(df, f"LHC_{date_used}.xlsx")
        combined.to_excel(MASTER_FILE, index=False)
        print(f"✅ {MASTER_FILE} updated — {len(df)} new rows scraped, {len(combined)} total rows.")
