import streamlit as st
from auth.session_manager import SessionManager
from components.auth_pages import show_login_page
from components.sidebar import show_sidebar
from components.analysis_form import show_analysis_form
from services.ai_service import get_chat_response

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Health Copilot",
    page_icon="🧠",
    layout="wide"
)

# ---------- GLOBAL STYLES (SIDEBAR + MAIN DIFFERENTIATION) ----------
st.markdown(
    """
    <style>

    /* MAIN CONTENT AREA */
    .main {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* SIDEBAR BACKGROUND */
    section[data-testid="stSidebar"] {
        background: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* SIDEBAR SHADOW */
    div[data-testid="stSidebar"] {
        box-shadow: 4px 0 12px rgba(0,0,0,0.25);
    }

    /* MAIN CONTENT SPACING */
    .block-container {
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
def show_header():
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("### 🧠 AI Health Copilot")
    with col2:
        st.markdown(
            "<div style='text-align:right;color:#9aa0a6'>v1.0</div>",
            unsafe_allow_html=True
        )

# ---------- HERO ----------
def show_hero():
    st.markdown(
        """
        <div style="
            text-align:center;
            padding:70px 20px;
            max-width:900px;
            margin:auto;
        ">
            <h1 style="font-size:3rem;margin-bottom:10px;">
                Your AI Health Insights Platform
            </h1>
            <p style="font-size:1.3rem;color:#9aa0a6;margin-bottom:30px;">
                Upload medical reports and get instant, intelligent analysis
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- FEATURES ----------
def show_features():
    st.markdown("### 🚀 Why use AI Health Copilot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📊 Smart Analysis**  \nAI extracts insights from reports instantly")

    with col2:
        st.markdown("**💬 Conversational AI**  \nAsk follow-up questions naturally")

    with col3:
        st.markdown("**🔒 Secure Sessions**  \nYour data stays private and safe")

# ---------- START BUTTON ----------
def show_start_button():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("✨ Start New Analysis", use_container_width=True, type="primary"):
            success, session = SessionManager.create_chat_session()
            if success:
                st.session_state.current_session = session
                st.rerun()

# ---------- GREETING ----------
def show_user_greeting():
    if st.session_state.user:
        name = st.session_state.user.get("name") or st.session_state.user.get("email", "")
        st.markdown(
            f"""
            <div style="
                background:rgba(79,70,229,0.1);
                padding:10px 15px;
                border-radius:10px;
                text-align:right;
                margin-bottom:15px;
            ">
                👋 Welcome back, <b>{name}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- CHAT HISTORY ----------
def show_chat_history():
    success, messages = st.session_state.auth_service.get_session_messages(
        st.session_state.current_session["id"]
    )

    if success:
        for msg in messages:
            if msg.get("role") == "system":
                continue
            if msg["role"] == "user":
                st.info(msg["content"])
            else:
                st.success(msg["content"])
        return messages
    return []

# ---------- CHAT INPUT ----------
def handle_chat_input(messages):
    if prompt := st.chat_input("Ask a follow-up question..."):
        st.info(prompt)

        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"], prompt, role="user"
        )

        context_text = st.session_state.get("current_report_text", "")

        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, context_text, messages)
            st.success(response)

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], response, role="assistant"
            )
            st.rerun()

# ---------- MAIN ----------
def main():
    SessionManager.init_session()

    if not SessionManager.is_authenticated():
        show_login_page()
        return

    show_header()
    show_user_greeting()
    show_sidebar()

    if st.session_state.get("current_session"):
        st.markdown(f"## 📊 {st.session_state.current_session['title']}")
        messages = show_chat_history()

        if messages:
            handle_chat_input(messages)
        else:
            show_analysis_form()
    else:
        show_hero()
        show_features()
        show_start_button()

if __name__ == "__main__":
    main()
