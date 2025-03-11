import os
from Bio import Entrez
import pandas as pd
import csv
import json
import logging

# ✅ Set your email for NCBI
Entrez.email = "phanigrandhi91@gmail.com"   # Replace with your actual email

# ✅ Configure logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Fetch papers from PubMed using Entrez API
def fetch_papers(query, max_results=10):
    logging.info(f"Fetching papers for query: {query}")
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        ids = record["IdList"]
        logging.info(f"✅ Found {len(ids)} paper IDs.")

        if not ids:
            return []

        papers = []
        handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="medline", retmode="text")
        data = handle.read()
        handle.close()

        # ✅ Basic Parsing (Example format, you can adjust)
        for id in ids:
            papers.append({
                'ID': id,
                'Title': f"Sample Title for {id}",
                'Authors': 'Sample Author',
                'Journal': 'Sample Journal',
                'Publication Date': '2025-03-01'
            })

        logging.info(f"✅ Fetched {len(papers)} papers.")
        return papers
    
    except Exception as e:
        logging.error(f"❌ Error fetching papers: {str(e)}")
        return []


# ✅ Save papers to CSV
def save_papers(papers, filename="papers.csv"):
    if papers:
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"✅ Saved to {filename}")
    else:
        print("❌ No papers to save.")


# ✅ Export to JSON
def export_papers():
    input_file = 'papers.csv'
    output_file = 'papers.json'

    if not os.path.exists(input_file):
        print(f"❌ {input_file} not found. Run the search command first.")
        return

    try:
        with open(input_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            papers = [row for row in reader]

        with open(output_file, mode='w', encoding='utf-8') as jsonfile:
            json.dump(papers, jsonfile, indent=4)

        print(f"✅ Exported to {output_file}")

    except Exception as e:
        print(f"❌ Error exporting papers: {e}")


# ✅ No CLI handling (since Flask will handle it)
