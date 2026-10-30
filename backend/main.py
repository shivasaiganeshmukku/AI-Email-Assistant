import json

from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from ollama_service import generate_response
from models import (
    Email, 
    EmailAnalysis, 
    EmailClassification, 
    ActionItem, 
    ActionItemsResponse,
    EmailReplyRequest,
    EmailReplyResponse
    )
app = FastAPI(
    title="AI Email Assistant",
    description="GenAI-powered email understanding and automation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5133",
        "http://127.0.0.1:5133"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception
):
    print(
        f"Unexpected server error on {request.method} "
        f"{request.url.path}: {type(exc).__name__}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred. Please try again."
        }
    )




@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Email Assistant"
    }


@app.post("/api/test-ai")
async def test_ai():
    prompt = "Explain Artificial Intelligence in one simple sentence."

    response = await generate_response(prompt)

    return {
        "response": response
    }



@app.post("/api/analyze-email", response_model=EmailAnalysis)
async def analyze_email(email: Email):
    prompt = f"""
You are an email status and action intelligence assistant.

Analyze the email and return a JSON object with exactly these fields:
- summary: short, factual summary of the email
- category: one of Work, Personal, Finance, Meeting, Support, Other
- priority: one of Low, Medium, High
- action_required: true or false
- email_status: one of Action Required, Reply Needed, Awaiting Response,
  Informational, No Action Needed, Unclear
- deadline: explicit deadline wording from the email, or null
- recommended_action: concise next step for the recipient

Status rules:
1. Action Required: the email explicitly asks the recipient to perform a task.
2. Reply Needed: the sender asks a question or clearly requests a response,
   without a more important task being the main purpose.
3. Awaiting Response: use only when the email content indicates that
   the recipient has already sent a message and is waiting for a response.
   This is an inference from the content, not confirmation of the actual inbox.
4. Informational: the email mainly shares information and does not clearly
   request a task or response.
5. No Action Needed: the email explicitly indicates that no action is needed.
6. Unclear: the intended next step cannot be determined confidently.

Additional rules:
- Set action_required to true only when the recipient is asked to take an action.
- Use only deadlines explicitly stated in the email. Do not calculate or invent dates.
- If no deadline is explicitly stated, return JSON null.
- Do not claim an email is overdue, a reply was received, or a task was completed.
- If the email asks the recipient to do a task, recommend that task.
- If a reply is requested, recommend responding to the sender.
- If the email is informational, recommend reviewing or retaining it only if useful.
- Do not invent facts, commitments, or actions.
- Return valid JSON only. Do not include Markdown or explanations.

Sender: {email.sender}
Recipient: {email.recipient}
Subject: {email.subject}
Body: {email.body}
"""

    try:
        response = await generate_response(prompt)

        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        analysis_data = json.loads(cleaned_response)
        analysis = EmailAnalysis.model_validate(analysis_data)

        return analysis

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned invalid JSON. Please try again."
        )

    except ValidationError as exc:
        print("Email analysis validation error:", exc)

        raise HTTPException(
            status_code=502,
            detail="The AI response did not match the expected email analysis structure."
        )



@app.post("/api/summarize-email")
async def summarize_email(email: Email):
    prompt = f"""
    Summarize the following email in 2-3 concise sentences.
    Preserve important deadlines, amounts, and requested actions.
    Do not invent information that is not present in the email.

    Rules:
    1. Use only information explicitly stated in the email.
    2. Do not invent dates, times, names, amounts, or deadlines.
    3. Preserve dates, times, amounts, percentages, and identifiers exactly as written.
    4. Do not change the meaning of any instruction.
    5. If information is unclear, do not guess.
    6. Include important deadlines and requested actions.
    7. Return only the summary text, without headings or explanations.


    Subject: {email.subject}
    Body: {email.body}

    Return only the summary text.
    """

    summary = await generate_response(prompt)

    return {
        "subject": email.subject,
        "summary": summary.strip()
    }

