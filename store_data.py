import os
import csv
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define new index name
index_name = "brain-box"

# Delete existing index (if it exists)
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

# Create a new Pinecone index
pc.create_index(
    name=index_name,
    dimension=384,  # Matching embedding model dimension
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
)

# Connect to the new index
index = pc.Index(index_name)

# Read scraped data from CSV
course_data = []
with open("brainlox_courses.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        course_data.append(row)

# Initialize Hugging Face embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Generate embeddings
texts = [f"{course['Title']} - {course['Description']} - {course['Price']}" for course in course_data]
course_vectors = embedding_model.embed_documents(texts)

# Prepare data for Pinecone (Upserting with metadata)
upsert_data = [
    (
        f"course-{i}",
        vector,
        {"title": course["Title"], "description": course["Description"], "price": course["Price"], "link": course["Link"]}
    )
    for i, (vector, course) in enumerate(zip(course_vectors, course_data))
]

# Upsert the data into the new "brain-box" index
index.upsert(vectors=upsert_data)

print(f"✅ {len(course_data)} courses successfully stored in Pinecone index: '{index_name}'!")
