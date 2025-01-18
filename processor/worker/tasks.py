from processor.worker.celery_config import celery_app
from typing import Any, Dict, List, Tuple
from processor.service import IMAGE_RESOLUTION_SCALE, DoclingDocumentConversion, DocumentConverterService

@celery_app.task(name="celery.ping")
def ping():
    print("Ping task received!")  # or use a logger
    return "pong"

@celery_app.task(bind=True, name="convert_document")
def convert_document_task(
    self,
    document: Tuple[str, bytes],
    extract_tables: bool = False,
    image_resolution_scale: int = IMAGE_RESOLUTION_SCALE,
) -> Dict[str, Any]:
    
    document_service = DocumentConverterService(document_converter=DoclingDocumentConversion())
    result = document_service.convert_document_task(
        document, extract_tables=extract_tables, image_resolution_scale=image_resolution_scale
    )
    return result.model_dump(exclude_unset=True)


@celery_app.task(bind=True, name="convert_document")
def convert_documents_task(
    self,
    document: List[Tuple[str, bytes]],
    extract_tables: bool = False,
    image_resolution_scale: int = IMAGE_RESOLUTION_SCALE,
) -> List[Dict[str, Any]]:
    
    document_service = DocumentConverterService(document_converter=DoclingDocumentConversion())
    results = document_service.convert_documents_task(
        document, extract_tables=extract_tables, image_resolution_scale=image_resolution_scale
    )
    return [result.model_dump(exclude_unset=True) for result in results]

