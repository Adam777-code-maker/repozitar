"""

projekt_1.py: druhý projekt do Engeto Online Python Akademie

author: Adam Směšný

email: adamsmesny@email.cz

discord: adams._25049

"""

#podtrzeni
podtrzeni = "*"

#uvitani
print(podtrzeni * 24)
print("Vítejte ve hře piškvorky")
print(podtrzeni * 24)

# Zobrazeni herni plochy
def vytvor_plochu(plocha):
    print("\n")
    for i in range(3):
        print(" | ".join(plocha[i]))
        if i < 2:
            print("---------")
    print("\n")

# Kontrola, jestli je někdo vítěz
def vitez(plocha, znak):
    # Kontrola radku, sloupců a diagonál
    for i in range(3):
        if all([plocha[i][j] == znak for j in range(3)]) or all([plocha[j][i] == znak for j in range(3)]):
            return True
    if plocha[0][0] == plocha[1][1] == plocha[2][2] == znak or plocha[0][2] == plocha[1][1] == plocha[2][0] == znak:
        return True
    return False

# Kontrola remízy
def remiza(plocha):
    return all([plocha[i][j] != " " for i in range(3) for j in range(3)])

# Platný pohyb?
def platny_pohyb(plocha, radek, sloupec):
    return 0 <= radek < 3 and 0 <= sloupec < 3 and plocha[radek][sloupec] == " "

# Funkce pro hru
def hrat():
    plocha = [[" " for _ in range(3)] for _ in range(3)]  # Vytvoření prázdné herní plochy
    znaky = ["X", "O"]
    tahy = 0
    hrac = 0  # 0 pro X, 1 pro O
    
    while True:
        vytvor_plochu(plocha)
        print(f"Na tahu je hráč {znaky[hrac]}")

        # Získání vstupu od hráče
        try:
            radek = int(input("Zadejte číslo řádku (0, 1, 2): "))
            sloupec = int(input("Zadejte číslo sloupce (0, 1, 2): "))
        except ValueError:
            print("Neplatný vstup, zadejte čísla.")
            continue

        if platny_pohyb(plocha, radek, sloupec):
            plocha[radek][sloupec] = znaky[hrac]
            tahy += 1
        else:
            print("Toto není povolené místo, zvol jiné!")
            continue
        
        # Kontrola vítězství nebo remízu
        if vitez(plocha, znaky[hrac]):
            vytvor_plochu(plocha)
            print(f"Hráč {znaky[hrac]} je vítěz!")
            break
        if remiza(plocha):
            vytvor_plochu(plocha)
            print("Remíza!")
            break
        
        # Střídání hráčů
        hrac = 1 - hrac

# Spustí hru
if __name__ == "__main__":
    hrat()