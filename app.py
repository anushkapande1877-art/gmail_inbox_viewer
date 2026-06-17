from flask import Flask, request
import imaplib
import email

app = Flask(__name__)

# ==========================
# Gmail Configuration
# ==========================
EMAIL_ADDRESS = "abc@gmail.com"
APP_PASSWORD = "---- ---- ---- ----"

FILTER_SENDER = "xyz@gmail.com"


# ==========================
# Inbox Route
# ==========================
@app.route("/")
def inbox():

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(
            EMAIL_ADDRESS,
            APP_PASSWORD
        )

        mail.select("INBOX")

        status, messages = mail.search(
            None,
            f'(FROM "{FILTER_SENDER}")'
        )

        mail_ids = messages[0].split()

        html = f"""
        <html>
        <head>
            <title>Mail Viewer</title>

            <style>

                body {{
                    font-family: Arial;
                    margin: 30px;
                    background: #f5f5f5;
                }}

                .mail {{
                    background: white;
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                }}

                pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}

                button {{
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                }}

                button:hover {{
                    background: #0056b3;
                }}

            </style>

        </head>

        <body>

        <h1>Inbox Viewer</h1>

        <h3>Sender Filter: {FILTER_SENDER}</h3>

        <hr>
        """

        for msg_id in reversed(mail_ids[-10:]):

            _, data = mail.fetch(
                msg_id,
                "(RFC822)"
            )

            raw_email = data[0][1]

            msg = email.message_from_bytes(
                raw_email
            )

            subject = msg.get(
                "Subject",
                "No Subject"
            )

            sender = msg.get(
                "From",
                "Unknown"
            )

            date = msg.get(
                "Date",
                ""
            )

            body = ""

            if msg.is_multipart():

                for part in msg.walk():

                    content_type = (
                        part.get_content_type()
                    )

                    disposition = str(
                        part.get(
                            "Content-Disposition"
                        )
                    )

                    if (
                        content_type == "text/plain"
                        and "attachment"
                        not in disposition
                    ):

                        payload = part.get_payload(
                            decode=True
                        )

                        if payload:

                            body = payload.decode(
                                errors="ignore"
                            )

                            break

            else:

                payload = msg.get_payload(
                    decode=True
                )

                if payload:

                    body = payload.decode(
                        errors="ignore"
                    )

            html += f"""
            <div class="mail">

                <h2>{subject}</h2>

                <b>From:</b> {sender}<br>
                <b>Date:</b> {date}

                <hr>

                <pre>{body}</pre>

            </div>
            """

        mail.logout()

        html += """
        </body>
        </html>
        """

        return html

    except Exception as e:

        return f"""
        <h2>Error</h2>
        <pre>{str(e)}</pre>
        """

# ==========================
# Run App
# ==========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
