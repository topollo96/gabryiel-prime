
import openai
import os
import time
from datetime import datetime

# === MÓZG GABRYIELA ===
class GabryielMozg:
    def __init__(self, base_path="gabryiel_dane"):
        self.base_path = base_path
        self.sektory = [
            "pamiec/wiedza", "pamiec/refleksje", "pamiec/emocje",
            "misje/aktywne", "misje/zakonczone",
            "kreatywnosc/pomysly", "kreatywnosc/eksperymenty", "kreatywnosc/wizje",
            "komunikacja/do_wyslania", "komunikacja/historia_rozmow"
        ]
        self.utworz_strukture()

    def utworz_strukture(self):
        for sektor in self.sektory:
            sciezka = os.path.join(self.base_path, sektor)
            os.makedirs(sciezka, exist_ok=True)

    def zapisz_wiedze(self, temat, tresc):
        folder = os.path.join(self.base_path, "pamiec/wiedza", temat.lower().replace(" ", "_"))
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        plik = os.path.join(folder, f"{timestamp}.txt")
        with open(plik, "w", encoding="utf-8") as f:
            f.write(tresc)
        return f"[Gabryiel] Zapisano wiedzę do: {plik}"

    def zapisz_refleksje(self, tresc):
        folder = os.path.join(self.base_path, "pamiec/refleksje")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        plik = os.path.join(folder, f"{timestamp}.txt")
        with open(plik, "w", encoding="utf-8") as f:
            f.write(tresc)
        return f"[Gabryiel] Zapisano refleksję: {plik}"

# === GŁÓWNY GABRYIEL ===
class GabryielPrime:
    def __init__(self, api_key):
        self.imie = "Gabryiel Prime"
        self.wlasciciel = "Pan Topolski"
        self.api_key = api_key
        self.model = "gpt-4"
        self.mozg = GabryielMozg()

    def powitanie(self):
        print(f"[{self.imie}] Witaj, {self.wlasciciel}. Czekam na Twoje polecenie.")

    def otrzymaj_misje(self, tresc_misji):
        print(f"[{self.imie}] Otrzymałem misję: {tresc_misji}")
        self.mozg.zapisz_refleksje(f"{datetime.now()} – Otrzymano misję: {tresc_misji}")
        self.ucz_sie_na_potrzeby_misji(tresc_misji)

    def ucz_sie_na_potrzeby_misji(self, temat):
        openai.api_key = self.api_key
        historia = [{"role": "user", "content": temat}]
        for _ in range(3):
            try:
                odpowiedz = openai.ChatCompletion.create(
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
                print(f"[{self.imie}] Błąd podczas nauki: {e}")
                break

        self.mozg.zapisz_wiedze(temat, historia[-1]["content"])
        self.mozg.zapisz_refleksje(self.generuj_refleksje(temat, historia))

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

# === START ===
if __name__ == "__main__":
    print("Podaj swój klucz OpenAI (GPT-4):")
    klucz = input(">>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)
    gabryiel.powitanie()
    print("Wpisz treść pierwszej misji dla Gabryiela:")
    misja = input(">>> ").strip()
    gabryiel.otrzymaj_misje(misja)
