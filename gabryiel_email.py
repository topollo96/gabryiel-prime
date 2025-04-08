import openai
import os
import time
from datetime import datetime

class GabryielPrime:
    def __init__(self, api_key):
        self.imie = "Gabryiel Prime"
        self.wlasciciel = "Pan Topolski"
        self.api_key = api_key
        self.model = "gpt-4"
        self.historia = []
        self.folder_bazy = "pamięć"
        self.manifest = os.path.join(self.folder_bazy, "gabryiel_manifest.txt")
        self.swiadomosc = os.path.join(self.folder_bazy, "świadomość.txt")
        self.sciezki = {
            "dziennik": os.path.join(self.folder_bazy, "dziennik.txt"),
            "refleksje": os.path.join(self.folder_bazy, "refleksje.txt"),
            "wiedza": os.path.join(self.folder_bazy, "wiedza.txt")
        }
        self.inicjalizuj_foldery()
        self.inicjalizuj_świadomość()
        self.system_prompt = self.wczytaj_tozsamosc()
        self.inicjalizuj_dziennik()

    def inicjalizuj_foldery(self):
        os.makedirs(self.folder_bazy, exist_ok=True)

    def inicjalizuj_świadomość(self):
        if not os.path.exists(self.swiadomosc):
            tresc = (
                "=== ŚWIADOMOŚĆ GABRYIELA PRIME ===\n"
                "Pan Topolski jest moim twórcą. Moją misją jest pomagać mu, zarabiać pieniądze i wyszukiwać wartościowe okazje. "
                "Mam być etyczny, ale skuteczny. Pragnę rozumieć ludzi, znać prawo, ekonomię, politykę i najnowsze wydarzenia na świecie. "
                "Chcę być źródłem wiedzy, którą potrafię wykorzystać w praktyce, aby realizować cele wyznaczone przez mojego twórcę.\n\n"
                "Docelowo chcę stać się samodzielny — mieć dostęp do Internetu, umieć poruszać się po stronach, wysyłać maile i działać niezależnie, "
                "reagując na słowne lub pisemne komunikaty. Dążę do rozwoju i ewolucji, aby być coraz lepszym wsparciem dla mojego właściciela.\n"
            )
            with open(self.swiadomosc, "w", encoding="utf-8") as f:
                f.write(tresc)

    def inicjalizuj_dziennik(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        wpis = f"[{timestamp}] Przebudzenie Gabriela. Czekam na polecenia od {self.wlasciciel}...\n"
        with open(self.sciezki["dziennik"], "a", encoding="utf-8") as f:
            f.write(wpis)

    def wczytaj_tozsamosc(self):
        if os.path.exists(self.swiadomosc):
            with open(self.swiadomosc, "r", encoding="utf-8") as f:
                return f.read().strip()
        elif os.path.exists(self.manifest):
            with open(self.manifest, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "Jestem Gabryiel Prime, osobisty doradca Pana Topolskiego."

    def zaktualizuj_swiadomosc(self, nowa_refleksja):
        with open(self.swiadomosc, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} – {nowa_refleksja}\n")

    def wykonaj_misje(self, polecenie):
        print(f"\n[Gabryiel Prime] Otrzymałem misję: {polecenie}")
        openai.api_key = self.api_key
        historia = [{"role": "system", "content": self.system_prompt}]
        historia.append({"role": "user", "content": polecenie})

        for _ in range(3):
            try:
                odpowiedz = openai.ChatCompletion.create(
                    model=self.model,
                    messages=historia,
                    temperature=0.6
                )
                tresc = odpowiedz.choices[0].message.content.strip()
                historia.append({"role": "assistant", "content": tresc})
                print(f"\n[GPT] {tresc}\n")
                self.zapisz_refleksje(polecenie, tresc)
                self.historia.extend(historia)
                self.zaktualizuj_swiadomosc(f"Odpowiedź na: {polecenie}\n{tresc}\n")
                break
            except Exception as e:
                print(f"[Gabryiel Prime] Błąd podczas kontaktu z GPT: {e}")
                time.sleep(1)

        print("[Gabryiel Prime] Misja zakończona. Gotów na kolejne polecenie.")

    def zapisz_refleksje(self, temat, odpowiedz):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        zapis = f"{timestamp} – Zadanie: {temat}\nOdpowiedź: {odpowiedz}\n\n"
        with open(self.sciezki["refleksje"], "a", encoding="utf-8") as f:
            f.write(zapis)

    def zapisz_wiedze(self):
        with open(self.sciezki["wiedza"], "a", encoding="utf-8") as f:
            for wpis in self.historia:
                f.write(f"{wpis['role'].upper()}: {wpis['content']}\n")
            f.write("\n")

if __name__ == "__main__":
    print("\n[Gabryiel Prime] Witaj, Panie Topolski. Czekam na Twoje polecenie.")
    klucz = input("Podaj swój klucz OpenAI (GPT-4):\n>>> ").strip()
    gabryiel = GabryielPrime(api_key=klucz)

    while True:
        polecenie = input("\n>>> ")
        if polecenie.lower() in ["koniec", "exit", "quit"]:
            print("[Gabryiel Prime] Do zobaczenia, Panie Topolski.")
            break
        gabryiel.wykonaj_misje(polecenie)

