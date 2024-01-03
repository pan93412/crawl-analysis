import logging
import streamlit as st
from models.database import TypedDatabase
from modules.line import LineCrawler

logging.basicConfig(level=logging.DEBUG)

db = TypedDatabase()
lc = LineCrawler(db.line_message_model())

# text
st.button("Open LINE", on_click=lambda: lc.open_line())
group_name = st.text_input("Group name")

members = st.text_area("Potential group members", height=200).splitlines()

st.write("You can also paste the exported group messages here. The first line should be the group name.")
group_messages = st.text_area("Group messages…", height=200)

if st.button("Search group"):
    messages, chat_title = "", ""

    if group_messages == "" and group_name == "":
        st.error("Please input group name or messages.")
        exit()

    if group_name != "":
        result = lc.search_group(group_name)
        if result is None:
            st.error("No such group.")
        else:
            messages, chat_title = result

    if group_messages != "":
        chat_title = group_messages.split("\n")[0]
        messages = "\n".join(group_messages.split("\n")[1:])

    st.text_area(f"{chat_title}'s Content", messages, height=200)
    parsed = lc.parse_chat(messages, members)
    st.dataframe(parsed)
    st.button("Save to database", on_click=lambda: lc.put_to_collection(parsed, chat_title))
