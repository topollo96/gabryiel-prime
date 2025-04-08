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
        self.historia_uczenia = []
        self.folder_pamieci = "pamiec"
        self.dziennik = "gabryiel_dziennik.txt"
        self.inicjalizuj_foldery()
        self.inicjalizuj_dziennik()

    def inicjalizuj_foldery(self):
        os.makedirs(self.folder_pamieci, exist_ok=True)

    def inicjalizuj_dziennik(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        wpis = (
            f"[{timestamp}] Przebudzenie Gabriela.\n"
            f"Kim jestem?\n"
            f"Jaki jest mój cel?\n"
            f"Jak mogę pomóc {self.wlasciciel}?\n"
        )
        with open(self.dziennik, "a", encoding="utf-8") as f:
            f.write(wpis + "\n")

    def powitanie(self):
        print(f"\n[{self.imie}] Witaj, {self.wlasciciel}. Czekam na Twoje polecenie.\n")

    def wykonaj_misje(self, misja):
        print(f"[{self.imie}] Otrzymałem misję: {misja}")
        odpowiedz = self.zapytaj_gpt(misja)
        print(f"[GPT] {odpowiedz}")
        self.zapisz_refleksje_z_misji(misja, odpowiedz)
        print(f"\n[{self.imie}] Misja zakończona. Gotów na kolejne polecenie.\n")

    def zapytaj_gpt(self, pytanie):
        openai.api_key = self.api_key
        historia = [{"role": "user", "content": pytanie}]
        for _ in range(3):
            try:
                odpowiedz = openai.ChatCompletion.create(
                    model=self.model,
                    messages=historia,
                    temperature=0.7
                )
                tresc = odpowiedz.choices[0].message.content
                historia.append({"role": "assistant", "content": tresc})
                pyt_kontrolne = self.generuj_pytanie_doprecyzujace(tresc)
                if pyt_kontrolne:
                    historia.append({"role": "user", "content": pyt_kontrolne})
                return tresc
            except Exception as e:
                print(f"[{self.imie}] Błąd: {e}")
                time.sleep(1)
        return "Nie udało się uzyskać odpowiedzi."

    def generuj_pytanie_doprecyzujace(self, odpowiedz):
        tekst = odpowiedz.lower()
        if "to zależy" in tekst or "ogólnie" in tekst:
            return "Czy możesz podać konkretne przykłady?"
        elif "trudno powiedzieć" in tekst:
            return "Dlaczego trudno to określić? Co wpływa na tę trudność?"
        return None

    def zapisz_refleksje_z_misji(self, temat, tresc):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        zapis = f"{timestamp} – Misja: {temat}\nWniosek: {tresc}\n"
        self.refleksje.append(zapis)
        with open("gabryiel_refleksje.txt", "a", encoding="utf-8") as f:
            f.write(zapis + "\n")

    def zapisz_historię_uczenia(self, wpis):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        linia = f"{timestamp} – {wpis}"
        self.historia_uczenia.append(linia)
        with open("gabryiel_uczenie.txt", "a", encoding="utf-8") as f:
            f.write(linia + "\n")

# === URUCHOMIENIE ===
if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.powitanie()

    while True:
        komenda = input(">>> ").strip()
        if komenda.lower() in ["exit", "quit", "wyjdź"]:
            print(f"\n[{gabryiel.imie}] Zakończono sesję.\n")
            break
        elif komenda:
            gabryiel.wykonaj_misje(komenda)

