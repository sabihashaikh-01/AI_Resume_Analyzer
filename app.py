import streamlit as st
import pymupdf
from docx import Document
import re
import os
import html

from sentence_transformers import SentenceTransformer, util
from google import genai


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS  (MIDNIGHT + MINT THEME)
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');

:root{
    --bg:#080C12; --card:#0F1620; --card2:#131C28; --line:#1F2C3D;
    --text:#E8EEF6; --muted:#8A9BB1;
    --mint:#5EEAD4; --sky:#38BDF8; --amber:#FBBF24; --coral:#FB7185;
}

html, body, .stApp, [class*="css"]{
    font-family:'Figtree', sans-serif !important;
    color:var(--text);
}
.stApp{
    background:
        radial-gradient(700px 380px at 12% -8%, rgba(94,234,212,.14), transparent 60%),
        radial-gradient(700px 380px at 92% 0%, rgba(56,189,248,.12), transparent 60%),
        var(--bg) !important;
}
header[data-testid="stHeader"]{ background:transparent !important; }
footer, #MainMenu{ visibility:hidden; }
.block-container{ max-width:1200px; padding-top:2.2rem; padding-bottom:4rem; }

p, span, label, li{ color:var(--text); }
h1,h2,h3,h4{
    font-family:'Bricolage Grotesque', sans-serif !important;
    letter-spacing:-.02em; color:#fff !important;
}

