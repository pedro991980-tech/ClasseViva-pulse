import streamlit as st
from classeviva import Session
from twilio.rest import Client

st.set_page_config(page_title="ClasseViva Smart Monitor", page_icon="🎓", layout="centered")

st.title("🎓 ClasseViva Smart Monitor")
st.write("Inserisci le tue credenziali di ClasseViva. L'app verificherà l'accesso e invierà automaticamente la notifica WhatsApp.")

# --- CONFIGURAZIONE TWILIO FISSA ---
TWILIO_ACCOUNT_SID = "IL_TUO_SID_QUI"
TWILIO_AUTH_TOKEN = "IL_TUO_TOKEN_QUI"
TWILIO_FROM_PHONE = "whatsapp:+14155238886"  # Numero sandbox o mittente Twilio
TWILIO_TO_PHONE = "+393331234567"          # Il numero che deve ricevere il messaggio

# Campi di input per l'utente
username = st.text_input("Username ClasseViva")
password = st.text_input("Password ClasseViva", type="password")

if st.button("Verifica e Invia Notifica", type="primary"):
    if not username or not password:
        st.error("Per favore, inserisci username e password.")
    else:
        try:
            # 1. Connessione e login a ClasseViva
            ses = Session()
            ses.login(username, password)
            st.success("Connessione a ClasseViva stabilita con successo! 🎉")
            
            # 2. Controllo dei dati (es. voti)
            try:
                voti = ses.grades()
                messaggio_testo = "🤖 ClasseViva Monitor: Accesso effettuato e voti controllati con successo!"
            except Exception:
                messaggio_testo = "🤖 ClasseViva Monitor: Accesso effettuato con successo!"

            # 3. Invio automatico del messaggio WhatsApp via Twilio
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=messaggio_testo,
                    from_=TWILIO_FROM_PHONE,
                    to=TWILIO_TO_PHONE
                )
                st.success("Messaggio WhatsApp inviato automaticamente al tuo numero! 📱")
            except Exception as twilio_err:
                st.warning(f"Login riuscito, ma c'è stato un problema con l'invio WhatsApp: {twilio_err}")
                
        except Exception as e:
            st.error(f"Errore di Accesso a ClasseViva: {e}")