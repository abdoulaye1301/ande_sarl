import streamlit as st
import base64

def style_ande_sarl():
    st.markdown("""
        <style>
        /* Couleur de fond de toute la page */
        .stApp {
            background-color: #87c28e;
        }

        /* Couleur de fond de la barre latérale */
        [data-testid="stSidebar"] {
            background-color: #D6EAF2;
        }

        /* Couleur des tableaux */
        [data-testid="stDataFrame"] {
            background-color: white;
        }


        /* Bande supérieure blanche */
        header[data-testid="stHeader"] {
            background-color: white !important;
            height: 45px !important;
            border-bottom: 1px solid #e5e5e5;
        }

        /* Conserver la barre visible */
        header[data-testid="stHeader"] {
            display: flex !important;
            visibility: visible !important;
        }

        /* Masquer Deploy et le menu à trois points */
        header[data-testid="stHeader"] div[data-testid="stToolbar"] {
            visibility: hidden !important;
        }

        /* Texte défilant dans la bande supérieure */
        header[data-testid="stHeader"]::after {
            content: "ADHESION NATIONALE AU DEVELOPPEMENT ECONOMIQUE (ANDE)";
            position: absolute;
            left: 0;
            top: 0;
            height: 45px;
            width: 100%;
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            color: #008000;
            white-space: nowrap;
            overflow: hidden;
            animation: defilement 30s linear infinite;
        }

        /* Animation horizontale */
        @keyframes defilement {
            0% {
                transform: translateX(100%);
            }
            100% {
                transform: translateX(-100%);
            }
        }

        /* Réduire l'espace entre la bande blanche et le contenu */
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 0px !important;
        }

        /* Rapprocher la navigation de la bande blanche sans la masquer */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre) {
            margin-top: -45px !important;
            position: relative;
            z-index: 1;
            background-color: #008000 !important;
            padding: 8px 12px !important;
            border-radius: 6px;
            box-sizing: border-box;
        }
        </style>
        """, unsafe_allow_html=True
    )

def style_barre_de_navigation():
     st.markdown("""
        <style>
        /* Barre de navigation */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre) {
            background-color: #0d7a2e;
            padding: 4px 12px !important;
            min-height: 0 !important;
            border-radius: 8px;
            align-items: center !important;
        }
    
        /* Colonnes : conserver la structure native de Streamlit */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        > div[data-testid="column"] {
            align-self: center !important;
        }
    
        /* Conteneur des boutons */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] {
            width: 100%;
            padding: 0 !important;
            margin: 0 !important;
        }
    
        /* Tous les boutons ont la même hauteur */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] button {
            width: 100%;
            height: 38px !important;
            min-height: 38px !important;
            padding: 0.5rem 1rem !important;
            margin: 0 !important;
            border: none !important;
            border-radius: 7px;
            background-color: white;
            color: #0d7a2e;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    
        /* Texte centré dans chaque bouton */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] button p {
            margin: 0 !important;
            line-height: 1.2 !important;
        }
    
        /* Bouton actif : orange */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #FF9800 !important;
            color: white !important;
            border: none !important;
        }
    
        /* Boutons inactifs : blanc */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: white !important;
            color: #0d7a2e !important;
            border: none !important;
        }
    
        /* Survol */
        div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
        div[data-testid="stButton"] button:hover {
            filter: brightness(0.96);
        }
        </style>
        """, unsafe_allow_html=True)


def style_barre_accueil():
     st.markdown("""
         <style>
         /* Barre de navigation */
         div[data-testid="stHorizontalBlock"]:has(.navigation-ancre) {
             background-color: #87c28e;
             padding: 8px;
             border-radius: 6px;
             align-items: center !important;
         }
     
         /* Boutons */
         div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
         div[data-testid="stButton"] button {
             width: 100%;
             height: 38px !important;
             min-height: 38px !important;
             padding: 0.5rem 1rem !important;
             margin: 0 !important;
             border: none !important;
             border-radius: 7px;
             display: flex;
             align-items: center;
             justify-content: center;
         }
     
         /* Boutons inactifs */
         div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
         div[data-testid="stButton"] button[kind="secondary"] {
             background-color: white !important;
             color: #87c28e !important;
         }
     
         /* Bouton actif */
         div[data-testid="stHorizontalBlock"]:has(.navigation-ancre)
         div[data-testid="stButton"] button[kind="primary"] {
             background-color: #FF9800 !important;
             color: white !important;
         }
         </style>
         """, unsafe_allow_html=True)


