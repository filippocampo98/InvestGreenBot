import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Caricamento delle chiavi API
load_dotenv()
llama3_api_key = os.getenv("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")
llama3_api_url = os.getenv("https://download6.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoiaG03bHdoYnEyMGlyeHNhNTFyOXlrbGswIiwiUmVzb3VyY2UiOiJodHRwczpcL1wvZG93bmxvYWQ2LmxsYW1hbWV0YS5uZXRcLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MTY3OTM4MTJ9fX1dfQ__&Signature=HGj3HDQVGauxt0l2QM5%7EzMLieNEn-eOjOUiRDoUzCPDihIvrBG0auKnl13WJPxv%7ElBdgYMOVh6j40aNMXe3mgTE5NNt3Y94Tc0tFNkSlNNR2LahR65wvGAD6uIdqV%7EY0qH2-ksXdgCYcWGDvFGCWdeS4EkL-Lcqkk10VaCuPJrrck%7EaGCxZElTFUtC1Jz51XkrTWaPUAu22Ugkb5JlVrDyFSXk6lhToG0I0GzgKeBG8K%7Eg9wrW78dfDSQVkdTRcELRRb-kSeiT5s1O2dIO39x4IDXDMwP5NsKv%7EZchrOJN2Tl1Ec-CD8c3fLuer05Y2PIylziEYZoItP5Wjx6l0XOQ__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=981136506499991")

# Implementazione del Chatbot con Llama3 via API HTTP
class Llama3Chatbot:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.history = []

    def ask(self, question):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'prompt': question,
            'max_tokens': 150  # Adjust based on your requirement
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code == 200:
            answer = response.json().get('choices', [{}])[0].get('text', '').strip()
            self.history.append({"question": question, "answer": answer})
            return answer
        else:
            return "Errore nella chiamata API a Llama 3"

    def get_prospect(self):
        prospect = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in self.history])
        return prospect

# Funzione principale per Streamlit
def main():
    llama3_bot = Llama3Chatbot(api_key=llama3_api_key, api_url=llama3_api_url)

    st.title("InvestGreenBot")
    st.write("Benvenuto in InvestGreenBot! Fai una domanda sulla finanza green o sul mercato azionario.")

    question = st.text_input("Fai una domanda:")

    if question:
        st.write("### Risposta di Llama3Bot:")
        llama3_response = llama3_bot.ask(question)
        st.write(llama3_response)

        st.write("## Prospetto delle domande e risposte di Llama3Bot:")
        st.text(llama3_bot.get_prospect())

if __name__ == "__main__":
    main()
