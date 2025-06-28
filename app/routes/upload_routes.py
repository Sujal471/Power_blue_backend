'''from flask import Blueprint, request, jsonify
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.services.doc_clean import clean_chunk, get_document_splits_with_ids
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import Config
from langchain_pinecone import PineconeVectorStore
from app.services.User_login import verify_user
upload_bp = Blueprint("upload_bp", __name__)

@upload_bp.route("/", methods=["POST"])
def upload_pdf():
    data=request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if not verify_user(username, password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp:
            temp.write(file.read())
            temp.flush()

            loader = PyPDFLoader(temp.name)
            document = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs_splits = text_splitter.split_documents(document)
            cleaned_docs = [
                Document(page_content=clean_chunk(doc.page_content), metadata=doc.metadata)
                for doc in docs_splits
            ]

            ids = get_document_splits_with_ids(cleaned_docs)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            vectorstore = PineconeVectorStore.from_documents(
            documents=cleaned_docs,
            embedding=embeddings,
            index_name=Config.INDEX_NAME,
            ids=ids
            )

        return jsonify({"message": "Uploaded and stored chunks from PDF"})

    return jsonify({"error": "Invalid file type"}), 400'''

from flask import Blueprint, request, jsonify
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.services.doc_clean import clean_chunk, get_document_splits_with_ids
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import Config
from langchain_pinecone import PineconeVectorStore
from app.services.User_login import verify_user

upload_bp = Blueprint("upload_bp", __name__)

@upload_bp.route("/", methods=["POST"])
def upload_pdf():
    # Get credentials from form data instead of JSON
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if not verify_user(username, password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp:
                temp.write(file.read())
                temp.flush()

                loader = PyPDFLoader(temp.name)
                document = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                docs_splits = text_splitter.split_documents(document)
                cleaned_docs = [
                    Document(page_content=clean_chunk(doc.page_content), metadata=doc.metadata)
                    for doc in docs_splits
                ]

                ids = get_document_splits_with_ids(cleaned_docs)
                embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
                vectorstore = PineconeVectorStore.from_documents(
                    documents=cleaned_docs,
                    embedding=embeddings,
                    index_name=Config.INDEX_NAME,
                    ids=ids
                )

            return jsonify({"message": "Uploaded and stored chunks from PDF"}), 200
        
        except Exception as e:
            return jsonify({"error": f"Processing failed: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400  
