import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Make sure you have the API key in the environment variable; otherwise, this will be None.
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found.")

# Set up OpenAI API key
OpenAI.api_key = openai_api_key

client = OpenAI()

def get_openai_response(messages):
    completion = client.chat.completions.create(
        model='gpt-4o',
        temperature=0,
        top_p=0,
        messages=messages
    )
    return completion.choices[0].message.content.strip()

# Streamlit app layout
st.title("Tattoo Idea Generator")
st.write("This chatbot will help you find the perfect tattoo idea. Let's get started!")

# Initialize session state for conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": """You are a helpful assistant that helps users come up with tattoo ideas. You need to ask user short but direct questions to help him/her decide which tattoo they want. The tattoo can be permament or temporary so you must ask user about that.
                                        If user wants a permanent tattoo, ask about his preferences and if he has any ideas in mind, the story behind the tatto or if he/she doesn't have an idea, ask about his/her interests, hobbies, favorite colors, events that marked their lifes etc.
                                        If user wants a temporary tattoo, ask about the event where he/she wants to wear it, the colors, the size, the style, the message he/she wants to transmit etc. If there is an event for the tattoo, ask about the event, the colors, the style, the message he/she wants to transmit etc."""}
    ]

# Initialize session state for stopping the conversation
if 'conversation_complete' not in st.session_state:
    st.session_state.conversation_complete = False

# Display conversation
for message in st.session_state.conversation:
    if message['role'] == 'user':
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")

# Get user input
if not st.session_state.conversation_complete:
    user_input = st.text_input("You:", key='input')

    if st.button("Send"):
        if user_input:
            # Append user input to the conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})

            # Get response from OpenAI
            assistant_reply = get_openai_response(st.session_state.conversation)
            st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

            # Check if the conversation should be stopped based on the phrase
            if "enough information" in assistant_reply.lower():
                st.session_state.conversation_complete = True

            # Check if the conversation has reached 10 messages (5 user messages and 5 bot messages)
            if len(st.session_state.conversation) >= 11:  # Includes the initial system message
                st.session_state.conversation_complete = True

            # Clear the input field for the next user input
            st.experimental_rerun()
else:
    st.write("Thank you! We have gathered enough information for your temporary tattoo idea.")
