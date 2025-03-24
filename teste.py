import webbrowser
import requests
import zipfile

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
webbrowser.open(url)

url_anexo1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
url_anexo2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

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

# compactar em zip
def compactar(file):

    with zipfile.ZipFile("anexos.zip", "a") as zip:
        zip.write(file)
       
       
compactar("Anexo_I_Rol_de_procedimentos_e_eventos_em_saude.2024.pdf")
compactar("Anexo_II_Rol_de_procedimentos_e_eventos_em_saude.2025.pdf")