from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException,Depends

app = FastAPI()
security = HTTPBearer()

class TextData(BaseModel):
    text: str = Field(..., example="string")

class QueryData(BaseModel):
    query: str = Field(..., example="string")

class ConversationData(BaseModel):
    conversation_id: str = Field(..., example="random-uuid")
    query: str = Field(..., example="Hello World")

class ContextData(BaseModel):
    query: str = Field(..., example="string")
    context: str = Field(..., example="string")

class AuthData(BaseModel):
    email: str = Field(..., example="test@example.com")
    password: str = Field(..., example="password")

class StripeResponse(BaseModel):
    email: str
    stripe_subscription_id: str
    stripe_plan_id: str
    stripe_plan_name: str
    subscription_status: str
    current_period_start: str
    current_period_end: str
    latest_invoice: str
    trial_start: str
    trial_end: str
    stripe_price_id: Optional[str] = None
    customer_id: str

@app.post("/chat/summarize")
async def summarize(text_data: TextData):
    return {
        "summary":"Scientists have discovered that viruses are extremely abundant on Earth, with millions of times more viruses than stars in the universe. Viruses also hold the majority of genetic diversity on Earth and are now being recognized as a powerful force in shaping the planet's climate and geochemical cycles. Additionally, viruses have had a significant impact on the evolution of their hosts, including humans, with the human genome containing thousands of segments of virus DNA."
    }

@app.post("/chat/start-conversation")
async def start_conversation(query_data: QueryData):
    return {
        "conversation_id": str(uuid.uuid4()),
        "response": "Hello! How can I assist you today?"
    }

@app.post("/chat/continue-conversation")
async def continue_conversation(conversation_data: ConversationData):
    return {
        "conversation_id": conversation_data.conversation_id,
        "response": "Certainly! I would be delighted to write a poem for you. Please provide me with a theme or any specific details you would like to include in the poem, and I will do my best to create a beautiful piece of verse for you."
    }

@app.post("/chat/start-conversation-with-context")
async def start_conversation_with_context(context_data: ContextData):
    return {
        "conversation_id": str(uuid.uuid4()),
        "response": "The context provided states that scientists have discovered that viruses are the most abundant life forms on Earth, outnumbering stars in the universe by a million times. It also mentions that viruses hold the majority of genetic diversity on the planet and have a significant impact on global climate and geochemical cycles. Additionally, viruses have played a crucial role in the evolution of their hosts, with the human genome containing 100,000 segments of virus DNA."
    }

@app.post("/auth/login")
async def login(auth_data: AuthData):
    return {
        "access_token": "eyJraWQiOiIwUIn0.ZXZpY2Vfa2V5IjoidXMtZWFzdC0xX2NjOWI4YTNkLTg1YmlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX1A1VG9pYlh3aSIsImNsaWVudF9pZCI6IjZqbjlzM2w3Zm81NzNmYXA2aTltNzVlajlkIiwib3JpZ2luX2p0aSI6IjE5ZDNiNDc0LWRkYjAtNDkzMy04Zjc1LWZiYmRkNzhjZTJmMSIsImV2ZW50X2lkIjoiNTdhMjczNzktMGYyZi00NjQ3LWJiZjUtYTIxZmQyM2ZkZDhiIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTY4ODQ0OTQ0MywiZXhwIjoxNjg4NDUzMDQzLCJpYXQiOjE2ODg0NDk0NDMsImp0aSI6IjA1MjQzNzZmLTE3NTctNDU4Yy1iNDUxLTdjYzdmYmM2YzliMSIsInVzZXJuYW1lIjoiYWUyMWIwN2QtMWYxNi00YzQ3LTg1ZDgtZDExYWNjOGE5NGZlIn0.Jhn_nG3FLhPODFFbwGPCeogmk77S59f1nHKt-F5skXxgrbhemRLVdEpfkinpe-2Z81ZWoplYI_ngX_qvLRAY3omglCn-KOCCWKc5m7s2OktuPSUAAS9_oJULfjFeiEca33tKBopZP4tshQQ-VgVe5mYjduUegitEJ5LlIn7iK9DX_rHHBxqkSZl7uAspyPhLRi5oHUiyGfP3m7SBuFLJv5euKJ7x_EjhqSNE024NYgtWqeXdmX4J7AUjAQJ25LMWCkuku7hE-SVberF6-YDTMibC93MwQpWH9ie7TXGgwnlzpOUdsm9V8YcYvApFMB6v0vaZcFXT1l4cnYe6C5DNfg",
        "stripe_subscription_id": "1234-2134-45654-32444",
        "stripe_plan_id": "23493-34234-243-2949-423",
        "stripe_plan_name": "STRIPE_PLAN_1",
        "subscription_status": "active",
        "current_period_start": "01-06-2023",
        "current_period_end": "01-12-2023",
        "latest_invoice": "DSJKFHK-ASDFAS-DFSD-13214-ASDF",
        "trial_start": "01-06-2023",
        "trial_end": "01-12-2023",
        "stripe_price_id": None
    }

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "asdfjkl":
        raise HTTPException(
            status_code=401, 
            detail="Invalid authorization code."
        )
    return token

@app.get("/stripe/stripe-details", response_model=StripeResponse,
    summary="Retrieve stripe details",
    description='''## Usage Instructions
    To use this endpoint, follow these steps:
    1. Click on the lock icon next to this endpoint.
    2. In the Authorization modal, select "HTTP Bearer" as the type.
    3. In the 'value' field, enter the access token "asdfjkl".
    4. Click 'Authorize' to close the modal.
    5. Now you can click 'Try it out' and 'Execute' to test the endpoint with the provided access token.
    Remember to use the correct access token for production applications.''')
async def stripe_details(token: str = Depends(verify_token)):
    return {
        "email": "grandlens14@gmail.com",
        "stripe_subscription_id": "1234-2134-45654-32444",
        "stripe_plan_id": "23493-34234-243-2949-423",
        "stripe_plan_name": "STRIPE_PLAN_1",
        "subscription_status": "active",
        "current_period_start": "01-06-2023",
        "current_period_end": "01-12-2023",
        "latest_invoice": "DSJKFHK-ASDFAS-DFSD-13214-ASDF",
        "trial_start": "01-06-2023",
        "trial_end": "01-12-2023",
        "stripe_price_id": None,
        "customer_id": "cus_O3ugN4OWsUiQf0"
    }