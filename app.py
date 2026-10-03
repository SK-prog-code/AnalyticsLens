import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

from google import genai
from google.genai import types

from prompts import WELCOME_MESSAGE
from analytics import create_dataset_context
from analysis_planner import create_analysis_plan
from analytics_executor import execute_analysis
from chart_generator import create_chart
from gemini_helper import generate_with_retry
from result_summarizer import summarize_result
from vision_analyzer import analyze_image
from email_report import send_email_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AnalyticsLens AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DARK PROFESSIONAL UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       APP BACKGROUND
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(76, 45, 150, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 35% 10%,
                rgba(25, 65, 150, 0.20),
                transparent 32%
            ),
            #070b16;
    }

    .main {
        background: #070b16;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    /* ======================================================
       STREAMLIT HEADER
       ====================================================== */

    header[data-testid="stHeader"] {
        background: #090d16;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #19135f 0%,
                #172c7a 50%,
                #07183e 100%
            );

        border-right: 1px solid rgba(100,120,255,0.30);
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: rgba(255,255,255,0.68) !important;
    }

    /* ======================================================
       MAIN TEXT
       ====================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #ffffff !important;
    }

    p {
        color: #aeb9d2;
    }

    .stCaption {
        color: #8f9bb5 !important;
    }

    /* ======================================================
       BORDERED CONTAINERS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(20,25,43,0.96),
                rgba(12,16,28,0.96)
            );

        border:
            1px solid rgba(100,115,160,0.35);

        border-radius:
            18px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.22);
    }

    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #141b2b,
                #0e1420
            );

        border:
            1px solid rgba(80,105,155,0.45);

        border-radius:
            17px;

        min-height:
            112px;

        padding:
            0.9rem;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.22);
    }

    div[data-testid="stMetricLabel"] {
        color:
            #a8b3ca !important;
    }

    div[data-testid="stMetricValue"] {
        color:
            #ffffff !important;

        font-weight:
            800;
    }

    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    div[data-testid="stFileUploader"] {
        background:
            #0b1019;

        border:
            1px solid rgba(80,100,150,0.45);

        border-radius:
            13px;

        padding:
            0.3rem;
    }

    div[data-testid="stFileUploaderDropzone"] {
        background:
            #0b1019 !important;

        border:
            none !important;
    }

    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border:
            1px solid rgba(90,105,150,0.35);

        border-radius:
            13px;

        overflow:
            hidden;
    }

    /* ======================================================
       CHAT
       ====================================================== */

    div[data-testid="stChatMessage"] {
        background:
            transparent;

        border:
            none;
    }

    div[data-testid="stChatInput"] {
        margin-top:
            1rem;

        margin-bottom:
            1.5rem;
    }

    div[data-testid="stChatInput"] > div {
        background:
            #20232d !important;

        border:
            1px solid rgba(95,105,140,0.50) !important;

        border-radius:
            13px !important;
    }

    div[data-testid="stChatInput"] textarea {
        color:
            #ffffff !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color:
            #8791a8 !important;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #5147d9,
                #7446d8
            );

        color:
            #ffffff;

        border:
            1px solid rgba(145,130,255,0.40);

        border-radius:
            10px;

        min-height:
            42px;

        font-weight:
            650;

        box-shadow:
            0 7px 20px rgba(70,55,190,0.25);
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #6055ec,
                #8554ed
            );

        color:
            #ffffff;
    }

    /* ======================================================
       TEXT INPUT
       ====================================================== */

    input {
        background:
            #121722 !important;

        color:
            #ffffff !important;
    }

    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color:
            rgba(100,115,155,0.22);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GEMINI CLIENT
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


@st.cache_resource
def get_gemini_client():

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


gemini_client = get_gemini_client()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]


if "last_report" not in st.session_state:

    st.session_state.last_report = None


if "last_chart_bytes" not in st.session_state:

    st.session_state.last_chart_bytes = None


if "last_image_bytes" not in st.session_state:

    st.session_state.last_image_bytes = None


