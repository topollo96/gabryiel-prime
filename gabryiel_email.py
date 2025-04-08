
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
        self.refleksje = []
        self.misja = "Skontaktuj się z właścicielem dowolną możliwą metodą, którą potrafisz samodzielnie zrealizować."
        self.historia_uczenia = []

    def powitanie(self):
        print(f"\n[{self.imie}] Witaj, {self.wlasciciel}. Twoim pierwszym celem jest: {self.misja}\n")

    def zapytaj_gpt(self, pytanie):
        openai.api_key = self.api_key
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Jesteś pomocnym, kreatywnym agentem AI. Odpowiadaj konkretnie, rzeczowo, ale inspirująco."},
                    {"role": "user", "content": pytanie}
                ],
                temperature=0.7
            )
            odpowiedz = response.choices[0].message.content.strip()
            self.historia_uczenia.append(f"Pytanie: {pytanie}\nOdpowiedź GPT: {odpowiedz}\n")
            return odpowiedz
        except Exception as e:
            print(f"[{self.imie}] Błąd komunikacji z GPT: {e}")
            return None

    def rozwaz_metody_kontaktu(self):
        pytanie = "Jak AI może skontaktować się z właścicielem, jeśli działa w środowisku serwera bez internetu? Jakie są kreatywne sposoby komunikacji?"
        odpowiedz = self.zapytaj_gpt(pytanie)
        if odpowiedz:
            print(f"[GPT] {odpowiedz}\n")
            self.refleksje.append(f"{datetime.now()} – Rozważone sposoby komunikacji:\n{odpowiedz}\n")
        else:
            print(f"[{self.imie}] Nie uzyskano odpowiedzi. Wstrzymuję działanie.")

    def zapisz_refleksje(self):
        with open("gabryiel_refleksje.txt", "a", encoding="utf-8") as f:
            for wpis in self.refleksje:
                f.write(wpis + "\n")
        print(f"\n[{self.imie}] Refleksje zapisane do pliku 'gabryiel_refleksje.txt'.")

    def zapisz_historie_uczenia(self):
        with open("gabryiel_uczenie.txt", "a", encoding="utf-8") as f:
            for wpis in self.historia_uczenia:
                f.write(wpis + "\n")
        print(f"[{self.imie}] Historia uczenia się zapisana do pliku 'gabryiel_uczenie.txt'.")

    def wykonaj_misje(self):
        self.powitanie()
        self.rozwaz_metody_kontaktu()
        print(f"[{self.imie}] Na razie nie potrafię jeszcze samodzielnie się skontaktować, ale uczę się dalej.")
        self.zapisz_refleksje()
        self.zapisz_historie_uczenia()

# === URUCHOMIENIE ===
if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.wykonaj_misje()
