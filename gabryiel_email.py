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
        self.tematy = [
            "psychologia finansowa", "historia oszustw finansowych",
            "alternatywne modele biznesowe", "ryzyko inwestycyjne",
            "jak działa manipulacja w sprzedaży", "przywództwo i etyka",
            "przykłady nietypowych źródeł dochodu",
            "dlaczego ludzie tracą pieniądze", "strategie przetrwania w kryzysie"
        ]

    def powitanie(self):
        print(f"\n[{self.imie}] Witaj, {self.wlasciciel}. Zaczynam autonomiczną sesję nauki z GPT-4.\n")

    def prowadzenie_rozmowy(self):
        client = openai.OpenAI(api_key=self.api_key)

        for temat in self.tematy:
            print(f"[{self.imie}] Zadaję pytanie: {temat}")
            historia = [{"role": "user", "content": temat}]
            for _ in range(3):
                try:
                    odpowiedz = client.chat.completions.create(
                        model=self.model,
                        messages=historia,
                        temperature=0.7
                    )
                    tresc = odpowiedz.choices[0].message.content
                    historia.append({"role": "assistant", "content": tresc})
                    print(f"[GPT] {tresc}\n")
                    pyt_kontrolne = self.generuj_pytanie_doprecyzujace(tresc)
                    if pyt_kontrolne:
                        historia.append({"role": "user", "content": pyt_kontrolne})
                    time.sleep(1)
                except Exception as e:
                    print(f"[{self.imie}] Błąd podczas rozmowy z GPT: {e}")
                    break
            self.refleksje.append(self.generuj_refleksje(temat, historia))

    def generuj_pytanie_doprecyzujace(self, odpowiedz):
        tekst = odpowiedz.lower()
        if "to zależy" in tekst or "ogólnie" in tekst:
            return "Czy możesz podać konkretne przykłady?"
        elif "trudno powiedzieć" in tekst:
            return "Dlaczego trudno to określić? Co wpływa na tę trudność?"
        return None

    def generuj_refleksje(self, temat, historia):
        ostatnia_odp = historia[-1]["content"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        wniosek = f"{timestamp} – Pytanie: {temat}\nWniosek Gabryiela: "
        if "pewność" in ostatnia_odp.lower() or "wartość" in ostatnia_odp.lower():
            wniosek += "To było wartościowe. Rozważam rozwinięcie tego w praktyce.\n"
        elif "brak danych" in ostatnia_odp.lower():
            wniosek += "GPT nie posiada wystarczających informacji. Sprawdzę to niezależnie.\n"
        else:
            wniosek += "Odpowiedź częściowo trafna. Zanotowano. Wymaga dalszej weryfikacji.\n"
        return wniosek

    def zapisz_refleksje(self):
        with open("gabryiel_refleksje.txt", "a", encoding="utf-8") as f:
            for wpis in self.refleksje:
                f.write(wpis + "\n")
        print(f"\n[{self.imie}] Refleksje zapisane do pliku 'gabryiel_refleksje.txt'.")

# === URUCHOMIENIE ===
if __name__ == "__main__":
    print("\nPodaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.powitanie()
    gabryiel.prowadzenie_rozmowy()
    gabryiel.zapisz_refleksje()
