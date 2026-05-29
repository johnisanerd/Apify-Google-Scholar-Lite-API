"""
Google Scholar Lite API: A Quick Start Example
See more at: https://apify.com/johnvc/google-scholar-lite-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-scholar-lite-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Scholar Lite API on Apify from Python and
read its structured JSON output. It searches Google Scholar for academic papers and
returns clean bibliometric records (title, authors and journal line, year, citation
count, snippet, and links to the paper and its PDF). It exercises several input
parameters so you can see what is configurable, while keeping the run small so your
first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (one search term, maxResultsPerSearch=10 which is a single
# page) to keep this first run inexpensive. Billing is per paper returned, so raise
# maxResultsPerSearch (and add more searchTerms) once you know your budget.
run_input = {
    "searchTerms": ["transformer attention mechanism"],
    "yearFrom": 2020,
    "yearTo": 2026,
    "language": "en",
    "maxResultsPerSearch": 10,
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-scholar-lite-api").call(run_input=run_input)

# Read structured results from the run's default dataset.
# apify-client 3.x returns a typed Run object, so use the attribute (not run["..."]).
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} paper(s).\n")

# Show a few key fields from each paper.
for item in items:
    title = item.get("title", "(no title)")
    year = item.get("year", "n/a")
    cited_by = item.get("citedBy", 0)
    link = item.get("link", "")
    pdf = item.get("pdfUrl", "")
    print(f"[{item.get('position', '?')}] {title}")
    print(f"    {item.get('publicationInfo', '')}")
    print(f"    year={year}  cited_by={cited_by}")
    print(f"    link: {link}")
    if pdf:
        print(f"    pdf:  {pdf}")
    print()
