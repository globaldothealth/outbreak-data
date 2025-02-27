# /// script
# dependencies = [
#   "pandas>2",
#   "openai>1",
#   "tqdm",
# ]
# ///

# Script to take the '2_Timeline' sheet from the Influenza A Google sheets and
# extract structured information from the free text that contains details of
# positive cases in cattle

# An example free text input:
# USDA confirms 21 positive dairy farms in six states (Texas (9), Kansas (3),
# New Mexico (5), Idaho (1), Michigan (2), and Ohio (1))

# after extraction with extract_state_counts() will read as
# [('TX', 9), ('KS', 3), ('NM', 5), ('ID', 1), ('MI', 2), ('OH', 1)]

# This information is used with other fields to expand the sheet into a full linelist

import os
import sys
import json
import logging

import pandas as pd
from tqdm import tqdm
from openai import OpenAI

INPUT = "G.h Avian Influenza 2024-2025 - 2_Timeline.csv"
OUTPUT = "G.h_Avian_Influenza_2024-2025_Timeline_expanded.csv"

US_STATES = state_dict = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

if not os.environ.get("OPENAI_API_KEY"):
    print("""\033[1mThis script requires an OpenAI key\033[0m
You can obtain one from https://platform.openai.com/api-keys

Once you have the key, export it in the terminal or shell environment:
    export OPENAI_API_KEY=sk-...
""")
    sys.exit(1)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)


def extract_state_counts(text, model: str = "gpt-4o-mini"):
    # Define the prompt to ask OpenAI to extract state codes and case counts
    prompt = f"""
    Extract state codes and their respective case counts from the following text:
    
    TEXT
    
    Return the result as a JSON array with state_id and count keys. Do not return
    any other text other than JSON output.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt.replace("TEXT", text)},
                ],
            }
        ],
    )
    # remove code delimiters if present
    res = response.choices[0].message.content.replace("```json", "").replace("```", "")
    try:
        data = json.loads(res)
        return [(x["state_id"], int(x["count"])) for x in data]
    except json.decoder.JSONDecodeError:
        logging.error("Failed to decode %s", res)
        return None


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    columns = list(df.columns) + ["Location_Admin1", "Location_Admin1_ID", "Count"]
    out = []

    i = 0
    N = 100
    # Run on first N records for testing
    records = df.to_dict("records")[:N]
    for row in tqdm(records):
        i += 1
        if i == 100:
            break
        if state_counts := extract_state_counts(row["Event"]):
            for state, count in state_counts:
                rec = dict(row)
                rec.update(
                    {
                        "Location_Admin1_ID": state,
                        "Count": count,
                        "Location_Admin1": US_STATES.get(state, "ZZ"),
                    }
                )
                out.append(rec)
        else:
            out.append(row)
    df = pd.DataFrame(data=out, columns=columns)
    df["Location_Admin1"] = df["Location_Admin1"].fillna("")
    df["Location_Admin1_ID"] = df["Location_Admin1_ID"].fillna("")
    df["Count"] = df["Count"].fillna(0).astype(int)
    return df


print(f"{INPUT=}\n{OUTPUT=}")
process_data(pd.read_csv(INPUT)).to_csv(OUTPUT, index=False)
