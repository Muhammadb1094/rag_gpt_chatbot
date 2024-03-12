# Retrieval Augmented Generation (RAG) Implementation With GPT Using Python Django


## Overview

This project involves the creation of an API server that harnesses Retrieval Augmented Generation (RAG) with GPT to answer user queries within a chatbot application. The ultimate objective is to develop a robust API capable of utilizing a knowledge base to provide well-informed responses.


## Getting Started With Code

### To run the code on your local host, follow these steps:

#### 1. Clone repository to your local machine:
    >>> git clone git@github.com:Muhammadb1094/rag_gpt_chatbot.git

#### 2. Set up a virtual environment and install the required dependencies, using:
    
    >>> pip install -r requirements.txt

#### 3. Setup Enviroment Variables and Databse to run Django Project:
    1. Create .env file in rga_chatapp directory.
    2. Create Your PosgreSQL Database, and use your own databse credentials.
    3. Add your OPENAI_API_KEY.
    4. Run Command to Migrate with Database:
        >>>  python manage.py migrate


#### 4. Setup Qdrant to store the Vector's Data

    Install Qdrant:
    >>> docker pull qdrant/qdrant

    To start Qdrant DB Server, run command in your terminal:

    >>> docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

    Access Qdrant server web UI:

    >>> http://localhost:6333/dashboard



#### 5. Run Your Django Project in your local host:
    >>> python manage.py runserver

#### 6. Access Your Django Project:
    🎉🙌🏻 http://127.0.0.1:8000/ 🎉🙌🏻


## Code Base Documentation

    There are 3 modules (apps) available in the code:
    1. User
        This module (app) contains all the user authentication api's. We are using Django RestFramework token to authenticate user.
    2. doc_processing 
        This module (app) contains api's or functions which process the pdf documents into Qdrant vector database.
    3. chat
        This module (app) contains conversation and message management api's. It also process or calls the Qdran and llm calls to search and ask query using both of them in parallel.
    
## PostMan Collection
    1. Postman collection is being attached with the code in directory postman_collection/
    2. It contains both the enviroment variables json and also the collection json

