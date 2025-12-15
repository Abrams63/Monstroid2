"""
FastAPI Server for serving static website and handling form submissions
"""
import json
import os
import re
import smtplib
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

app = FastAPI()

# Define the path to the site directory
site_path = Path(__file__).parent.parent / "site"

# Serve static files from the site directory
app.mount("/static", StaticFiles(directory=site_path), name="static")

@app.get("/")
async def read_root():
    """
    Serve the main index.html file when accessing the root URL
    """
    index_path = site_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        return {"error": "index.html not found"}

@app.get("/{full_path:path}")
async def serve_static_files(full_path: str):
    """
    Serve any requested file from the site directory
    This handles all other routes and serves the appropriate static file
    """
    file_path = site_path / full_path
    
    # If the file exists, return it
    if file_path.is_file():
        return FileResponse(file_path)
    
    # If it's not a file but a directory, try to find an index.html in that directory
    if file_path.is_dir():
        dir_index = file_path / "index.html"
        if dir_index.is_file():
            return FileResponse(dir_index)
    
    # If the file doesn't exist, return the main index.html (for SPA routing)
    fallback_path = site_path / full_path
    if fallback_path.suffix.lower() in ['.html', '.htm']:
        return FileResponse(site_path / "index.html")
    
    # For non-existent files, return the main index.html to allow client-side routing
    return FileResponse(site_path / "index.html")
# Load form configuration from a JSON file
config_path = Path(__file__).parent / "email_config.json"
if config_path.exists():
    with open(config_path, 'r', encoding='utf-8') as f:
        email_config = json.load(f)
else:
    # Default configuration
    email_config = {
        "useSmtp": False,
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "demo@gmail.com",
        "password": "demopassword",
        "recipientEmail": "demo@gmail.com"
    }

@app.post("/contact")
async def handle_contact_form(
    request: Request,
    form_type: str = Form(...),
    email: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    g_recaptcha_response: Optional[str] = Form(None),
    **kwargs
):
    """
    Handle form submissions similar to the original rd-mailform.php
    """
    # Validate reCAPTCHA if present
    if g_recaptcha_response:
        captcha_result = await verify_recaptcha(g_recaptcha_response, request)
        if not captcha_result:
            return {"status": "error", "code": "CPT002", "message": "reCAPTCHA verification failed"}
    
    # Validate email format
    if email:
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return {"status": "error", "code": "MF001", "message": "Invalid email format"}
    
    # Check if recipient email is valid
    recipient_emails = email_config['recipientEmail']
    if not recipient_emails:
        return {"status": "error", "code": "MF001", "message": "No recipient email configured"}
    
    # Determine subject based on form type
    subjects = {
        "contact": "A message from your site visitor",
        "subscribe": "Subscribe request",
        "order": "Order request"
    }
    subject = subjects.get(form_type, "A message from your site visitor")
    
    # Build the email content
    email_content = build_email_content(form_type, name, email, message, **kwargs)
    
    # Send the email
    try:
        send_email(recipient_emails, subject, email_content, name or "Site Visitor")
        return {"status": "success", "code": "MF000", "message": "Message sent successfully"}
    except smtplib.SMTPException as e:
        return {"status": "error", "code": "MF255", "message": f"Failed to send email: {str(e)}"}

async def verify_recaptcha(response_token: str, request: Request = None) -> bool:
    """
    Verify reCAPTCHA response
    """
    # In a real implementation, you would verify with Google's API
    # For now, we'll just return True as a placeholder
    # You would need to set up your own reCAPTCHA keys
    # secret_key = os.getenv('RECAPTCHA_SECRET_KEY', 'your-secret-key-here')
    
    # Uncomment the following to implement actual verification:
    # data = {
    #     'secret': secret_key,
    #     'response': response_token,
    #     'remoteip': request.client.host
    # }
    # response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    # result = response.json()
    # return result.get('success', False)
    
    # For demo purposes, return True
    return True