@app.post(
    "/api/classify-email",
    response_model=EmailClassification
)
async def classify_email(email: Email):

    prompt = f"""
You are an email classification assistant.

ou are a careful email classification assistant.

Your task is to classify the email into exactly ONE primary category based on its main purpose.

Allowed categories and their meanings:

Work: Project updates, work assignments, reports, deadlines, and workplace communication.

Personal: Family messages, friendships, invitations for personal activities, and private matters.

Finance: Invoices, bills, payments, refunds, salaries, banking, expenses, and financial transactions.

Meeting: Meeting invitations, appointment scheduling, agendas, and meeting rescheduling.

Support: Customer complaints, technical problems, help requests, and troubleshooting.

Other: Emails that do not reasonably fit any of the categories above.

Classification rules:

Read both the subject and body before deciding.

Identify the primary purpose of the email.

Choose the category that best represents the requested action or main topic.

Do not classify an email as Work merely because it mentions a company or employee.

If the email primarily concerns an invoice, bill, payment, or financial transaction, choose Finance.

If the email primarily schedules or invites someone to a meeting, choose Meeting.

Return exactly one category from the allowed list.

Do not invent information or provide explanations.

Examples:

Subject: "Invoice Payment Reminder"; Body: "Your invoice of ₹25,000 is due tomorrow." → Finance

Subject: "Project Report Deadline"; Body: "Submit the project report by Friday." → Work

Subject: "Team Meeting Invitation"; Body: "Join our meeting on Monday at 10 AM." → Meeting

Subject: "Laptop Not Working"; Body: "Please help me fix my laptop." → Support

Subject: "Dinner This Weekend"; Body: "Would you like to join us for dinner?" → Personal

Email subject: {email.subject}
Email body: {email.body}


Return only the JSON object. Do not include Markdown or explanations.
"""

    response = await generate_response(prompt)

    try:
        classification_data = json.loads(response)
        classification = EmailClassification.model_validate(
            classification_data
        )
        return classification

    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid classification response."
        )

@app.post(
    "/api/extract-action", response_model=ActionItemsResponse)
async def extract_action(email: Email):


    prompt = f"""
Extract the action items from this email.

Return ONLY a valid JSON object. Do not include Markdown,
code fences, explanations, or text before or after the JSON.

Use exactly this structure:
{{
  "action_items": [
    {{
      "task": "task description",
      "deadline": null,
      "assignee": null
    }}
  ]
}}


Extract only explicit tasks from the email.

Rules:
- Preserve the meaning of each task and use concise action-oriented wording.
- Assign a person only when the email clearly connects that person to the task.
- Do not assume that the email recipient ("you") is responsible unless explicitly stated.
- Use null for missing deadlines or assignees. Never return "null", "unknown", or "not specified" as strings for these fields.
- Do not invent tasks, dates, or assignments.
- Return valid JSON matching the required schema, with no Markdown or explanations.


Sender: {email.sender}
Recipient: {email.recipient}
Subject: {email.subject}
Body: {email.body}
"""

    response = await generate_response(prompt)

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        action_data = json.loads(cleaned_response)
        result = ActionItemsResponse.model_validate(action_data)
        return result

    except (json.JSONDecodeError, ValidationError) as exc:
        print("Action-item parsing error:", repr(exc))
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid action-item response."
        )


@app.post(
    "/api/generate-reply",
    response_model=EmailReplyResponse
)
async def generate_email_reply(request: EmailReplyRequest):
    email = request.email
    tone = request.tone.value.lower()

    allowed_tones = {
        "professional": "polite, clear, and business-appropriate",
        "friendly": "warm, natural, and conversational",
        "concise": "brief, direct, and respectful"
    }

    if tone not in allowed_tones:
        raise HTTPException(
            status_code=400,
            detail="Tone must be Professional, Friendly, or Concise."
        )

    
    
    prompt = f"""
You are a reliable email reply assistant.

Write a natural, relevant email reply in a {tone} tone.
Style: {allowed_tones[tone]}.

Instructions:
- Respond directly to the sender's main message and purpose.
- Use only facts provided in the email. Never invent names,
  dates, availability, workload, decisions, or circumstances.
- For a request, acknowledge it politely without claiming the
  task is complete or promising a deadline, action, or update
  unless the user explicitly authorizes that commitment.
- For meeting invitations, do not accept or decline unless
  the user's decision is provided. If unknown, say you will
  check and confirm.
- Do not introduce unrelated topics, unnecessary questions,
  explanations, or statements about missing information.
- Do not include placeholder names or identify yourself as AI.
- Use a simple greeting and sign-off when appropriate.
- Return only the reply body. No Markdown, analysis, or commentary.
- This is a draft for the user to review, not a sent email.

Sender: {email.sender}
Recipient: {email.recipient}
Subject: {email.subject}
Original email:
{email.body}

Write the final reply now.
"""

    reply = await generate_response(prompt)

    reply = reply.strip()

    # Remove a surrounding Markdown code fence if the model
    # accidentally returns one.
    if reply.startswith("```") and reply.endswith("```"):
        lines = reply.splitlines()
        reply = "\n".join(lines[1:-1]).strip()

    if not reply:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an empty reply. Please try again."
        )

    reply_subject = (
        email.subject
        if email.subject.lower().startswith("re:")
        else f"Re: {email.subject}"
    )

    return EmailReplyResponse(
        subject=reply_subject,
        body=reply,
        tone=request.tone
    )
