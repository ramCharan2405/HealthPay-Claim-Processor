import json
from app.services import generate_content
from app.schemas import Bill, DischargeSummary, IDCard, MedicalRecord

class BaseAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name

    async def run(self, *args, **kwargs):
        raise NotImplementedError

class ClassifierAgent(BaseAgent):
    async def run(self, text: str) -> str:
        prompt = f"""
        Classify the following document text into one of these categories: 
        'bill', 'discharge_summary', 'id_card', 'medical_record', or 'unknown'.
        
        Text:
        ---
        {text[:2000]}
        ---
        
        Category:
        """
        response = await generate_content(prompt)
        return response.strip().lower()

class ExtractionAgent(BaseAgent):
    async def run(self, text: str, doc_type: str):
        if doc_type == "bill":
            schema = Bill.model_json_schema()
        elif doc_type == "discharge_summary":
            schema = DischargeSummary.model_json_schema()
        elif doc_type == "id_card":
            schema = IDCard.model_json_schema()
        elif doc_type == "medical_record":
            schema = MedicalRecord.model_json_schema()
        else:
            return {"type": "unknown", "error": "Document type not supported for extraction"}

        prompt = f"""
        Extract the information from the following text based on the document type '{doc_type}'
        and format it into a JSON object that matches this schema:
        
        Schema:
        ---
        {json.dumps(schema, indent=2)}
        ---
        
        Text:
        ---
        {text}
        ---
        
        Extracted JSON:
        """
        response = await generate_content(prompt)
        
        try:
            # Clean the response to get a valid JSON
            json_str = response.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"type": doc_type, "error": "Failed to parse LLM response as JSON"}

class ValidationAgent(BaseAgent):
    async def run(self, documents: list):
        prompt = f"""
        Review the following extracted documents from a medical claim.
        1. Identify any missing essential documents. A standard claim requires at least a 'bill' and a 'discharge_summary'.
        2. Identify any discrepancies between the documents (e.g., patient name mismatch).
        
        Documents:
        ---
        {json.dumps(documents, indent=2)}
        ---
        
        Return a JSON object with two keys:
        - "missing_documents": a list of strings describing missing document types.
        - "discrepancies": a list of strings describing any data inconsistencies.
        
        Example Response:
        {{
          "missing_documents": ["id_card"],
          "discrepancies": ["Patient name on bill (John Doe) does not match discharge summary (Jon Smith)."]
        }}
        
        Validation JSON:
        """
        response = await generate_content(prompt)
        
        try:
            json_str = response.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {
                "missing_documents": [],
                "discrepancies": ["Failed to parse validation agent response."]
            }
