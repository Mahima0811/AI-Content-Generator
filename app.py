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

# 📊 DISPLAY
outputs = st.session_state.get("outputs", {})

if outputs:

    # 📥 Download button (TOP)
    all_content = ""
    for k, v in outputs.items():
        all_content += f"{k}:\n{v}\n\n"

    st.download_button(
        "📥 Download All Content",
        data=all_content,
        file_name="ai_content.txt"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
         copy_box("📱 Instagram", outputs.get("Instagram", ""), "copy_insta", 200)

         st.markdown("---")

         copy_box("📝 Blog", outputs.get("Blog", ""), "copy_blog", 500)

    with col2:
         copy_box("💼 LinkedIn", outputs.get("LinkedIn", ""), "copy_linkedin", 500)

         st.markdown("---")

         copy_box("🐦 Twitter", outputs.get("Twitter", ""), "copy_twitter", 200)

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
