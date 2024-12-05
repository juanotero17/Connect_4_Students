class DatabaseInterface:
    def __init__(self):
        self.main_menu = """+----------+-------------------------------------------------+
| Auswahl  | Beschreibung                                    |
+----------+-------------------------------------------------+
| 1        | Lieferanten auflisten                           |
+----------+-------------------------------------------------+
| 2        | Artikel auflisten (nach Name)                   |
+----------+-------------------------------------------------+
| 3        | Bestellmöglichkeiten abrufen (nach ItemID)      |
+----------+-------------------------------------------------+
| 4        | Artikel scannen (nach Bestellnummer)            |
+----------+-------------------------------------------------+
| 5        | Beenden                                         |
+----------+-------------------------------------------------+
"""

    def display_menu(self):
        print(self.main_menu)

    def list_vendors(self):
        sub_menu = """+----------+-------------------------------------------------+
| 1        | Lieferanten auflisten                           |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        print("\nListe der Lieferanten:")
        print("\n \nNoch nicht Implementiert... \n \n \n")
        # TODO: Implementieren Sie den Code hier

    def list_items(self):
        sub_menu = """+----------+-------------------------------------------------+
| 2        | Artikel auflisten (nach Name)                   |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        item_name = input("\nGeben Sie den Artikelnamen ein: ")
        print(f"\nListe der Artikel mit '{item_name}' im Namen:")
        print("\n \nNoch nicht Implementiert... \n \n \n")
        # TODO: Implementieren Sie den Code hier

    def get_orders(self):
        sub_menu = """+----------+-------------------------------------------------+
| 3        | Bestellmöglichkeiten abrufen (nach ItemID)      |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        item_id = input("\nGeben Sie die ItemID ein: ")
        print(f"\nBestellmöglichkeiten für ItemID {item_id}:")
        print("\n \nNoch nicht Implementiert... \n \n \n")
        # TODO: Implementieren Sie den Code hier

    def scan_item(self):
        sub_menu = """+----------+-------------------------------------------------+
| 4        | Artikel scannen (nach Bestellnummer)            |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        order_nr = input("\nGeben Sie die Bestellnummer ein: ")
        print(f"\nScanne Artikel mit Bestellnummer {order_nr}...")
        print("\n \nNoch nicht Implementiert... \n \n \n")
        # TODO: Implementieren Sie den Code hier

    def end_menu(self):
        sub_menu = """+----------+-------------------------------------------------+
|  5        | Beenden                                        |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        print("\nProgramm beendet. Auf Wiedersehen!")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nWählen Sie eine Option (1-5): ")

            if choice == "1":
                self.list_vendors()
            elif choice == "2":
                self.list_items()
            elif choice == "3":
                self.get_orders()
            elif choice == "4":
                self.scan_item()
            elif choice == "5":
                self.end_menu()
                break
            else:
                print("\nUngültige Eingabe. Bitte wählen Sie eine gültige Option (1-5).\n")

# Hauptprogramm starten
if __name__ == "__main__":
    print("Willkommen im Datenbank-Interface! Bitte wählen Sie eine Option:")
    interface = DatabaseInterface()
    interface.run()
