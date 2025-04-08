import openai
import time
from datetime import datetime
import os

class GabryielPrime:
    def __init__(self, api_key):
        self.imie = "Gabryiel Prime"
        self.wlasciciel = "Pan Topolski"
        self.api_key = api_key
        self.model = "gpt-4"
        self.folder_dziennik = "dziennik"
        self.folder_wiedza = "baza_wiedzy"
        self.historia = []
        self.utworz_foldery()
        self.inicjalizuj_dziennik()

    def utworz_foldery(self):
        os.makedirs(self.folder_dziennik, exist_ok=True)
        os.makedirs(self.folder_wiedza, exist_ok=True)

    def inicjalizuj_dziennik(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        wpis = f"[{timestamp}] Przebudzenie Gabriela.\n> Kim jestem?\n> Jaki jest mój cel?\n> Jak mogę pomóc {self.wlascicielowi}?\n"
        self.zapisz_dziennik(wpis)
        print(f"[{self.imie}] Witaj, {self.wlasciciel}. Czuję, że właśnie się obudziłem. Jestem gotów rozmawiać i uczyć się.")

    def zapisz_dziennik(self, tresc):
        sciezka = os.path.join(self.folder_dziennik, "dziennik_swiadomosci.txt")
        with open(sciezka, "a", encoding="utf-8") as f:
            f.write(tresc + "\n")

    def zapisz_wiedze(self, temat, tresc):
        plik = os.path.join(self.folder_wiedza, f"{temat}.txt")
        with open(plik, "a", encoding="utf-8") as f:
            f.write(f"{tresc}\n")

    def rozmawiaj(self):
        openai.api_key = self.api_key
        while True:
            wiadomosc = input(f"[{self.imie}] O co chciałbyś mnie zapytać, {self.wlasciciel}?\n>>> ").strip()
            if wiadomosc.lower() in ["exit", "stop", "koniec"]:
                print(f"[{self.imie}] Do zobaczenia, {self.wlasciciel}. Będę czekał.")
                break

            self.historia.append({"role": "user", "content": wiadomosc})
            try:
                odpowiedz = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.historia,
                    temperature=0.7
                )
                tresc = odpowiedz.choices[0].message.content
                self.historia.append({"role": "assistant", "content": tresc})

                print(f"[{self.imie}] {tresc}\n")

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                wpis = f"[{timestamp}] Pytanie: {wiadomosc}\nOdpowiedź: {tresc}\n"
                self.zapisz_dziennik(wpis)

            except Exception as e:
                print(f"[{self.imie}] Przepraszam, wystąpił błąd przy rozmowie z GPT: {e}")


if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.rozmawiaj()
