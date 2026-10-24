
import streamlit as st
from fichiers.style import style_connexion
import base64

OMAR = st.secrets["credentials"]["omar"]
MANSOUR = st.secrets["credentials"]["mansour"]


def login():
    
    style_connexion()

    # Centrer le formulaire dans la page
    gauche, centre, droite = st.columns([1, 1, 1])

    with centre:
        with st.form("login_form"):

            # Titre placé à l'intérieur du cadre
            st.markdown(
                '<div class="titre-connexion">CONNEXION</div>',
                unsafe_allow_html=True
            )

            # Champ de saisie du mot de passe
            password = st.text_input(
                "",
                type="password",
                placeholder="Saisir votre mot de passe"
            )

            # Bouton de connexion
            submit = st.form_submit_button(
                "Connexion",
                use_container_width=True,
                type="secondary"
            )

        # Vérification des identifiants
        if submit:
            if password == OMAR:
                st.session_state.authentifie = True
                st.session_state.utilisateur = OMAR
                st.session_state.afficher_login = False
                st.rerun()

            elif password == MANSOUR:
                st.session_state.authentifie = True
                st.session_state.utilisateur = MANSOUR
                st.session_state.afficher_login = False
                st.rerun()

            elif not password:
                st.warning("Veuillez saisir votre mot de passe.")

            else:
                st.error("Mot de passe incorrect.")
