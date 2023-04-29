import os


class ksiazka:
    def __init__(id, tytul, autor, rok, kategoria, wypozyczona):
        id.tytul = tytul
        id.autor = autor
        id.rok = rok
        id.kategoria = kategoria
        id.wypozyczona = False


class biblioteka:


    def __init__(id):
        id.lista = []

    def dodaj(id, tytul, autor, rok, kategoria,wypozyczona):
        nowa = ksiazka(tytul, autor, rok, kategoria,wypozyczona)
        id.lista.append(nowa)


    def wyswietl(id):
        print("\n")
        for i in id.lista:
            print(i.tytul)
        print("\n")


    def wypozycz(id):
        nazwa = input("\nPodaj nazwe ksiazki ktora chcesz wypozyczyc:\n")
        for i in id.lista:
            if i.tytul == nazwa and i.wypozyczona == False :
                os.system('cls')
                print(f"\nWypozyczono ksiazke: {i.tytul}\n")
                i.wypozyczona = True
            elif i.tytul == nazwa and i.wypozyczona == True:
                os.system('cls')
                print("\nKsiazka jest niedostepna\n")


    def oddaj(id):
        nazwa = input("\nPodaj nazwe ktora chcesz oddac:\n")
        for i in id.lista:
            if i.tytul == nazwa and i.wypozyczona == True:
                os.system('cls')
                i.wypozyczona = False
                print(f"\nOddano ksiazke: {i.tytul}\n")
            elif i.tytul == nazwa and i.wypozyczona == False:
                os.system('cls')
                print("\nKsiazka nie zostala wypozyczona\n")


    def sprawdz(id):
        nazwa = input("\nPodaj nazwe ksiazki:\n")
        for i in id.lista:
            if i.tytul == nazwa and i.wypozyczona == False:
                os.system('cls')
                print(f"\n{i.tytul} jest dostepna\n")
            elif i.tytul == nazwa and i.wypozyczona == True:
                os.system('cls')
                print(f"\n{i.tytul} jest niedostepna\n")


wypozyczalnia = biblioteka()
wypozyczalnia.dodaj("Władca much", "William Golding", 1954, "powieść",False)
wypozyczalnia.dodaj("Złodziejka książek", "Markus Zusak", 2005, "powieść historyczna",False)
wypozyczalnia.dodaj("Nineteen Eighty-Four", "George Orwell", 1949, "literatura dystopijna",False)
wypozyczalnia.dodaj("Bieguni", "Olga Tokarczuk", 2007, "powieść",False)
wypozyczalnia.dodaj("Podróż do wnętrza Ziemi", "Jules Verne", 1864, "powieść science-fiction",False)
wypozyczalnia.dodaj("O psie, który jeździł koleją", "Agatha Christie", 1951, "powieść kryminalna",False)
wypozyczalnia.dodaj("Mały Książę", "Antoine de Saint-Exupéry", 1943, "literatura dziecięca",False)
wypozyczalnia.dodaj("Harry Potter i Kamień Filozoficzny", "J.K. Rowling", 1997, "literatura fantasy",False)
wypozyczalnia.dodaj("Kapitan Łosoś", "Jack London", 1900, "powieść przygodowa",False)
wypozyczalnia.dodaj("Romeo i Julia", "William Szekspir", 1597, "dramat",False)

while True:
    wybor = input("Witaj w bibliotece:\n(1)Wyswietl dostepne ksiazki\n(2)Sprawdz dostepnosc ksiazki\n(3)Wypozycz ksiazke\n(4)Oddaj ksiazke\n(5)Wyjdz z programi\nPodaj numer opcji ktora chcesz wykonac:")
    if wybor == "1":
        wypozyczalnia.wyswietl()
    elif wybor == "2":
        wypozyczalnia.sprawdz()
    elif wybor == "3":
        wypozyczalnia.wypozycz()
    elif wybor == "4":
        wypozyczalnia.oddaj()
    elif wybor == "5":
        exit()
    else:
        print("Podaj odpowiedni wybor\n")
