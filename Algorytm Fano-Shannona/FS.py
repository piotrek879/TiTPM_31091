import numpy as np
def skaluj_kraw_interw(orgin_kraw_interw, min_val, max_val):
    "Skalujemy oryginalne krawędzie przedziału do nowych wartości minimalnych i maksymalnych"
    nowe_krawedzie = min_val + (max_val - min_val)*orgin_kraw_interw
    return nowe_krawedzie
def symbol_na_indeks(symbol, alfabet):
    """Przyporządkuj symbol do indeksu według alfabetu (indeksowanie na podstawie 1, ponieważ pracujemy na przedziałach,
       zwracany indeks będzie zgodny z górną krawędzią interwału.)"""
    assert len(set(alfabet)) == len(alfabet), 'Niepotrzebny'
    assert symbol in alfabet, 'Symbolu {} nie ma w alfabecie'.format(symbol)
    return alfabet.index(symbol) + 1 #


def pobierz_inter_z_symbolu(aktualny_symbol, alfabet, aktualny_min, aktualny_max, orgin_kraw_interw):
    """Uzyskujemy nowy interwał dla nowego symbolu na podstawie bieżących min i maks oraz oryginalnych krawędzi interwału"""
    aktualny_sygnal_ind = symbol_na_indeks(aktualny_symbol, alfabet)
    aktualne_krawedzie_interw = skaluj_kraw_interw(orgin_kraw_interw, aktualny_min, aktualny_max)
    nowe_min = aktualne_krawedzie_interw[aktualny_sygnal_ind - 1]
    nowe_max = aktualne_krawedzie_interw[aktualny_sygnal_ind]

    return (nowe_min, nowe_max)
def krawedzie_interw(pmf):
    """Zwracamy listę krawędzi przedziałów, biorąc pod uwagę funkcję masy prawdopodobieństwa"""
    return np.array([np.sum(pmf[:i]) for i in range(len(pmf) + 1)])


def interw_arytmet(alfabet, sygnal, pmf):
    """Uzyskujemy listę przedziałów uzyskanych przez arytmetyczne kodowanie sygnału.

    Arg:
        alfabet: Lista unikalnych znaakow.
        sygnal: Ciąg symboli, w którym każdy symbol musi należeć do alfabetu.
        pmf: Funkcja masy prawdopodobieństwa dla elementów w alfabecie.
            pmf[i] jest prawdopodobieństwem alfabetu[i].

    Zwraca:
        Przedziały: Lista (min, max) krotek zmiennoprzecinkowych, 
        gdzie (min, max) to krawędzie przedziału odpowiedniego symbolu. Ta lista ma jeden przedział na symbol 
        w sygnał wejściowy..
    """
    orgin_kraw_interw = krawedzie_interw(pmf)
    sygnal_list = list(sygnal)
    aktualny_min, aktualny_max = pobierz_inter_z_symbolu(sygnal_list[0], alfabet, 0.0, 1.0, orgin_kraw_interw)
    przedzialy = [(aktualny_min, aktualny_max)]

    for i, symbol in enumerate(sygnal_list[1:]):
        aktualny_min, aktualny_max = pobierz_inter_z_symbolu(symbol, alfabet, aktualny_min, aktualny_max, orgin_kraw_interw)
        przedzialy.append((aktualny_min, aktualny_max))
    return przedzialy

#na binarne
def sekwencja_binarna(dziesietne):
    """Zwraca binarną reprezentację danych wejściowych.

    Argumenty, jakie przyjmuje:
        dziesietne: skalarne float w [0, 1) przedział jest w połowie otwarty
    Zwraca:
        sekwencja_bin: Lista liczb całkowitych w {0, 1}
    """
    reminder = dziesietne
    sekwencja_bin = [int(np.floor(2 * reminder))]
    ind = 0
    while reminder > 1e-10:
        reminder = 2 * reminder - sekwencja_bin[ind]
        sekwencja_bin.append(int(np.floor(2 * reminder)))
        ind += 1
    return sekwencja_bin

