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
        self.folder_misji = "misje"
        self.folder_logow = "logi"
        self.folder_wiedzy = "baza_wiedzy"
        self.utworz_foldery()

    def utworz_foldery(self):
        os.makedirs(self.folder_misji, exist_ok=True)
        os.makedirs(self.folder_logow, exist_ok=True)
        os.makedirs(self.folder_wiedzy, exist_ok=True)

    def zapytaj_uzytkownika(self):
        print(f"\n[{self.imie}] Czekam na Twoje polecenie, {self.wlasciciel}.")
        return input(">>> ").strip()

    def rozpocznij_misje(self, polecenie):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plik_misji = os.path.join(self.folder_misji, f"misja_{timestamp}.txt")
        with open(plik_misji, "w", encoding="utf-8") as f:
            f.write(f"Misja: {polecenie}\nStatus: W toku\n")
        return plik_misji

    def pytaj_gpt(self, pytanie, historia=[]):
        openai.api_key = self.api_key
        historia.append({"role": "user", "content": pytanie})
        try:
            odpowiedz = openai.ChatCompletion.create(
                model=self.model,
                messages=historia,
                temperature=0.7
            )
            tresc = odpowiedz.choices[0].message.content
            historia.append({"role": "assistant", "content": tresc})
            return tresc, historia
        except Exception as e:
            return f"Błąd: {e}", historia

    def zapisz_log(self, tresc):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plik_logu = os.path.join(self.folder_logow, f"log_{timestamp}.txt")
        with open(plik_logu, "w", encoding="utf-8") as f:
            f.write(tresc)

    def zapisz_wiedze(self, temat, tresc):
        plik = os.path.join(self.folder_wiedzy, f"{temat}.txt")
        with open(plik, "a", encoding="utf-8") as f:
            f.write(f"{tresc}\n")

    def wykonuj(self):
        while True:
            polecenie = self.zapytaj_uzytkownika()
            if polecenie.lower() in ["stop", "exit", "koniec"]:
                print(f"[{self.imie}] Kończę pracę. Do zobaczenia!")
                break

            plik_misji = self.rozpocznij_misje(polecenie)
            historia = []
            odpowiedz, historia = self.pytaj_gpt(polecenie, historia)
            print(f"[GPT] {odpowiedz}\n")
            self.zapisz_log(f"MISJA: {polecenie}\n\n{odpowiedz}")
            self.zapisz_wiedze("wykonane_misje", f"{datetime.now()} - {polecenie}\n{odpowiedz}\n")
            print(f"[{self.imie}] Misja zakończona. Gotów na kolejne polecenie.")


if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.wykonuj()
