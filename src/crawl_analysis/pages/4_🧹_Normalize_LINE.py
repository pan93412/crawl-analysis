import streamlit as st

from models.database import TypedDatabase

st.set_page_config(page_title="Normalize: LINE", page_icon="🧹")

db = TypedDatabase()
model = db.line_message_model()

filter_by = st.selectbox("Filter by…", ["", "Source", "Full-text search"])
filter = st.text_input("Filter…")

if st.button("Search"):
    match filter_by:
        case "Source":
            posts = model.find({"source": filter})
        case "Content (full-text search)":
            posts = model.find({"$text": {"$search": filter}})
        case _:
            posts = model.find()

    st.dataframe(posts)

    for post in posts:
        st.markdown(
            f"""
- 👨 Sender: {post["sender"]}
- 🕒 Post at: {post["post_at"].isoformat()}
- Source: {post["source"]}

*ID: `{post["_id"] if "_id" in post else "<?>"}`*

```
{post["content"]}
```

---
            """
        )
