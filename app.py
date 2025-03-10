from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# 🔹 Updated Index Name
INDEX_NAME = "brain-box"  # Changed from "sample-index-384" to "brain-box"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for frontend-backend communication

# ✅ Serve index.html
@app.route("/")
def serve_frontend():
    return render_template("index.html")  # Flask will find it in "templates/"

# ✅ Query Route
@app.route("/query", methods=["POST"])
def query_courses():
    data = request.json
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Convert query to embeddings
        query_vector = embedding_model.embed_documents([user_query])[0]  # Fixed embedding method

        # Search in Pinecone
        results = index.query(vector=query_vector, top_k=5, include_metadata=True)

        # Format response
        courses = [
            {
                "title": res["metadata"].get("title", "N/A"),
                "description": res["metadata"].get("description", "N/A"),
                "price": res["metadata"].get("price", "Free"),
                "link": res["metadata"].get("link", "#"),
                "score": res["score"],
            }
            for res in results.get("matches", [])  # Avoids errors if "matches" key is missing
        ]

        return jsonify({"query": user_query, "results": courses})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