def style_connexion():

    # Image d'arrière-plan du formulaire
    chemin_image = "images/logo_ande.jpeg"

    with open(chemin_image, "rb") as fichier:
        image_base64 = base64.b64encode(fichier.read()).decode()

     
    st.markdown(f"""
        <style>
        /* ================= CADRE DU FORMULAIRE ================= */

        div[data-testid="stForm"] {{
            background-image:
                linear-gradient(
                    rgba(0, 80, 0, 0.45),
                    rgba(0, 80, 0, 0.45)
                ),
                url("data:image/jpeg;base64,{image_base64}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            min-height: 300px;
            padding: 12px 30px 30px 30px !important;
            border-radius: 16px;
            border: 2px solid rgba(255, 255, 255, 0.85);
            box-sizing: border-box;
        }}

        /* ================= TITRE CONNEXION ================= */

        .titre-connexion {{
            text-align: center;
            color: white;
            font-size: 42px;
            font-weight: bold;
            margin: 0 0 22px 0;
            padding: 0;
            line-height: 1.2;
        }}

        /* Réduire l'espace au-dessus du contenu du formulaire */
        div[data-testid="stForm"] [data-testid="stVerticalBlock"] {{
            gap: 0.6rem;
        }}

        /* ================= CHAMP MOT DE PASSE ================= */

        div[data-testid="stForm"] div[data-testid="stTextInput"] input {{
            min-height: 55px;
            background-color: white !important;
            color: #87c28e !important;
            border: 2px solid #87c28e !important;
            border-radius: 12px !important;
            font-size: 18px !important;
            padding: 10px 15px !important;
            box-shadow: none !important;
        }}

        /* Couleur du champ lorsqu'il est sélectionné */
        div[data-testid="stForm"] div[data-testid="stTextInput"] input:focus {{
            border: 2px solid #87c28e !important;
            box-shadow: 0 0 0 2px rgba(77, 170, 180, 0.2) !important;
        }}

        /* Libellé Mot de passe */
        div[data-testid="stForm"] div[data-testid="stTextInput"] label {{
            color: white !important;
            font-size: 18px !important;
            font-weight: 500 !important;
        }}

        /* Icône pour afficher ou masquer le mot de passe */
        div[data-testid="stForm"] div[data-testid="stTextInput"] button {{
            color: #87c28e !important;
            background-color: white !important;
            border: none !important;
        }}

        /* ================= BOUTON CONNEXION ================= */

        div[data-testid="stForm"] button[kind="primary"],
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {{
            min-height: 48px !important;
            width: 100%;
            background-color: #87c28e !important;
            color: white !important;
            border: 2px solid #87c28e !important;
            border-radius: 12px !important;
            font-size: 20px !important;
            font-weight: bold !important;
            transition: background-color 0.2s ease;
        }}

        /* Survol du bouton */
        div[data-testid="stForm"] button:hover {{
            background-color: #87c28e !important;
            color: white !important;
            border-color: white !important;
        }}

        /* Texte du bouton */
        div[data-testid="stForm"] button p {{
            color: white !important;
            font-weight: bold !important;
        }}

        
        /* Fond blanc du champ de saisie */
        div[data-testid="stForm"] div[data-testid="stTextInput"] {{
            background-color: transparent !important;
        }}

        div[data-testid="stForm"] div[data-testid="stTextInput"] input {{
            background: #FFFFFF !important;
            color: #87c28e !important;
            -webkit-text-fill-color: #267780 !important;
            border: 2px solid #87c28e !important;
            border-radius: 12px 0 0 12px !important;
            box-shadow: none !important;
        }}

        /* Fond blanc du bouton afficher/masquer */
        div[data-testid="stForm"] div[data-testid="stTextInput"] button {{
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            color: #87c28e !important;
            border: 2px solid #87c28e !important;
            border-left: none !important;
            border-radius: 0 12px 12px 0 !important;
            box-shadow: none !important;
        }}

        /* Supprimer le fond sombre au survol */
        div[data-testid="stForm"] div[data-testid="stTextInput"] button:hover,
        div[data-testid="stForm"] div[data-testid="stTextInput"] button:focus {{
            background: #FFFFFF !important;
            color: #87c28e !important;
            box-shadow: none !important;
        }}

        /* Empêcher le fond noir du conteneur interne */
        div[data-testid="stForm"] div[data-testid="stInputRootElement"],
        div[data-testid="stForm"] div[data-baseweb="input"] {{
            background: #FFFFFF !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }}

        </style>
        """, unsafe_allow_html=True
    )