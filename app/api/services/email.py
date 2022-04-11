from datetime import datetime, timedelta, timezone
import secrets
from fastapi import HTTPException, status
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from db import database
import json

from api.settings import settings

def get_current_utc_time_with_hour_delta(delta: int = 48):
    return get_current_utc_time() + timedelta(hours=delta)

def get_current_utc_time() -> datetime:
    return datetime.now(timezone.utc).astimezone()

async def reset_password(email: str) -> bool:
    async with database.connection():
        result = await database.fetch_one(
            query="SELECT profile_id FROM profile WHERE email=:email", 
            values={'email': email}
        )
    if result is None: 
        raise HTTPException(status.HTTP_204_NO_CONTENT, "Please check your email.")

    profile_id = result["profile_id"]
    token = secrets.token_urlsafe()
    expiration = get_current_utc_time_with_hour_delta(delta=48)

    async with database.connection():
        await database.execute(
            query="""
                INSERT INTO reset_token 
                    (reset_token_id, expiration_date, profile_id) 
                VALUES
                    (:token, :expiration, :profile_id)
                """,
            values={'token': token, 'expiration': expiration, 'profile_id': profile_id}
        )
    params = {"url": f"{settings.client_hostname}/reset-password/{token}"}

    dispatch_sendgrid_email("VCU Crew Backstay: Reset Password", email, params, settings.sendgrid_password_reset_key)
    return True

def dispatch_sendgrid_email(subject, to_emails, params: dict, template_id: str):
    '''Sends an templated email with sendgrids API.'''
    message = Mail(from_email=(settings.no_reply_email, settings.app_name), to_emails=to_emails, subject=subject, html_content=subject)

    message.dynamic_template_data = params
    print(message)

    message.template_id = template_id
    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        response = sg.send(message)
        del response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send email.{e}")