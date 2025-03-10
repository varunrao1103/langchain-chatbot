import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connect to the new "brain-box" index
index_name = "brain-box"  # Updated index name
index = pc.Index(index_name)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define a sample query
query_text = "Python programming for beginners"
query_vector = embedding_model.embed_documents([query_text])[0]

# Query Pinecone
query_result = index.query(vector=query_vector, top_k=5, include_metadata=True)

# Print results
print("\n🔍 Query Results:")
for match in query_result['matches']:
    print(f"📚 Title: {match['metadata'].get('title', 'N/A')}")
    print(f"📖 Description: {match['metadata'].get('description', 'N/A')}")
    print(f"💰 Price: {match['metadata'].get('price', 'Free')}")
    print(f"🔗 Link: {match['metadata'].get('link', 'N/A')}")
    print(f"⭐ Score: {match['score']}")
    print("-" * 50)
