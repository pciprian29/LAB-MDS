cursuri = []

def adauga_curs():
    nume = input("Nume curs: ")
    profesor = input("Profesor: ")
    credite = input("Nr. credite: ")
    cursuri.append({"nume": nume, "profesor": profesor, "credite": credite})
    print("Curs adaugat cu succes!\n")

def afiseaza_cursuri():
    if not cursuri:
        print("Nu exista cursuri.\n")
        return
    print("\n--- Lista cursuri ---")
    for i, c in enumerate(cursuri, 1):
        print(f"{i}. {c['nume']} | Prof: {c['profesor']} | Credite: {c['credite']}")
    print()

def modifica_curs():
    afiseaza_cursuri()
    if not cursuri:
        return
    try:
        idx = int(input("Nr. curs de modificat: ")) - 1
        if idx < 0 or idx >= len(cursuri):
            print("Index invalid.\n")
            return
        c = cursuri[idx]
        c["nume"] = input(f"Nume ({c['nume']}): ") or c["nume"]
        c["profesor"] = input(f"Profesor ({c['profesor']}): ") or c["profesor"]
        c["credite"] = input(f"Credite ({c['credite']}): ") or c["credite"]
        print("Curs modificat!\n")
    except ValueError:
        print("Eroare: introdu un numar.\n")

def sterge_curs():
    afiseaza_cursuri()
    if not cursuri:
        return
    try:
        idx = int(input("Nr. curs de sters: ")) - 1
        if idx < 0 or idx >= len(cursuri):
            print("Index invalid.\n")
            return
        curs = cursuri.pop(idx)
        print(f"Cursul '{curs['nume']}' a fost sters.\n")
    except ValueError:
        print("Eroare: introdu un numar.\n")

while True:
    print("=== MENIU CURSURI ===")
    print("1. Adaugare curs")
    print("2. Afisare")
    print("3. Modificare")
    print("4. Stergere")
    print("5. Iesire")
    opt = input("Alege optiunea: ")

    if opt == "1":
        adauga_curs()
    elif opt == "2":
        afiseaza_cursuri()
    elif opt == "3":
        modifica_curs()
    elif opt == "4":
        sterge_curs()
    elif opt == "5":
        print("La revedere!")
        break
    else:
        print("Optiune invalida.\n")
