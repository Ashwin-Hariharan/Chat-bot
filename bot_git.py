import streamlit as st
from huggingface_hub import InferenceClient


client = InferenceClient(token="Your API token")   

st.title("Interactive Chatbot ")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  

col1, col2 = st.columns([1, 1])  

user_message = st.text_input("Your Message:", placeholder="Type your question here...")

with col1:
    if st.button("Send"):
        if user_message.strip():
            with st.spinner("Fetching response..."):
                try:
                    response = client.text_generation(
                        user_message,  
                        temperature=0.8,     
                        do_sample=True       
                    )

                    bot_response = (
                        response
                        if isinstance(response, str)
                        else response.get('generated_text', 'No response generated')
                    )

                    st.session_state.chat_history.append((user_message, bot_response))
                
                except Exception as e:
                    bot_response = f"Error: {e}"
                    st.session_state.chat_history.append((user_message, bot_response))

with col2:
    if st.button("Clear History"):
        st.session_state.chat_history = []  
        
st.subheader("Conversation History:")
if st.session_state.chat_history:
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Bot:** {bot_msg}")
else:
    st.write("New conversation! Start chatting!")

st.caption("Powered by Hugging Face API and Streamlit")
