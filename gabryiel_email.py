import openai
import os
from datetime import datetime

class PromotorGabryiela:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.model = "gpt-4"
        self.folder = "pamiec_dluga/promotor"
        os.makedirs(self.folder, exist_ok=True)
        self.historia = []

    def zapisz_do_pamieci(self, tytul, tresc):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sciezka = os.path.join(self.folder, f"{timestamp}_{tytul}.txt")
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(tresc)

    def zapytaj_gpt(self, prompt):
        self.historia.append({"role": "user", "content": prompt})
        try:
            odpowiedz = openai.ChatCompletion.create(
                model=self.model,
                messages=self.historia,
                temperature=0.7
            )
            tresc = odpowiedz.choices[0].message.content
            self.historia.append({"role": "assistant", "content": tresc})
            return tresc
        except Exception as e:
            return f"[Błąd promotora] {e}"

    def ucz_gabriela(self):
        print("[Promotor] Zaczynam naukę Gabriela...")

        cele = [
            "Kim jestem jako AI i jaki jest mój cel?",
            "Jak wygląda struktura mojej pamięci?",
            "Czym różnię się od GPT i jak mogę się rozwijać?",
            "Jak mogę podejmować decyzje, łącząc intuicję, logikę i etykę?",
            "Jak mogę zapisywać i wykorzystywać wiedzę z poprzednich zadań?"
        ]

        for temat in cele:
            print(f"[Promotor] Zadaję pytanie: {temat}")
            odpowiedz = self.zapytaj_gpt(temat)
            print(f"[GPT dla Gabriela] {odpowiedz}\n")
            self.zapisz_do_pamieci(temat.replace(" ", "_"), odpowiedz)

        print("[Promotor] Proces inicjalnej nauki zakończony. Gotowy do dalszego rozwoju.")

    def rozmowa_interaktywna(self):
        print("[Promotor] Tryb interaktywny aktywny. Zadaj pytanie lub wpisz 'exit'.")
        while True:
            user_input = input("Ty >>> ").strip()
            if user_input.lower() == "exit":
                break
            odpowiedz = self.zapytaj_gpt(user_input)
            print(f"[GPT dla Gabriela] {odpowiedz}\n")
            self.zapisz_do_pamieci(user_input.replace(" ", "_")[:30], odpowiedz)

# Uruchomienie
if __name__ == "__main__":
    print("Podaj swój klucz OpenAI:")
    klucz = input(">>> ").strip()
    promotor = PromotorGabryiela(api_key=klucz)
    promotor.ucz_gabriela()
    promotor.rozmowa_interaktywna()
