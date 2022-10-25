import string
import random
from collections import Counter
import time

# Kodowanie
def ac_dekod(txt):

    res = Counter(txt)

    # znaki
    znaki = list(res.keys())

    # czestotliwosc poszczegolnych znakow
    czestotl = list(res.values())

    prawdop = []
    for i in czestotl:
        prawdop.append(i / len(txt))

    print("Podane znaki: ")
    print(znaki)
    print("Czesc wiadomosci jaka pelnia poszczegolne znaki: ")
    print(prawdop)

    wysoki = 1.0
    niski = 0.0
    print("Zestawy przedzialow: ")
    for c in txt:
        diff = wysoki - niski
        index = znaki.index(c)
        for i in range(index):
            wysoki = niski + diff * prawdop[i]
            niski = wysoki

        wysoki = niski + diff * prawdop[index]
        print(f'Znak {c} -> Przedzial od: {niski}   do: {wysoki}')

    tag = (niski+wysoki)/2.0

    print('To co podales z klawiatury: ' + txt)
    print(str(niski) + '< zakodowany_tekst <' + str(wysoki))
    print('Zakodowana postac = ' + str(tag))

    with open('encode.ac', 'w') as fw:
        for i in znaki:
            fw.write(i + ' ')
        fw.write('\n')

        for i in prawdop:
            fw.write(str(i) + ' ')
        fw.write('\n')

        fw.write(str(tag))

    return znaki, prawdop, tag


# Dekodowanie
def ac_dekodowanie(znaki, prawdop, tag):
    wysoki = 1.0
    niski = 0.0
    output = ''
    c = ''
    while (c != '$'):
        diff = wysoki - niski
        for i in range(len(znaki)):
            wysoki = niski + diff * prawdop[i]
            if niski < tag < wysoki:
                break
            else:
                niski = wysoki
        c = znaki[i]
        output += c

    return output

def kodowanie_arytm(input):
    if '$' in input:
        input = input[0:input.index('$')]
    if input[-1] != '$':
        input += ''

    (znaki, prawdop, tag) = ac_dekod(input)
    output = ac_dekodowanie(znaki, prawdop, tag)
    return input == output
# podawane przez Uzytkownika
# tylko male litery, do 13 znakow
txt = input("Podaj tekst do zakodowania: ")
kodowanie_arytm(txt)


