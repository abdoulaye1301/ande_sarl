import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch
import textwrap
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from io import BytesIO
from matplotlib.image import imread

st.set_page_config(
    page_title="Ingénieur NDAO", layout="wide", page_icon="ndao abdoulaye.png"
)
profil = Image.open("Logo Afrika Leyri.png")
st.logo(profil)

# Upload du fichier Excel

# ========================REMPLISSAGE PROMOTEUR================================#

#Chargement = pd.read_excel("Donnees_Promoteurs.xlsx", engine='openpyxl')
donnee_promoteur_ande=pd.ExcelFile("https://kf.kobotoolbox.org/api/v2/assets/afxRhMSWSYvHTNh8VJJ6Q8/export-settings/esgmhxWNou7EgDaaTirMNgU/data.xlsx", engine='openpyxl')


# Charger le fichier Excel

# Importer les trois feuilles
team_leader_ande = pd.read_excel(donnee_promoteur_ande, sheet_name="PROMOTEUR")
groupe_promoteur = pd.read_excel(donnee_promoteur_ande, sheet_name="group_xe4ga41")
groupe_produits = pd.read_excel(donnee_promoteur_ande, sheet_name="groupe_produits")

#=======TEAM LEADER========================#

colonne_Team_Leader = ["today"
,"Operation"
,"zone"
,"Transport"
,"Stationnement"
,"Commentaire","_submission_time","_submitted_by","_index"
]
Team_Leader = team_leader_ande[colonne_Team_Leader]
Team_Leader = Team_Leader.rename(
    columns={
        "today": "Date Remplissage",
        "Operation": "Operation",
        "zone": "zone",
        "Transport": "Transport",
        "Stationnement": "Stationnement",
        "Commentaire": "Commentaire",
        "_submission_time": "Date",
        "_submitted_by": "team_leader",
        "_index": "ID_Team_Leader"
    }
)
# Colonne "Numero_semaine" pour extraire le numéro de semaine à partir de la colonne "Date"
Team_Leader["Numero_semaine"] = Team_Leader["Date"].dt.isocalendar().week
mois_fr = {
            1: "JANVIER", 2: "FÉVRIER", 3: "MARS",
            4: "AVRIL", 5: "MAI", 6: "JUIN",
            7: "JUILLET", 8: "AOÛT", 9: "SEPTEMBRE",
            10: "OCTOBRE", 11: "NOVEMBRE", 12: "DÉCEMBRE"
        }
# Colonne "Mois" pour extraire le mois à partir de la colonne "Date"
Team_Leader["Mois"] = Team_Leader["Date"].dt.month.map(mois_fr)
Team_Leader["Date"] = pd.to_datetime(Team_Leader["Date"]).dt.date
Team_Leader["Date Remplissage"] = pd.to_datetime(Team_Leader["Date Remplissage"]).dt.date
Team_Leader["team_leader"] = Team_Leader["team_leader"].apply(lambda x: "ALIOUNE BADARA (MANSOUR) SANE" if x == "sane_mansour" else x)

#st.write(Team_Leader.head())

# =======================PROMOTEUR================================#

colonne_promoteur = ["Prenom Nom","Precisez","_index","_parent_index"]
groupe_promoteur = groupe_promoteur[colonne_promoteur]
groupe_promoteur = groupe_promoteur.rename(
    columns={
        "Prenom Nom": "Prenom_Nom_Promoteur",
        "Precisez": "Precisez",
        "_index": "ID_Promoteur",
        "_parent_index": "ID_Team_Leader"
    }
)
#st.write(groupe_promoteur.head())
#========================PRODUITS================================#
colonne_produits = ["Produit",
"Quantites_Cartons","Montant","_index","_parent_index"]
groupe_produits = groupe_produits[colonne_produits]
groupe_produits = groupe_produits.rename(
    columns={
        "Produit": "Produit",
        "Quantites_Cartons": "Quantites_Cartons",
        "Montant": "Montant",
        "_index": "ID_Produit",
        "_parent_index": "ID_Promoteur"
    }
)
#st.write(groupe_produits.head())

# ==========Effectuer les jointures sur la clé commune============== #

donnee_promoteur_ande = Team_Leader.merge(
    groupe_promoteur,
    on="ID_Team_Leader",
    how="left"
).merge(
    groupe_produits,
    on="ID_Promoteur",
    how="left"
)
donnee_promoteur_ande["tata"] = donnee_promoteur_ande["team_leader"].apply(lambda x: "TATA 2" if x == "ALIOUNE BADARA (MANSOUR) SANE" else x)
#st.write(donnee_promoteur_ande.columns.tolist())
colonne_finale =["Date","Date Remplissage","tata","team_leader","Operation","zone","Prenom_Nom_Promoteur",
                 "Precisez","Produit","Quantites_Cartons","Montant","Transport","Stationnement","Commentaire","Numero_semaine","Mois"]

Chargement=donnee_promoteur_ande[colonne_finale]

# Trier de la date la plus récente à la plus ancienne
Chargement = Chargement.sort_values( by="Date",ascending=False)
#st.write(Chargement.head())

# ========================VERSEMENT DES RZ AVEC DJIBRIL================================#

donnee_RZ_ANDE = pd.read_excel("https://kf.kobotoolbox.org/api/v2/assets/aJj8LNSp65GUsBF4HSYaeq/export-settings/esuMq6M4dz43tSTpXb3N7rV/data.xlsx", engine='openpyxl')
colonne_rz=["today","Date","Opération","Equipe","Agent","Montant","Remise","Mode de versement","_submitted_by"]
donnee_RZ = donnee_RZ_ANDE[colonne_rz]
donnee_RZ = donnee_RZ.rename(
    columns={
        "today": "Date Remplissage","Opération": "Operation",
        "Equipe": "Equipe","Agent": "Agent","Montant": "Montant",
        "Remise": "Remise","Mode de versement": "Mode de versement",
        "_submitted_by": "Superviseur"
    })

