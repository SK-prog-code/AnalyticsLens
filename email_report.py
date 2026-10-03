import smtplib
import html

from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.image import MIMEImage


def send_email_report(
    sender_email,
    app_password,
    recipient_email,
    subject,
    report,
    chart_bytes=None,
    image_bytes=None,
    image_mime_type=None
):
    """
    Send an AnalyticsLens AI analysis report through Gmail.

    Features:
    - Gmail SMTP SSL on port 465
    - Clean HTML email
    - Plain-text fallback
    - Optional generated chart
    - Optional uploaded visualization/image
    - Images displayed inside the email
    - Images also attached to the email
    """

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    sender_email = str(sender_email).strip()
    recipient_email = str(recipient_email).strip()

    # Escape report text so that accidental HTML inside
    # the analysis result does not break the email layout.
    safe_report = html.escape(
        report if report else "No analysis result available."
    )

    # Convert line breaks into HTML breaks.
    safe_report = safe_report.replace(
        "\n",
        "<br>"
    )

    # ========================================================
    # CREATE MESSAGE
    # ========================================================

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = recipient_email

    message["Subject"] = (
        subject
        if subject
        else "AnalyticsLens AI Analysis Report"
    )

    # ========================================================
    # PLAIN TEXT VERSION
    # ========================================================

    plain_text = f"""
AnalyticsLens AI
Your conversational AI data analyst

DATA ANALYSIS REPORT

{report}

------------------------------------------------------------

AnalyticsLens AI
Your conversational AI data analyst
"""

    message.set_content(
        plain_text
    )

    # ========================================================
    # IMAGE CONTENT IDS
    # ========================================================

    chart_cid = None
    image_cid = None

    if chart_bytes:

        chart_cid = make_msgid(
            domain="analyticslens.ai"
        )

    if image_bytes:

        image_cid = make_msgid(
            domain="analyticslens.ai"
        )

    # Remove angle brackets from Content-ID values
    # for use inside HTML cid references.
    chart_cid_value = (
        chart_cid.strip("<>")
        if chart_cid
        else None
    )

    image_cid_value = (
        image_cid.strip("<>")
        if image_cid
        else None
    )

    # ========================================================
    # OPTIONAL VISUALIZATION SECTION
    # ========================================================

    visualization_html = ""

    if chart_cid_value:

        visualization_html += f"""
        <div style="
            margin-top:28px;
            padding:20px;
            background:#f7f8fc;
            border:1px solid #e3e6ef;
            border-radius:12px;
        ">

            <h2 style="
                margin:0 0 14px 0;
                font-family:Arial,Helvetica,sans-serif;
                font-size:18px;
                color:#172554;
            ">
                📊 Generated Analysis Chart
            </h2>

            <img
                src="cid:{chart_cid_value}"
                alt="AnalyticsLens AI generated chart"
                style="
                    display:block;
                    width:100%;
                    max-width:760px;
                    height:auto;
                    margin:0 auto;
                    border-radius:8px;
                "
            >

        </div>
        """

    if image_cid_value:

        visualization_html += f"""
        <div style="
            margin-top:20px;
            padding:20px;
            background:#f7f8fc;
            border:1px solid #e3e6ef;
            border-radius:12px;
        ">

            <h2 style="
                margin:0 0 14px 0;
                font-family:Arial,Helvetica,sans-serif;
                font-size:18px;
                color:#172554;
            ">
                🖼️ Uploaded Visualization
            </h2>

            <img
                src="cid:{image_cid_value}"
                alt="Uploaded visualization"
                style="
                    display:block;
                    width:100%;
                    max-width:760px;
                    height:auto;
                    margin:0 auto;
                    border-radius:8px;
                "
            >

        </div>
        """

    # ========================================================
    # HTML EMAIL
    # ========================================================

    html_content = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        AnalyticsLens AI Analysis Report
    </title>

</head>


<body style="
    margin:0;
    padding:0;
    background:#f1f5f9;
    font-family:Arial,Helvetica,sans-serif;
