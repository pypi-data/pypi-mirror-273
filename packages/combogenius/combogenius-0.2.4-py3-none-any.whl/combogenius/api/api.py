import uvicorn
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "smtp.gmail.com"
USERNAME = "combogeniustest@gmail.com"
PASSWORD = "rxaqhipiukzzlxwr"
PORT = 587

app = FastAPI()

# SQLite database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

def generate_html_template(combos: list, discount: int, custom_html: str) -> str:
    """
    Generates an HTML template for email content.

    Args:
        combos (list): List of dictionaries containing combo information.
        discount (int): Discount percentage to be applied.
        custom_html (str): Custom HTML content if provided.

    Returns:
        str: Generated HTML content for the email.
    """
    combos_html = ""
    for combo in combos:
        combo_html = f"""
        <div class="combo">
            <h2>{combo['name']}</h2>
            <p>Price: ${combo['price']}</p>
            <p>Get {discount}% off on this combo!</p>
            <p class="discount">Use code: COMBO{combo['code']}</p>
        </div>
        """
        combos_html += combo_html

    if custom_html:
        html_content = custom_html
    else:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Combo Offer!</title>
            <style>
                /* CSS Styles */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: orange;
                    color: #ffffff;
                    padding: 20px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                .combo {{
                    margin-bottom: 20px;
                    padding: 10px;
                    background-color: yellow;
                    border-radius: 5px;
                }}
                .combo h2 {{
                    margin-top: 0;
                }}
                .discount {{
                    font-weight: bold;
                    color: red;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Combo Offer!</h1>
                </div>
                <div class="content">
                    {combos_html}
                </div>
                <div class="footer">
                    <p>This offer is valid for a limited time only. Visit us today!</p>
                </div>
            </div>
        </body>
        </html>
        """
    return html_content

@app.get("/")
def index() -> dict:
    """
    Endpoint to check if the FastAPI mailserver is running.

    Returns:
        dict: A dictionary indicating the status of the server.
    """
    return {"status": "fastapi mailserver is running"}

@app.post("/send_email/")
def send_email(recipient: str, subject: str, discount: int, custom_html: str = None) -> dict:
    """
    Sends an email to the specified recipient.

    Args:
        recipient (str): Email address of the recipient.
        subject (str): Subject of the email.
        discount (int): Discount percentage to be applied.
        custom_html (str): Custom HTML content for the email (optional).

    Returns:
        dict: A message indicating the status of the email sending process.
    """
    # Database Connection
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT email FROM companies")

    # Generate Combos
    combos = [
        {"name": "Deluxe Burger Combo", "code": "12345", "price": 10},
        {"name": "Family Pizza Combo", "code": "67890", "price": 20}
    ]

    # Generate HTML Template
    html_content = generate_html_template(combos, discount, custom_html)

    # Email Content
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # SMTP Connection and Sending Email
    with smtplib.SMTP(HOST, PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, recipient, msg.as_string())
        server.quit()

    return {"message": "Emails sent successfully"}

@app.get("/mark_interested/{email}")
async def mark_interested(email: str) -> dict:
    """
    Marks an email as interested in the database.

    Args:
        email (str): Email address to mark as interested.

    Returns:
        dict: A message indicating the status of the operation.
    """
    try:
        # Update interested column in the database
        c.execute("UPDATE companies SET clicked = 1 WHERE email = ?", (email,))
        conn.commit()
        return {"message": f"Email {email} marked as interested"}
    except Exception as e:
        return {"error": str(e)}

def run_api() -> None:
    """
    Runs the FastAPI server for sending emails.
    """
    uvicorn.run(app, host="127.0.0.1", port=5000,)