# Colonne "Numero_semaine" pour extraire le numéro de semaine à partir de la colonne "Date"
donnee_RZ["Numero_semaine"] = donnee_RZ["Date"].dt.isocalendar().week
# Colonne "Mois" pour extraire le mois à partir de la colonne "Date"
donnee_RZ["Mois"] = donnee_RZ["Date"].dt.month.map(mois_fr)
donnee_RZ["Date"] = pd.to_datetime(donnee_RZ["Date"]).dt.date
donnee_RZ["Date Remplissage"] = pd.to_datetime(donnee_RZ["Date Remplissage"]).dt.date
donnee_RZ["Superviseur"] = donnee_RZ["Superviseur"].apply(lambda x: "DJIBRIL DIOP" if x == "diop_djibril" else x)
donnee_RZ["Semaine"] = donnee_RZ["Date"].apply(lambda x: pd.Timestamp(x).isocalendar().week)
#st.write(donnee_RZ)

# Définir les bornes du slider
num_semaine = Chargement["Numero_semaine"].unique()
colone= st.columns(5)
# Choix de l’onglet
menu = st.sidebar.radio("Navigation", ["AGREGATION","DETAIL","FICHE"])
periode = colone[0].selectbox("", ["Jour","Semaine","Mois"])
if periode == "Jour":
    semaine = colone[2].selectbox("", num_semaine)
    min_date = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()
    dat = colone[4].selectbox("", min_date)
    datea = dat.strftime("%d-%m-%Y")
    statio = Chargement[(Chargement["Date"] == dat)]
    stationnement = Team_Leader[(Team_Leader["Date"] == dat)]
    transport = Team_Leader[(Team_Leader["Date"] == dat)]
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Date"] == dat)]
elif periode == "Semaine":
    semaine = colone[2].selectbox("", num_semaine)
    statio = Chargement[(Chargement["Numero_semaine"] == semaine)]
    stationnement = Team_Leader[(Team_Leader["Numero_semaine"] == semaine)]
    transport = Team_Leader[(Team_Leader["Numero_semaine"] == semaine)]
    datea = semaine
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine)]
elif periode == "Mois":
    mois = colone[2].selectbox("", Chargement["Mois"].unique())
    statio = Chargement[(Chargement["Mois"] == mois)]
    stationnement = Team_Leader[(Team_Leader["Mois"] == mois)]
    transport = Team_Leader[(Team_Leader["Mois"] == mois)]
    datea = mois
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Mois"] == mois)]
#------------------------MENU AGREGATION-----------------------------------------#
if menu == "AGREGATION":
    sous_menu = st.sidebar.selectbox("", ["Versement","Stock","Stock Départ","Récapitulatif"])
    if sous_menu == "Versement":
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        
        st.markdown(f"<h4 style='text-align: center;'>!---------- Versement des promoteurs du {datea} ----------!</h4><br>", unsafe_allow_html=True)
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)

        colone= st.columns(3)
        #colone[0].metric("💴 CA TATA 1", f"{donnee_ordre[donnee_ordre['tata'] =='TATA 1']['Montant A verser'].sum():,.2f}".replace(",", " ")+" XOF")
        colone[0].metric("💴 Chiffre d'affaires", f"{donnee_ordre['Montant A verser'].sum():,.2f}".replace(",", " ")+" XOF")
        colone[1].metric("🚐 Transport", f"{transport['Transport'].sum():,.0f}".replace(",", " ")+" XOF")
        colone[2].metric("🅿️ Stationnement", f"{stationnement['Stationnement'].sum():,.0f}".replace(",", " ")+" XOF")
        

    elif sous_menu == "Stock Départ" and periode == "Semaine":
        st.markdown(f"<h4 style='text-align: center;'>!---------- Stock de départ du {datea} ----------!</h4><br>", unsafe_allow_html=True)
        
        #prom = colone[4].selectbox("", ["TATA 3"])
        
        statio1= statio[(statio["Operation"] == "Stock Lundi")]
        donnee_agre = (
            statio1.groupby(["tata", "Produit"])
            .agg({"Quantites_Cartons": "sum",
                  "Montant": "sum"})
            .reset_index()
        )
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
        ndao=f"{donnee_ordre['Montant'].sum():,.2f}".replace(",", " ")+" XOF"
        st.markdown(f"<h2 style='text-align: center;'> CA : {ndao}</h2><br>", unsafe_allow_html=True)
        st.dataframe(donnee_ordre)

    elif sous_menu == "Stock Départ" and periode == "Jour":
        st.warning("Cette option n'est disponible que pour la vue Semaine.")


    elif sous_menu == "Stock":
        if periode == "Jour":
            donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine) & (Chargement["Date"] == dat)]
        elif periode == "Semaine":
            donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine)]
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)