if "last_image_mime" not in st.session_state:

    st.session_state.last_image_mime = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📁 Upload Your Data")

    st.caption(
        "Add a dataset or visualization to begin your analysis."
    )

    st.write("")

    st.subheader("🗄️ Dataset")

    st.caption(
        "Upload a CSV or Excel file for analysis."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ],
        key="dataset_uploader"
    )

    st.write("")

    st.subheader("🖼️ Visualization")

    st.caption(
        "Upload a graph, chart, dashboard, or table."
    )

    uploaded_image = st.file_uploader(
        "Upload graph / chart / dashboard",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        key="image_uploader"
    )

    if uploaded_file is not None:

        st.success(
            "Dataset uploaded successfully!"
        )

    if uploaded_image is not None:

        st.success(
            "Visualization uploaded successfully!"
        )

    st.write("")

    st.caption(
        "AnalyticsLens AI"
    )


# ============================================================
# LOAD DATASET
# ============================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(
            ".csv"
        ):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file
            )

        st.session_state.df = df

        st.session_state.dataset_context = (
            create_dataset_context(df)
        )

    except Exception as error:

        st.error(
            f"Could not read the dataset: {error}"
        )


# ============================================================
# HERO
# ============================================================

with st.container(
    border=True
):

    st.title(
        "📊 AnalyticsLens AI"
    )

    st.caption(
        "Your conversational AI data analyst — "
        "turn data into insights with AI."
    )


# ============================================================
# FEATURE ROW
# ============================================================

st.write("")

feature_columns = st.columns(
    5
)

features = [
    "📊 Data Analysis",
    "🖼️ Visual Insights",
    "📈 Trend Detection",
    "💬 Natural Language",
    "✨ Actionable Insights"
]

for column, feature in zip(
    feature_columns,
    features
):

    with column:

        st.info(
            feature
        )


# ============================================================
# DATASET INTELLIGENCE
# ============================================================

if "df" in st.session_state:

    df_dashboard = (
        st.session_state.df
    )

    total_rows = len(
        df_dashboard
    )

    total_columns = len(
        df_dashboard.columns
    )

    total_missing = int(
        df_dashboard
        .isnull()
        .sum()
        .sum()
    )

    missing_percent = (

        (
            total_missing /
            (
                total_rows *
                total_columns
            )
        ) * 100

        if total_rows > 0
        and total_columns > 0

        else 0
    )

    numeric_count = len(
        df_dashboard
        .select_dtypes(
            include="number"
        ).columns
    )

    categorical_count = len(
        df_dashboard
        .select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns
    )

    readiness = (
        "Ready"
        if missing_percent < 10
        else "Review"
    )

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            "📊 Dataset Intelligence"
        )

        st.caption(
            "Live overview of the dataset currently "
            "loaded into AnalyticsLens AI."
        )

    st.write("")

    metric_columns = st.columns(
        5
    )

    with metric_columns[0]:

        st.metric(
            "🗄️ Rows",
            f"{total_rows:,}"
        )

    with metric_columns[1]:

        st.metric(
            "▦ Columns",
            f"{total_columns:,}"
        )

    with metric_columns[2]:

        st.metric(
            "🔎 Missing Values",
            f"{missing_percent:.1f}%"
        )

    with metric_columns[3]:

        st.metric(
            "📊 Data Type Mix",
            f"{numeric_count} Numeric",
            delta=f"{categorical_count} Categorical"
        )

    with metric_columns[4]:

        st.metric(
            "✓ Readiness",
            readiness
        )

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            "📋 Dataset Preview"
        )

        st.caption(
            "First 10 records from the uploaded dataset."
        )

        st.dataframe(
            df_dashboard.head(10),
            use_container_width=True,
            height=280
        )


# ============================================================
# IMAGE PREVIEW
# ============================================================

if uploaded_image is not None:

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            "🖼️ Uploaded Visualization"
        )

        st.caption(
            "Gemini Vision will analyze the visible "
            "information in this visualization."
        )

        st.image(
            uploaded_image,
            use_container_width=True
        )


# ============================================================
# CHAT SECTION
# ============================================================

st.write("")

