# 📊 AnalyticsLens AI

### Your conversational AI data analyst

AnalyticsLens AI is an interactive Streamlit application that helps users understand datasets, charts, dashboards, trends, patterns, and analytical results using natural-language questions.

The application combines **Pandas-based numerical analysis** with **Google Gemini** for planning, explanation, and visual analysis.

---

## ✨ Features

### 📊 Dataset Analysis
Upload CSV or Excel files and ask questions in natural language.

AnalyticsLens AI can perform:

- Dataset profiling
- Row and column counts
- Missing-value analysis
- Duplicate detection
- Aggregations
- Group-by analysis
- Filtering
- Sorting
- Top-N and Bottom-N analysis
- Correlation analysis
- IQR-based outlier detection
- Trend analysis
- Distribution analysis
- Numeric-variable comparison

### 📈 Automatic Visualizations

Depending on the question, AnalyticsLens AI can generate:

- Bar charts
- Line charts
- Histograms
- Scatter plots

### 🖼️ Vision Analysis

Upload:

- Graphs
- Charts
- Dashboards
- Tables
- Other data visualizations

Google Gemini Vision analyzes the visible information and explains the patterns without inventing unreadable values.

### 🤖 Natural-Language Analytics

Examples:

```text
What is the average sales?

Which category has the highest sales?

Are there any missing values?

Show the sales trend.

What are the top 5 categories by sales?

Are there any outliers?

What is the relationship between sales and profit?

Explain this chart.
```

### 📧 Email Reports

After an analysis, users can send the generated report to an email address.

The project uses Gmail SMTP with SSL on port 465.

---

## 🏗️ Architecture

```text
                    AnalyticsLens AI
                           │
                           ▼
                  Streamlit Interface
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        CSV / Excel                  Image Upload
             │                           │
             ▼                           ▼
      Dataset Context              Gemini Vision
             │                           │
             ▼                           │
       Gemini Planner                    │
             │                           │
             ▼                           │
      Structured JSON Plan               │
             │                           │
             ▼                           │
       Pandas Executor                  │
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    Analysis Result
                           │
                           ▼
                    Gemini Explanation
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
              Chart              Email Report
```

---

## 📁 Project Structure

```text
AnalyticsLens/
│
├── app.py
├── prompts.py
├── analytics.py
├── analysis_planner.py
├── analytics_executor.py
├── chart_generator.py
├── gemini_helper.py
├── result_summarizer.py
├── vision_analyzer.py
├── email_report.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml.example
```

---

## 🧠 How the Analysis Works

AnalyticsLens AI separates **planning** from **numerical calculation**.

### 1. User asks a question

Example:

```text
What is the average sales?
```

### 2. Gemini creates an analysis plan

Example:

```json
{
    "operation": "aggregate",
    "value_column": "Sales",
    "aggregation": "mean",
    "visualization": "none"
}
```

### 3. Pandas performs the calculation

The numerical result is calculated directly from the uploaded dataset.

### 4. Gemini explains the result

Gemini receives the calculated result and generates a clear natural-language explanation.

This design helps keep numerical calculations grounded in the actual dataset.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- OpenPyXL
- Google Gemini API
- Gmail SMTP

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AnalyticsLens
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure secrets

Create:

```text
.streamlit/secrets.toml
```

Use:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GMAIL_SENDER_EMAIL = "yourgmail@gmail.com"
GMAIL_APP_PASSWORD = "your_16_character_app_password"
```

Never commit `secrets.toml` to GitHub.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

---

## 🔐 Security

API keys, Gmail credentials, and other secrets must not be committed to GitHub.

The local secret file is excluded using `.gitignore`.

For Streamlit Community Cloud, secrets should be entered through the application's Secrets configuration rather than stored in the repository.

---

## 📧 Gmail Configuration

The email-report feature uses:

```text
SMTP server: smtp.gmail.com
Port: 465
Security: SSL
```

A Gmail **App Password** is required rather than the normal Gmail account password.

---

## 🚀 Deployment

AnalyticsLens AI can be deployed using Streamlit Community Cloud.

Basic deployment flow:

```text
Local Project
     ↓
GitHub Repository
     ↓
Streamlit Community Cloud
     ↓
Configure Secrets
     ↓
Deploy
     ↓
Public Streamlit App
```

After deployment, changes pushed to the connected GitHub repository can be reflected in the Streamlit application.

---

## 🎯 Example Use Cases

AnalyticsLens AI can be used for:

- Business datasets
- Sales analysis
- Customer analysis
- Financial datasets
- Experimental data
- Engineering datasets
- Academic projects
- Exploratory data analysis
- Chart interpretation
- Data-quality inspection

---

## 🔮 Future Improvements

Potential future extensions include:

- Monthly and yearly time-series aggregation
- More statistical tests
- Interactive Plotly visualizations
- Downloadable PDF reports
- Multi-file analysis
- Automated insight generation
- More visualization types
- Database connections
- Advanced anomaly detection
- Dashboard-style KPI monitoring

---

## 👨‍💻 Project

**AnalyticsLens AI**

Your conversational AI data analyst.

Built with:

**Streamlit + Pandas + Google Gemini**
