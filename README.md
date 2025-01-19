# repozitar

POPIS PROJEKTU Č. 3 - ELECTIONS SCRAPER
---------------------------------------
Tento projekt slouží k extrahování výsledků z parlamentních voleb 2017. Odkaz k prohlédnutí nalaznete zde: 
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

INSTALACE KNIHOVEN
------------------
Knihovny, které jsou použity v kódu, jsou uloženy v souboru requirements.txt. Po instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version                      # overim verzi manazeru
$ pip3 install -r requirements.txt    # nainstaluji knihovny

SPUŠTĚNÍ PROJEKTU
-----------------
Spouštění souboru elections-scraper.py v rámci příkazového řádku, požaduje dva povinné argumenty.

python elections-scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202" vysledky.csv

Následně se Vám stáhnou výsledky, jako soubor s příponou .csv.

UKÁZKA PROJEKTU
---------------
Výsledky hlasování pro okres Uherské Hradiště:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
2. argument: vysledky.csv

Průbeh stahování:
Zpracovávám data z URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
Výsledky byly úspěšně uloženy do souboru vysledky.csv

ČÁSTEČNÝ VÝSTUP
---------------
code,	location,	registered,	envelopes,	valid, ...
592013	Babice	1452	873	866	100.0	79	0	0	60	0	55	66	5	6	3	0	2	74	0	23	254	1	0	95	5	1	0	133	4
592021	Bánov	1707	1070	1063	0	92	2	1	75	0	117	62	10	1	11	1	2	71	1	11	293	1	0	148	6	0	0	156	2
592030	Bílovice	1473	1018	1008	0	98	0	0	67	1	66	80	10	5	14	0	1	90	0	28	264	0	2	147	4	3	1	92	35
592048	Bojkovice	3635	2183	2170	0	290	6	0	165	1	79	225	23	7	20	1	1	134	4	37	612	0	3	208	16	1	3	322	12