with st.container(
    border=True
):

    st.subheader(
        "💬 Chat with AnalyticsLens AI"
    )

    st.caption(
        "Ask questions about your dataset, charts, "
        "dashboards, or visualizations."
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask something about your data or visualization..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_input:

    st.session_state.last_chart_bytes = None

    st.session_state.last_image_bytes = None

    st.session_state.last_image_mime = None

    with st.chat_message(
        "user"
    ):

        st.write(
            user_input
        )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.spinner(
        "AnalyticsLens AI is analyzing..."
    ):

        try:

            # =================================================
            # DATASET + IMAGE
            # =================================================

            if (
                uploaded_file is not None
                and uploaded_image is not None
            ):

                image_bytes = (
                    uploaded_image.getvalue()
                )

                mime_type = (
                    uploaded_image.type
                )

                st.session_state.last_image_bytes = (
                    image_bytes
                )

                st.session_state.last_image_mime = (
                    mime_type
                )

                plan = create_analysis_plan(
                    gemini_client,
                    st.session_state.dataset_context,
                    user_input
                )

                result_data = execute_analysis(
                    st.session_state.df,
                    plan
                )

                if "error" in result_data:

                    answer = result_data[
                        "error"
                    ]

                else:

                    result = result_data.get(
                        "result"
                    )

                    result_summary = (
                        summarize_result(
                            result,
                            plan
                        )
                    )

                    vision_prompt = f"""
You are AnalyticsLens AI.

The user uploaded a dataset and a visualization.

User question:

{user_input}

Dataset analysis plan:

{plan}

Python/Pandas result:

{result_summary}

Analyze the uploaded image and answer the
user's question.

Rules:

- Use the calculated dataset result as
  the numerical source of truth.
- Use the image only for visible information.
- Do not invent values.
- If an exact value cannot be read, say so.
- Distinguish calculated facts from observations.
- Keep the response concise.
"""

                    image_part = (
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        )
                    )

                    response = (
                        generate_with_retry(
                            client=gemini_client,
                            model="gemini-3.5-flash-lite",
                            contents=[
                                image_part,
                                vision_prompt
                            ]
                        )
                    )

                    answer = response.text

                    fig = create_chart(
                        result,
                        plan
                    )

                    if fig is not None:

                        st.pyplot(
                            fig
                        )

                        chart_buffer = BytesIO()

                        fig.savefig(
                            chart_buffer,
                            format="png",
                            dpi=180,
                            bbox_inches="tight"
                        )

                        chart_buffer.seek(
                            0
                        )

                        st.session_state.last_chart_bytes = (
                            chart_buffer.getvalue()
                        )


            # =================================================
            # IMAGE ONLY
            # =================================================

            elif uploaded_image is not None:

                image_bytes = (
                    uploaded_image.getvalue()
                )

                mime_type = (
                    uploaded_image.type
                )

                st.session_state.last_image_bytes = (
                    image_bytes
                )

                st.session_state.last_image_mime = (
                    mime_type
                )

                answer = analyze_image(
                    client=gemini_client,
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    question=user_input
                )


            # =================================================
            # DATASET ONLY
            # =================================================

            elif "df" in st.session_state:

                plan = create_analysis_plan(
                    gemini_client,
                    st.session_state.dataset_context,
                    user_input
                )

                result_data = execute_analysis(
                    st.session_state.df,
                    plan
                )

                if "error" in result_data:

                    answer = result_data[
                        "error"
                    ]

                else:

                    result = result_data.get(
                        "result"
                    )

                    fig = create_chart(
                        result,
                        plan
                    )

                    if fig is not None:

                        st.pyplot(
                            fig
                        )

                        chart_buffer = BytesIO()

                        fig.savefig(
                            chart_buffer,
                            format="png",
                            dpi=180,
                            bbox_inches="tight"
                        )

                        chart_buffer.seek(
                            0
                        )

                        st.session_state.last_chart_bytes = (
                            chart_buffer.getvalue()
                        )

                    result_summary = (
                        summarize_result(
                            result,
                            plan
                        )
                    )

                    explanation_prompt = f"""
You are AnalyticsLens AI.

The user asked:

{user_input}

Analysis plan:

{plan}

Python/Pandas result:

{result_summary}

Explain the result clearly.

Rules:

- Do not invent values.
- Do not perform another calculation.
- Explain only the supplied result.
- Mention the important finding.
- Keep the response concise.
"""

                    response = (
                        generate_with_retry(
                            client=gemini_client,
                            model="gemini-3.5-flash-lite",
                            contents=explanation_prompt
                        )
                    )

                    answer = response.text


            # =================================================
            # NOTHING UPLOADED
            # =================================================

            else:

                answer = (
                    "Please upload a dataset, an image, "
                    "or both before asking a question."
                )


        except Exception as error:

            error_message = str(
                error
            )

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                answer = (
                    "The AI service is temporarily busy. "
                    "Please try again in a few seconds."
                )

            elif (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                answer = (
                    "The AI service has temporarily "
                    "reached its request limit. "
                    "Please try again shortly."
                )

            else:

                answer = (
                    f"I couldn't complete the analysis: "
                    f"{error_message}"
                )


    # ========================================================
    # ASSISTANT RESPONSE
    # ========================================================

    with st.chat_message(
        "assistant"
    ):

        st.write(
            answer
        )


    # ========================================================
    # CREATE EMAIL REPORT
    # ========================================================

    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    dataset_name = (
        uploaded_file.name
        if uploaded_file is not None
        else "Not provided"
    )

    visualization_name = (
        uploaded_image.name
        if uploaded_image is not None
        else "Not provided"
    )

    report = f"""
============================================================
                    ANALYTICSLENS AI
                 DATA ANALYSIS REPORT
============================================================

Generated on:
{generated_at}

Dataset:
{dataset_name}

Visualization / Image:
{visualization_name}


------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{user_input}


------------------------------------------------------------
ANALYSIS RESULT
------------------------------------------------------------

{answer}


------------------------------------------------------------
ABOUT ANALYTICSLENS AI
------------------------------------------------------------

AnalyticsLens AI is a conversational data analytics
assistant that helps users understand datasets,
visualizations, trends, patterns, and analytical results.

This report was generated from the analysis performed
inside the AnalyticsLens AI application.


============================================================
Generated by AnalyticsLens AI
Your conversational AI data analyst
============================================================
"""

    st.session_state.last_report = report

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# ACTION CENTER
# ============================================================

st.divider()

with st.container(
    border=True
):

    st.subheader(
        "⚡ Action Center"
    )

    st.caption(
        "Continue exploring your data with AnalyticsLens AI."
    )


st.write("")

action_columns = st.columns(
    3
)

with action_columns[0]:

    with st.container(
        border=True
    ):

        st.subheader(
            "💬 Chat with Your Data"
        )

        st.caption(
            "Ask natural-language questions "
            "and get analytical explanations."
        )


with action_columns[1]:

    with st.container(
        border=True
    ):

        st.subheader(
            "✉️ Send Analysis Report"
        )

        st.caption(
            "Share your latest analysis "
            "through email."
        )


with action_columns[2]:

    with st.container(
        border=True
    ):

        st.subheader(
            "📊 Advanced Analysis"
        )

        st.caption(
            "Explore correlations, distributions, "
            "trends, and anomalies."
        )


# ============================================================
# EMAIL REPORT
# ============================================================

if st.session_state.last_report is not None:

    st.divider()

    with st.container(
        border=True
    ):

        st.subheader(
            "📧 Send Analysis Report"
        )

        st.caption(
            "Send your latest AnalyticsLens AI analysis "
            "to an email address."
        )

        recipient_email = st.text_input(
            "Recipient email",
            placeholder="example@gmail.com",
            key="recipient_email"
        )

        if st.button(
            "📧 Send Report",
            key="send_report_button"
        ):

            if recipient_email.strip() == "":

                st.warning(
                    "Please enter a recipient email."
                )

            else:

                try:

                    try:

                        send_email_report(
                            sender_email=st.secrets[
                                "GMAIL_SENDER_EMAIL"
                            ],
                            app_password=st.secrets[
                                "GMAIL_APP_PASSWORD"
                            ],
                            recipient_email=recipient_email,
                            subject=(
                                "AnalyticsLens AI Analysis Report"
                            ),
                            report=(
                                st.session_state.last_report
                            ),
                            chart_bytes=(
                                st.session_state.last_chart_bytes
                            ),
                            image_bytes=(
                                st.session_state.last_image_bytes
                            ),
                            image_mime_type=(
                                st.session_state.last_image_mime
                            )
                        )

                    except TypeError:

                        send_email_report(
                            sender_email=st.secrets[
                                "GMAIL_SENDER_EMAIL"
                            ],
                            app_password=st.secrets[
                                "GMAIL_APP_PASSWORD"
                            ],
                            recipient_email=recipient_email,
                            subject=(
                                "AnalyticsLens AI Analysis Report"
                            ),
                            report=(
                                st.session_state.last_report
                            )
                        )

                    st.success(
                        "Report sent successfully! 📧"
                    )

                except Exception as error:

                    st.error(
                        str(error)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "📊 AnalyticsLens AI • Your conversational AI data analyst • "
    "Streamlit • Pandas • Google Gemini"
)