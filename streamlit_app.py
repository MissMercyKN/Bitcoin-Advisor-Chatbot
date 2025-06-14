import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # loads variables from .env

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat_session = model.start_chat(history=[])

if "skip_input_processing" not in st.session_state:
    st.session_state.skip_input_processing = False

# ---- Set Page Config ----
st.set_page_config(page_title="BitMentor", page_icon="🧠")

# ---- Title and Description ----
st.title("🧠 BitMentor - Your Bitcoin Sidekick")
st.markdown("Ask me anything about Bitcoin — from basics to best practices!")

# ---- Predefined Questions & Answers ----
qa_data = {
    "what is bitcoin": "Bitcoin is a decentralized digital currency that lets people send money directly to each other without banks. Trust the code, not the suits. 🟠",
    "what is sats": "Sats (or satoshis) are the smallest unit of Bitcoin. 1 BTC = 100,000,000 sats.",
    "why bitcoin": "Bitcoin offers decentralized, censorship-resistant money with a limited supply of 21 million coins.",
    "what's the hype around bitcoin": "People are excited because it's scarce, global, and not controlled by any government. Some call it digital gold.",
    "what is a wallet": "A wallet is a tool (software or hardware) that stores your Bitcoin private keys and lets you send/receive BTC.",
    "how to back up your wallet": "Most wallets give you a 12- or 24-word recovery phrase. Write it down and store it safely offline.",
    "how to protect your seed phrase": "Never share it online. Store it in a secure place, like a safe. Consider metal backup plates for fire/water protection.",
    "wallet types": "There are hot wallets (apps connected to the internet) and cold wallets (like hardware wallets, safer for long-term storage).",
    "key management": "Your private key = your Bitcoin. Never share it. Use multi-signature or hardware wallets for extra safety.",
    "is bitcoin legal": "In most countries, yes. But laws vary — always check your local regulations.",
    "how many bitcoins exist": "There will only ever be 21 million Bitcoins. Over 19 million are already mined.",
    "is bitcoin anonymous": "Bitcoin is pseudonymous. Your name isn’t tied to your address, but all transactions are visible on the blockchain.",
}

# ---- Function to get response from Gemini AI ----
def ask_gemini(question):
    try:
        response = st.session_state.chat_session.send_message(question)
        return response.text 
    except Exception as e:
        st.error(f"An error occurred with Gemini AI: {e}") # Added st.error for visibility
        return "Sorry, I had trouble reaching the AI service or processing your request."

def clear_everything():
    st.session_state.user_question_input = "" 
    st.session_state.skip_input_processing = True
    
# ---- Chat Interface ----
user_input = st.text_input("💬 Ask BitMentor a question about Bitcoin", key="user_question_input")

if user_input and not st.session_state.skip_input_processing:
    user_question = user_input.lower()

    found_answer = None
    for key in qa_data:
        if key in user_question:
            found_answer = qa_data[key]
            break

    if found_answer:
        st.success(found_answer)
    else:
        # If no predefined answer, ask Gemini AI
        with st.spinner("Thinking... 🤖"):
            gemini_answer = ask_gemini(user_input)
            st.info(gemini_answer)
          
st.session_state.skip_input_processing = False

st.button("Clear", on_click=clear_everything)


# ---- Disclaimer ----
st.markdown("---")
st.caption("⚠️ This is not financial advice. Always do your own research before investing.")
