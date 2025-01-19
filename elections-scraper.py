"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Adam Směšný

email: adamsmesny@email.cz

discord: adams._25049

"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def fetch_url(url):
    """
    Fetch the content of the given URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        raise ConnectionError(f"Chyba při načítání URL: {url} (HTTP {response.status_code})")

def clean_number(value):
    """
    Convert a formatted string number (e.g., '1 000,00') to an integer or float.
    """
    value = value.replace("\xa0", "").replace(",", ".").strip()
    if "." in value:
        return float(value)
    return int(value)

def extract_municipality_links(main_url, start_name, end_name):
    """
    Extract links to municipalities between start_name and end_name.
    """
    soup = fetch_url(main_url)
    tables = soup.find_all("table", class_="table")  # Najít všechny tabulky s obcemi

    if not tables:
        raise ValueError("Chyba: Nepodařilo se najít tabulky se seznamem obcí na hlavní stránce.")

    links = []
    collect = False
    for table in tables:
        for row in table.find_all("tr")[2:]:  # Přeskakujeme hlavičku
            cells = row.find_all("td")
            code = cells[0].text.strip()
            name = cells[1].text.strip()
            relative_url = cells[0].find("a")["href"]
            full_url = f"https://www.volby.cz/pls/ps2017nss/{relative_url}"

            # Start collecting when reaching start_name
            if name == start_name:
                collect = True

            # Stop collecting when reaching end_name
            if collect:
                links.append({"code": code, "name": name, "url": full_url})

            if name == end_name:
                collect = False

    return links

def extract_voting_results(municipality_url):
    """
    Extract voting results for a given municipality.
    """
    soup = fetch_url(municipality_url)

    # Extrahování obecné statistiky
    try:
        stats_table = soup.find("table", id="ps311_t1")  # Identifikace tabulky statistik
        stats_row = stats_table.find_all("tr")[2]  # Třetí řádek obsahuje data
        cells = stats_row.find_all("td")

        registered = clean_number(cells[3].text)
        envelopes = clean_number(cells[4].text)
        valid = clean_number(cells[7].text)
    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Chyba při extrahování statistik: {e}")

    # Extrahování výsledků stran
    party_results = {}
    try:
        party_tables = soup.find_all("table", class_="table")  # Tabulky s výsledky stran
        for table in party_tables:
            rows = table.find_all("tr")[2:]  # Přeskakujeme hlavičku
            for row in rows:
                cells = row.find_all("td")
                party_name = cells[1].text.strip()
                votes = clean_number(cells[2].text)
                party_results[party_name] = votes
    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Chyba při extrahování výsledků stran: {e}")

    return {
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid,
        "parties": party_results
    }

def save_to_csv(output_file, data):
    """
    Save extracted data into a CSV file with proper delimiters for Excel.
    """
    parties = list(data[0]["parties"].keys())
    header = ["code", "location", "registered", "envelopes", "valid"] + parties

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")  # Použijeme středník jako oddělovač
        writer.writerow(header)  # Zápis hlavičky

        for record in data:
            row = [
                record["code"],
                record["location"],
                record["registered"],
                record["envelopes"],
                record["valid"]
            ]
            row += [record["parties"].get(party, 0) for party in parties]
            writer.writerow(row)

def main():
    """
    Main function to handle command-line arguments and run the scraper.
    """
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL> <výstupní_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    start_name = "Babice"
    end_name = "Žítková"

    print(f"Zpracovávám data z URL: {url}")
    
    try:
        municipalities = extract_municipality_links(url, start_name, end_name)
        all_results = []

        for municipality in municipalities:
            print(f"Zpracovávám obec: {municipality['name']} (kód: {municipality['code']})")
            try:
                result = extract_voting_results(municipality["url"])
                result["code"] = municipality["code"]
                result["location"] = municipality["name"]
                all_results.append(result)
            except Exception as e:
                print(f"Chyba při zpracování obce {municipality['name']}: {e}")

        save_to_csv(output_file, all_results)
        print(f"Výsledky byly úspěšně uloženy do souboru {output_file}")

    except Exception as e:
        print(f"Chyba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

