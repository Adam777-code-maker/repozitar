import requests
from bs4 import BeautifulSoup
import csv
import sys

def načti_url(url):
    """
    Načte obsah dané URL.
    """
    odpověď = requests.get(url)
    if odpověď.status_code == 200:
        return BeautifulSoup(odpověď.content, "html.parser")
    else:
        raise ConnectionError(f"Chyba při načítání URL: {url} (HTTP {odpověď.status_code})")

def vyčisti_číslo(hodnota):
    """
    Převede formátované číslo (např. '1 000,00') na celé nebo desetinné číslo.
    """
    hodnota = hodnota.replace("\xa0", "").replace(",", ".").strip()
    if "." in hodnota:
        return float(hodnota)
    return int(hodnota)

def extrahuj_odkazy_na_obce(hlavní_url, počáteční_obec, koncová_obec):
    """
    Extrahuje odkazy na obce mezi počáteční_obec a koncová_obec.
    """
    soup = načti_url(hlavní_url)
    tabulky = soup.find_all("table", class_="table")  # Najde všechny tabulky s obcemi

    if not tabulky:
        raise ValueError("Chyba: Nepodařilo se najít tabulky se seznamem obcí na hlavní stránce.")

    odkazy = []
    sbírej = False
    for tabulka in tabulky:
        for řádek in tabulka.find_all("tr")[2:]:  # Přeskakujeme hlavičku
            buňky = řádek.find_all("td")
            kód = buňky[0].text.strip()
            název = buňky[1].text.strip()
            relativní_url = buňky[0].find("a")["href"]
            plná_url = f"https://www.volby.cz/pls/ps2017nss/{relativní_url}"

            # Začneme sbírat odkazy od počáteční obce
            if název == počáteční_obec:
                sbírej = True

            # Přidáme odkaz, pokud sbíráme
            if sbírej:
                odkazy.append({"kód": kód, "název": název, "url": plná_url})

            # Přestaneme sbírat, když dosáhneme koncové obce
            if název == koncová_obec:
                sbírej = False

    return odkazy

def extrahuj_výsledky_voleb(obec_url):
    """
    Extrahuje volební výsledky pro danou obec.
    """
    soup = načti_url(obec_url)

    # Extrahování obecné statistiky
    try:
        statistická_tabulka = soup.find("table", id="ps311_t1")  # Identifikace tabulky statistik
        statistický_řádek = statistická_tabulka.find_all("tr")[2]  # Třetí řádek obsahuje data
        buňky = statistický_řádek.find_all("td")

        registrovaní = vyčisti_číslo(buňky[3].text)
        obálky = vyčisti_číslo(buňky[4].text)
        platné = vyčisti_číslo(buňky[7].text)
    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Chyba při extrahování statistik: {e}")

    # Extrahování výsledků stran
    výsledky_stran = {}
    try:
        tabulky_stran = soup.find_all("table", class_="table")  # Tabulky s výsledky stran
        for tabulka in tabulky_stran:
            řádky = tabulka.find_all("tr")[2:]  # Přeskakujeme hlavičku
            for řádek in řádky:
                buňky = řádek.find_all("td")
                název_strany = buňky[1].text.strip()
                hlasy = vyčisti_číslo(buňky[2].text)
                výsledky_stran[název_strany] = hlasy
    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Chyba při extrahování výsledků stran: {e}")

    return {
        "registrovaní": registrovaní,
        "obálky": obálky,
        "platné": platné,
        "strany": výsledky_stran
    }

def ulož_do_csv(výstupní_soubor, data):
    """
    Uloží extrahovaná data do CSV souboru s vhodným oddělovačem pro Excel.
    """
    strany = list(data[0]["strany"].keys())
    # Hlavička bez sloupce „1“
    hlavička = ["code", "location", "registered", "envelopes", "valid"] + [strana for strana in strany if strana != "1"]

    with open(výstupní_soubor, "w", newline="", encoding="utf-8-sig") as f:
        zapisovač = csv.writer(f, delimiter=";")  # Použijeme středník jako oddělovač
        zapisovač.writerow(hlavička)  # Zápis hlavičky

        for záznam in data:
            # Řádek bez hodnot pro stranu „1“
            řádek = [
                záznam["kód"],
                záznam["obec"],
                záznam["registrovaní"],
                záznam["obálky"],
                záznam["platné"]
            ]
            řádek += [záznam["strany"].get(strana, 0) for strana in strany if strana != "1"]
            zapisovač.writerow(řádek)

def hlavní():
    """
    Hlavní funkce, která zpracovává argumenty příkazového řádku a spouští scraper.
    """
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL> <výstupní_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    výstupní_soubor = sys.argv[2]

    počáteční_obec = "Babice"
    koncová_obec = "Žítková"

    print(f"Zpracovávám data z URL: {url}")
    
    try:
        obce = extrahuj_odkazy_na_obce(url, počáteční_obec, koncová_obec)
        všechny_výsledky = []

        for obec in obce:
            print(f"Zpracovávám obec: {obec['název']} (kód: {obec['kód']})")
            try:
                výsledek = extrahuj_výsledky_voleb(obec["url"])
                výsledek["kód"] = obec["kód"]
                výsledek["obec"] = obec["název"]
                všechny_výsledky.append(výsledek)
            except Exception as e:
                print(f"Chyba při zpracování obce {obec['název']}: {e}")

        ulož_do_csv(výstupní_soubor, všechny_výsledky)
        print(f"Výsledky byly úspěšně uloženy do souboru {výstupní_soubor}")

    except Exception as e:
        print(f"Chyba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    hlavní()
