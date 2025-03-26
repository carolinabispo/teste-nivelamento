import webbrowser
import requests
import zipfile
import PyPDF2
import tabula
import pandas as pd
import csv


# acesso ao navegador default do user
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
webbrowser.open(url)

url_anexo1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
url_anexo2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

# funçao de download dos anexos
def download_pdf(url, filename):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Arquivo {filename} salvo com sucesso!")
    else:
        print(f"Erro ao baixar {filename}: Status {response.status_code}")
  
download_pdf(url_anexo1, "Anexo_I_Rol_de_procedimentos_e_eventos_em_saude.2024.pdf")
download_pdf(url_anexo2, "Anexo_II_Rol_de_procedimentos_e_eventos_em_saude.2025.pdf")


# funçao para compactar em zip
def compactar(file):

    with zipfile.ZipFile("anexos.zip", "a") as zip:
        zip.write(file)
       
compactar("Anexo_I_Rol_de_procedimentos_e_eventos_em_saude.2024.pdf")
compactar("Anexo_II_Rol_de_procedimentos_e_eventos_em_saude.2025.pdf")

# abrir o arquivo pdf
pdf_file = open("Anexo_I_Rol_de_procedimentos_e_eventos_em_saude.2024.pdf", 'rb')

pdf = PyPDF2.PdfReader(pdf_file)
total_paginas = len(pdf.pages)

# peço que faça a extração do dados da paginas 3 em diante
tabela_colum = tabula.read_pdf(pdf_file, pages=f"3-{total_paginas}")


# modificação de colunas para forma não abreviada
for linhas in tabela_colum:
    linhas.rename(columns = {"OD":"Seg. Odontológica", 
    "AMB" : "Seg. Ambulatorial"} , inplace = True)

# criação do arquivo csv apos modificações
def criar_csv(file):

    with open(file, 'w', newline='', encoding="utf-8" ) as file:
        writer = csv.writer(file)

        for tabela in tabela_colum:
            writer.writerow(tabela.columns) 
            writer.writerows(tabela.values.tolist())

criar_csv("tabelas_anexo.csv")

# compactação do arquivo csv
with zipfile.ZipFile("Teste_Carolina_Bispo.zip", "a") as zip:
    zip.write("tabelas_anexo.csv")

