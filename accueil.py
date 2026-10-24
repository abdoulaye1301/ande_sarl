import streamlit as st
import pandas as pd
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch
import textwrap
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from io import BytesIO
from matplotlib.image import imread
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import os
from connexion import login

def page_accueil():
    st.write("BIENVENUE DANS LA PAGE D'ACCUEIL DE LA SOCIETE ANDE")
