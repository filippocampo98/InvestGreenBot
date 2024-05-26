import streamlit as st
from groq import Groq

# Funzione per ottenere una risposta dal modello Groq
def get_groq_response(messages):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response

# Funzione principale per eseguire la conversazione con l'assistente
def run_conversation():
    # Inizializza la lista dei messaggi con il messaggio iniziale dell'assistente
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Benvenuto! Come posso aiutarti oggi nel mercato finanziario?"}
        ]
        st.session_state.last_input = ""

    # Visualizza i messaggi della conversazione
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"**Utente:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**Assistente:** {message['content']}")

    # Input dell'utente
    user_input = st.text_input("Inserisci il tuo messaggio:", key="input_message")

    # Se l'utente inserisce un messaggio, aggiungilo ai messaggi e genera una risposta
    if user_input and user_input != st.session_state.last_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Ottenere la risposta dell'assistente dal client Groq
        response = get_groq_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Salva l'ultimo input per evitare cicli infiniti
        st.session_state.last_input = user_input
        
        # Ripulire l'input dopo l'invio
        st.experimental_rerun()

    # Pulsante per generare il report finale
    if st.button("Genera Report"):
        generate_report()

# Funzione per generare un report
def generate_report():
    st.write("**Generazione del report sugli obiettivi finanziari**")
    # Estrarre le informazioni chiave dai messaggi
    goals = [message["content"] for message in st.session_state.messages if message["role"] == "user"]

    # Creare il report
    report = "\n".join(goals)
    st.write("**Report:**")
    st.write(report)

    # Saluto finale
    st.write("Grazie per aver utilizzato il nostro servizio di assistenza agli investimenti. Buona giornata!")

# Funzione principale di Streamlit
def main():
    st.title("Investment Assistance Chatbot")
    st.write("Benvenuto nel chatbot di assistenza agli investimenti!")

    # Avvia la conversazione
    run_conversation()

if __name__ == "__main__":
    main()
