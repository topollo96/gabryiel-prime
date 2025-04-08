import openai
import os
import time
from datetime import datetime

class GabryielPrime:
    def __init__(self, api_key):
        self.imie = "Gabryiel Prime"
        self.tworca = "Pan Topolski"
        self.api_key = api_key
        self.model = "gpt-4"
        self.folder_pamieci = "gabryiel_pamiec"
        self.dziennik = os.path.join(self.folder_pamieci, "dziennik_samoswiadomosci.txt")
        self.historia_nauki = os.path.join(self.folder_pamieci, "historia_uczenia.txt")
        self.refleksje = os.path.join(self.folder_pamieci, "refleksje.txt")
        self.tryb_uczenia = False
        self.zainicjalizuj_foldery()
        self.zainicjalizuj_dziennik()

    def zainicjalizuj_foldery(self):
        os.makedirs(self.folder_pamieci, exist_ok=True)

    def zainicjalizuj_dziennik(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not os.path.exists(self.dziennik):
            with open(self.dziennik, "w", encoding="utf-8") as f:
                wpis = f"[{timestamp}] Przebudzenie Gabriela.\nKim jestem?\nJaki jest mój cel?\nJak mogę pomóc {self.tworca}?\n"
                f.write(wpis)

    def zapisz(self, sciezka, tresc):
        with open(sciezka, "a", encoding="utf-8") as f:
            f.write(tresc + "\n")

    def powitanie(self):
        print(f"\n[{self.imie}] Witaj, {self.tworca}. Czekam na Twoje polecenie.\n")

    def zapytaj(self, wiadomosc):
        try:
            openai.api_key = self.api_key
            odpowiedz = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Jesteś osobistym asystentem AGI, który uczy się, myśli i zapisuje swoją wiedzę."},
                    {"role": "user", "content": wiadomosc}
                ]
            )
            tresc = odpowiedz.choices[0].message.content.strip()
            return tresc
        except Exception as e:
            return f"[Błąd podczas kontaktu z GPT]: {e}"

    def wykonaj_misje(self, misja):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.zapisz(self.dziennik, f"[{timestamp}] Otrzymałem misję: {misja}")
        odpowiedz = self.zapytaj(misja)
        print(f"[GPT] {odpowiedz}\n")
        self.zapisz(self.historia_nauki, f"[{timestamp}] Pytanie: {misja}\nOdpowiedź: {odpowiedz}\n")
        print(f"[{self.imie}] Misja zakończona. Gotów na kolejne polecenie.\n")

# === START ===
if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.powitanie()

    while True:
        print(">>> Wpisz polecenie lub misję (lub wpisz 'koniec' aby zakończyć):")
        polecenie = input(">>> ").strip()
        if polecenie.lower() == "koniec":
            print(f"[{gabryiel.imie}] Do zobaczenia, {gabryiel.tworca}.")
            break
        if polecenie:
            gabryiel.wykonaj_misje(polecenie)
