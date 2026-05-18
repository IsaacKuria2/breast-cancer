import streamlit as st
import pandas as pd
from utils.comments import load_comments, delete_comment, save_reply

st.set_page_config(page_title="Admin", page_icon="🔐", layout="wide")
st.title("🔐 Admin Panel")

password = st.text_input("Enter admin password", type="password")

if password != st.secrets["ADMIN_PASSWORD"]:
    st.warning("Enter the correct password to access this panel.")
    st.stop()

st.success("✅ Access granted!")
comments = load_comments()

if not comments:
    st.info("No comments yet.")
    st.stop()

df = pd.DataFrame(comments)

# --- Export ---
st.subheader("📥 Export Comments")
csv = df.to_csv(index=False)
st.download_button("Download as CSV", csv, "comments.csv", "text/csv")

st.markdown("---")

# --- View, Reply, Delete ---
st.subheader("🗨️ All Comments")
for i, c in enumerate(comments):
    with st.expander(f"#{c['id']} — {c['name']} ({c['timestamp']})"):
        st.markdown(f"**Email:** {c['email']}")
        st.markdown(f"**Comment:** {c['comment']}")
        if c.get("reply"):
            st.markdown(f"**Your reply:** {c['reply']}")

        reply_text = st.text_input(f"Reply to {c['name']}", key=f"reply_{i}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send Reply", key=f"send_{i}"):
                save_reply(i, reply_text)
                st.success("Reply saved!")
                st.rerun()
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{i}"):
                delete_comment(i)
                st.success("Comment deleted!")
                st.rerun()