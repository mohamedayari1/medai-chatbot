import logging
import os
import shutil
import string
import zipfile
from collections import Counter
from urllib.parse import urljoin

from app.parser.file.bulk import SimpleDirectoryReader
from app.parser.chunking import Chunker



import logging
import os
import shutil
import string
import zipfile
from collections import Counter
from urllib.parse import urljoin

import requests
from bson.objectid import ObjectId

from app.core.mongodb import MongoDB
from app.core.settings import settings
from app.parser.file.bulk import SimpleDirectoryReader
from app.parser.embedding_pipeline import embed_and_store_documents
# from app.parser.remote.remote_creator import RemoteCreator
from app.parser.schema.base import Document
from app.parser.chunking import Chunker
from app.utils.token_management import count_tokens_docs

mongo = MongoDB.get_client()
db = mongo["docsgpt"]
sources_collection = db["sources"]

# Constants
MIN_TOKENS = 150
MAX_TOKENS = 1250
RECURSION_DEPTH = 2

# Define a function to extract metadata from a given filename.
def metadata_from_filename(title):
    return {"title": title}

# Define a function to generate a random string of a given length.
def generate_random_string(length):
    return "".join([string.ascii_letters[i % 52] for i in range(length)])

current_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

def extract_zip_recursive(zip_path, extract_to, current_depth=0, max_depth=5):
    """
    Recursively extract zip files with a limit on recursion depth.

    Args:
        zip_path (str): Path to the zip file to be extracted.
        extract_to (str): Destination path for extracted files.
        current_depth (int): Current depth of recursion.
        max_depth (int): Maximum allowed depth of recursion to prevent infinite loops.
    """
    if current_depth > max_depth:
        logging.warning(f"Reached maximum recursion depth of {max_depth}")
        return

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)  # Remove the zip file after extracting
    except Exception as e:
        logging.error(f"Error extracting zip file {zip_path}: {e}")
        return

    # Check for nested zip files and extract them
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file.endswith(".zip"):
                # If a nested zip file is found, extract it recursively
                file_path = os.path.join(root, file)
                extract_zip_recursive(file_path, root, current_depth + 1, max_depth)

def download_file(url, params, dest_path):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        raise

def upload_index(full_path, file_data):
    try:
        if settings.VECTOR_STORE == "faiss":
            files = {
                "file_faiss": open(full_path + "/index.faiss", "rb"),
                "file_pkl": open(full_path + "/index.pkl", "rb"),
            }
            response = requests.post(
                urljoin(settings.API_URL, "/api/upload_index"), files=files, data=file_data
            )
        else:
            response = requests.post(
                urljoin(settings.API_URL, "/api/upload_index"), data=file_data
            )
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error uploading index: {e}")
        raise
    finally:
        if settings.VECTOR_STORE == "faiss":
            for file in files.values():
                file.close()

def metadata_from_filename(title):
    return {"title": title}

def ingest_worker(directory, formats, name_job, filename, user, retriever="classic"):
    input_files = None
    recursive = True
    limit = None
    exclude = True
    sample = False
    full_path = os.path.join(directory, user, name_job)


    logging.info(f"Ingest file: {full_path}", extra={"user": user, "job": name_job})
    file_data = {"name": name_job, "file": filename, "user": user}


    raw_docs = SimpleDirectoryReader(
        input_dir=full_path,
        input_files=input_files,
        recursive=recursive,
        required_exts=formats,
        num_files_limit=limit,
        exclude_hidden=exclude,
        file_metadata=metadata_from_filename,
    ).load_data()

    chunker = Chunker(
        chunking_strategy="classic_chunk",
        max_tokens=MAX_TOKENS,
        min_tokens=MIN_TOKENS,
        duplicate_headers=False
    )
    raw_docs = chunker.chunk(documents=raw_docs)

    docs = [Document.to_langchain_format(raw_doc) for raw_doc in raw_docs]
    id = ObjectId()

    embed_and_store_documents(docs, full_path, id)
    tokens = count_tokens_docs(docs)

    if sample:
        for i in range(min(5, len(raw_docs))):
            logging.info(f"Sample document {i}: {raw_docs[i]}")

    file_data.update({
        "tokens": tokens,
        "retriever": retriever,
        "id": str(id),
        "type": "local",
    })
    upload_index(full_path, file_data)

    shutil.rmtree(full_path)

    return {
        "directory": directory,
        "formats": formats,
        "name_job": name_job,
        "filename": filename,
        "user": user,
        "limited": False,
    }
    
    
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import os
import shutil
from werkzeug.utils import secure_filename
from typing import Optional

router = APIRouter()

class UploadResponse(BaseModel):
    success: bool
    task_id: Optional[str] = None
    error: Optional[str] = None

@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(
    user: str = Form(...),
    name: str = Form(...),
    file: List[UploadFile] = File(...)
):
    # Validate input
    if not user or not name or not file or all(not f.filename for f in file):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Missing required fields or files"
            }
        )

    try:
        user = secure_filename(user)
        job_name = secure_filename(name)
        save_dir = os.path.join(current_dir, settings.UPLOAD_FOLDER, user, job_name)
        os.makedirs(save_dir, exist_ok=True)

        if len(file) > 1:
            # Handle multiple files
            temp_dir = os.path.join(save_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)

            for upload_file in file:
                filename = secure_filename(upload_file.filename)
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, "wb") as f:
                    content = await upload_file.read()
                    f.write(content)
                print(f"Saved file: {filename}")

            zip_path = shutil.make_archive(
                base_name=os.path.join(save_dir, job_name),
                format="zip",
                root_dir=temp_dir,
            )
            final_filename = os.path.basename(zip_path)
            shutil.rmtree(temp_dir)
        else:
            # Handle single file
            upload_file = file[0]
            final_filename = secure_filename(upload_file.filename)
            file_path = os.path.join(save_dir, final_filename)
            with open(file_path, "wb") as f:
                content = await upload_file.read()
                f.write(content)

        # # Start ingestion task
        # task = ingest.delay(
        #     settings.UPLOAD_FOLDER,
        #     [
        #         ".rst", ".md", ".pdf", ".txt", ".docx", ".csv",
        #         ".epub", ".html", ".mdx", ".json", ".xlsx",
        #         ".pptx", ".png", ".jpg", ".jpeg",
        #     ],
        #     job_name,
        #     final_filename,
        #     user,
        # )

        ingest_worker(settings.UPLOAD_FOLDER, [".pdf"], job_name, final_filename, user)



        task_id = "123"
        return JSONResponse(
            status_code=200,
            content={"success": True, "task_id": task_id}
        )

    except Exception as err:
        print(f"Error: {err}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": str(err)}
        )