">

    <div style="
        width:100%;
        padding:30px 0;
        background:#f1f5f9;
    ">

        <div style="
            max-width:760px;
            margin:0 auto;
            background:#ffffff;
            border-radius:16px;
            overflow:hidden;
            box-shadow:0 8px 30px rgba(15,23,42,0.10);
        ">


            <!-- ==================================================
                 HEADER
                 ================================================== -->

            <div style="
                padding:28px 32px;
                background:
                    linear-gradient(
                        110deg,
                        #18245f 0%,
                        #28358a 50%,
                        #7139d8 100%
                    );
            ">

                <div style="
                    color:#ffffff;
                    font-size:25px;
                    font-weight:700;
                    line-height:1.3;
                ">

                    📊 AnalyticsLens
                    <span style="
                        color:#c4b5fd;
                    ">
                        AI
                    </span>

                </div>


                <div style="
                    margin-top:7px;
                    color:#dbeafe;
                    font-size:14px;
                ">

                    Your conversational AI data analyst

                </div>

            </div>


            <!-- ==================================================
                 TITLE
                 ================================================== -->

            <div style="
                padding:30px 32px 12px 32px;
            ">

                <div style="
                    color:#111827;
                    font-size:23px;
                    font-weight:700;
                ">

                    Data Analysis Report

                </div>

                <div style="
                    margin-top:8px;
                    color:#64748b;
                    font-size:14px;
                ">

                    Generated by AnalyticsLens AI

                </div>

            </div>


            <!-- ==================================================
                 REPORT CONTENT
                 ================================================== -->

            <div style="
                padding:10px 32px 32px 32px;
            ">


                <!-- ANALYSIS REPORT -->

                <div style="
                    margin-top:12px;
                    padding:22px;
                    background:#f8fafc;
                    border:1px solid #e2e8f0;
                    border-radius:12px;
                ">

                    <div style="
                        margin-bottom:14px;
                        color:#172554;
                        font-size:17px;
                        font-weight:700;
                    ">

                        📋 Analysis Summary

                    </div>

                    <div style="
                        color:#334155;
                        font-size:14px;
                        line-height:1.75;
                        word-wrap:break-word;
                    ">

                        {safe_report}

                    </div>

                </div>


                <!-- ==================================================
                     VISUALIZATIONS
                     ================================================== -->

                {visualization_html}


                <!-- ==================================================
                     ABOUT
                     ================================================== -->

                <div style="
                    margin-top:28px;
                    padding:20px;
                    background:#f8fafc;
                    border-left:4px solid #6366f1;
                    border-radius:8px;
                ">

                    <div style="
                        color:#172554;
                        font-size:16px;
                        font-weight:700;
                        margin-bottom:8px;
                    ">

                        About AnalyticsLens AI

                    </div>

                    <div style="
                        color:#64748b;
                        font-size:13px;
                        line-height:1.65;
                    ">

                        AnalyticsLens AI is a conversational
                        data analytics assistant that helps
                        users understand datasets,
                        visualizations, trends, patterns,
                        and analytical results.

                    </div>

                </div>


            </div>


            <!-- ==================================================
                 FOOTER
                 ================================================== -->

            <div style="
                padding:20px 32px;
                background:#f8fafc;
                border-top:1px solid #e2e8f0;
                text-align:center;
            ">

                <div style="
                    color:#475569;
                    font-size:13px;
                    font-weight:600;
                ">

                    📊 AnalyticsLens AI

                </div>

                <div style="
                    margin-top:5px;
                    color:#94a3b8;
                    font-size:12px;
                ">

                    Your conversational AI data analyst

                </div>

            </div>


        </div>

    </div>

</body>

</html>
"""

    # ========================================================
    # ADD HTML VERSION
    # ========================================================

    message.add_alternative(
        html_content,
        subtype="html"
    )

    # ========================================================
    # GET HTML PART
    # ========================================================

    html_part = message.get_payload()[-1]

    # ========================================================
    # ATTACH GENERATED CHART
    # ========================================================

    if chart_bytes:

        chart_image = MIMEImage(
            chart_bytes,
            _subtype="png"
        )

        chart_image.add_header(
            "Content-ID",
            f"<{chart_cid_value}>"
        )

        chart_image.add_header(
            "Content-Disposition",
            "inline",
            filename="analyticslens_chart.png"
        )

        html_part.add_related(
            chart_image
        )

    # ========================================================
    # ATTACH UPLOADED IMAGE
    # ========================================================

    if image_bytes:

        image_subtype = "jpeg"

        if image_mime_type:

            if "/" in image_mime_type:

                image_subtype = (
                    image_mime_type.split(
                        "/"
                    )[-1].lower()
                )

        if image_subtype == "jpg":

            image_subtype = "jpeg"

        uploaded_image = MIMEImage(
            image_bytes,
            _subtype=image_subtype
        )

        uploaded_image.add_header(
            "Content-ID",
            f"<{image_cid_value}>"
        )

        uploaded_image.add_header(
            "Content-Disposition",
            "inline",
            filename=(
                "uploaded_visualization."
                + (
                    "jpg"
                    if image_subtype == "jpeg"
                    else image_subtype
                )
            )
        )

        html_part.add_related(
            uploaded_image
        )

    # ========================================================
    # SEND THROUGH GMAIL
    # ========================================================

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30
        ) as server:

            server.login(
                sender_email,
                app_password
            )

            server.send_message(
                message
            )

    except smtplib.SMTPAuthenticationError:

        raise Exception(
            "Gmail authentication failed. "
            "Make sure 2-Step Verification is enabled "
            "and that you are using a Gmail App Password, "
            "not your normal Gmail password."
        )

    except smtplib.SMTPRecipientsRefused:

        raise Exception(
            "Gmail rejected the recipient email address. "
            "Please check the recipient email."
        )

    except smtplib.SMTPServerDisconnected:

        raise Exception(
            "Gmail disconnected the SMTP connection. "
            "Please try again."
        )

    except smtplib.SMTPConnectError:

        raise Exception(
            "Could not connect to Gmail SMTP. "
            "Make sure port 465 is allowed on your network."
        )

    except smtplib.SMTPException as error:

        raise Exception(
            f"Gmail SMTP error: {error}"
        )

    except Exception as error:

        raise Exception(
            f"Email error: {error}"
        )