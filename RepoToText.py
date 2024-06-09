import os
import re
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from github import Github
from dotenv import load_dotenv
import logging
from retry import retry

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Get GitHub API key from environment variables
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

# Initialize GitHub instance
github_instance = Github(GITHUB_API_KEY)

class GitHubRepoScraper:
    def __init__(self, repo_name, selected_file_types=[]):
        self.repo_name = repo_name
        self.selected_file_types = selected_file_types

    @retry(tries=3, delay=2)
    def fetch_all_files(self):
        repo = github_instance.get_repo(self.repo_name)
        contents = repo.get_contents("")
        files_data = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if not self.selected_file_types or any(file_content.name.endswith(file_type) for file_type in self.selected_file_types):
                    file_data = self.process_file(file_content)
                    if file_data:
                        files_data.append(file_data)
        return files_data

    def process_file(self, file_content):
        logging.info(f"Processing file {file_content.path}")
        try:
            file_data = {
                "name": file_content.path,
                "content": file_content.decoded_content.decode("utf-8", errors="replace")
            }
            return file_data
        except Exception as e:
            logging.error(f"Error processing file {file_content.path}: {e}")
            return None

    def write_to_file(self, files_data):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.repo_name.replace('/', '_')}_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for file_data in files_data:
                f.write(f"--- {file_data['name']} ---\n")
                f.write(file_data["content"])
                f.write("\n\n")
        return filename

    def clean_up_text(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned_text = re.sub("\n{3,}", "\n\n", text)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

    def run(self):
        logging.info(f"Fetching all files from {self.repo_name}...")
        files_data = self.fetch_all_files()

        logging.info("Writing to file...")
        filename = self.write_to_file(files_data)

        logging.info("Cleaning up file...")
        self.clean_up_text(filename)

        logging.info("Done.")
        return filename

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    repo_url = data.get("repoUrl")
    selected_file_types = data.get("selectedFileTypes", [])

    if not repo_url:
        return jsonify({"error": "Repository URL is required"}), 400

    repo_name = repo_url.replace("https://github.com/", "")
    scraper = GitHubRepoScraper(repo_name, selected_file_types)

    try:
        filename = scraper.run()
        return jsonify({"message": "Success", "filename": filename})
    except Exception as e:
        logging.error(f"Error scraping repository: {e}")
        return jsonify({"error": "Failed to scrape repository"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
