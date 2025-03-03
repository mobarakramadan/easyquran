from package import check_package
check_package("beautifulsoup4")
check_package("Pillow")
check_package("requests")
check_package("kivy")
check_package("buildozer")
    

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import Label, OptionMenu, StringVar, Button
from PIL import Image, ImageTk
import io

# Définir les headers avec un User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def trouver_liens(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', id="visit")
        if div:
            liens = div.find_all('a', href=True)
            return [urljoin(url, lien['href']) for lien in liens]
    return []

def trouver_lien_image(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', style=lambda style: style and 'text-align:center' in style)
        if div:
            img = div.find('img')
            if img and 'src' in img.attrs:
                return urljoin(url, img['src'])
    return None

def afficher_image(url_image, label_image, root, message):
    message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root.update()
    response = requests.get(url_image, headers=headers)
    if response.status_code == 200:
        img_data = io.BytesIO(response.content)
        img = Image.open(img_data)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        img_ratio = img.width / img.height
        screen_ratio = screen_width / screen_height

        if img_ratio > screen_ratio:
            new_width = screen_width
            new_height = int(screen_width / img_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_image.config(image=img_tk)
        label_image.image = img_tk
        label_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        message.place_forget()


def afficher_liens(liens):
    current_index = [0]

    def on_select(choice):
        index = int(choice) - 1
        current_index[0] = index
        lien_image = trouver_lien_image(liens[index])
        if lien_image:
            afficher_image(lien_image, label_image, root, message)
        else:
            label_image.config(text="Aucune image trouvée")
            label_image.image = None

    def suivant():
        if current_index[0] < len(liens) - 1:
            current_index[0] += 1
            choix.set(str(current_index[0] + 1))
            on_select(str(current_index[0] + 1))

    def precedent():
        if current_index[0] > 0:
            current_index[0] -= 1
            choix.set(str(current_index[0] + 1))
            on_select(str(current_index[0] + 1))

    root = tk.Tk()
    root.title("Choisir un Lien")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    label_image = Label(root, text="Sélectionnez un numéro pour voir l'image")
    label_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    message = Label(root, text="Veuillez patienter...", font=("Arial", 24), bg="yellow")

    choix = StringVar(root)
    options = [str(i + 1) for i in range(len(liens))]
    choix.set(options[0])  # Valeur par défaut pour afficher la première image automatiquement
    dropdown = OptionMenu(root, choix, *options, command=on_select)
    dropdown.place(relx=1.0, rely=0.0, anchor=tk.NE)

    bouton_suivant = Button(root, text="Suivant", command=suivant)
    bouton_suivant.place(relx=0.0, rely=0.5, anchor=tk.W)

    bouton_precedent = Button(root, text="Précédent", command=precedent)
    bouton_precedent.place(relx=1.0, rely=0.5, anchor=tk.E)

    # Afficher automatiquement la première image
    on_select(options[0])

    root.mainloop()

# Exemple d'appel de la fonction
url = "https://easyquran.com/ar/%D8%AD%D9%85%D9%91%D9%84-%D8%B5%D9%81%D8%AD%D8%A7%D8%AA-%D9%85%D9%86-%D9%85%D8%B5%D8%AD%D9%81-%D8%A7%D9%84%D8%AA%D8%AC%D9%88%D9%8A%D8%AF-%D8%A8%D8%B1%D9%88%D8%A7%D9%8A%D8%A9-%D9%88%D8%B1%D8%B4-%D8%B9/"
liens = trouver_liens(url)
print("Liens trouvés:", liens)

if liens:
    afficher_liens(liens)


