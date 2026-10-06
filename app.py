import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="AgriScan",
    page_icon="🌱",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background: #dff3df;
}

.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #1b5e20;
    margin-top: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #424242;
    margin-bottom: 25px;
}

.info-box {
    background-color: #fff9c4;
    color: #222222;
    padding: 18px;
    border-radius: 15px;
    border-left: 6px solid #f9a825;
    margin-bottom: 25px;
}

.section-title {
    color: #1b5e20;
    font-size: 25px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
}

.stSelectbox label,
.stFileUploader label {
    color: #1b5e20 !important;
    font-weight: bold !important;
}

.stFileUploader {
    color: #1b5e20 !important;
}

.stSpinner > div {
    color: #1b5e20 !important;
}

.result-box {
    background-color: white;
    color: black !important;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #66bb6a;
    margin-top: 10px;
    font-size: 16px;
    line-height: 1.6;
}

.result-box * {
    color: black !important;
}

.stButton > button {
    width: 100%;
    background-color: #f9a825;
    color: #1b1b1b;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 10px;
}

.stButton > button:hover {
    background-color: #2e7d32;
    color: white;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">🌱 AgriScan</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Based Plant Disease Detection System</div>',
    unsafe_allow_html=True
)


st.markdown("""
<div class="info-box">
🌾 <b>Help your plants stay healthy!</b><br>
Upload a clear image of a plant leaf and AgriScan will analyze it using AI.
</div>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">🌐 Select Language</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "Choose the language for the result:",
    [
        "English",
        "తెలుగు",
        "हिंदी"
    ]
)


if language == "English":

    language_instruction = """
Give the complete answer in simple English.
"""

elif language == "తెలుగు":

    language_instruction = """
Give the complete answer in simple Telugu.
Use Telugu script.
Keep the explanation easy for a farmer to understand.
"""

else:

    language_instruction = """
Give the complete answer in simple Hindi.
Use Hindi Devanagari script.
Keep the explanation easy for a farmer to understand.
"""


st.markdown(
    '<div class="section-title">📸 Upload Plant Leaf</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png"],
    key="leaf_upload"
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="🌿 Uploaded Plant Leaf",
        use_container_width=True
    )

    st.write("")

    if st.button("🔍 Detect Plant Disease"):

        image_data = uploaded_file.getvalue()

        image_base64 = base64.b64encode(
            image_data
        ).decode("utf-8")

        data = {

            "model": "gemma3:4b",

            "prompt": f"""
Analyze this plant leaf image.

{language_instruction}

Give a short and simple answer with:

1. Plant name
2. Healthy or Diseased
3. Possible disease
4. Visible symptoms
5. Basic treatment
6. Prevention tips

Do not use complicated technical words.
Make the information useful for a farmer.
""",

            "images": [image_base64],

            "stream": False
        }

        with st.spinner(
            "🌱 AI is analyzing the leaf... Please wait"
        ):

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=data
            )

            result = response.json()

        st.success("✅ Analysis Completed!")

        st.markdown(
            '<div class="section-title">🌿 Detection Result</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-box">
                {result["response"]}
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("""
<div style="
    text-align:center;
    color:#424242;
    padding:25px;
    font-size:15px;
">
🌾 <b>AgriScan</b> — Smart Farming with AI 🌱
</div>
""", unsafe_allow_html=True)