/* hero */
.hero{
    position:relative; overflow:hidden;
    background:linear-gradient(135deg, #0F1B26 0%, #0B1119 100%);
    border:1px solid var(--line); border-radius:26px;
    padding:2.6rem 2.6rem 2.3rem; margin-bottom:1.6rem;
}
.hero:after{
    content:""; position:absolute; right:-80px; top:-80px; width:300px; height:300px; border-radius:50%;
    background:radial-gradient(circle, rgba(94,234,212,.28), transparent 65%);
}
.brand{ display:flex; align-items:center; gap:.65rem; font:800 1.45rem 'Bricolage Grotesque'; color:#fff; }
.brand i{
    width:34px; height:34px; border-radius:11px 11px 11px 3px; display:inline-block;
    background:linear-gradient(135deg, var(--mint), var(--sky));
}
.hero h1{ font-size:2.9rem !important; line-height:1.06; margin:1rem 0 .6rem; max-width:720px; font-weight:800 !important; }
.hero p{ color:var(--muted); font-size:1.08rem; max-width:640px; margin:0; position:relative; z-index:1; }
.pills{ margin-top:1.3rem; position:relative; z-index:1; }
.pills span{
    display:inline-block; margin:0 .4rem .4rem 0; padding:.32rem .85rem; border-radius:999px;
    font-size:.82rem; font-weight:600; color:var(--mint);
    background:rgba(94,234,212,.08); border:1px solid rgba(94,234,212,.25);
}

/* section headings */
h2{
    font-size:1.65rem !important; font-weight:800 !important;
    padding-left:.85rem; border-left:4px solid var(--mint); margin-top:.6rem !important;
}
h3{ font-size:1.15rem !important; font-weight:700 !important; }
hr{ border:none !important; height:1px !important; background:var(--line) !important; margin:2rem 0 !important; }

/* metric cards */
[data-testid="stMetric"]{
    background:linear-gradient(180deg, var(--card2), var(--card)) !important;
    border:1px solid var(--line) !important; border-top:3px solid var(--mint) !important;
    border-radius:16px !important; padding:1.15rem 1.3rem !important;
}
[data-testid="stMetricLabel"] p{ color:var(--muted) !important; font-size:.86rem !important; }
[data-testid="stMetricValue"]{
    font-family:'Bricolage Grotesque' !important; font-weight:800 !important;
    font-size:2rem !important; color:#fff !important;
}

/* uploader + text area */
[data-testid="stFileUploader"] section, [data-testid="stFileUploaderDropzone"]{
    background:var(--card) !important; border:2px dashed #2B4A55 !important; border-radius:16px !important;
}
[data-testid="stFileUploaderDropzone"]:hover{ border-color:var(--mint) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] *{ color:var(--muted) !important; }
[data-testid="stFileUploader"] button{
    background:transparent !important; color:var(--mint) !important; border:1px solid var(--mint) !important; border-radius:10px !important;
}
textarea, [data-baseweb="textarea"], [data-baseweb="textarea"] textarea{
    background:var(--card) !important; color:var(--text) !important;
    border-radius:14px !important; font-family:'Figtree' !important;
}
[data-baseweb="textarea"]{ border:1px solid var(--line) !important; }
[data-baseweb="textarea"]:focus-within{ border-color:var(--mint) !important; box-shadow:0 0 0 3px rgba(94,234,212,.15) !important; }
textarea::placeholder{ color:#5B6B80 !important; }

/* button */
.stButton > button{
    width:100%; min-height:52px; border:none !important; border-radius:999px !important;
    background:linear-gradient(135deg, var(--mint), var(--sky)) !important;
    color:#04231F !important; font:800 1rem 'Bricolage Grotesque' !important;
    box-shadow:0 10px 30px rgba(56,189,248,.22); transition:.2s;
}
.stButton > button p{ color:#04231F !important; font-weight:800 !important; }
.stButton > button:hover{ transform:translateY(-2px); box-shadow:0 14px 36px rgba(94,234,212,.32); }

/* progress */
[data-testid="stProgress"] > div > div{ background:#16212F !important; height:10px !important; border-radius:99px !important; }
[data-testid="stProgress"] div[role="progressbar"] > div,
[data-testid="stProgress"] div[data-baseweb="progress-bar"] > div > div{
    background:linear-gradient(90deg, var(--mint), var(--sky)) !important; border-radius:99px !important;
}

/* alerts, tinted by type */
[data-testid="stAlert"]{ border-radius:14px !important; border:1px solid var(--line) !important; }
[data-testid="stAlert"] *{ color:var(--text) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]){ background:rgba(94,234,212,.09) !important; border-color:rgba(94,234,212,.3) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]){ background:rgba(251,191,36,.09) !important; border-color:rgba(251,191,36,.3) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]){ background:rgba(56,189,248,.09) !important; border-color:rgba(56,189,248,.3) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]){ background:rgba(251,113,133,.09) !important; border-color:rgba(251,113,133,.3) !important; }

/* expander, captions, misc */
[data-testid="stExpander"]{ background:var(--card) !important; border:1px solid var(--line) !important; border-radius:14px !important; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] p{ color:var(--text) !important; }
[data-testid="stCaptionContainer"], .stCaption{ color:var(--muted) !important; }
code{ background:#16212F !important; color:var(--mint) !important; }
pre{ background:var(--card) !important; border:1px solid var(--line) !important; color:var(--text) !important; }
[data-testid="stSidebar"]{ background:var(--card) !important; }
::-webkit-scrollbar{ width:8px; }
::-webkit-scrollbar-track{ background:var(--bg); }
::-webkit-scrollbar-thumb{ background:#26374B; border-radius:10px; }

@media (max-width:700px){ .hero{ padding:1.6rem; } .hero h1{ font-size:1.9rem !important; } }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="brand"><i></i>ResumeIQ</div>
    <h1>See how your resume stacks up against the job.</h1>
    <p>Upload your resume, paste a job description, and get an ATS score,
    a skill and keyword gap analysis, and AI suggestions you can act on.</p>
    <div class="pills">
        <span>ATS scoring</span><span>NLP semantic match</span>
        <span>Keyword analysis</span><span>Skill matching</span><span>Gemini AI tips</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# NLP MODEL
# ============================================================

@st.cache_resource
def load_nlp_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


nlp_model = load_nlp_model()


# ============================================================
# GEMINI AI
# ============================================================

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key:

    gemini_client = genai.Client(
        api_key=gemini_api_key
    )

else:

    gemini_client = None


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

def generate_ai_recommendations(
    resume_text,
    job_description
):

    if gemini_client is None:

        return (
            "Gemini AI recommendations are unavailable "
            "because the Gemini API key is not configured."
        )

    prompt = f"""
You are an expert ATS resume analyst and career-document reviewer.

Analyze the resume against the job description provided below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide practical recommendations for improving the resume.

Focus on:

1. Missing or weakly demonstrated skills
2. Important job requirements not clearly addressed
3. Resume summary improvements
4. Experience and project bullet improvements
5. ATS keyword alignment
6. Quantification opportunities
7. Overall content alignment

Important rules:

- Do not invent experience, skills, qualifications, achievements, or metrics.
- Only recommend changes supported by the resume.
- Keep recommendations concise and actionable.
- Do not rewrite the entire resume.

Return exactly 6 recommendations as a numbered list.
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite"
    ]

    for model in models:

        try:

            response = gemini_client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response and response.text:

                return response.text

        except Exception as e:

            error_message = str(e)

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                continue

            return (
                "Gemini AI recommendation error: "
                + error_message
            )

    return (
        "AI recommendations are temporarily unavailable. "
        "The ATS and NLP analysis is still available."
    )


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        pdf = pymupdf.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        text = ""

        for page in pdf:

            text += page.get_text()

        pdf.close()

        return text

    elif file_name.endswith(".docx"):

        document = Document(
            uploaded_file
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    return ""


# ============================================================
# INPUT SECTION
# ============================================================

st.header("1. Upload Your Resume")

st.caption(
    "Upload your resume and provide the job description you want to target."
)

col1, col2 = st.columns(2, gap="large")


with col1:

    st.subheader("📄 Resume")

    resume = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description",
        height=230,
        placeholder=(
            "Paste the complete job description here..."
        )
    )


st.write("")


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_col1, analyze_col2, analyze_col3 = st.columns(
    [1, 2, 1]
)

with analyze_col2:

    analyze_button = st.button(
        "🚀 Analyze Resume",
        type="primary"
    )


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if resume is None:

        st.error(
            "Please upload your resume first."
        )

        st.stop()

    if not job_description.strip():

        st.error(
            "Please paste the job description first."
        )

        st.stop()


    # --------------------------------------------------------
    # EXTRACT RESUME
    # --------------------------------------------------------

    resume_text = extract_resume_text(
        resume
    )


    if not resume_text.strip():

        st.error(
            "Could not extract text from the resume."
        )

        st.stop()


    st.success(
        "Resume successfully uploaded and analyzed."
    )


    # ========================================================
    # NLP SEMANTIC MATCHING
    # ========================================================

    with st.spinner(
        "Running NLP semantic analysis..."
    ):

        resume_embedding = nlp_model.encode(
            resume_text,
            convert_to_tensor=True
        )

        jd_embedding = nlp_model.encode(
            job_description,
            convert_to_tensor=True
        )

        semantic_similarity = util.cos_sim(
            resume_embedding,
            jd_embedding
        ).item()


    semantic_match_score = round(
        max(
            0,
            min(
                semantic_similarity * 100,
                100
            )
        )
    )


    # ========================================================
    # SKILL LIBRARY
    # ========================================================

    skill_library = [

        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "r",
        "statistics",
        "data analysis",
        "data visualization",
        "machine learning",
        "artificial intelligence",
        "generative ai",
        "prompt engineering",
        "natural language processing",
        "nlp",
        "human resources",
        "recruitment",
        "talent acquisition",
        "hr analytics",
        "business analytics",
        "business intelligence",
        "project management",
        "communication",
        "leadership",
        "research",
        "problem solving",
        "process improvement",
        "process management",
        "reporting",
        "documentation",
        "customer service",
        "stakeholder management",
        "microsoft office",
        "powerpoint",
        "word"
    ]


    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()


    # ========================================================
    # SKILL MATCHING
    # ========================================================

    jd_skills = [
        skill
        for skill in skill_library
        if skill in jd_lower
    ]


    matched_skills = [
        skill
        for skill in jd_skills
        if skill in resume_lower
    ]


    missing_skills = [
        skill
        for skill in jd_skills
        if skill not in resume_lower
    ]


    if jd_skills:

        skill_match_score = round(
            (
                len(matched_skills)
                /
                len(jd_skills)
            )
            * 100
        )

    else:

        skill_match_score = 0


    skill_match_score = max(
        0,
        min(
            skill_match_score,
            100
        )
    )


    # ========================================================
    # KEYWORD ANALYSIS
    # ========================================================

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "your",
        "you",
        "are",
        "will",
        "have",
        "has",
        "our",
        "their",
        "they",
        "job",
        "work",
        "role",
        "into",
        "about",
        "using",
        "must",
        "should",
        "would",
        "can"
    }


    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
        job_description.lower()
    )


    important_keywords = []

    for word in words:

        if (
            word not in stop_words
            and word not in important_keywords
        ):

            important_keywords.append(
                word
            )


    matched_keywords = [
        keyword
        for keyword in important_keywords
        if keyword in resume_lower
    ]


    if important_keywords:

        keyword_match_score = round(
            (
                len(matched_keywords)
                /
                len(important_keywords)
            )
            * 100
        )

    else:

        keyword_match_score = 0


    keyword_match_score = max(
        0,
        min(
            keyword_match_score,
            100
        )
    )


    # ========================================================
    # CONTENT ANALYSIS
    # ========================================================

    word_count = len(
        resume_text.split()
    )


    has_summary = bool(
        re.search(
            r"\b(summary|profile|objective)\b",
            resume_lower
        )
    )


    has_experience = bool(
        re.search(
            r"\b(experience|employment|work experience)\b",
            resume_lower
        )
    )


    has_education = bool(
        re.search(
            r"\beducation\b",
            resume_lower
        )
    )


    has_skills = bool(
        re.search(
            r"\bskills\b",
            resume_lower
        )
    )


    section_count = sum(
        [
            has_summary,
            has_experience,
            has_education,
            has_skills
        ]
    )


    content_score = min(
        100,
        round(
            (section_count / 4) * 70
            +
            min(word_count / 500, 1) * 30
        )
    )


    # ========================================================
    # ACHIEVEMENT DETECTION
    # ========================================================

    quantified_achievements = re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        resume_text
    )


    # ========================================================
    # ACTION VERBS
    # ========================================================

    action_verbs = [

        "analyzed",
        "developed",
        "created",
        "managed",
        "led",
        "built",
        "implemented",
        "improved",
        "optimized",
        "designed",
        "conducted",
        "coordinated",
        "organized",
        "researched",
        "evaluated",
        "supported",
        "delivered",
        "executed",
        "prepared"
    ]


    action_verb_count = sum(
        resume_lower.count(
            verb
        )
        for verb in action_verbs
    )


    # ========================================================
    # ATS SCORE
    # ========================================================

    keyword_coverage_score = (
        round(
            (
                len(matched_keywords)
                /
                len(important_keywords)
            )
            * 100
        )
        if important_keywords
        else 0
    )


    ats_score = round(

        (skill_match_score * 0.30)

        +

        (keyword_match_score * 0.20)

        +

        (semantic_match_score * 0.30)

        +

        (content_score * 0.10)

        +

        (keyword_coverage_score * 0.10)
    )


    # IMPORTANT: keep score between 0 and 100

    ats_score = max(
        0,
        min(
            ats_score,
            100
        )
    )


    # ========================================================
    # RULE-BASED RECOMMENDATIONS
    # ========================================================

    recommendations = []


    if not has_summary:

        recommendations.append(
            "Add a concise professional summary aligned with the target role."
        )


    if not has_experience:

        recommendations.append(
            "Clearly organize your professional experience section."
        )


    if not has_education:

        recommendations.append(
            "Add a clearly labeled education section."
        )


    if not has_skills:

        recommendations.append(
            "Create a dedicated skills section containing relevant job keywords."
        )


    if not quantified_achievements:

        recommendations.append(
            "Add measurable results, percentages, counts, or other quantified achievements where applicable."
        )


    if action_verb_count < 3:

        recommendations.append(
            "Strengthen experience bullets with action-oriented verbs."
        )


    if missing_skills:

        recommendations.append(
            "Review the missing skills identified below and add only those you genuinely possess."
        )


    if not recommendations:

        recommendations.append(
            "Your resume structure is well aligned. Focus on refining keyword relevance and measurable achievements."
        )


    # ========================================================
    # GEMINI ANALYSIS
    # ========================================================

    with st.spinner(
        "Generating AI recommendations..."
    ):

        ai_recommendations = (
            generate_ai_recommendations(
                resume_text,
                job_description
            )
        )


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.header("2. Resume Intelligence Dashboard")


    # ========================================================
    # MAIN SCORE
    # ========================================================

    score_col1, score_col2 = st.columns(
        [1, 2],
        gap="large"
    )


    with score_col1:

        st.metric(
            "Overall ATS Score",
            f"{ats_score}/100"
        )


    with score_col2:

        st.subheader(
            "ATS Compatibility"
        )

        st.progress(
            ats_score / 100
        )

        st.caption(
            "Combined score based on skills, keywords, semantic similarity, and resume content."
        )


    st.write("")


    # ========================================================
    # SCORE CARDS
    # ========================================================

    st.subheader(
        "Performance Overview"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🎯 Skill Match",
            f"{skill_match_score}%"
        )


    with c2:

        st.metric(
            "🔎 Keyword Match",
            f"{keyword_match_score}%"
        )


    with c3:

        st.metric(
            "🧠 Semantic Match",
            f"{semantic_match_score}%"
        )


    with c4:

        st.metric(
            "📝 Content Score",
            f"{content_score}%"
        )


    # ========================================================
    # MATCH OVERVIEW
    # ========================================================

    st.divider()

    st.header(
        "3. Match Overview"
    )


    match_col1, match_col2 = st.columns(2, gap="large")


    with match_col1:

        st.subheader(
            "Skills"
        )

        st.write(
            f"Matched: **{len(matched_skills)}**"
        )

        st.write(
            f"Missing: **{len(missing_skills)}**"
        )

        st.progress(
            skill_match_score / 100
        )


    with match_col2:

        st.subheader(
            "Keywords"
        )

        st.write(
            f"Matched: **{len(matched_keywords)}**"
        )

        st.write(
            f"Detected in JD: **{len(important_keywords)}**"
        )

        st.progress(
            keyword_match_score / 100
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.divider()

    st.header(
        "4. Skill Analysis"
    )


    skill_col1, skill_col2 = st.columns(2, gap="large")


    with skill_col1:

        st.subheader(
            "✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    skill.title()
                )

        else:

            st.info(
                "No matching skills detected."
            )


    with skill_col2:

        st.subheader(
            "⚠️ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    skill.title()
                )

        else:

            st.success(
                "No major missing skills detected."
            )


    # ========================================================
    # KEYWORDS
    # ========================================================

    st.divider()

    st.header(
        "5. Job Description Keyword Analysis"
    )


    if matched_keywords:

        st.write(
            "### Matched Keywords"
        )

        keyword_text = ", ".join(
            keyword.title()
            for keyword in matched_keywords[:50]
        )

        st.info(
            keyword_text
        )

    else:

        st.warning(
            "No major keyword matches detected."
        )


    # ========================================================
    # RESUME STRENGTHS
    # ========================================================

    st.divider()

    st.header(
        "6. Resume Strengths"
    )


    strengths = []


    if has_summary:

        strengths.append(
            "Professional summary/profile section detected."
        )


    if has_experience:

        strengths.append(
            "Professional experience section detected."
        )


    if has_education:

        strengths.append(
            "Education section detected."
        )


    if has_skills:

        strengths.append(
            "Dedicated skills section detected."
        )


    if quantified_achievements:

        strengths.append(
            f"Quantified information detected ({len(quantified_achievements)} numeric references)."
        )


    if action_verb_count >= 3:

        strengths.append(
            f"Action-oriented language detected ({action_verb_count} action verb occurrences)."
        )


    if semantic_match_score >= 60:

        strengths.append(
            "Strong semantic relationship detected between the resume and job description."
        )


    if not strengths:

        strengths.append(
            "The resume has opportunities for stronger structure and role alignment."
        )


    for strength in strengths:

        st.success(
            strength
        )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "7. 🤖 Gemini AI Recommendations"
    )


    st.info(
        ai_recommendations
    )


    # ========================================================
    # RULE BASED RECOMMENDATIONS
    # ========================================================

    st.header(
        "8. Resume Improvement Recommendations"
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.warning(
            f"**{index}.** {recommendation}"
        )


    # ========================================================
    # RESUME QUALITY
    # ========================================================

    st.divider()

    st.header(
        "9. Resume Quality Analysis"
    )


    q1, q2, q3, q4 = st.columns(4)


    with q1:

        st.metric(
            "Word Count",
            word_count
        )


    with q2:

        st.metric(
            "Sections Detected",
            f"{section_count}/4"
        )


    with q3:

        st.metric(
            "Numbers Detected",
            len(quantified_achievements)
        )


    with q4:

        st.metric(
            "Action Verbs",
            action_verb_count
        )


    # ========================================================
    # RESUME STRUCTURE
    # ========================================================

    st.divider()

    st.header(
        "10. Resume Structure"
    )


    structure = {
        "Professional Summary": has_summary,
        "Experience": has_experience,
        "Education": has_education,
        "Skills": has_skills
    }


    for section, present in structure.items():

        if present:

            st.success(
                f"✓ {section}"
            )

        else:

            st.error(
                f"✗ {section}"
            )


    # ========================================================
    # NLP ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "11. NLP Semantic Analysis"
    )


    st.metric(
        "Semantic Similarity",
        f"{semantic_similarity:.3f}"
    )


    st.progress(
        semantic_match_score / 100
    )


    st.caption(
        "Sentence Transformer: all-MiniLM-L6-v2"
    )


    # ========================================================
    # EXTRACTED CONTENT
    # ========================================================

    st.divider()

    st.header(
        "12. Extracted Resume Content"
    )


    with st.expander(
        "View extracted resume text"
    ):

        st.text(
            resume_text
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built By SABIHA"
)

st.caption(
    "Python • Streamlit • NLP • Sentence Transformers • Gemini AI"
)