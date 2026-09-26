import streamlit as st
from classeviva import Session
from twilio.rest import Client

st.set_page_config(page_title="ClasseViva Smart Monitor", page_icon="📱", layout="centered")

st.title("📱 ClasseViva Smart Monitor")
st.write("Inserisci le tue credenziali di ClasseViva per verificare l'accesso e inviare la notifica.")

TWILIO_ACCOUNT_SID = "IL_TUO_SID_QUI"
TWILIO_AUTH_TOKEN = "IL_TUO_TOKEN_QUI"
TWILIO_FROM_PHONE = "whatsapp:+14155238886"
TWILIO_TO_PHONE = "+393331234567"

username = st.text_input("Username ClasseViva")
password = st.text_input("Password ClasseViva", type="password")

if st.button("Verifica e Invia Notifica", type="primary"):
    if not username or not password:
        st.error("Inserisci username e password.")
    else:
        try:
            ses = Session()
            ses.login(username, password)
            st.success("Connessione a ClasseViva stabilita con successo!")
            try:
                voti = ses.grades()
                msg = "✅ ClasseViva Monitor: Accesso e voti verificati!"
            except:
                msg = "✅ ClasseViva Monitor: Accesso effettuato con successo!"
            
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(body=msg, from_=TWILIO_FROM_PHONE, to=TWILIO_TO_PHONE)
            st.success("Notifica WhatsApp inviata con successo!")
        except Exception as e:
            st.error(f"Errore: {e}")
