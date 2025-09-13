import streamlit as st
import cohere

st.title("🌱 MindfulBuddy: Your Wellness Chatbot (Cohere)")

# Insert your Cohere API key here
COHERE_API_KEY = "XzMspVE7b6kXtDES6U1tgEn0b2kAAMjXpjRNjZQp"
client = cohere.Client(COHERE_API_KEY)

# Chat history initialization
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Mood selector
mood = st.select_slider(
    "Choose your mood:",
    options=['😊 Happy', '😔 Sad', '😣 Stressed', '😃 Excited', '😴 Tired']
)

# User message input
user_message = st.text_input("Your message:")

# Function to get response from Cohere Generate endpoint
def get_cohere_response(mood, user_message):
    prompt = f"You are a friendly mental wellness coach speaking to a young person who feels {mood}. The user says: {user_message}. Reply with empathy and encouragement."
    response = client.generate(
        model="xlarge",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"]
    )
    return response.generations[0].text.strip()

if st.button("Send") and user_message:
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    try:
        bot_reply = get_cohere_response(mood, user_message)
    except Exception as e:
        bot_reply = f"Error contacting Cohere API: {e}"
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# Display conversation history
st.write("### Conversation")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"👤 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Buddy:** {msg['content']}")

st.markdown("---")
st.markdown("All chats are confidential. For emergencies, contact a helpline.")
