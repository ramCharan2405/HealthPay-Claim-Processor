import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from io import BytesIO

from app.schemas import ClaimResponse, Bill, DischargeSummary, MedicalRecord, IDCard
from app.utils import extract_text_from_pdf
from app.agents import ClassifierAgent, ExtractionAgent, ValidationAgent

app = FastAPI(title="HealthPay Claim Processor")

# Initialize agents
classifier_agent = ClassifierAgent()
extraction_agent = ExtractionAgent()
validation_agent = ValidationAgent()

@app.post("/process-claim", response_model=ClaimResponse)
async def process_claim(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")

    # 1. Extract text and classify documents
    async def process_file(file: UploadFile):
        contents = await file.read()
        text = await extract_text_from_pdf(BytesIO(contents))
        doc_type = await classifier_agent.run(text)
        return {"filename": file.filename, "text": text, "type": doc_type}

    classification_tasks = [process_file(file) for file in files]
    classified_docs = await asyncio.gather(*classification_tasks)

    # 2. Extract structured data
    async def extract_data(doc):
        if doc["type"] != "unknown":
            extracted_data = await extraction_agent.run(doc["text"], doc["type"])
            # Add the type back if it's not in the extracted data
            if 'type' not in extracted_data:
                extracted_data['type'] = doc['type']
            return extracted_data
        return {"type": "unknown", "filename": doc["filename"]}
    
    extraction_tasks = [extract_data(doc) for doc in classified_docs]
    structured_data = await asyncio.gather(*extraction_tasks)
    
    documents_for_response = []
    doc_map = {
        "bill": Bill,
        "discharge_summary": DischargeSummary,
        "medical_record": MedicalRecord,
        "id_card": IDCard
    }
    for data in structured_data:
        doc_type = data.get("type")
        if doc_type in doc_map:
            documents_for_response.append(doc_map[doc_type](**data))

    # 3. Validate the claim
    validation_result = await validation_agent.run([doc.model_dump() for doc in documents_for_response])

    # 4. Make a final decision
    status = "approved"
    reason = "All required documents present and data is consistent."

    if validation_result["missing_documents"]:
        status = "rejected"
        reason = f"Missing documents: {', '.join(validation_result['missing_documents'])}."
    
    if validation_result["discrepancies"]:
        status = "rejected"
        reason += f" Data discrepancies found: {', '.join(validation_result['discrepancies'])}."

    return ClaimResponse(
        documents=documents_for_response,
        validation=validation_result,
        claim_decision={"status": status, "reason": reason},
    )

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the HealthPay Claim Processing API"}