#-----------------------------------------------------------------#
        st.sidebar.markdown("---")
        password = st.sidebar.text_input("Veuillez entrer le code d'accès", type="password")
        OMAR = st.secrets["credentials"]["omar"]
        MANSOUR = st.secrets["credentials"]["mansour"]
        #OMAR=""
        #MANSOUR=""
        st.markdown(f"<h4 style='text-align: center;'>!---------- Stock restant après les ventes du {datea} ----------!</h4><br>", unsafe_allow_html=True)
        if password in [OMAR, MANSOUR]:
        
            if password == OMAR:
                st.success("Accès autorisé, vous êtes connectés avec les identifiants de "+("OMAR" if password == OMAR else "DJIBRIL"))
                #if sous_menu=="Stock":
                 #       prom = colone[3].selectbox("", ["TATA 1", "TATA 2", "TATA 3","Tous les TATAS"])
                #else:
                    #prom = colone[4].selectbox("", ["TATA 1", "TATA 2", "TATA 3","Tous les TATAS"]) 
            elif password == MANSOUR:
                st.success("Accès autorisé, vous êtes connectés avec les identifiants de MANSOUR")
             #   prom = "TATA 2"
        
            if periode == "Jour" :
                #if prom == "Tous les TATAS":
                 #   stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine)]
                  #  ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement['Numero_semaine'] == semaine) & (Chargement["Date"] <= dat)]
                   # descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == dat)]
                #else:
                    stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine)]
                    ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement['Numero_semaine'] == semaine) & (Chargement["Date"] <= dat)]
                    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == dat)]
           
            elif periode == "Semaine":
                #if prom == "Tous les TATAS":
                 #   stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine)]
                  #  ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement['Numero_semaine'] == semaine)]
                   # min_dat = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()[0]
                    #descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat)]
                #else:
                    stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine)]
                    ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement["Numero_semaine"] == semaine)]
                    min_dat = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()[0]
                    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat)]
            elif periode == "Mois":
                #if prom == "Tous les TATAS":
                 #   stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Mois'] == mois)]
                  #  ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement['Mois'] == mois)]
                   # min_dat = Chargement[Chargement["Mois"] == mois]["Date"].dropna().unique()[0]
                    #descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Mois'] == mois) & (Chargement['Date'] == min_dat)]
                #else:
                    stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Mois'] == mois)]
                    ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement["Mois"] == mois)]
                    min_dat = Chargement[Chargement["Mois"] == mois]["Date"].dropna().unique()[0]
                    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Mois'] == mois) & (Chargement['Date'] == min_dat)]
            # Regrouper par tata et produit
            #if prom == "Tous les TATAS":
             #   stock_init = stock_lundi.groupby(['Produit'])['Quantites_Cartons'].sum()
              #  ventes_total = ventes.groupby(['Produit'])['Quantites_Cartons'].sum()
               # stock_descente = descente.groupby(['Produit'])['Quantites_Cartons'].sum()
                
                #stock_Theorique = stock_init.subtract(ventes_total, fill_value=0)

                #df_final = stock_Theorique.reset_index().rename(columns={'Quantites_Cartons': 'Stock Théorique'})
                #df_final['Stock Restant'] = df_final.apply(
                 #   lambda row: stock_descente.get((row['Produit']), 0), axis=1
                #)
            #else:
            stock_init = stock_lundi.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()
            ventes_total = ventes.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()
            stock_descente = descente.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

            stock_Theorique = stock_init.subtract(ventes_total, fill_value=0)

            df_final = stock_Theorique.reset_index().rename(columns={'Quantites_Cartons': 'Stock Théorique'})
            df_final['Stock Restant'] = df_final.apply(
                lambda row: stock_descente.get((row['tata'], row['Produit']), 0), axis=1
            )
                
            df_final['Stock Théorique'] = df_final['Stock Théorique'].astype(float).round(2)
            df_final['Stock Restant'] = df_final['Stock Restant'].astype(float).round(2)

            df_final['Statut'] = df_final.apply(
                lambda row: 'OK' if row['Stock Théorique'] == row['Stock Restant'] else 'Différence',
                axis=1
            )
            
            #if prom == "Tous les TATAS":
             #   st.dataframe(df_final)
              #  donn = df_final[["Produit", "Stock Restant"]].copy()
               # donn["TATA"] = "Tous les TATAS"
            #else:
            df_final1 = df_final.drop("tata", axis=1).copy()
            st.dataframe(df_final1)
            donn = df_final[["tata", "Produit", "Stock Restant"]].sort_values(by=["tata"], ascending=False)
            donn = donn.rename(columns={"tata": "TATA", "Produit": "Produit", "Stock Restant": "Stock Restant"})

        #-----------------------------------------------------------------#
        #---------------------------- Rapport de Omar et Tous les TATAS ---#
            #if prom == "Tous les TATAS":
             #   donnee_agr_total = donne_vente.groupby(["Produit"]).agg({"Quantites_Cartons": "sum"}).reset_index()
              #  donnee_agr_total["TATA"] = "Tous les TATAS"
               # donnee_ordr = donnee_agr_total
            #else:
            #===block else ========
            donnee_agr = (
                donne_vente.groupby(["tata","Produit"])
                .agg({"Quantites_Cartons": "sum"})
                .reset_index()
            )
            donnee_agr = donnee_agr.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités vendues"
                }
            )
            donnee_ordr = donnee_agr.sort_values(by=["TATA"], ascending=False)

            #===block else ========


            st.markdown(f"<br><h4 style='text-align: center;'>!---------- Rapport des ventes du {datea} ----------!</h4>", unsafe_allow_html=True)
            
            #if prom == "Tous les TATAS":
             #   donne_vente_sum = donne_vente.groupby(["Produit"])["Quantites_Cartons"].sum().reset_index()
              #  donne_vente_sum = donne_vente_sum.rename(columns={"Quantites_Cartons": "Quantités vendues"})
               # donnee_ordr = pd.merge(donn, donne_vente_sum, on=["Produit"], how="left")
                #if "TATA" in donnee_ordr.columns:
                 #   donnee_ordr = donnee_ordr.drop("TATA", axis=1)
            #else:
            donnee_ordr = pd.merge(donn, donnee_ordr, on=["TATA", "Produit"], how="left")

            #if prom == "Tous les TATAS":
            filtre = donnee_ordr.copy()
            #else:
                #filtre = donnee_ordr[(donnee_ordr["TATA"] == prom)]
                
            filtre['Quantités vendues'] = filtre['Quantités vendues'].fillna(0)
            
            quantite_total = filtre['Quantités vendues'].sum().round(2)
            stock_restant_total = filtre['Stock Restant'].sum().round(2)
            
            total_row = {
                "Produit": "TOTAL", 
                "Stock Restant": stock_restant_total,
                "Quantités vendues": quantite_total
            }
            #if prom != "Tous les TATAS":
             #   total_row["TATA"] = ""

            df_final_total = pd.concat([filtre, pd.DataFrame([total_row])], ignore_index=True)
            df_final_total["Stock Restant"] = df_final_total["Stock Restant"].round(2)
            df_final_total["Quantités vendues"] = df_final_total["Quantités vendues"].round(2)
            
            if "TATA" in df_final_total.columns:
                df_final_total1 = df_final_total.drop("TATA", axis=1).copy()
            else:
                df_final_total1 = df_final_total.copy()

            def generate_png_report(df, date_str, zone_str, nb_promoteurs, commentaire,chiffre_affaires):
                fig, ax = plt.subplots(figsize=(12, len(df) * 0.6+1.5))
                ax.axis('off')
                if commentaire:
                    comment_box = FancyBboxPatch(
                        (0.63, 0.78),
                        0.35,
                        0.18,
                        boxstyle="round,pad=0.01",
                        transform=ax.transAxes,
                        linewidth=1,
                        edgecolor='#008000',
                        facecolor='#f0f0f0',
                        zorder=1
                    )
                    ax.add_patch(comment_box)
                wrapped_comment = textwrap.fill(commentaire, width=45)
                ax.text(0.8, 0.88, wrapped_comment,
                transform=ax.transAxes,
                fontsize=11,
                weight='bold',
                va='center',
                ha='center',
                style='italic',
                color='red',
                wrap=True,
                zorder=2) 
                
                header_x = 0.001
                header_y = 0.76
                header_width = 0.996
                header_height = 0.24

            
                rect = Rectangle(
                    (header_x, header_y),
                    header_width,
                    header_height,
                    transform=ax.transAxes,
                    fill=False,
                    edgecolor='#008000',
                    linewidth=1.8
                )
                ax.add_patch(rect)

                plt.text(0.45, 0.95, f"Rapport Promotion - ANDE", ha='center', fontsize=14, transform=ax.transAxes, weight='bold')
                plt.text(0.01, 0.89, f"Date : {date_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
                plt.text(0.01, 0.84, f"Zone : {zone_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
                plt.text(0.01, 0.79, f"Nombre de promoteurs : {nb_promoteurs}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
                # Logo placé au milieu, entre les informations et le commentaire
                chemin_logo = "logo_ande.jpeg"

                try:
                    logo = imread(chemin_logo)

                    # Position du logo dans la zone d'en-tête
                    logo_ax = fig.add_axes([0.43, 0.710, 0.12, 0.12])
                    logo_ax.imshow(logo)
                    logo_ax.axis("off")

                except FileNotFoundError:
                    print(f"Logo introuvable : {chemin_logo}")
                table = ax.table(cellText=df.values,
                                colLabels=df.columns,
                                cellLoc='center',
                                loc='center')
                
                # Mettre les noms des colonnes en gras
                for j in range(len(df.columns)):
                    cell = table[0, j]
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#D9F2E6')  # Vert clair facultatif
                    cell.set_edgecolor('#008000')
                    cell.set_linewidth(1.2)


                table.scale(1, 1.5)
                # Mettre toutes les bordures du tableau en vert
                for cell in table.get_celld().values():
                    cell.set_edgecolor('#008000')
                    cell.set_linewidth(1.2)
                # Réserver un espace en bas pour le chiffre d'affaires
                plt.subplots_adjust(bottom=0.15)


                stock_col_idx = df.columns.get_loc("Stock Restant")
                for i in range(len(df)):
                    val = df.iloc[i, stock_col_idx]
                    if isinstance(val, (int, float)) and val < 10:
                        cell = table[i + 1, stock_col_idx]
                        cell.set_text_props(color='white', weight='bold')
                        cell.set_facecolor('#FF5C5C')
                        
                total_row_index = len(df)
                for j in range(len(df.columns)):
                    cell = table[total_row_index, j]
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor("#74E9A3")

                
                # Chiffre d'affaires réalisé, centré sous le tableau
                if password != OMAR:
                    chiffre_affaires_formate = f"{chiffre_affaires:,.0f}".replace(",", " ")

                    fig.text(
                        0.5, 0.055,
                        f"Chiffre d'affaires réalisé : {chiffre_affaires_formate} FCFA",
                        ha="center",
                        va="center",
                        fontsize=16,
                        weight="bold",
                        color="#006400",
                        bbox=dict(
                            boxstyle="round,pad=0.4",
                            facecolor="#E8F5E9",
                            edgecolor="#74E9A3"
                        )
                    )
                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight', dpi=200)
                plt.close()
                buffer.seek(0)
                return buffer

            if periode == "Jour":
                #if prom == "Tous les TATAS":
                 #   zone_str = "Toutes les zones"
                  #  nb_promoteurs = len(Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                   # commente = ["Rapport global Tous les TATAS"]
                #else:
                    zone_vals = Chargement[ (Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat)]["zone"].dropna().unique()
                    zone_str = str(zone_vals[0]) if len(zone_vals) > 0 else "Non définie"
                    nb_promoteurs = len(Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                    commente = Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat)]["Commentaire"].dropna().unique().tolist()
                    ca_realise = Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat) & (Chargement['Operation'] == "Vente")]["Montant"].sum()
            elif periode == "Semaine":
                #if prom == "Tous les TATAS":
                 #   zone_str = "Toutes les zones"
                  #  nb_promoteurs = len(Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                   # commente = ["Rapport global Tous les TATAS"]
                #else:
                    zone_vals = Chargement[(Chargement["Numero_semaine"] == semaine)]["zone"].dropna().unique()
                    zone_str = str(zone_vals[0]) if len(zone_vals) > 0 else "Non définie"
                    nb_promoteurs = len(Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                    commente = Chargement[(Chargement["Numero_semaine"] == semaine)]["Commentaire"].dropna().unique().tolist()
                    ca_realise = Chargement[(Chargement["Numero_semaine"] == semaine) & (Chargement['Operation'] == "Vente")]["Montant"].sum()
            elif periode == "Mois":
                #if prom == "Tous les TATAS":
                 #   zone_str = "Toutes les zones"
                  #  nb_promoteurs = len(Chargement[(Chargement["Mois"] == mois) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                   # commente = ["Rapport global Tous les TATAS"]
                #else:
                    zone_vals = Chargement[(Chargement["Mois"] == mois)]["zone"].dropna().unique()
                    zone_str = str(zone_vals[0]) if len(zone_vals) > 0 else "Non définie"
                    nb_promoteurs = len(Chargement[(Chargement["Mois"] == mois) & (Chargement['Prenom_Nom_Promoteur'] != "Autre") & (Chargement['Prenom_Nom_Promoteur'].notna())]["Prenom_Nom_Promoteur"].unique())
                    commente = Chargement[(Chargement["Mois"] == mois)]["Commentaire"].dropna().unique().tolist()
                    ca_realise = Chargement[(Chargement["Mois"] == mois) & (Chargement['Operation'] == "Vente")]["Montant"].sum()
            if not commente: 
                commente.append("Aucune observation") 

            png_bytes = generate_png_report(df_final_total1, datea, zone_str, nb_promoteurs, commente[0], ca_realise)
            st.image(png_bytes, caption="", use_container_width=True)
            st.download_button(
                label="📥 Télécharger le rapport en PNG",
                data=png_bytes,
                file_name=f"rapport_TATA_du_{datea}.png",
                mime="image/png"
            )
        else:
            st.error("Accès refusé, code d'accès incorrect.")

    elif sous_menu == "Récapitulatif" and periode in ["Semaine", "Mois"]:
        st.markdown(f"<h4 style='text-align: center;'>!---------- Récapitulatif des ventes TATA et RZ du {periode.lower()} {datea} ----------!</h4><br>", unsafe_allow_html=True)
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
        if periode == "Semaine":
            donnee_RZ_Livr= donnee_RZ[(donnee_RZ["Operation"] == "FACTURE") & (donnee_RZ["Semaine"] == semaine)]
            CA_donnee_RZ=donnee_RZ_Livr["Montant"].sum()-donnee_RZ_Livr["Remise"].sum()
            
            min_dat = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()[0]
            #descente_T1 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == "TATA 1")]
            #stock_descente_T1 = descente_T1.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

            descente_T2 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat)]
            stock_descente_T2 = descente_T2.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

            #descente_T3 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == "TATA 3")]
            #stock_descente_T3 = descente_T3.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

        elif periode == "Mois":
            donnee_RZ_Livr= donnee_RZ[(donnee_RZ["Operation"] == "FACTURE") & (donnee_RZ["Mois"] == mois)]
            CA_donnee_RZ=donnee_RZ_Livr["Montant"].sum()-donnee_RZ_Livr["Remise"].sum()

            min_dat = Chargement[Chargement["Mois"] == mois]["Date"].dropna().unique()[0]
            
            descente_T2 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Mois'] == mois) & (Chargement['Date'] == min_dat)]
            stock_descente_T2 = descente_T2.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()


        colonnne= st.columns(2)
        colonnne[0].metric("💴 CA RZ", f"{CA_donnee_RZ:,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("💴 CA RZ + TATA", f"{CA_donnee_RZ+donnee_ordre['Montant A verser'].sum():,.2f}".replace(",", " ")+" XOF")
        colonnne[0].metric("💴 CA TATA", f"{donnee_ordre['Montant A verser'].sum():,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🔢 Quantité vendue", f"{donnee_ordre['Quantités'].sum():,.2f}".replace(",", " "))
        
        ca_restant=descente_T2["Montant"].sum()
        rest=stock_descente_T2.sum()

        colonnne[0].metric("🚐 Transport TATA", f"{transport['Transport'].sum():,.0f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🅿️ Stationnement", f"{stationnement['Stationnement'].sum():,.0f}".replace(",", " ")+" XOF")
        colonnne[0].metric("🏠 **Stock Restant (CA)**", f"{ca_restant:,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🏠 **Quantité Restante (STOCK)**", f"{rest:,.2f}".replace(",", " "))
    
    elif sous_menu == "Récapitulatif" and periode == "Jour":
        st.warning("Cette option n'est disponible que pour la vue Semaine.")
    
#-----------------------------------------------------------------#
elif menu == "DETAIL":
    donnee = donne_vente
    #menu_sambou = st.sidebar.selectbox("TATAS", ["TATA 1","TATA 2", "TATA 3"])
    #donnee1 = donnee[(donnee["tata"] == menu_sambou)]
    donnee1 = donnee.copy()
    nom_promo=donnee1["Prenom_Nom_Promoteur"].dropna().unique().tolist()
    produit_list=donnee1[donnee1["Operation"] == "Vente"]["Produit"].dropna().unique().tolist()
    tat_indi= st.sidebar.selectbox("Option", ["TATA","INDIVIDUEL"])
    if tat_indi == "INDIVIDUEL":
        choix= st.sidebar.selectbox("Votre choix", ["Promoteur","Produit"])
        if choix == "Promoteur":
            if periode == "Jour":
                promoteur = st.sidebar.selectbox("Promoteurs", nom_promo)
                donnee2 = donnee1[(donnee["Prenom_Nom_Promoteur"] == promoteur)]
                donne_vente = donnee2[donnee2["Operation"] == "Vente"]
                if promoteur=="Autre":
                    donnee_agre = (
                        donne_vente.groupby(["tata","zone","Precisez","Produit"])
                        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
                        .reset_index()
                    )
                    st.subheader("Ventes des promoteurs")
                    donnee_agre = donnee_agre.rename(
                        columns={
                            "tata": "TATA",
                            "Precisez": "RZ",
                            "Quantites_Cartons": "Quantités",
                            "Montant": "Montant A verser",
                        }
                    )
                    donnee_ordre = donnee_agre.sort_values(by=["TATA","RZ"], ascending=False)
                else:
                    donnee_agre = (
                        donne_vente.groupby(["tata","zone","Prenom_Nom_Promoteur","Produit"])
                        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
                        .reset_index()
                    )
                    st.subheader("Ventes des promoteurs")
                    donnee_agre = donnee_agre.rename(
                        columns={
                            "tata": "TATA",
                            "Prenom_Nom_Promoteur": "Promoteur",
                            "Quantites_Cartons": "Quantités",
                            "Montant": "Montant A verser",
                        }
                    )
                    donnee_ordre = donnee_agre.sort_values(by=["TATA","Promoteur"], ascending=False)
            elif periode == "Semaine":
                donne_vente = donnee1[donnee1["Operation"] == "Vente"]
                donnee_agre = (
                    donne_vente.groupby(["tata","Prenom_Nom_Promoteur"])
                    .agg({"Montant": "sum"})
                    .reset_index()
                )
                st.subheader("Ventes de promoteurs")
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Montant": "CA SEMAINE",
                    }
                )
                donnee_ordre = donnee_agre.sort_values(by=["Promoteur"], ascending=False)
            elif periode == "Mois":
                donne_vente = donnee1[donnee1["Operation"] == "Vente"]
                donnee_agre = (
                    donne_vente.groupby(["tata","Prenom_Nom_Promoteur"])
                    .agg({"Montant": "sum"})
                    .reset_index()
                )
                st.subheader("Ventes de promoteurs")
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Montant": "CA MOIS",
                    }
                )
                donnee_ordre = donnee_agre.sort_values(by=["Promoteur"], ascending=False)
        elif choix == "Produit":
            menu_prin=st.sidebar.selectbox("PRODUITS", produit_list)
            donnee2 = donnee1[(donnee["Produit"] == menu_prin)]
            donne_vente = donnee2[donnee2["Operation"] == "Vente"]
            donnee_agre = (
                donne_vente.groupby(["tata","zone","Prenom_Nom_Promoteur","Produit"])
                .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
                .reset_index()
            )
            st.subheader("Ventes de promoteurs")
            if periode == "Semaine":
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Quantites_Cartons": "Quantités",
                        "Montant": "CA SEMAINE",
                    }
                )
            elif periode == "Jour":
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Quantites_Cartons": "Quantités",
                        "Montant": "Montant A verser",
                    }
                )
            donnee_ordre = donnee_agre.sort_values(by=["TATA","Promoteur"], ascending=False)

    elif tat_indi == "TATA":
        #donnee2 = donnee1[(donnee["tata"] == menu_sambou)]
        donnee2 = donnee1.copy()
        donne_vente = donnee2[donnee2["Operation"] == "Vente"]
        donnee_agre = (
            donne_vente.groupby(["tata","zone","Produit"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        st.subheader("Ventes de promoteurs")
        if periode == "Semaine":
            donnee_agre = donnee_agre.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités",
                    "Montant": "CA SEMAINE",
                }
            )
        elif periode == "Jour":
            donnee_agre = donnee_agre.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités",
                    "Montant": "Montant A verser",
                }
            )
        elif periode == "Mois":
            donnee_agre = donnee_agre.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités",
                    "Montant": "CA MOIS",
                }
            )
        donnee_ordre = donnee_agre.sort_values(by=["TATA"], ascending=False)
        
    st.dataframe(donnee_ordre.drop("TATA", axis=1))
    
    colone= st.columns(3)
    if periode== "Semaine":
        colone[1].metric("💴 CA TATA", f"{donnee_ordre['CA SEMAINE'].sum():,.0f}".replace(",", " ")+" XOF")
    elif periode == "Jour":
        colone[1].metric("💴 CA TATA", f"{donnee_ordre['Montant A verser'].sum():,.0f}".replace(",", " ")+" XOF")
    elif periode == "Mois":
        colone[1].metric("💴 CA TATA", f"{donnee_ordre['CA MOIS'].sum():,.0f}".replace(",", " ")+" XOF")

