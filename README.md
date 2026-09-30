# ResumeIQ — AI Resume Analyzer

> **Analyze your resume. Match it with a job description. Get actionable insights.**

ResumeIQ is an AI-powered resume analysis application built with **Python, Streamlit, NLP, Sentence Transformers, and Gemini AI**.

It analyzes how well a resume matches a specific job description and provides insights into **ATS compatibility, skills, keywords, semantic similarity, resume quality, and improvement areas**.

---

## ✨ Features

* 📄 **Resume Upload** — Supports PDF and DOCX files
* 🎯 **ATS Compatibility Score** — Calculates an overall resume-job match score
* 🧠 **Semantic Matching** — Uses NLP embeddings to measure contextual similarity
* 🛠️ **Skill Analysis** — Identifies matched and missing skills
* 🔑 **Keyword Analysis** — Extracts important keywords from the job description
* 📊 **Resume Quality Analysis** — Checks structure, word count, achievements, and action verbs
* 🤖 **Gemini AI Recommendations** — Generates personalized resume improvement suggestions
* 📋 **Rule-Based Recommendations** — Provides additional recommendations using resume analysis rules
* 📑 **Extracted Content Viewer** — Allows users to review the text extracted from their resume

---

## 🔍 How ResumeIQ Works

```text
Resume + Job Description
          ↓
   Text Extraction
          ↓
   Resume Analysis
          ↓
 ┌─────────────────────┐
 │ Skill Matching      │
 │ Keyword Matching    │
 │ Semantic Matching   │
 │ Resume Structure   │
 │ Content Quality     │
 └─────────────────────┘
          ↓
      ATS Score
          ↓
 AI + Rule-Based Recommendations
```

---

## 📊 ATS Score

ResumeIQ calculates the ATS score using multiple components:

| Component        | Weight |
| ---------------- | -----: |
| Skill Match      |    30% |
| Keyword Match    |    20% |
| Semantic Match   |    30% |
| Content Score    |    10% |
| Keyword Coverage |    10% |

The final score provides an overall indication of how closely the resume aligns with the provided job description.

> **Note:** The score is an analytical estimate and should not be considered an actual score from a specific company's ATS.

---

## 🛠️ Skill Analysis

ResumeIQ compares skills detected in the resume with skills identified from the job description.

### Provides:

* Matched skills
* Missing skills
* Skill match percentage
* Job-relevant skill coverage

This helps identify important areas that may need stronger representation in the resume.

---

## 🔑 Keyword Analysis

The application extracts relevant keywords from the job description and checks their presence in the resume.

### Analyzes:

* Important job-specific terms
* Keyword matches
* Missing keywords
* Keyword coverage

This helps improve the visibility of relevant resume content during automated screening.

---

## 🧠 NLP Semantic Analysis

ResumeIQ uses **Sentence Transformers** to understand the contextual similarity between the resume and job description.

The application uses:

```text
all-MiniLM-L6-v2
```

Cosine similarity is used to calculate the semantic relationship between the resume content and the job description.

This goes beyond simple keyword matching by evaluating **contextual meaning**.

---

## 📋 Resume Quality Analysis

ResumeIQ evaluates several aspects of the resume content, including:

* Resume word count
* Professional summary/profile/objective
* Work experience
* Education
* Skills section
* Quantified achievements
* Action verbs
* Resume structure

These checks provide a broader view of resume completeness and content quality.

---

## 🤖 AI-Powered Recommendations

ResumeIQ integrates **Google Gemini** to generate personalized recommendations based on the resume and job description.

The AI recommendations focus on areas such as:

* Missing skills
* Relevant keywords
* Resume positioning
* Content improvements
* Job-description alignment
* Areas requiring stronger evidence

The system is instructed **not to invent experience, skills, qualifications, achievements, or metrics** that are not supported by the resume.

---

## 🧩 Technology Stack

| Technology                                                         | Purpose                       |
| ------------------------------------------------------------------ | ----------------------------- |
| Python                                                             | Core application logic        |
| Streamlit                                                          | Web application interface     |
| PyMuPDF                                                            | PDF text extraction           |
| python-docx                                                        | DOCX text extraction          |
| Sentence Transformers                                              | NLP semantic analysis         |
| Scikit-style cosine similarity via Sentence Transformers utilities | Similarity calculation        |
| Google Gemini API                                                  | AI-powered recommendations    |
| Regular Expressions                                                | Keyword and content detection |

---

## 📁 Project Structure

```text
ResumeIQ/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Gemini API Configuration

ResumeIQ can use the Gemini API for AI-powered recommendations.

Create an environment variable named:

```text
GEMINI_API_KEY
```

Do **not** upload your API key directly to GitHub.

For local development, configure your API key through your environment or secure secrets configuration.

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📄 Supported Resume Formats

ResumeIQ currently supports:

* PDF
* DOCX

The application extracts the resume text and analyzes it against the provided job description.

---

## ⚙️ Analysis Modules

ResumeIQ contains the following major analysis modules:

```text
Resume Upload
     │
     ├── Text Extraction
     │
     ├── Skill Analysis
     │
     ├── Keyword Analysis
     │
     ├── Semantic Analysis
     │
     ├── Content Analysis
     │
     ├── ATS Score
     │
     └── AI Recommendations
```

---

## 🔒 Privacy & Security

ResumeIQ processes the uploaded resume within the application workflow.

**Important:** Do not upload sensitive personal information unnecessarily, and never commit API keys, passwords, or other secrets to the GitHub repository.

---

## 🚧 Current Limitations

* ATS scoring is an analytical estimate rather than an actual company's ATS score.
* Skill detection is based on the application's predefined skill library and extracted job-description terms.
* Keyword analysis depends on the text successfully extracted from the uploaded document.
* AI recommendations require a valid Gemini API key.
* Results may vary depending on the quality and structure of the resume and job description.

---

## 🔮 Future Enhancements

Potential future improvements include:

* 📈 Interactive score visualizations
* 📄 Resume improvement tracking
* 🎯 Job-specific resume optimization
* 🔎 More advanced skill extraction
* 📚 Expanded industry-specific skill libraries
* 💼 Multiple job-description comparison
* 📊 Resume analytics dashboard
* ☁️ Cloud deployment

---

## 👩‍💻 Author

**SABIHA**

---

## ⭐ Project

If you find ResumeIQ useful, consider giving the repository a **star ⭐** on GitHub.
