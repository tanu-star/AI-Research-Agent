import streamlit as st
import requests
import json
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
    .stButton>button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 AI Research Assistant")
st.markdown("### Intelligent Research & Summarization System")

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.header("🔑 Login / Register")

    tab = st.tabs(["Login", "Register"])

    # -------------------------
    # LOGIN
    # -------------------------
    with tab[0]:
        login_username = st.text_input(
            "Username",
            key="login_user"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            if login_username and login_password:

                try:
                    response = requests.post(
                        "http://localhost:8000/token",
                        data={
                            "username": login_username,
                            "password": login_password
                        }
                    )

                    if response.status_code == 200:

                        st.session_state["token"] = response.json()["access_token"]
                        st.session_state["username"] = login_username

                        st.success("Logged in!")

                    else:
                        st.error("Invalid credentials")

                except Exception:
                    st.error("Start API first!")

    # -------------------------
    # REGISTER
    # -------------------------
    with tab[1]:

        reg_username = st.text_input(
            "Username",
            key="reg_user"
        )

        reg_email = st.text_input(
            "Email",
            key="reg_email"
        )

        reg_password = st.text_input(
            "Password",
            type="password",
            key="reg_pass"
        )

        if st.button("Register"):

            try:
                response = requests.post(
                    "http://localhost:8000/register",
                    json={
                        "username": reg_username,
                        "email": reg_email,
                        "password": reg_password
                    }
                )

                if response.status_code == 200:
                    st.success("Registered! Please login.")
                else:
                    st.error("Username already exists")

            except Exception:
                st.error("Start API first!")

    # =========================
    # HISTORY
    # =========================
    if "token" in st.session_state:

        st.markdown("---")
        st.subheader("📜 Research History")

        if st.button("View History"):

            try:

                headers = {
                    "Authorization": f"Bearer {st.session_state['token']}"
                }

                response = requests.get(
                    "http://localhost:8000/research/history",
                    headers=headers
                )

                if response.status_code == 200:

                    history = response.json()

                    if history:

                        for item in history:

                            st.write(f"🔍 {item['query']}")
                            st.caption(item["created_at"])
                            st.markdown("---")

                    else:
                        st.info("No history found.")

                else:
                    st.error("Could not load history.")

            except Exception as e:
                st.error(str(e))

# =========================
# MAIN INTERFACE
# =========================

query = st.text_input(
    "📝 Enter research topic:",
    placeholder="e.g., Latest AI developments"
)

num_sources = st.slider(
    "📊 Sources",
    3,
    10,
    5
)

if st.button("🚀 Run Research", use_container_width=True):

    if "token" not in st.session_state:

        st.error("⚠️ Please login first!")

    elif not query:

        st.error("⚠️ Please enter a topic!")

    else:

        with st.spinner(
            "🔍 Searching, extracting, and AI processing..."
        ):

            try:

                headers = {
                    "Authorization": f"Bearer {st.session_state['token']}"
                }

                response = requests.post(
                    "http://localhost:8000/research/",
                    json={
                        "query": query,
                        "num_sources": num_sources
                    },
                    headers=headers
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"✅ Found {data['count']} sources!"
                    )

                    for i, item in enumerate(data["results"], 1):

                        with st.expander(
                            f"📄 {i}. {item['title']}"
                        ):

                            st.markdown(
                                f"**🔗 Link:** [{item['link']}]({item['link']})"
                            )

                            st.markdown(
                                f"**📅 Date:** {item.get('date', 'Unknown')}"
                            )

                            st.markdown(
                                f"**🏷️ Topic:** {item.get('topic')} ({item.get('topic_confidence')})"
                            )

                            st.markdown(
                                f"**💭 Sentiment:** {item.get('sentiment')} ({item.get('sentiment_confidence')})"
                            )

                            st.markdown("---")
                            st.markdown("**📝 Summary:**")

                            st.write(item["summary"])

                else:
                    st.error(
                        f"Error: {response.status_code}"
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")