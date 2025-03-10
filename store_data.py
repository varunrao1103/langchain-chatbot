import os
import csv
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "brain-box"

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
)

index = pc.Index(index_name)

course_data = []
with open("brainlox_courses.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        course_data.append(row)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

texts = [f"{course['Title']} - {course['Description']} - {course['Price']}" for course in course_data]
course_vectors = embedding_model.embed_documents(texts)

upsert_data = [
    (
        f"course-{i}",
        vector,
        {"title": course["Title"], "description": course["Description"], "price": course["Price"], "link": course["Link"]}
    )
    for i, (vector, course) in enumerate(zip(course_vectors, course_data))
]

index.upsert(vectors=upsert_data)

print(f"✅ {len(course_data)} courses successfully stored in Pinecone index: '{index_name}'!")
