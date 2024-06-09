from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from RepoToText import GitHubRepoScraper

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/scrape', methods=['POST'])
def scrape_repo():
    data = request.json
    repo_url = data['repoUrl']
    file_types = data['selectedFileTypes']
    scraper = GitHubRepoScraper(repo_url, file_types)
    try:
        result = scraper.run()
        return jsonify({"message": "Success", "data": result}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
