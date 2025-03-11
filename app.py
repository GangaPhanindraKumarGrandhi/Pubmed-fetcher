from flask import Flask, request, jsonify, send_file
import json
import csv
import pandas as pd
import logging
from .fetcher import fetch_papers

app = Flask(__name__)

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Route to serve papers data
@app.route('/papers', methods=['GET'])
def get_papers():
    try:
        # Read papers from JSON file
        with open('papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)

        if not papers:
            logging.warning("⚠️ No papers found.")
            return jsonify({"message": "No papers found"}), 404

        # Write papers to CSV
        df = pd.DataFrame(papers)
        df.to_csv('exported_papers.csv', index=False)
        logging.info("✅ Papers exported to CSV successfully.")

        return jsonify({"message": "Papers exported to CSV successfully"}), 200
    
    except FileNotFoundError:
        logging.error("❌ papers.json file not found.")
        return jsonify({"error": "Papers file not found"}), 404

    except json.JSONDecodeError:
        logging.error("❌ Error decoding JSON file.")
        return jsonify({"error": "Invalid JSON format"}), 500

    except Exception as e:
        logging.error(f"❌ Error exporting papers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Route to search papers
@app.route('/search', methods=['GET'])
def search_papers():
    query = request.args.get('query')
    if not query:
        logging.warning("⚠️ Missing query parameter.")
        return jsonify({"error": "Missing query parameter"}), 400
    
    try:
        papers = fetch_papers(query)
        if papers:
            logging.info(f"✅ Found {len(papers)} papers for query '{query}'.")
            return jsonify(papers), 200
        else:
            logging.warning(f"⚠️ No papers found for query '{query}'.")
            return jsonify({"message": "No papers found"}), 404

    except Exception as e:
        logging.error(f"❌ Error fetching papers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Route to export papers in JSON or CSV
@app.route('/export/<format>', methods=['GET'])
def export_papers(format):
    if format not in ['json', 'csv']:
        logging.warning(f"⚠️ Invalid format '{format}'.")
        return jsonify({"error": "Invalid format. Use 'json' or 'csv'."}), 400
    
    try:
        if format == 'json':
            return send_file('papers.json', as_attachment=True)
        elif format == 'csv':
            return send_file('exported_papers.csv', as_attachment=True)

    except FileNotFoundError:
        logging.error(f"❌ {format} file not found.")
        return jsonify({"error": f"{format} file not found"}), 404

    except Exception as e:
        logging.error(f"❌ Error exporting papers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Route to get a single paper by ID
@app.route('/paper/<paper_id>', methods=['GET'])
def get_paper(paper_id):
    try:
        with open('papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        paper = next((p for p in papers if p['ID'] == paper_id), None)
        if paper:
            logging.info(f"✅ Paper with ID {paper_id} found.")
            return jsonify(paper), 200
        else:
            logging.warning(f"⚠️ Paper with ID {paper_id} not found.")
            return jsonify({"error": "Paper not found"}), 404

    except FileNotFoundError:
        logging.error("❌ papers.json file not found.")
        return jsonify({"error": "Papers file not found"}), 404

    except json.JSONDecodeError:
        logging.error("❌ Error decoding JSON file.")
        return jsonify({"error": "Invalid JSON format"}), 500

    except Exception as e:
        logging.error(f"❌ Error getting paper: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Route to test fetching papers (for debugging)
@app.route('/test_fetch', methods=['GET'])
def test_fetch():
    try:
        papers = fetch_papers("cancer")
        if papers:
            logging.info("✅ Test fetch successful.")
            return jsonify(papers), 200
        else:
            logging.warning("⚠️ No papers found.")
            return jsonify({"message": "No papers found"}), 404
    
    except Exception as e:
        logging.error(f"❌ Error fetching papers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Home route
@app.route('/')
def home():
    logging.info("✅ Home route accessed.")
    return "Welcome to PubMed Fetcher API!"


# ✅ Custom error handlers
@app.errorhandler(404)
def not_found(error):
    logging.warning("⚠️ Route not found.")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logging.error("❌ Internal server error.")
    return jsonify({"error": "Internal server error"}), 500


# ✅ List all registered routes
logging.info("✅ Listing all registered routes:")
for rule in app.url_map.iter_rules():
    logging.info(f"{rule} -> {rule.endpoint}")


# ✅ Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
