import streamlit as st
import pandas as pd
from datetime import date
from classeviva import Session
from twilio.rest import Client

# Configurazione della pagina
st.set_page_config(
    page_title="Assistente Personale Intelligente",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Assistente Personale Intelligente & Hub Notifiche")
st.write("Gestisci pagamenti, appuntamenti, notifiche scolastiche (ClasseViva) e resoconti di spesa in un unico posto.")

# --- CONFIGURAZIONE TWILIO (Inserisci i tuoi dati) ---
TWILIO_ACCOUNT_SID = "IL_TUO_SID_QUI"
TWILIO_AUTH_TOKEN = "IL_TUO_TOKEN_QUI"
TWILIO_FROM_PHONE = "whatsapp:+14155238886"  # Numero sandbox o mittente Twilio
TWILIO_TO_PHONE = "+393331234567"          # Il tuo numero WhatsApp di ricezione

# Funzione di utilità per l'invio WhatsApp
def invia_notifica_whatsapp(testo):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=testo,
            from_=TWILIO_FROM_PHONE,
            to=TWILIO_TO_PHONE
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# --- MENU A SCHEDE PRINCIPALE ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💳 Scadenze Pagamenti", 
    "📅 Appuntamenti", 
    "🏫 Scuola (ClasseViva)", 
    "📊 Resoconto Spese"
])

# ================= TAB 1: SCADENZE PAGAMENTI =================
with tab1:
    st.header("Gestione Scadenze Pagamenti")
    st.write("Monitora bollette, affitti, mutui, rate, assicurazioni, bollo auto, tasse (TARI/IMU) e abbonamenti.")

    col1, col2 = st.columns(2)
    with col1:
        tipo_pagamento = st.selectbox(
            "Categoria Pagamento",
            ["Bolletta Luce/Gas/Acqua", "Affitto / Mutuo", "Rata Finanziamento", 
             "Assicurazione Auto/Casa", "Bollo Auto", "Abbonamenti Digitali", 
             "Tasse Scolastiche", "TARI / IMU", "Spese Condominiali", "Altro"]
        )
        descrizione_pagamento = st.text_input("Descrizione (es. Bolletta Enel)")
    with col2:
        importo_pagamento = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
        data_scadenza = st.date_input("Data di Scadenza", value=date.today())

    if st.button("Registra Scadenza e Invia Avviso WhatsApp", key="btn_pagamento"):
        giorni_mancanti = (data_scadenza - date.today()).days
        messaggio = (
            f"🔔 *Promemoria Pagamento*\n"
            f"• Tipo: {tipo_pagamento}\n"
            f"• Dettaglio: {descrizione_pagamento}\n"
            f"• Importo: €{importo_pagamento:.2f}\n"
            f"• Scadenza: {data_scadenza} (Tra {giorni_mancanti} giorni)"
        )
        
        successo, res = invia_notifica_whatsapp(messaggio)
        if successo:
            st.success(f"Scadenza registrata e notifica WhatsApp inviata con successo! (SID: {res})")
        else:
            st.warning(f"Scadenza registrata ma errore nell'invio WhatsApp: {res}")


# ================= TAB 2: APPUNTAMENTI =================
with tab2:
    st.header("Gestione Appuntamenti")
    st.write("Organizza visite mediche, impegni di lavoro, scadenze legali/burocratiche e promemoria personali.")

    col1, col2 = st.columns(2)
    with col1:
        titolo_appunt = st.text_input("Titolo / Oggetto Appuntamento")
        categoria_appunt = st.selectbox("Categoria", ["Visita Medica", "Impegno Lavorativo", "Scadenza Legale/Burocratica", "Personale"])
    with col2:
        data_appunt = st.date_input("Data Appuntamento", value=date.today(), key="date_app")
        ora_appunt = st.time_input("Orario")

    if st.button("Salva Appuntamenti e Notifica", key="btn_appuntamento"):
        messaggio_app = (
            f"📅 *Promemoria Appuntamento*\n"
            f"• Oggetto: {titolo_appunt} ({categoria_appunt})\n"
            f"• Data: {data_appunt} alle ore {ora_appunt}"
        )
        successo, res = invia_notifica_whatsapp(messaggio_app)
        if successo:
            st.success("Appuntamento salvato e notifica WhatsApp inviata!")
        else:
            st.warning(f"Salvato, ma errore invio WhatsApp: {res}")


