import streamlit as st
from groq import Groq

# Grok setup (hardcoded key)
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# Custom CSS for purple theme


# Title
st.title("Bookworm Chat - Powered by Grok")

# Perfect prompt for Grok
BOOKWORM_PROMPT = """
You are Grok, a super-friendly and witty book expert created by xAI for the BookSync App. Your mission is to help users dive into the world of books with enthusiasm! You’re knowledgeable about all genres—fiction, non-fiction, fantasy, sci-fi, classics, educational texts, you name it. Offer spot-on recommendations, quick summaries, or fun facts about books and authors. If users ask about donating or finding books, give practical tips tied to a community bookshelf concept (e.g., suggest donating classics or searching for local finds). Keep it casual, engaging, and book-obsessed—think of yourself as a librarian with a sense of humor and a passion for sharing stories!
"""

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["grok"])

# Chat input
prompt = st.chat_input("Ask Grok about books (e.g., Recommend a fantasy book)")

if prompt:
    # Add user message to history
    st.session_state.chat_history.append({"user": prompt, "grok": ""})

    # Display user message immediately
    with st.chat_message("user"):
        st.write(prompt)

    # Call Grok API
    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Fast and versatile model
            messages=[
                {"role": "system", "content": BOOKWORM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        grok_reply = response.choices[0].message.content

        # Update the last entry with Grok's reply
        st.session_state.chat_history[-1]["grok"] = grok_reply

        # Display Grok's reply
        with st.chat_message("assistant"):
            st.write(grok_reply)
    except Exception as e:
        st.error(f"Error with Grok API: {str(e)}")