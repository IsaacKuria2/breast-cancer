import streamlit as st
from utils.comments import load_comments, save_comment

def render_comment_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Leave a Comment")

    name = st.sidebar.text_input("Your name", placeholder="Jane Doe")
    email = st.sidebar.text_input("Your email", placeholder="jane@email.com")
    comment = st.sidebar.text_area("Comment", placeholder="What do you think?", height=100)

    if st.sidebar.button("Submit", use_container_width=True):
        if name.strip() and email.strip() and comment.strip():
            if "@" not in email:
                st.sidebar.warning("Please enter a valid email address.")
            else:
                save_comment(name.strip(), email.strip(), comment.strip())
                st.sidebar.success("✅ Comment submitted! Thank you.")
        else:
            st.sidebar.warning("Please fill in all fields.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🗨️ Recent Comments")
    try:
        comments = load_comments()
        if not comments:
            st.sidebar.info("No comments yet. Be the first!")
        else:
            for c in reversed(comments[-5:]):
                st.sidebar.markdown(f"**{c['name']}** · *{c['timestamp']}*")
                st.sidebar.markdown(f"> {c['comment']}")
                if c.get("reply"):
                    st.sidebar.markdown(f"↩️ *Admin: {c['reply']}*")
                st.sidebar.markdown("---")
    except Exception as e:
        st.sidebar.error(f"Could not load comments: {e}")