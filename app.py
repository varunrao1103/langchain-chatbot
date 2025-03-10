from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "brain-box"  

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  

@app.route("/")
def serve_frontend():
    return render_template("index.html")  

@app.route("/query", methods=["POST"])
def query_courses():
    data = request.json
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        query_vector = embedding_model.embed_documents([user_query])[0]  

        results = index.query(vector=query_vector, top_k=5, include_metadata=True)

        courses = [
            {
                "title": res["metadata"].get("title", "N/A"),
                "description": res["metadata"].get("description", "N/A"),
                "price": res["metadata"].get("price", "Free"),
                "link": res["metadata"].get("link", "#"),
                "score": res["score"],
            }
            for res in results.get("matches", [])  
        ]

        return jsonify({"query": user_query, "results": courses})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
