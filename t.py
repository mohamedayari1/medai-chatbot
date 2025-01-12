import sys
import os

# Add the project directory to the Python path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docling-pdf-processor'))
sys.path.append(project_path)

# Now try importing
from docling_pdf_processor.route import route 