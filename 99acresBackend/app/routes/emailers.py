from fastapi import APIRouter, HTTPException, Depends, status, Query, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.database.schemas.common import SuccessResponse, PaginatedResponse
from app.database.models import User, EmailLog as EmailLogDoc
from app.utils.dependencies import get_current_active_user, get_admin_user
from app.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
from datetime import datetime

router = APIRouter()

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str
    template_id: Optional[str] = None

class EmailTemplate(BaseModel):
    id: str
    name: str
    subject: str
    body: str
    created_at: datetime
    updated_at: datetime

class EmailLog(BaseModel):
    id: str
    to_email: str
    subject: str
    status: str  # sent, failed, pending
    sent_at: Optional[datetime]
    error_message: Optional[str]

# In-memory storage for demo (replace with database in production)
email_templates = {}
email_logs = []

async def send_email_background(to_email: str, subject: str, message: str):
    """Background task to send email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(message, 'html'))

        # Create SMTP session
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.FROM_EMAIL, to_email, text)
        server.quit()

        # Log success - try to persist to DB, otherwise fallback to in-memory
        try:
            db_log = EmailLogDoc(
                to_email=to_email,
                subject=subject,
                status="sent",
                sent_at=datetime.utcnow(),
                metadata={}
            )
            await db_log.insert()
        except Exception:
            log_id = str(uuid.uuid4())
            email_logs.append(EmailLog(
                id=log_id,
                to_email=to_email,
                subject=subject,
                status="sent",
                sent_at=datetime.utcnow()
            ))

    except Exception as e:
        # Log failure - try DB then fallback
        try:
            db_log = EmailLogDoc(
                to_email=to_email,
                subject=subject,
                status="failed",
                error_message=str(e),
                metadata={}
            )
            await db_log.insert()
        except Exception:
            log_id = str(uuid.uuid4())
            email_logs.append(EmailLog(
                id=log_id,
                to_email=to_email,
                subject=subject,
                status="failed",
                error_message=str(e)
            ))

@router.post("/send", response_model=SuccessResponse)
async def send_email(
    email_data: EmailRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Send an email"""
    try:
        # Add to background tasks
        background_tasks.add_task(
            send_email_background,
            email_data.to_email,
            email_data.subject,
            email_data.message
        )

        return SuccessResponse(
            message="Email queued for sending",
            data={"email_id": str(uuid.uuid4())}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue email: {str(e)}"
        )

@router.get("/templates", response_model=PaginatedResponse)
async def get_email_templates(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_admin_user)
):
    """Get email templates (Admin only)"""
    templates_list = list(email_templates.values())
    start = (page - 1) * size
    end = start + size

    return PaginatedResponse(
        items=templates_list[start:end],
        total=len(templates_list),
        page=page,
        size=size,
        pages=(len(templates_list) + size - 1) // size
    )

@router.post("/templates", response_model=SuccessResponse)
async def create_email_template(
    template_data: dict,
    current_user: User = Depends(get_admin_user)
):
    """Create email template (Admin only)"""
    template_id = str(uuid.uuid4())
    template = EmailTemplate(
        id=template_id,
        name=template_data.get("name"),
        subject=template_data.get("subject"),
        body=template_data.get("body"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    email_templates[template_id] = template

    return SuccessResponse(
        message="Email template created successfully",
        data={"template_id": template_id}
    )

@router.get("/logs", response_model=PaginatedResponse)
async def get_email_logs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_admin_user)
):
    """Get email logs (Admin only)"""
    logs = email_logs

    if status_filter:
        logs = [log for log in logs if log.status == status_filter]

    start = (page - 1) * size
    end = start + size

    return PaginatedResponse(
        items=[log.dict() for log in logs[start:end]],
        total=len(logs),
        page=page,
        size=size,
        pages=(len(logs) + size - 1) // size
    )

@router.get("", response_model=SuccessResponse)
async def get_emailers_info():
    """Get emailers service information"""
    return SuccessResponse(
        message="Emailers service is available",
        data={
            "service": "emailers",
            "version": "1.0.0",
            "endpoints": [
                "GET /api/emailers - Service info",
                "GET /api/emailers/test - Test configuration",
                "POST /api/emailers/send - Send email",
                "GET /api/emailers/templates - Get templates (admin)",
                "POST /api/emailers/templates - Create template (admin)",
                "GET /api/emailers/logs - Get email logs (admin)"
            ]
        }
    )

@router.get("/test")
async def test_email_config():
    """Test email configuration"""
    return {
        "smtp_host": settings.SMTP_HOST,
        "smtp_port": settings.SMTP_PORT,
        "from_email": settings.FROM_EMAIL,
        "status": "Email service configured"
    }

@router.post("", response_model=SuccessResponse)
async def send_email_custom(
    email_data: dict,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """Send an email with custom data format"""
    try:
        # Debug: log incoming payload shape (avoid sensitive data in real logs)
        print(f"[DEBUG] send_email_custom payload keys: {list(email_data.keys()) if isinstance(email_data, dict) else type(email_data)}")
        # Extract data from the request
        name = email_data.get("name", "")
        subject = email_data.get("subject", "")
        recipients = email_data.get("recipients", [])
        body = email_data.get("body", "")

        # Handle different recipients formats
        if isinstance(recipients, int):
            # If recipients is a number, this might be a template or bulk send
            # For now, we'll treat it as a single email
            to_email = "default@example.com"  # This should be configured
        elif isinstance(recipients, list) and recipients:
            to_email = recipients[0]  # Use first recipient
        else:
            to_email = "default@example.com"

        # Add to background tasks
        background_tasks.add_task(
            send_email_background,
            to_email,
            subject,
            body
        )

        return SuccessResponse(
            message="Email queued for sending",
            data={
                "email_id": str(uuid.uuid4()),
                "name": name,
                "subject": subject,
                "recipients_count": len(recipients) if isinstance(recipients, list) else recipients
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue email: {str(e)}"
        )