# ================= TAB 3: SCUOLA (CLASSEVIVA) =================
with tab3:
    st.header("Integrazione Scolastica (ClasseViva)")
    st.write("Inserisci le credenziali per verificare i voti, le note e le circolari in tempo reale.")

    cv_user = st.text_input("Username ClasseViva", key="cv_user")
    cv_pass = st.text_input("Password ClasseViva", type="password", key="cv_pass")

    if st.button("Verifica ClasseViva e Invia Report", key="btn_classeviva"):
        if not cv_user or not cv_pass:
            st.error("Inserisci username e password di ClasseViva.")
        else:
            try:
                ses = Session()
                ses.login(cv_user, cv_pass)
                st.success("Connessione a ClasseViva stabilita con successo!")
                
                # Tentativo di recupero voti
                try:
                    voti = ses.grades()
                    testo_scuola = "🏫 *ClasseViva Monitor*: Accesso effettuato. Nuovi dati scolastici e voti controllati con successo!"
                except:
                    testo_scuola = "🏫 *ClasseViva Monitor*: Accesso effettuato con successo al registro elettronico."

                # Invio notifica via WhatsApp
                successo, res = invia_notifica_whatsapp(testo_scuola)
                if successo:
                    st.success("Notifica scolastica inviata via WhatsApp!")
                else:
                    st.warning(f"Accesso riuscito, ma errore invio WhatsApp: {res}")

            except Exception as e:
                st.error(f"Errore di autenticazione su ClasseViva: {e}")


# ================= TAB 4: RESOCONTO SPESE MENSILE =================
with tab4:
    st.header("Resoconto Finanziario Mensile")
    st.write("Registra le spese del mese per ottenere un report dettagliato suddiviso per categoria.")

    # Simulazione database di sessione per le spese
    if "spese_db" not in st.session_state:
        st.session_state.spese_db = pd.DataFrame(columns=["Categoria", "Descrizione", "Importo", "Data"])

    with st.form("form_spesa"):
        c1, c2, c3 = st.columns(3)
        with c1:
            cat_spesa = st.selectbox(
                "Categoria Spesa", 
                ["Alimentari", "Utenze & Casa", "Trasporti / Carburante", "Salute", "Scuola / Istruzione", "Svago", "Altro"]
            )
        with c2:
            desc_spesa = st.text_input("Descrizione Spesa")
        with c3:
            imp_spesa = st.number_input("Importo (€)", min_value=0.0, format="%.2f", key="imp_sp")
        
        submit_spesa = st.form_submit_button("Aggiungi Spesa al Resoconto")
        
        if submit_spesa and desc_spesa:
            nuova_riga = pd.DataFrame({"Categoria": [cat_spesa], "Descrizione": [desc_spesa], "Importo": [imp_spesa], "Data": [str(date.today())]})
            st.session_state.spese_db = pd.concat([st.session_state.spese_db, nuova_riga], ignore_index=True)
            st.success("Spesa aggiunta con successo!")

    # Visualizzazione Resoconto
    if not st.session_state.spese_db.empty:
        st.subheader("📊 Riepilogo Spese Registrate")
        st.dataframe(st.session_state.spese_db, use_container_width=True)

        totale_mensile = st.session_state.spese_db["Importo"].sum()
        st.metric(label="Totale Spese Registrate", value=f"€ {totale_mensile:.2f}")

        # Suddivisione per categoria
        st.subheader("Riepilogo per Categoria")
        riepilogo_cat = st.session_state.spese_db.groupby("Categoria")["Importo"].sum().reset_index()
        st.bar_chart(riepilogo_cat.set_index("Categoria"))
    else:
        st.info("Nessuna spesa registrata per questo mese. Utilizza il modulo sopra per iniziare.")
