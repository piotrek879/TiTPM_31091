#include<iostream>
#include<stdlib.h>
#include<math.h>
#include<string.h>

using namespace std;

int a, b, c, t, i, flag;
long int e[50], d[50], temp[50], j;
char en[50], m[50];
char wiadomosc[100];
int prime(long int);
void klucz_szyfrujacy();
long int cd(long int);
void szyfrowanie();
void deszyfrowanie();

int main()
{
    cout << endl << "Podaj liczbe pierwsza: ";
    cin >> a;

    //sprawdzamy czy ta liczba jest pierwsza czy tez nie
    flag = prime(a);
    if (flag == 0)
    {
        cout << endl << "Podana liczba nie jest liczba pierwsza!!!";
        exit(0);
    }

    cout << endl << "Podaj kolejna liczbe pierwsza: ";
    cin >> b;

    flag = prime(b);
    if (flag == 0 || a == b)
    {
        cout << endl << "Podana liczba nie jest liczba pierwsza!!!";
        exit(0);
    }

    cout << endl << "Podaj wiadomosc do zaszyfrowania: ";
    cin >> wiadomosc;

    for (i = 0; wiadomosc[i] != NULL; i++)
        m[i] = wiadomosc[i];
    c = a * b;
    t = (a - 1) * (b - 1);

    klucz_szyfrujacy();
    cout << endl << "Mozliwe wartosci wykladnika prywatnego i publicznego to: ";

    for (i = 0; i < j - 1; i++)
        cout << "\c" << e[i] << "\t" << d[i];

    szyfrowanie();
    deszyfrowanie();
    return 0;
}

int prime(long int pr)
{
    int i;
    j = sqrt(pr);
    for (i = 2; i <= j; i++)
    {
        if (pr % i == 0)
            return 0;
    }
    return 1;
}

//deszyfrowanie
void klucz_szyfrujacy()
{
    int k;
    k = 0;
    for (i = 2; i < t; i++)
    {
        if (t % i == 0)
            continue;
        flag = prime(i);
        if (flag == 1 && i != a && i != b)
        {
            e[k] = i;
            flag = cd(e[k]);
            if (flag > 0)
            {
                d[k] = flag;
                k++;
            }
            if (k == 99)
                break;
        }
    }
}

long int cd(long int a)
{
    long int k = 1;
    while (1)
    {
        k = k + t;
        if (k % a == 0)
            return(k / a);
    }
}

//zaszyfrowanie
void szyfrowanie()
{
    long int pt, ct, key = e[0], k, len;
    i = 0;
    len = strlen(wiadomosc);

    while (i != len)
    {
        pt = m[i];
        pt = pt - 96;
        k = 1;
        for (j = 0; j < key; j++)
        {
            k = k * pt;
            k = k % c;
        }
        temp[i] = k;
        ct = k + 96;
        en[i] = ct;
        i++;
    }
    en[i] = -1;
    cout << endl << "Zaszyfrowana wiadomosc ma postac: ";
    for (i = 0; en[i] != -1; i++)
        cout << en[i];
}

//odszyfrowywaniea
void deszyfrowanie()
{
    long int pt, ct, key = d[0], k;
    i = 0;
    while (en[i] != -1)
    {
        ct = temp[i];
        k = 1;
        for (j = 0; j < key; j++)
        {
            k = k * ct;
            k = k % c;
        }
        pt = k + 96;
        m[i] = pt;
        i++;
    }
    m[i] = -1;
    cout << endl << "Rozszyfrowana wiadomosc ma postac: ";
    for (i = 0; m[i] != -1; i++)
        cout << m[i];

    cout << endl;
}