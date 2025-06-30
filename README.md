# HealthPay AI Claim Processor

This project is a real-world agentic backend pipeline that processes medical insurance claim documents using AI tools and agent orchestration frameworks. It's built with FastAPI and uses a multi-agent workflow to classify, extract, and validate information from PDF documents.

## Project Overview

- **Single Endpoint**: All claim processing is handled via the `/process-claim` endpoint, which accepts a single multi-page PDF file.
- **Multi-Agent Workflow**: The system uses three main agents:
  - **ClassifierAgent**: Determines the type of each page (bill, discharge summary, id card, etc.).
  - **ExtractionAgent**: Extracts structured data from each classified page using dynamic Pydantic schemas.
  - **ValidationAgent**: Checks for missing documents and data inconsistencies, then makes a claim decision.
- **Async Processing**: All pages are processed concurrently for speed and scalability.
- **Mock AI Service**: For demo purposes, the AI logic is simulated using regex and pattern matching, so no real API keys are required.

## Architecture & Logic

1.  **File Upload**: The `/process-claim` endpoint accepts a single PDF file via a `multipart/form-data` request.
2.  **PDF Splitting**: The PDF is split into individual pages and each page is processed independently.
3.  **Document Classification**: Each page is classified by the `ClassifierAgent` using the mock AI service.
4.  **Information Extraction**: The `ExtractionAgent` extracts structured data from each page, using regex and pattern matching to simulate AI extraction.
5.  **Validation**: The `ValidationAgent` reviews all extracted data, checks for required documents, and identifies inconsistencies.
6.  **Claim Decision**: The system returns a structured JSON response with the extracted documents, validation results, and a claim decision (approved/rejected).

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

3.  **(Optional) Set up your environment variables:**
    If you want to use the real Google Gemini API, create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY="your_google_api_key"
    ```
    For demo purposes, this is not required—the system will use the mock AI logic by default.

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

5.  **Test the endpoint:**
    Use the built-in FastAPI documentation at `http://127.0.0.1:8000/docs` to upload a multi-page PDF and test the `/process-claim` endpoint.

## Mock AI Service (Demo Mode)

For demonstration, the AI logic is simulated in `app/services.py`:
- **Classification**: Uses keyword and pattern matching to determine document type.
- **Extraction**: Uses regex to extract fields like patient name, amount, diagnosis, dates, etc., from the text.
- **Validation**: Checks for required documents and data consistency.

This allows you to demo the full workflow without any external dependencies or API rate limits.

## Example Output

A successful response from `/process-claim` looks like:

```json
{
  "documents": [
    {
      "type": "bill",
      "hospital_name": "General Hospital",
      "total_amount": 5000,
      "date_of_service": "2024-05-01"
    },
    {
      "type": "discharge_summary",
      "patient_name": "John Smith",
      "diagnosis": "Hypertension",
      "admission_date": "2024-04-28",
      "discharge_date": "2024-05-01"
    }
  ],
  "validation": {
    "missing_documents": [],
    "discrepancies": []
  },
  "claim_decision": {
    "status": "approved",
    "reason": "All required documents present and data is consistent."
  }
}
```

## File Structure

- `main.py` — FastAPI entry point, orchestrates the workflow.
- `app/agents.py` — Agent classes for classification, extraction, and validation.
- `app/services.py` — Contains the mock AI logic (regex, pattern matching, simulated responses).
- `app/schemas.py` — Pydantic models for structured data.
- `app/utils.py` — PDF text extraction and splitting utilities.
- `requirements.txt` — Python dependencies.

## Key Features

- Modular, async, and schema-driven design.
- Works out-of-the-box for demos (no API keys needed).
- Easily extendable for real AI integration.
- Robust error handling and clear, structured API responses.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE) 