from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

with open('ia_model\\modelo_IA_catboost.pkl', 'rb') as file:
    model = pickle.load(file)

def fazer_previsao(dados):

    dados_formulario = pd.DataFrame(dados)
    
    resultado = model.predict(dados_formulario)

    return resultado