#--------------------------FICHE DE PAIE---------------------------------------#
elif menu == "FICHE":
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from io import BytesIO
    import os
    #Donnees_Mens = pd.read_excel("Donnees_Mensuelle.xlsx", engine='openpyxl')
    Donnees_Mens = Chargement[Chargement["Operation"] == "Vente"]
    if periode == "Semaine":
        st.sidebar.markdown("---")
        password = st.sidebar.text_input("Code d'accès requis", type="password")
        
        OMAR = st.secrets["credentials"]["omar"]
        MANSOUR = st.secrets["credentials"]["mansour"]
        #OMAR=""
        #MANSOUR=""
        if password in [MANSOUR, OMAR]:
            st.success(f"ACCES AUTORISE POUR {password}")
            data_semaine = Donnees_Mens[
                (Donnees_Mens["Numero_semaine"] == semaine) &
                (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_Mens["Prenom_Nom_Promoteur"].notna())
            ]
        elif password == "":
            st.warning("Veuillez entrer un code d'accès pour continuer.")
            st.stop()
        else:
            st.error("Code d'accès incorrect. Veuillez réessayer.")
            st.stop()

        if data_semaine.empty or data_semaine["Date"].isna().all():
            st.warning(f"Les informations de la semaine {semaine} ne sont pas encore disponible")
            st.stop()
        jour_min = data_semaine["Date"].min().day
        jour_max = data_semaine["Date"].max().day
        mois_num = data_semaine["Date"].min().month
        mois_max = data_semaine["Date"].max().month
        annee=data_semaine["Date"].min().year

        mois_fr = {
            1: "JANVIER", 2: "FÉVRIER", 3: "MARS",
            4: "AVRIL", 5: "MAI", 6: "JUIN",
            7: "JUILLET", 8: "AOÛT", 9: "SEPTEMBRE",
            10: "OCTOBRE", 11: "NOVEMBRE", 12: "DÉCEMBRE"
        }
        mois_lettre = mois_fr[mois_num]
        mois_lettre_max = mois_fr[mois_max]
        if mois_num != mois_max:
            texte_periode = f"DU {jour_min} {mois_lettre} AU {jour_max} {mois_lettre_max} {annee}"
        else:
            texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
        st.markdown(f"""<h4 style='text-align: center;'>FICHE DE PAIE TATA {texte_periode}</h4>""", unsafe_allow_html=True)

        suivi = data_semaine.groupby(
            ['Prenom_Nom_Promoteur']
        )['Date'].nunique().reset_index()

        suivi.rename(columns={
            'Prenom_Nom_Promoteur': 'Nom',
            'Date': 'Jours travaillés'
        }, inplace=True)

        suivi["Salaire"] = suivi["Jours travaillés"].apply(lambda x: 5000 * x)

        total = suivi['Salaire'].sum()

        affichage=suivi.copy()
        affichage["Nom"] = affichage["Nom"].str.upper()
        st.dataframe(affichage)
        st.metric("💰 TOTAL À PAYER TATA", f"{total:,.0f} XOF".replace(",", " "))

        def generate_pdf_paie(df, jour_min, jour_max, mois_lettre, annee, mois_lettre_max, mois_num, mois_max):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)

            styles = getSampleStyleSheet()
            elements = []
            if mois_num != mois_max:
                texte_periode = f"DU {jour_min} {mois_lettre} AU {jour_max} {mois_lettre_max} {annee}"
            else:
                texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
            logo_path = "logo_ande.jpeg"

            if os.path.exists(logo_path):
                logo = Image(logo_path, width=2.5*cm, height=1.5*cm)
            else:
                logo = Paragraph("", styles["Normal"])

            tata_text = Paragraph(f"<b>TATA</b>", styles["Heading2"])

            header_table = Table(
                [[logo, tata_text]],
                colWidths=[14*cm, 3*cm]
            )

            header_table.setStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (1,0), (1,0), 'LEFT'),
            ])

            elements.append(header_table)
            elements.append(Spacer(1, 5))

            style_titre = ParagraphStyle(
                name="TitrePerso",
                parent=styles["Title"],
                fontSize=12,
                leading=14,
                alignment=1
            )

            titre = Table(
                [[Paragraph(
                    f"<b>ACTIVATION KAMLAC_PAIE SALAIRES FIXES {texte_periode}</b>",
                    style_titre
                )]],
                colWidths=[16.1*cm]
            )

            titre.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ADF0A4")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6),
            ]))

            elements.append(titre)
            elements.append(Spacer(0, 0))

            data = [["PRENOM & NOM", "JOURS TRAVAILLES", "MONTANT PAYE", "SIGNATURE"]]

            for _, row in df.iterrows():
                data.append([
                    row["Nom"].upper(),
                    row["Jours travaillés"],
                    f"{int(row['Salaire']):,}".replace(",", " "),
                    ""
                ])

            table = Table(data, colWidths=[6.5*cm, 4*cm, 3*cm, 2.5*cm])

            table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('BOX', (0,0), (-1,-1), 2, colors.HexColor("#6FCE63")),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D7D2C9")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (1,0), (1,0), colors.HexColor("#6FCE63")),
                ('TEXTCOLOR', (1,0), (1,0), colors.black),
                ('ALIGN',(1,1),(-2,-1),'CENTER'),
                ('ALIGN',(0,0),(-1,0),'CENTER'),
                ('ALIGN',(0,-1),(0,-1),'CENTER'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 8),
            ]))

            elements.append(table)
            doc.build(elements)
            buffer.seek(0)
            return buffer

        df_total = suivi.copy()
        df_total.loc[len(df_total)] = ["TOTAL", "", total]
        
        pdf_file = generate_pdf_paie(df_total, jour_min, jour_max, mois_lettre, annee, mois_lettre_max, mois_num, mois_max)

        if mois_num != mois_max:
            st.download_button(
                label="📥 Télécharger la fiche de paie PDF",
                data=pdf_file,
                file_name=f"FICHE DE PAIE TATA DU {jour_min:02d} {mois_num} AU {jour_max:02d} {mois_max} {annee}.pdf",
                mime="application/pdf"
            )
        else:
            st.download_button(
                label="📥 Télécharger la fiche de paie PDF",
                data=pdf_file,
                file_name=f"FICHE DE PAIE TATA DU {jour_min:02d} AU {jour_max:02d} {mois_num}.pdf",
                mime="application/pdf"
            )
        
        if password == OMAR:

                donnee_RZ_Livr= donnee_RZ[(donnee_RZ["Operation"] == "FACTURE") & (donnee_RZ["Semaine"] == semaine) & (donnee_RZ["Equipe"] == "RZ")]
                CA_donnee_RZ=donnee_RZ_Livr["Montant"].sum()

                colonnne= st.columns(2)
                colonnne[0].metric("CA RZ", f"{CA_donnee_RZ:,.2f}".replace(",", " ")+" XOF")
                colonnne[1].metric("CA TATA", f"{Donnees_Mens['Montant'].sum():,.2f}".replace(",", " ")+" XOF")
                colonnne[0].metric("CA TOTAL (RZ + TATA)", f"{CA_donnee_RZ+Donnees_Mens['Montant A verser'].sum():,.2f}".replace(",", " ")+" XOF")
                colonnne[1].metric("REMISE", f"{donnee_RZ_Livr["Remise"].sum():,.2f}".replace(",", " ")+" XOF")

                colonnne[0].metric("TRANSPORT TATA", f"{transport['Transport'].sum():,.0f}".replace(",", " ")+" XOF")
                colonnne[1].metric("STATIONNEMENT", f"{stationnement['Stationnement'].sum():,.0f}".replace(",", " ")+" XOF")
                st.markdown("---")
                st.markdown(f"<h4 style='text-align: center;'>SALAIRES TATAS : {total:,.2f}".replace(",", " ")+" XOF</h4>", unsafe_allow_html=True)
                Depenses = transport["Transport"].sum() + stationnement["Stationnement"].sum() + total
                st.markdown(f"<h3 style='text-align: center;'>SALAIRES + TRANSPORT + STATIONNEMENT : {Depenses:,.2f}".replace(",", " ")+" XOF</h3>", unsafe_allow_html=True)
                
                mnt_verser = (CA_donnee_RZ + Donnees_Mens['Montant'].sum()) - (Depenses + donnee_RZ_Livr["Remise"].sum())
                st.markdown(f"<h2 style='text-align: center;'>MONTANT À VERSER PAR OMAR : {mnt_verser:,.2f}".replace(",", " ")+" XOF</h2>", unsafe_allow_html=True)
    elif periode == "Mois":
        st.sidebar.markdown("---")
        password = st.sidebar.text_input("Code d'accès requis", type="password")
        
        OMAR = st.secrets["credentials"]["omar"]
        MANSOUR = st.secrets["credentials"]["mansour"]
        #OMAR=""
        #MANSOUR=""
        if password in [MANSOUR, OMAR]:
            st.success(f"ACCES AUTORISE POUR {password}")
            data_mois = Donnees_Mens[
                (Donnees_Mens["Mois"] == mois) &
                (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_Mens["Prenom_Nom_Promoteur"].notna())
            ]
        elif password == "":
            st.warning("Veuillez entrer un code d'accès pour continuer.")
            st.stop()
        else:
            st.error("Code d'accès incorrect. Veuillez réessayer.")
            st.stop()
        if data_mois.empty or data_mois["Date"].isna().all():
            st.warning(f"Les informations du mois {mois} ne sont pas encore disponible")
            st.stop()
        jour_min = data_mois["Date"].min().day
        jour_max = data_mois["Date"].max().day
        mois_num = data_mois["Date"].min().month
        mois_max = data_mois["Date"].max().month
        annee=data_mois["Date"].min().year
        mois_fr = {
            1: "JANVIER", 2: "FÉVRIER", 3: "MARS",
            4: "AVRIL", 5: "MAI", 6: "JUIN",
            7: "JUILLET", 8: "AOÛT", 9: "SEPTEMBRE",
            10: "OCTOBRE", 11: "NOVEMBRE", 12: "DÉCEMBRE"
        }
        mois_lettre = mois_fr[mois_num]
        mois_lettre_max = mois_fr[mois_max]
        if mois_num != mois_max:
            texte_periode = f"DU {jour_min} {mois_lettre} AU {jour_max} {mois_lettre_max} {annee}"
        else:
            texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
        st.markdown(f"""<h4 style='text-align: center;'>FICHE DE PAIE TATA {texte_periode}</h4>""", unsafe_allow_html=True)
        suivi = data_mois.groupby(
            ['Prenom_Nom_Promoteur']
        )['Date'].nunique().reset_index()
        suivi.rename(columns={
            "Prenom_Nom_Promoteur": "Nom",
            "Date": "Jours travaillés"
        }, inplace=True)
        suivi["Salaire"] = suivi["Jours travaillés"].apply(lambda x: 5000 * x)
        total = suivi["Salaire"].sum()
        affichage=suivi.copy()
        affichage["Nom"] = affichage["Nom"].str.upper()
        st.dataframe(affichage)
        st.metric("💰 TOTAL À PAYER TATA", f"{total:,.0f} FCFA".replace(",", " "))

        def generate_pdf_paie(df, jour_min, jour_max, mois_lettre, annee, mois_lettre_max, mois_num, mois_max):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            elements = []
            if mois_num != mois_max:
                texte_periode = f"DU {jour_min} {mois_lettre} AU {jour_max} {mois_lettre_max} {annee}"
            else:
                texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
            logo_path = "logo_ande.jpeg"
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=1.0*cm, height=1.0*cm)
            else:
                logo = Paragraph("", styles["Normal"])
            tata_text = Paragraph(f"<b>TATA</b>", styles["Heading2"])
            header_table = Table(
                [[logo, tata_text]],
                colWidths=[13*cm, 3*cm]
            )
            header_table.setStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (1,0), (1,0), 'LEFT'),
            ])
            elements.append(header_table)
            elements.append(Spacer(1, 5))
            style_titre = ParagraphStyle(
                name="TitrePerso",
                parent=styles["Title"],
                fontSize=12,
                leading=14,
                alignment=1
            )
            titre = Table(
                [[Paragraph(
                    f"<b>ACTIVATION KAMLAC_PAIE SALAIRES FIXES {texte_periode}</b>",
                    style_titre
                )]],
                colWidths=[16.1*cm]
            )
            titre.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#AAFA9F")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(titre)
            elements.append(Spacer(0, 0))
            data = [["PRENOM & NOM", "JOURS TRAVAILLES", "MONTANT PAYE", "SIGNATURE"]]
            for _, row in df.iterrows():
                data.append([
                    row["Nom"].upper(),
                    row["Jours travaillés"],
                    f"{int(row['Salaire']):,}".replace(",", " "),
                    ""
                ])
            table = Table(data, colWidths=[6.5*cm, 4*cm, 3*cm, 2.5*cm])
            table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('BOX', (0,0), (-1,-1), 2, colors.HexColor("#AAFA9F")),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D7D2C9")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (1,0), (1,0), colors.HexColor("#CEF3C1")),
                ('TEXTCOLOR', (1,0), (1,0), colors.black),
                ('ALIGN',(1,1),(-2,-1),'CENTER'),
                ('ALIGN',(0,0),(-1,0),'CENTER'),
                ('ALIGN',(0,-1),(0,-1),'CENTER'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(table)
            doc.build(elements)
            buffer.seek(0)
            return buffer
        df_total = suivi.copy()
        df_total.loc[len(df_total)] = ["TOTAL", "", total]
        pdf_file = generate_pdf_paie(df_total, jour_min, jour_max, mois_lettre, annee, mois_lettre_max, mois_num, mois_max)
        if mois_num != mois_max:
            st.download_button(
                label="📥 Télécharger la fiche de paie PDF",
                data=pdf_file,
                file_name=f"FICHE DE PAIE TATA DU {jour_min:02d} {mois_num} AU {jour_max:02d} {mois_max} {annee}.pdf",
                mime="application/pdf"
            )
        else:
            st.download_button(
                label="📥 Télécharger la fiche de paie PDF",
                data=pdf_file,
                file_name=f"FICHE DE PAIE TATA DU {jour_min:02d} AU {jour_max:02d} {mois_num}.pdf",
                mime="application/pdf"
            )
        if password == OMAR:
                donnee_RZ_Livr= donnee_RZ[(donnee_RZ["Operation"] == "FACTURE") & (donnee_RZ["Mois"] == mois) & (donnee_RZ["Equipe"] == "RZ")]
                CA_donnee_RZ=donnee_RZ_Livr["Montant"].sum()

                colonnne= st.columns(3)
                colonnne[0].metric("CA RZ", f"{CA_donnee_RZ:,.2f}".replace(",", " ")+" XOF")
                colonnne[1].metric("CA TATA", f"{Donnees_Mens['Montant'].sum():,.2f}".replace(",", " ")+" XOF")
                colonnne[2].metric("CA TOTAL (RZ + TATA)", f"{CA_donnee_RZ+Donnees_Mens['Montant'].sum():,.2f}".replace(",", " ")+" XOF")
                colonnne[0].metric("REMISE", f"{donnee_RZ_Livr["Remise"].sum():,.2f}".replace(",", " ")+" XOF")

                colonnne[1].metric("TRANSPORT TATA", f"{transport['Transport'].sum():,.0f}".replace(",", " ")+" XOF")
                colonnne[2].metric("STATIONNEMENT", f"{stationnement['Stationnement'].sum():,.0f}".replace(",", " ")+" XOF")
                st.markdown("---")
                st.markdown(f"<h4 style='text-align: center;'>SALAIRES TATAS : {total:,.2f}".replace(",", " ")+" XOF</h4>", unsafe_allow_html=True)
                Depenses = transport["Transport"].sum() + stationnement["Stationnement"].sum() + total
                st.markdown(f"<h3 style='text-align: center;'>SALAIRES + TRANSPORT + STATIONNEMENT : {Depenses:,.2f}".replace(",", " ")+" XOF</h3>", unsafe_allow_html=True)
                
                mnt_verser = (CA_donnee_RZ + Donnees_Mens['Montant'].sum()) - (Depenses + donnee_RZ_Livr["Remise"].sum())
                st.markdown(f"<h2 style='text-align: center;'>MONTANT À VERSER PAR OMAR : {mnt_verser:,.2f}".replace(",", " ")+" XOF</h2>", unsafe_allow_html=True)

    else:
        st.warning("Disponible uniquement en mode Semaine")