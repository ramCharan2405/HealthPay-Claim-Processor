# HealthPay AI Claim Processor

This project is a simplified, real-world agentic backend pipeline that processes medical insurance claim documents using AI tools and agent orchestration frameworks. It's built with FastAPI and uses a multi-agent workflow to classify, extract, and validate information from PDF documents.

## Architecture & Logic

The application is built around a modular and asynchronous FastAPI backend. The core logic is orchestrated in the `/process-claim` endpoint in `main.py`.

1.  **File Upload**: The endpoint accepts multiple PDF files via a `multipart/form-data` request.
2.  **Text Extraction**: For each uploaded PDF, the text is extracted using the `PyPDF2` library in `app/utils.py`.
3.  **Document Classification**: A `ClassifierAgent` (in `app/agents.py`) sends the extracted text to an LLM (Gemini) to determine the document's type (e.g., 'bill', 'discharge_summary').
4.  **Information Extraction**: An `ExtractionAgent` then processes the text of each classified document. It uses a dynamically selected Pydantic schema to instruct the LLM on what information to extract and in what format. This ensures the output is a structured JSON object.
5.  **Validation**: A `ValidationAgent` reviews all the extracted data. It checks for missing required documents and inconsistencies across the submitted files (e.g., mismatched patient names).
6.  **Claim Decision**: Based on the validation results, a final claim decision ('approved' or 'rejected') is made, and a detailed reason is provided.
7.  **Structured Response**: The final output is a structured JSON object, validated by the `ClaimResponse` Pydantic model, as specified in the assignment.

## How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY="your_google_api_key"
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

5.  **Test the endpoint:**
    You can use the built-in FastAPI documentation at `http://127.0.0.1:8000/docs` to upload files and test the `/process-claim` endpoint.

## AI Tool Usage & Prompt Examples

This project was built with the extensive use of an AI coding assistant (Gemini in Cursor) and the Gemini API for the agentic workflows.

### How AI Tools Were Used:

*   **Project Scaffolding**: I used the AI assistant to generate the initial project structure, including the `requirements.txt` file and the modular directory layout (`app/`, `main.py`).
*   **Code Generation**: The AI generated significant portions of the boilerplate code for FastAPI, Pydantic schemas, and the agent classes. This included writing the file handling logic, text extraction utilities, and the asynchronous orchestration in `main.py`.
*   **Prompt Engineering**: The core prompts for the agents were developed iteratively with the AI. I would describe the agent's goal (e.g., "classify this document"), and the AI would help craft a precise and effective prompt.
*   **Debugging and Refinement**: The AI was instrumental in debugging issues, particularly with asynchronous code (`asyncio`) and ensuring the LLM's JSON output was clean and parsable.

### Prompt Examples:

Here are a few examples of the prompts used in the agentic workflow.

**1. Classifier Agent Prompt:**
This prompt is designed to be simple and direct, asking the LLM to categorize a document based on its text content.

```
Classify the following document text into one of these categories: 
'bill', 'discharge_summary', 'id_card', 'medical_record', or 'unknown'.

Text:
---
{text[:2000]}
---

Category:
```

**2. Extraction Agent Prompt:**
This prompt is more complex. It leverages the concept of "few-shot" or "schema-guided" prompting. By providing the Pydantic JSON schema, we instruct the LLM to return a structured JSON object that matches our desired format, which significantly improves reliability.

```
Extract the information from the following text based on the document type '{doc_type}'
and format it into a JSON object that matches this schema:

Schema:
---
{
  "title": "Bill",
  "type": "object",
  "properties": {
    "type": {
      "title": "Type",
      "default": "bill",
      "type": "string"
    },
    "hospital_name": {
      "title": "Hospital Name",
      "type": "string"
    },
    // ... other properties
  }
}
---

Text:
---
{text}
---

Extracted JSON:
```

**3. Validation Agent Prompt:**
This prompt asks the LLM to perform a reasoning task. It needs to analyze multiple pieces of information, check for completeness against a set of rules (e.g., a bill and discharge summary are required), and identify inconsistencies.

```
Review the following extracted documents from a medical claim.
1. Identify any missing essential documents. A standard claim requires at least a 'bill' and a 'discharge_summary'.
2. Identify any discrepancies between the documents (e.g., patient name mismatch).

Documents:
---
[
  {
    "type": "bill",
    "hospital_name": "General Hospital",
    "total_amount": 5000
  },
  {
    "type": "discharge_summary",
    "patient_name": "John Smith",
    "diagnosis": "Hypertension"
  }
]
---

Return a JSON object with two keys:
- "missing_documents": a list of strings describing missing document types.
- "discrepancies": a list of strings describing any data inconsistencies.

Validation JSON:
``` 