#najkrotsze
def najkrotsza_binarnie(d_interval):
    """Znajdujemy najkrótszą reprezentację binarną w przedziale dziesietnym."""
    d_min, d_max = d_interval
    assert d_min < d_max, 'Potrzebujemy ściśle rosnącego interwału'
    assert d_min >= 0, 'Ujemna dolna granica na interwale / przedziale'
    assert d_max < 1, 'Górna granica przedziału większa lub równa 1'

    # Inicjalizacja bieżącego przedziału (c_min, c_max)
    c_min = 0.0
    c_max = 1.0

    # Kontynuujemy, aż obecny przedział (c_min, c_max) będzie zawarty w środku
    # przedziału (d_min, d_max).
    #  Dodanie 1 do sekwencji binarnej zwiększa c_min, ale pozostawia c_max stałe.
    # Dodanie 0 do sekwencji binarnej zmniejsza c_max, ale pozostawia c_min stałe.

    k = 1
    bin_sekw = []
    while True:
        # Zawsze dodaje 1 do bin_sekw, jeśli to możliwe
        if c_min < d_min and c_min + 1 / 2 ** k < d_max:
            c_min = c_min + 1 / 2 ** k
            bin_sekw.append(1)
        else:
            if c_max > d_max and c_max - 1 / 2 ** k > d_min:
                c_max = c_max - 1 / 2 ** k
                bin_sekw.append(0)
            else:
                # Brak zmian w bieżącym interwale, skończyliśmy
                break
        k = k + 1
    return bin_sekw

#kodowanie
def arithmetic_encoding(alfabet, pmf, sygnal):

    przedzialy = interw_arytmet(alfabet, sygnal, pmf)
    bin_sekw = najkrotsza_binarnie(przedzialy[-1])
    return bin_sekw

#dekodowanie
def interval_w_narastaniu(numer, lista_wzrast):
    """Znajdujemy przedział, w którym liczba znajduje się na liście rosnących liczb."""
    assert numer >= lista_wzrast[0], 'numer jest poza lista_wzrast'
    assert numer <= lista_wzrast[-1], 'numer jest poza lista_wzrast'
    interval = None
    for i in range(1, len(lista_wzrast)):
        if numer >= lista_wzrast[i-1] and numer <= lista_wzrast[i]:
            interval = (i-1, i)
    assert interval is not None, 'Nieprawidłowe dane wejściowe do interval_w_narastaniu'
    return interval


def dziesietne_z_binarnych(bin_sekw):

    half_powered = np.array([1 / 2 ** k for k in range(1, len(bin_sekw) + 1)])
    return np.dot(np.array(bin_sekw), half_powered)


def dekodowanie_arytm(alfabet, pmf, zakodowany_sygnal, num_to_decode):

    # Inicjalizacja
    dziesietne_sygnal = dziesietne_z_binarnych(zakodowany_sygnal)
    orgin_kraw_interw = krawedzie_interw(pmf)
    aktual_symbol_inds = interval_w_narastaniu(dziesietne_sygnal, orgin_kraw_interw)
    symbole = [alfabet[aktual_symbol_inds[0]]]
    nowe_min = orgin_kraw_interw[aktual_symbol_inds[0]]
    nowe_max = orgin_kraw_interw[aktual_symbol_inds[1]]
    for num_decoded in range(1, num_to_decode):
        aktualne_krawedzie_interw = skaluj_kraw_interw(orgin_kraw_interw, nowe_min, nowe_max)
        aktual_symbol_inds = interval_w_narastaniu(dziesietne_sygnal, aktualne_krawedzie_interw)
        symbole.append(alfabet[aktual_symbol_inds[0]])
        nowe_min = aktualne_krawedzie_interw[aktual_symbol_inds[0]]
        nowe_max = aktualne_krawedzie_interw[aktual_symbol_inds[1]]

    return ''.join(symbole)
alfabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
pmf = np.array([8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]) / 100
sygnal = input("Podaj tekst do zakodowania: ")
all_freq = {}

for i in sygnal:
    if i in all_freq:
        all_freq[i] += 1
    else:
        all_freq[i] = 1



zakodowany_sygnal = arithmetic_encoding(alfabet, pmf, sygnal)
odkodowany_sygnal = dekodowanie_arytm(alfabet, pmf, zakodowany_sygnal, len(sygnal))

print('Podany tekst:         {}'.format(sygnal))
print('Zakodowana postac: {}'.format(''.join([str(s) for s in zakodowany_sygnal])))
print('Odkodowana postac: {}'.format(odkodowany_sygnal))
print("Liczba poszczegolnych znakow w podanym przez Ciebie tekscie wynosi :\n "
      + str(all_freq))