def build_email_content(form_type: str, name: str, email: str, message: str, **kwargs) -> str:
    """
    Build the email content based on form data, similar to the original template
    """
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>A message from your site visitor</title>
    </head>
    <body style="font-family: Arial, sans-serif; background: #406c8d; margin: 0; padding: 0;">
        <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0" style="background: #406c8d;">
            <tr>
                <td align="center" valign="top" style="padding: 0 15px;">
                    <table align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <td height="15" style="height: 15px; line-height:15px;"></td>
                        </tr>
                        <tr>
                            <td width="600" align="center" valign="top" style="border-radius: 4px; overflow: hidden; box-shadow: 3px 3px 6px 0 rgba(0,0,0,0.2);background: #dde1e6;">
                                <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td align="center" valign="top" style="border-top-left-radius: 4px; border-top-right-radius: 4px; overflow: hidden; padding: 0 20px;background: #302f35;">
                                            <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                <tr>
                                                    <td height="30" style="height: 30px; line-height:30px;"></td>
                                                </tr>
                                                <tr>
                                                    <td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 32px; mso-line-height-rule: exactly; line-height: 32px; font-weight: 400; letter-spacing: 1px;color: #ffffff;">Notification</td>
                                                </tr>
                                                <tr>
                                                    <td height="30" style="height: 30px; line-height:30px;"></td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="center" valign="top" style="padding: 0 20px;">
                                            <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                <tr>
                                                    <td height="30" style="height: 30px; line-height:30px;"></td>
                                                </tr>
                                                <tr>
                                                    <td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 22px; font-weight: 400;color: #302f35;">Hi, someone left a message for you at {site_name}</td>
                                                </tr>
                                                <tr>
                                                    <td height="20" style="height: 20px; line-height:20px;"></td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="top">
                                                        <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                            <tr>
                                                                <td align="center" valign="top" style="background: #d1d5da;">
                                                                    <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                                        <tr>
                                                                            <td height="1" style="height: 1px; line-height:1px;"></td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="center" valign="top" style="background: #e4e6e9;">
                                                                    <table width="10%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                                        <tr>
                                                                            <td height="2" style="height: 2px; line-height:2px;"></td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="20" style="height: 20px; line-height:20px;"></td>
                                                </tr>
                                                <tr>
                                                    <td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 24px; mso-line-height-rule: exactly; line-height: 30px; font-weight: 700;color: #302f35;">
                                                        {subject}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="20" style="height: 20px; line-height:20px;"></td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="top">
                                                        <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                            <tr>
                                                                <td align="center" valign="top">
                                                                    <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                                                        <tr>
                                                                            <td width="10" align="left" valign="top" style="padding: 0 10px 0 0;font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;font-weight: 700;">Email:</td>
                                                                            <td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;">{email}</td>
                                                                        </tr>
                                                                        {info_rows}
                                                                        <tr>
                                                                            <td width="10" align="left" valign="top" style="padding: 0 10px 0 0;font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;font-weight: 70;">Message:</td>
                                                                            <td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;">{message}</td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td height="12" style="height: 12px; line-height:12px;"></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="40" style="height: 40px; line-height:40px;"></td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td height="20" style="height: 20px; line-height:20px;"></td>
                        </tr>
                        <tr>
                            <td width="600" align="center" valign="top">
                                <table width="100%" align="center" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td align="center" valign="top" style="font-family: Arial, sans-serif; font-size: 12px; mso-line-height-rule: exactly; line-height: 18px; font-weight: 400;color: #a1b4c4;">This is an automatically generated email, please do not reply.</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td height="20" style="height: 20px; line-height:20px;"></td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    # Add additional form fields
    info_rows = ""
    for key, value in kwargs.items():
        if key not in ["counter", "email", "message", "form-type", "g-recaptcha-response"] and value:
            info_row = f'<tr><td width="110" align="left" valign="top" style="padding: 0 10px 0 0;font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;font-weight: 70;">{key.title()}:</td><td align="left" valign="top" style="font-family: Arial, sans-serif; font-size: 14px; mso-line-height-rule: exactly; line-height: 20px; font-weight: 400;color: #302f35;">{value}</td></tr>'
            info_rows += info_row
    
    # Determine subject based on form type
    subjects = {
        "contact": "A message from your site visitor",
        "subscribe": "Subscribe request",
        "order": "Order request"
    }
    subject = subjects.get(form_type, "A message from your site visitor")
    
    # Replace template placeholders
    content = template.format(
        subject=subject,
        site_name="your-website.com",
        email=email or "Not provided",
        message=message or "Not provided",
        info_rows=info_rows
    )
    
    return content

def send_email(recipients: str, subject: str, content: str, sender_name: str = "Site Visitor"):
    """
    Send an email using SMTP
    """
    if email_config.get("useSmtp", False):
        # Use SMTP for sending emails
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{email_config['username']}>"
        msg['To'] = recipients
        msg['Subject'] = subject
        
        # Add HTML content
        html_part = MIMEText(content, 'html')
        msg.attach(html_part)
        
        # Connect to server and send email
        server = smtplib.SMTP(email_config['host'], email_config['port'])
        server.starttls()
        server.login(email_config['username'], email_config['password'])
        
        text = msg.as_string()
        server.sendmail(email_config['username'], recipients, text)
        server.quit()
    else:
        # For non-SMTP mode, just print to console (would be replaced with actual sending mechanism)
        print(f"Email would be sent to: {recipients}")
        print(f"Subject: {subject}")
        print(f"Content: {content}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
