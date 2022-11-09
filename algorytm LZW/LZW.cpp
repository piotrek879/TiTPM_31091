#include <map>
#include <string>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <fstream>
using namespace std;

vector<int> kodowanie(string s1)
{
	cout << "Kodowanie\n";
	unordered_map<string, int> table;
	for (int i = 0; i <= 255; i++) {
		string ch = "";
		ch += char(i);
		table[ch] = i;
		
	}

	string p = "", c = "";
	p += s1[0];
	int code = 256;
	vector<int> output_code;
	
	cout << "Sl.podst\tSl.pelny\tKodowanie\n";
	for (int i = 0; i < s1.length(); i++) {
		
		if (i != s1.length() - 1)
			c += s1[i + 1];
		if (table.find(p + c) != table.end()) {
			p = p + c;
			
		}
		else {
			cout << p << "\t" << table[p] << "\t\t"
				<< p + c << "\t" << code << endl;
			

			
			output_code.push_back(table[p]);
			table[p + c] = code;
			code++;
			
			p = c;
		}
		
		c = "";
		
	}
	cout << p << "\t" << table[p] << endl;
	output_code.push_back(table[p]);
	ofstream zapis("wynik.txt");
	for (int i = 0; i < output_code.size(); i++) {
		zapis <<code<<"\t"<<'.'<< p;
	zapis.close(); //zapis pliku - zamkniecie
	}
	
	return output_code;
}

void dekodowanie(vector<int> op)
{
	cout << "\nDekodowanie\n";
	unordered_map<int, string>table;
	for (int i = 0; i <= 255; i++) {
		string ch = "";
		ch += char(i);
		table[i] = ch;
	}
	int old = op[0], n;
	string s = table[old];
	string c = "";
	c += s[0];
	cout << s;
	int count = 256;
	for (int i = 0; i < op.size() - 1; i++) {
		n = op[i + 1];
		if (table.find(n) == table.end()) {
			s = table[old];
			s = s + c;
		}
		else {
			s = table[n];
		}
		cout << s;
		c = "";
		c += s[0];
		table[count] = table[old] + c;
		count++;
		old = n;
	}
}
int main()
{

	string s;
	cout << "Podaj swoj teskst do zakodowania: ";
	cin >> s;
	vector<int> output_code = kodowanie(s);
	cout << "Zakodowana postac: ";
	for (int i = 0; i < output_code.size(); i++) {
		cout << output_code[i] << " ";
	}
	cout << endl;
	dekodowanie(output_code);
	

	
	return 0;
}
