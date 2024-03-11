from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient,models
import openai as open_ai
from qdrant_client.http.models import PointStruct
import uuid




def read_data_from_pdf(pdf_path):
  text = ""
  with open(pdf_path, 'rb') as file:
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text


def get_text_chunks(text):
  text_splitter = CharacterTextSplitter(
    separator="\n",chunk_size=1000,chunk_overlap=200,length_function=len)
  chunks = text_splitter.split_text(text)
  return chunks


def get_embedding(text_chunks, model_id="text-embedding-ada-002"):
    points = []
    for idx, chunk in enumerate(text_chunks):
        response = open_ai.Embedding.create(
            input=chunk,
            model=model_id
        )
        embeddings = response['data'][0]['embedding']
        points.append(PointStruct(id=str(uuid.uuid4()), vector=embeddings,
                                   payload={"text": chunk}))

    return points


def create_qdrant_collection(collection_name):
    connection = QdrantClient("localhost", port=6333)    
    connection.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )
    info = connection.get_collection(collection_name=collection_name)
    
    return info


def add_points_qdrant(collection_name, points):
    
    connection = QdrantClient("localhost", port=6333)
    connection.upsert(collection_name=collection_name, points=points)
    
    return True