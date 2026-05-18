import streamlit as st
import pandas as pd
from utils.comments import load_comments, delete_comment, save_reply

st.set_page_config(page_title="Admin Panel", page_icon="🔐", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.admin-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.admin-header h1 {
    font-size: 3rem;
    background: linear-gradient(90deg, #e94560, #0f3460);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.comment-card {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #e94560;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class='admin-header'>
    <h1>🔐 Admin Command Center</h1>
    <p style='color: #aaa;'>Manage comments and monitor engagement</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Auth ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    password = st.text_input("🔑 Enter Admin Password", type="password", placeholder="Password")
    login_btn = st.button("Unlock Panel", use_container_width=True)

if not password or password != st.secrets["ADMIN_PASSWORD"]:
    st.markdown("""
    <div style='text-align:center; padding: 3rem; color: #aaa;'>
        🔒 Enter the correct password to access the admin panel.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.success("✅ Access Granted! Welcome back, Admin.")
st.markdown("---")

# --- Load comments ---
comments = load_comments()

# --- Stats Row ---
total = len(comments)
replied = sum(1 for c in comments if c.get("reply"))
unreplied = total - replied

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='stat-card'>
        <h2 style='color:#2ecc71'>💬 {total}</h2>
        <p>Total Comments</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='stat-card'>
        <h2 style='color:#3498db'>↩️ {replied}</h2>
        <p>Replied</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='stat-card'>
        <h2 style='color:#e74c3c'>⏳ {unreplied}</h2>
        <p>Awaiting Reply</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

if not comments:
    st.info("💬 No comments yet. Check back later!")
    st.stop()

# --- Export ---
df = pd.DataFrame(comments)
st.subheader("📥 Export Comments")
col1, col2 = st.columns([3, 1])
with col1:
    st.caption(f"{total} comments ready to export")
with col2:
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", csv, "comments.csv", "text/csv", use_container_width=True)

st.markdown("---")

# --- Filter ---
st.subheader("🗨️ All Comments")
filter_option = st.radio("Filter by", ["All", "Replied", "Unreplied"], horizontal=True)

filtered = comments
if filter_option == "Replied":
    filtered = [c for c in comments if c.get("reply")]
elif filter_option == "Unreplied":
    filtered = [c for c in comments if not c.get("reply")]

st.caption(f"Showing {len(filtered)} comment(s)")
st.markdown("---")

# --- Comments ---
for i, c in enumerate(reversed(filtered)):
    real_index = comments.index(c)
    status = "✅ Replied" if c.get("reply") else "⏳ Pending"
    status_color = "#2ecc71" if c.get("reply") else "#e74c3c"

    with st.expander(f"#{c['id']} — {c['name']} · {c['timestamp']} · {status}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📧 Email:** {c['email']}")
            st.markdown(f"**💬 Comment:** {c['comment']}")
        with col2:
            st.markdown(f"<span style='color:{status_color}; font-weight:bold'>{status}</span>",
                        unsafe_allow_html=True)

        if c.get("reply"):
            st.info(f"↩️ **Your reply:** {c['reply']}")

        st.markdown("**Reply:**")
        reply_text = st.text_area(f"Write reply", key=f"reply_{real_index}",
                                  placeholder="Type your reply here...", height=80)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📨 Send Reply", key=f"send_{real_index}", use_container_width=True):
                if reply_text.strip():
                    save_reply(real_index, reply_text)
                    st.success("Reply saved!")
                    st.rerun()
                else:
                    st.warning("Please write a reply first.")
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{real_index}", use_container_width=True):
                delete_comment(real_index)
                st.success("Comment deleted!")
                st.rerun()