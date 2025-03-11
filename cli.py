import argparse
import pandas as pd
from .fetcher import fetch_papers

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers based on a search query and save to CSV."
    )
    parser.add_argument(
        'query',
        type=str,
        help="Search query for PubMed"
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help="Output CSV file path"
    )

    args = parser.parse_args()

    # ✅ Fetch papers
    papers = fetch_papers(args.query)

    if papers:
        df = pd.DataFrame(papers)
        df.to_csv(args.file, index=False)
        print(f"✅ Papers saved to '{args.file}'")
    else:
        print("❌ No papers found.")



# ✅ Ensure that the function name matches pyproject.toml entry point
if __name__ == "__main__":
    main()
