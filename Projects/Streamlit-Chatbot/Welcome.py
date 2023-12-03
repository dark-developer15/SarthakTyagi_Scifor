import openai
import streamlit as st

openai.api_key = st.secrets["OPEN_API_KEY"]

st.set_page_config(
    page_title="Baatooni",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This is a Simple ChatBot Project made by **Sarthak Tyagi**"
    }
)
st.title("Baatooni")


# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message
    with st.chat_message("user"):
        st.markdown(prompt)
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Ans. {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "")
        except openai.RateLimitError as RLE:
            st.write("Rate Limit Reached: Please wait for 30 seconds then ReRun the application.")

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
