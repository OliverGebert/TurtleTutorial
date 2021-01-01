# zeigt den aktuelle Pfad, aus dem das Programm Dateien öffnet
# import os
# print(os.path.abspath('.'))

import string
import random

# map Funktion für LIste nutzen
# quadrate = [x**2 for x in range(21)]
# print("Liste der Quadratzahlen: ", quadrate)

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CEND = '\033[0m' # white again

zaehler = 0         # Zaehler für alle Zeilen
muster_Zaehler = 0  # muster zaehler für anzahl der treffer
anna_Zaehler = 0    # zaehler für anzahl der worte, die Annagramme sind
text_Block = ""     # ein String mit dem komplette Text für eine Markov Analyse
Markov_Dict = dict()
zeilen_Liste = []   # Liste aller Zeilen aus dem File
zeilen_Wort_Liste = [[]]  # Liste von Listen von Worten
worte_Menge = {None}    # Menge aller Worte in der Datei
muster_Liste = []   # Liste aller Zeilen, die das Muter enthalten
anna_Liste = []     # Liste aller Zeilen, die ein Annagramm sind
text_Histogram = dict() # erstellt ein Dictionary zum Zählen der Buchstaben im Text
wort_Histogram = dict() # erstellt ein Dictionary zum Zählen der Worte im Text
trennzeichen = " -> "  # Trennzeichen für join methode

def anna(txt):
    """Rekursive Funktion, die True liefert, wenn der übergebene Text ein Annagramm ist"""
    if len(txt)>1:
        if txt[:1].upper() == txt[len(txt)-1:].upper():
            inner_txt = txt[1:len(txt)-1]
            if anna(inner_txt):
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def histogram(d, text):
    """ zählt die Häufigkeit der elemente in text und addiert sie in einem dictionary"""
    # d = dict()
    for c in text:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def markov(text):
    """erstellt eine Markov Verteilung zu einen gegebenen Text - Häufigkeitszuordnung der Suffixe zum Präfix in einem Dictionary"""
    md = dict()
    wl = list(text.split())
    hl = []
    word1 = "initial"
    for word2 in wl:
        if word1 != "initial":
            # key = word1 + " " + word2
            if (word1, word2) not in md:
                md[(word1, word2)] = 1
            else:
                md[(word1, word2)] += 1
        word1 = word2
    for key, value in md.items():                       # Schleife über alle Elemente in WortHistogramm mit key + value
        hl.append((key[0], key[1], value))               # tausche key und value und hänge sie an das Dictionary für die Worthäufigkeit an
    return hl                                           # übergibt eine Tupelliste aus Präfix, Suffix und Häufigkeit

def zufalls_wort(h):
    """ liefert ein Zufallswort gemäß Häufigkeit in einem Histogramm"""
    t = []
    for wort, haeuf in h.items():
        t.extend([wort]*haeuf)
    return random.choice(t)

def extrahiere_liste(sl, pattern):
    """ extrahiert aus einer dreiTupel Liste alle zweier Tupel, zu denen das erste Element matched"""
    rd = {}
    for key1, key2, value in sl:                        # ietriere über dreier Tupel in der Liste
        if key1 == pattern:
            rd[key2] = value
    return rd

def textgenerator(ml, start, anz=50):
    d = []
    txt = start
    for i in range(anz):
        d = extrahiere_liste(ml, start)                  # erstelle subDictionary aus Folgewort + Häufigkeit für alle Elemente, bei denen der erste key korrekt ist
        start = zufalls_wort(d)                          # generiere ein Zufallswort aus dem Dictionary gemäß Häufigkeit und setze den Startwer neu
        txt += " " + start                              # hänge das Zufallswort an den text an
        print(txt)
    return txt

# Start des Text Analyse Programms
muster = input('Suchmuster für Mustervergleich und Zufallstext: ')

