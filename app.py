import streamlit as st
from openai import OpenAI

# 🔐 API key
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 🧠 Session state
if "outputs" not in st.session_state:
    st.session_state["outputs"] = {}

if "history" not in st.session_state:
    st.session_state["history"] = []

# 🎨 Page
st.set_page_config(page_title="AI Content Generator", layout="wide")

st.title("🚀 AI-Powered Multi-Platform Content Generator")
st.write("Generate Instagram, LinkedIn, Twitter & Blog content instantly")

# 🌙 Dark Mode Toggle
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }

        .stTextInput input, .stTextArea textarea {
            background-color: #262730;
            color: white;
        }

        .stButton button {
            background-color: #262730;
            color: white;
            border-radius: 8px;
        }

        .stDownloadButton button {
            background-color: #262730;
            color: white;
        }

        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ✅ CLEAR FLAG LOGIC (ADD HERE)
if "clear_flag" not in st.session_state:
    st.session_state.clear_flag = False

if st.session_state.clear_flag:
    st.session_state["topic"] = ""
    st.session_state["audience"] = ""
    st.session_state["outputs"] = {}
    st.session_state.clear_flag = False

# 📥 Inputs
topic = st.text_input("Enter Topic", key="topic", autocomplete="off")
audience = st.text_input("Target Audience", key="audience", autocomplete="off")
tone = st.selectbox(
    "Select Tone",
    ["Professional", "Casual", "Motivational", "Funny"]
)

st.session_state["tone"] = tone

# 🔘 Buttons (Generate LEFT, Clear RIGHT)
col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])

with col_btn1:
    generate = st.button("⚡ Generate", use_container_width=True)

with col_btn3:
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state.clear_flag = True
        st.rerun()

st.divider()

# ⚠️ Warning
if generate and (not topic or not audience):
    st.warning("⚠️ Please enter topic and target audience")

# 🤖 Generate Content
elif generate and topic and audience:

    with st.spinner("Generating AI content..."):

        tone = st.session_state["tone"]

        platforms = {
             "Instagram": f"Write a {tone.lower()} Instagram caption about {topic} for {audience}. Max 2-3 lines with emojis and hashtags.",
             "LinkedIn": f"Write a {tone.lower()} LinkedIn post about {topic} for {audience} in 10-12 lines.",
             "Twitter": f"Write a {tone.lower()} tweet about {topic} for {audience} under 25-30 words.",
             "Blog": f"Write a {tone.lower()} blog paragraph about {topic} for {audience} in 12-15 lines."
        }

        outputs = {}

        for platform, prompt in platforms.items():
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                outputs[platform] = response.choices[0].message.content
            except Exception as e:
                outputs[platform] = f"Error: {e}"

        st.session_state["outputs"] = outputs

        # 📜 Save history
        st.session_state["history"].append({
            "topic": topic,
            "audience": audience,
            "outputs": outputs
        })

    st.success("✅ Content generated successfully!")

# 📋 COPY BUTTON FUNCTION (FIXED)

def copy_box(label, text, key, height=200):
    st.markdown(f"## {label}")
    
    st.text_area(
        label=f"{label} Content",
        value=text,
        height=height,
        key=key
    )

def evaluate_content(text, platform):
    prompt = f"""
    Evaluate the following {platform} content.

    Give:
    1. Engagement score out of 10
    2. Readability (Short/Medium/Long)
    3. 2 improvement suggestions

    Content:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# 📊 DISPLAY
outputs = st.session_state.get("outputs", {})

if outputs:

    # 📥 Download button
    all_content = ""
    for k, v in outputs.items():
        all_content += f"{k}:\n{v}\n\n"

    st.download_button(
        "📥 Download All Content",
        data=all_content,
        file_name="ai_content.txt"
    )

    st.divider()

    # 🔥 Tabs UI
tab1, tab2, tab3, tab4 = st.tabs(["📱 Instagram", "💼 LinkedIn", "🐦 Twitter", "📝 Blog"])

# ---------- INSTAGRAM ----------
with tab1:
    content = outputs.get("Instagram", "")
    st.text_area("Instagram Content", content, height=200, key="insta_tab")

    st.markdown("### 📊 Evaluation")
    st.info(evaluate_content(content, "Instagram"))

    if st.button("✨ Improve Instagram", key="improve_insta"):
        improved = improve_content(content, "Instagram")
        st.text_area("Improved Instagram", improved, height=200)

# ---------- LINKEDIN ----------
with tab2:
    content = outputs.get("LinkedIn", "")
    st.text_area("LinkedIn Content", content, height=400, key="linkedin_tab")

    st.markdown("### 📊 Evaluation")
    st.info(evaluate_content(content, "LinkedIn"))

    if st.button("✨ Improve LinkedIn", key="improve_linkedin"):
        improved = improve_content(content, "LinkedIn")
        st.text_area("Improved LinkedIn", improved, height=400)

# ---------- TWITTER ----------
with tab3:
    content = outputs.get("Twitter", "")
    st.text_area("Twitter Content", content, height=200, key="twitter_tab")

    st.markdown("### 📊 Evaluation")
    st.info(evaluate_content(content, "Twitter"))

    if st.button("✨ Improve Twitter", key="improve_twitter"):
        improved = improve_content(content, "Twitter")
        st.text_area("Improved Twitter", improved, height=200)

# ---------- BLOG ----------
with tab4:
    content = outputs.get("Blog", "")
    st.text_area("Blog Content", content, height=500, key="blog_tab")

    st.markdown("### 📊 Evaluation")
    st.info(evaluate_content(content, "Blog"))

    if st.button("✨ Improve Blog", key="improve_blog"):
        improved = improve_content(content, "Blog")
        st.text_area("Improved Blog", improved, height=500)

      # 📊 Evaluation
    def evaluate_content(text, platform):
        prompt = f"""
        Evaluate the following {platform} content.

        Give:
        1. Engagement score out of 10
        2. Readability (Short/Medium/Long)
        3. 2 improvement suggestions

        Content:
        {text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    
    def improve_content(text, platform):
        prompt = f"""
        Improve the following {platform} content based on best practices.
        Make it more engaging, clear, and impactful.

        Content:
        {text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

# 📜 HISTORY SECTION (WITH TOGGLE)
show_history = st.toggle("📜 Show History")

if show_history and st.session_state["history"]:
    st.divider()
    st.markdown("## 🕘 History")

    for item in reversed(st.session_state["history"]):
        with st.expander(f"{item['topic']} → {item['audience']}"):
            for k, v in item["outputs"].items():
                st.markdown(f"**{k}**")
                st.write(v)
