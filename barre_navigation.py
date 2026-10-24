import streamlit as st
from connexion import login
from a_propos import propos
from accueil import page_accueil
from fichiers.style import style_barre_de_navigation, style_barre_accueil


def barre_de_navigation():
    # ================== BARRE DE NAVIGATION ============================== #

    if "menu" not in st.session_state:
        st.session_state.menu = "ACCUEIL"

    style_barre_de_navigation()
    navigation = st.columns([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5], gap="small", vertical_alignment="center")
    with navigation[0]:
        # Ancre CSS : permet de cibler la ligne complète de navigation
        st.markdown('<span class="navigation-ancre"></span>', unsafe_allow_html=True)
        st.image("logo_ande.jpeg", width=55)

    

    # Boutons de navigation
    menus = [
        ("ACCUEIL", "nav_accueil"),
        ("A PROPOS", "nav_propos"),
        ("AGREGATION", "nav_agregation"),
        ("DETAIL", "nav_detail"),
        ("FICHE", "nav_fiche"),
        ("DECONNEXION", "nav_deconnexion")
    ]

    for i, (nom, cle) in enumerate(menus, start=1):
        with navigation[i]:
            # Le bouton actif utilise le type "primary" (orange via le CSS).
            est_actif = st.session_state.menu == nom and cle != "nav_deconnexion"

            if st.button(
                nom,
                key=cle,
                use_container_width=True,
                type="primary" if est_actif else "secondary"
            ):
                if cle == "nav_deconnexion":
                    st.session_state.authentifie = False
                    #st.session_state.menu = "AGREGATION"
                    st.session_state.pop("menu_accueil", None)
                    st.rerun()
                else:
                    st.session_state.menu = nom
                    st.rerun()




    # ================== BARRE DE NAVIGATION ============================== #
def barre_accueil():
    # Initialiser la page active
    if "menu_accueil" not in st.session_state:
        st.session_state.menu_accueil = "ACCUEIL"

    style_barre_accueil()

    navigation = st.columns([1.5, 1.5, 1.5, 1, 1, 1], gap="small", vertical_alignment="center")
   

    with navigation[0]:
        # Ancre CSS : permet de cibler la ligne complète de navigation
        st.markdown('<span class="navigation-ancre"></span>', unsafe_allow_html=True)
        st.image("logo_ande.jpeg", width=55)

   

    # Bouton ACCUEIL
    with navigation[3]:
        if st.button(
            "ACCUEIL",
            key="nav_accueil",
            type=("primary" if st.session_state.get("menu_accueil") == "ACCUEIL"
                and not st.session_state.get("afficher_login", False) else "secondary"),
            use_container_width=True
        ):
            st.session_state.menu_accueil = "ACCUEIL"
            st.session_state.afficher_login = False
            st.rerun()


    # Bouton A PROPOS
    with navigation[4]:
        if st.button(
            "A PROPOS",
            key="nav_propos",
            type=("primary" if st.session_state.get("menu_accueil") == "A PROPOS"
                and not st.session_state.get("afficher_login", False) else "secondary"),
            use_container_width=True
        ):
            st.session_state.menu_accueil = "A PROPOS"
            st.session_state.afficher_login = False
            st.rerun()


    # Bouton CONNEXION
    with navigation[5]:
        if st.button(
            "CONNEXION",
            key="nav_connexion",
            type=( "primary" if st.session_state.get("afficher_login", False) else "secondary"),
            use_container_width=True
        ):
            st.session_state.afficher_login = True
            st.rerun()

    # Afficher le formulaire de connexion
    # Affichage du contenu
    if st.session_state.get("afficher_login", False):
        if not st.session_state.get("authentifie", False):
            login()
        else:
            st.session_state.afficher_login = False

    if not st.session_state.get("afficher_login", False):
        if st.session_state.get("menu_accueil", "ACCUEIL") == "A PROPOS":
            propos()
        else:
            page_accueil()