with open('/Users/oli/Python/TurtleWorld/TurtleTutorial/VettersEckfenster.txt') as fin:
    for line in fin:
        zaehler += 1                                        # Anzahl der Zeilen in der Datei
        sub_Dict = {10: 32}                                 # dictionary, dass für alle Line Feed ein Space setzt
        text_Block += line.translate(sub_Dict)              # erstellt Zeile für Zeile einen Textblock und ersetzt gemäß sub_Dict
        markov_List = markov(text_Block)                    # erstellt eine Häufigkeitsverteilung präfix zu suffix und Häufigkeit als dreier Tupel

        exclude_Dict = str.maketrans("", "", string.punctuation)      # erstellt ein dictionary, dass alle Sonderzeichen aus punctuation entfernt - Arg0+Arg1 ersetzen "" durch "" - der drite parameter wird zum entfernen genutzt
        zeile = line.strip().lower().translate(exclude_Dict)            # entfernt leerzeichen am Anfang und Ende vom String + ganzer String in lower case
        # zeile = line.strip().lower().strip(string.punctuation)            # entfernt leerzeichen am Anfang und Ende vom String + ganzer String in lower case - Alternative zu oben
        

        zeilen_Liste.append(zeile)               # hängt Zeile für Zeile an eine Liste von Zeilen - strip entfernt führende und endende leerzeichen
        zeilen_Wort_Liste.append(zeile.split())  # erweitert Zeile für Zeile eine Liste von Worten zu eine 2D Liste
        text_Histogram = histogram(text_Histogram, zeile)        # übergibt texthistogram und ergänzt alle neuen Einträge der neuen übergebenen Text Zeile
        wm = set(zeile.split())                  # erstellt ein Set von Worten (wm - wortmenge) aus der aktuellen Zeile
        for word in wm:
            if word not in wort_Histogram:
                worte_Menge.add(word)                       # ergänzt die Wortmenge der aktuellen Zeile zur Gesamtmenge
                wort_Histogram[word] = 1                    # Zähler für Wort histogramm auf 1
            else:
                wort_Histogram[word] += 1
        
        # muster prüfen
        if muster in line:
            muster_Zaehler += 1
            muster_Liste.append(zeile)

        # Annagramm prüfen
        if anna(zeile):
            anna_Zaehler += 1
            anna_Liste.append(zeile)

worte_Menge.remove(None)                            # erstes Element entfernen (NONE)
wortliste = list(worte_Menge)                       # Menge nach Liste transformieren
wortliste.sort()                                    # Liste sortieren

wh_ValueList = []                                   # initialisiert Liste für Worthäufigkeit
for key, value in wort_Histogram.items():           # Schleife über alle Elemente in WortHistogramm mit key + value
    wh_ValueList.append((value, key))               # tausche key und value und hänge sie an das Dictionary für die Worthäufigkeit an
wh_ValueList.sort(reverse=True)                     # sortiere umekehrt 

text_Zufall = textgenerator(markov_List, muster, zaehler//2)    # erstellt einen ZUfallstext auf Basis der Markov Verteilung und der Anzahl von Worten

print("Anzahl der Zeilen: ", zaehler)
print("Zeile 1, Wort 4: ", zeilen_Wort_Liste[1][3]) # Zugriff auf ein einzelnes Wort in der 2 D Liste
print("Anzahl der Buchstaben ingesammt: ", sum(text_Histogram.values()))
print("Anzahl der verschiedenen Buchtaben: ", len(text_Histogram))
for key in sorted(text_Histogram):                  # schleife über all Buchstaben, im Histogramm
    print(key, text_Histogram[key], "\t: ", "-" * int(text_Histogram[key]))

print(CGREEN + "Anzahl der Worte ingesammt: ", sum(wort_Histogram.values()))
print("Anzahl der verschiedenen Worte in der Datei: ", len(wortliste))
print("Liste aller Worte sortiert + Top 10: \n", wortliste)     # \ Shift + Alt + 7
for haeuf, wort in wh_ValueList[0:10]:               # Schleife über die 10 häufigsten Worte
    print(wort, "\t", haeuf)
print(CEND)                                          # Farbe zurück auf weiss

print(CBLUE + "Muster Zaehler: ", muster_Zaehler, CEND)
print(CBLUE + "Muster Match Liste: \n", trennzeichen.join(muster_Liste[:]), CEND)

print(CYELLOW + "Anna Zaehler: ", anna_Zaehler, CEND)
print(CYELLOW + "Annagramm Liste: \n", anna_Liste[:], CEND)

print(text_Block)
print(markov_List)
print(text_Zufall)