"""

projekt_1.py: první projekt do Engeto Online Python Akademie

author: Adam Směšný

email: adamsmesny@email.cz

discord: adams._25049

"""
#podtrzeni
podtrzeni = "*"

#uvitani
print(podtrzeni * 36)
print("Vítejte v programu pro analýzu textu")
print(podtrzeni * 36)

#seznam uzivatelu
uzivatele = {
"bob" : "123",
"ann" : "pass123",
"mike" : "password123",
"liz" : "pass123"
}

#vyzadani prihlasovacich udaju od uzivatele
jmeno = input("Zadejte prosím Vaše přihlašovací jméno: ") 
heslo = input("Zadejte prosím Vaše heslo: ")

#verifikace uzivatele
if jmeno in uzivatele and uzivatele[jmeno] == heslo:
    print("Dekuji za Vaše ověření")
    print(f"Vítej {jmeno} v aplikaci pro analýzu textu, nyní si vyber číslo od 1 do 3, pod kterými se nachází texty k analýze")
else:
    print("Bohužel, zadané údaje nejsou správné, program se ukončí")
    exit()

#seznam tri textu k analyze v seznamu
texty = ['''
Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley. ''',
'''At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.''',
'''The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.
''']

#vyber pozadovaneho textu           
vyber_textu = input("Zadejte číslo 1, 2 nebo 3 pro výběr požadovaného textu: ")
if vyber_textu.isdigit():
    vyber_textu = int(vyber_textu)
    if vyber_textu < 1 or vyber_textu > len(texty):
        print("Neplatná volba, ukončuji program..")
        exit()
else:
    print("Neplatný vstup, zadejte číslo. Ukončuji program..")
    exit()

#promena pozadovany_text odpovida textu od 1 do 3
pozadovany_text = texty[vyber_textu - 1]

#rozdeleni textu na slova
slova = pozadovany_text.split()

#pocet slov
pocet_slov = len(slova)

# počet slov začínajících velkým písmenem
Title_case_count = sum(1 for word in slova if word.istitle())

# počet slov psaných velkými písmeny
Upper_case_count = sum(1 for word in slova if word.isupper() and word.isalpha())

# počet slov psaných malými písmeny
Lower_case_count = sum(1 for word in slova if word.islower())

# počet čísel (ne cifer)
Numeric_count = sum(1 for word in slova if word.isdigit())

# součet všech čísel (ne cifer) v textu
Numeric_sum = sum(int(word) for word in slova if word.isdigit())

# výpis statistik
print(f"\nVe vybraném textu je celkem {pocet_slov} slov.")
print(f"Z toho {Title_case_count} slov začíná velkým písmenem.")
print(f"{Upper_case_count} slov je psáno velkými písmeny.")
print(f"{Lower_case_count} slov je psáno malými písmeny.")
print(f"V textu je {Numeric_count} čísel.")
print(f"Součet všech čísel v textu je {Numeric_sum}.")

# analýza délky slov
delka_slov = {}
for word in slova:
    delka = len(word.strip(",.!?"))
    delka_slov[delka] = delka_slov.get(delka, 0) + 1

# vykreslení jednoduchého grafu
print("\nDelka|  Vyskyt    |Pocet")
print("-" * 30)
for delka, pocet in sorted(delka_slov.items()):
    print(f"{delka:<3}| {'*' * pocet:<12} |{pocet}")