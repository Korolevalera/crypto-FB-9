#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

vector<int> q_v, x_invert_v, a_v, b_v;

//читання з файлу
string inputf(ifstream& f, string str) {
	string a;
	f.open(str);
	if (f.fail()) {
		cout << "\n Fail to open the file";
		exit(1);
	}
	string extra = "";
	while (getline(f, a)) {
		extra += a;
	}
	f >> extra;
	f.close();
	return extra;
}
void outputf(ofstream& f, string a, string str) {
	f.open(str);
	if (f.fail()) {
		cout << "\n Fail to open the file";
		exit(1);
	}
	f << a;
	f.close();
}

vector<int> bigram_freq(string a_bigram[31][31], string txt, int lengthOfText, string alphabet, vector<int> y1, vector<int> y2, vector<int> Y) {
	int counter[31][31] = { 0 };
	int j1, j2;
	//цикл на підрахунок біграм (так як крок і=і+2 - біграми без перетину)
	for (int i = 0; i < lengthOfText; i = i + 2) {
		j1 = alphabet.find(txt[i]);
		j2 = alphabet.find(txt[i + 1]);
		counter[j1][j2]++;
	}
	string sa_frequencyOfBi[31][31];
	double a_frequencyOfBi[31][31];
	double frequencyOfBi;
	//цикл на підрахунок частоти кожної біграми
	for (int r = 0; r < 31; ++r) {
		for (int c = 0; c < 31; ++c) {
			frequencyOfBi = (counter[r][c] * 1.0) / (lengthOfText / 2);
			sa_frequencyOfBi[r][c] = a_bigram[r][c] + ": " + to_string(frequencyOfBi) + " ";
			a_frequencyOfBi[r][c] = frequencyOfBi;
		}
	}
	//знаходження 5 найчастіших біграм ШТ
	double maximum;
	int l1, l2;
	int count_cycle = 5;
	while (count_cycle != 0) {
		maximum = 0;
		for (int r = 0; r < 31; ++r) {
			for (int c = 5 - count_cycle; c < 31; ++c) {
				if (maximum < a_frequencyOfBi[r][c]) {
					maximum = a_frequencyOfBi[r][c];
					l1 = r;
					l2 = c;
				}
			}
		}
		y1.push_back(l1);
		y2.push_back(l2);
		a_frequencyOfBi[l1][l2] = 0;
		cout << "Max: " << "(" << alphabet[l1] << "," << alphabet[l2] << ") = " << maximum << endl;
		count_cycle--;
	}
	for (int i = 0; i < 5; i++) {
		Y.push_back(y1[i] * 31 + y2[i]);
		cout << "Y" << i << ": " << alphabet[y1[i]] << alphabet[y2[i]] << " = " << Y[i] << endl;
	}
	return Y;
}

int Euclid(int a, int b) {
	int q, r;
	//cout << "GSD (" << a << ", " << b << ") " << "= ";
	q = a / b;
	q_v.push_back(q);
	r = a - (b * q);
	//cout << "GSD (" << b << ", " << r << ")" << endl;
	if (r == 0) {
		return b;
	}
	else {
		Euclid(b, r);
	}
}

int extra_Euclid(vector<int> q_, vector<int> u_, vector<int> v_, int count, int const_x, int const_y, int m) {
	int u1, v1, a, d;
	for (int i = 0; i < q_v.size() - 1; i++) {
		u1 = u_[count - 2] - q_[count - 2] * u_[count - 1];
		v1 = v_[count - 2] - q_[count - 2] * v_[count - 1];
		//cout << "u[" << count << "]: " << u1 << endl;
		//cout << "v[" << count << "]: " << v1 << endl;
		u_.push_back(u1);
		v_.push_back(v1);
		d = u_[count] * m + v_[count] * const_x;
		//cout << "d: " << d << endl;
		count++;
	}
	cout << "GSD (" << m << ", " << const_x << ") = " << d << endl;
	if (d == 1) {//один розв'язок
		a = v_[v_.size() - 1];
		if (a < 0) {
			a = a + m;
		}
		//cout << a << endl;
		return a;
	}
	else {//d!|y
		if (const_y % d != 0) {
			cout << d << "!|" << const_y << endl;
			a = 0;
			return a;
		}
		else {//d|y - d розв'язків
			const_x = const_x / d;
			cout << "x* = " << const_x << endl;
			const_y = const_y / d;
			cout << "y* = " << const_y << endl;
			m = m / d;
			cout << "m* = " << m << endl;
			vector<int>().swap(q_v);
			cout << Euclid(m, const_x) << endl;
			u_ = { 1, 0 };
			v_ = { 0, 1 };
			a = extra_Euclid(q_v, u_, v_, 2, const_x, const_y, m);
			cout << "d:" << d << endl;
			int a0;
			a0 = (const_y * a) % m;
			cout << "a: " << a0 << endl;
			for (int i = 0; i < d; i++) {
				cout << "a[" << i << "]: " << a0 + i * m << endl;
			}
			return a;
		}
	}

}

int/*vector<int>*/ inverted_element(int y, int x, int x_place, vector<int> check_x) {
	int x_invert, m, a, new_x_place;
	m = 961;
	cout << "a = " << x << "^(-1)*" << y << " mod" << m << endl;
	vector<int> u = { 1, 0 };
	vector<int> v = { 0, 1 };
	vector<int>().swap(q_v);
	bool check_repeat = true;
	for (int i = check_x.size()-1; i >= 1; i--) {
		if (check_x[x_place] == check_x[i - 1]) {
			check_repeat = false;
			new_x_place = i - 1;
		}
	}
	if (check_repeat == true) {
		Euclid(m, x);
		x_invert = extra_Euclid(q_v, u, v, 2, x, y, m);
		//cout << "x_invert: " << x_invert << endl;
		x_invert_v.push_back(x_invert);
	}
	else {
		x_invert = x_invert_v[new_x_place];
		if (x_invert == 0) {
			Euclid(m, x); //знаходження НСД та q
			x_invert = extra_Euclid(q_v, u, v, 2, x, y, m);//знаходження u та v, причому v останній - наш обернений 
		}
		//cout << "x_invert: " << x_invert << endl;
		x_invert_v.push_back(x_invert);
	}
	
	if (x_invert != 0) {
		cout << x << "^(-1) = " << x_invert << endl;
		cout << "a = " << x_invert << "*" << y << " mod" << m << endl;
		a = (x_invert * y) % m;
		//cout << "a: " << a << endl;
		return a;
	}
	else {
		cout << x << "^(-1) doesn't exist!" << endl;
		return 0;
	}
}

void lin_comparison(vector<int> Y, vector<int> X) {
	int y, x, a, b;
	vector<int> y_, x_, check_x;
	int count_eq = 0;
	for (int i = 0; i < Y.size(); i++) {
		for (int j = 0; j < Y.size(); j++) {
			if (i != j) {
				y = Y[i] - Y[j];
				if (y < 0) {
					y = 961 + y;
				}
				y_.push_back(y);
				cout << count_eq << ") Y(" << i << ")-Y(" << j << ") = " << Y[i] << "-" << Y[j] << " = " << y_[count_eq] << endl;

				x = X[i] - X[j];
				if (x < 0) {
					x = 961 + x;
				}
				x_.push_back(x);
				cout << "   X(" << i << ")-X(" << j << ") = " << X[i] << "-" << X[j] << " = " << x_[count_eq] << endl;

				//cout << "   " << y_[count_eq] << " = " << x_[count_eq] << "a mod961" << endl;
				cout << endl;
				count_eq++;
			}
		}
	}
	for (int i = 0; i < y_.size(); i++) {
		for (int j = 0; j < x_.size(); j++) {
			cout << y_[i] << " = " << x_[j] << "a mod961" << endl;

			check_x.push_back(x_[j]);
			//знаходження ключа (а) через знаходження оберненого елемента до х
			a = inverted_element(y_[i], x_[j], j, check_x);
			a_v.push_back(a);
			cout << "a = " << a << endl;
			cout << endl;
		}
	}
	int count_y, count_x, counter;
	count_y = 0;
	count_x = 0;
	counter = 0;
	//знаходження ключа (b)
	for (int i = 0; i < a_v.size(); i++) {
		for (int i_y = 0; i_y < Y.size(); i_y++) {
			for (int j_x = 0; j_x < X.size()-1; j_x++) {
				count_x = count_x % 5;
				if (a_v[i] != 0) {
					b = (Y[count_y] - a_v[i] * X[count_x]) % 961;
					if (b < 0) {
						b = b + 961;
					}
					b_v.push_back(b);
					cout << "b = Y" << count_y << "-a[" << i << "]*X" << count_x << " = ";
					cout << Y[count_y] << "-" << a_v[i] << "*" << X[count_x] << " mod961 = " << b << endl;
				}
				else {
					b = 0;
					cout << "empty set!" << endl;
					b_v.push_back(b);
				}
				i++;
			}
			count_x++;
		}
		counter++;
		if (counter == 4) {
			count_y++;
			counter = 0;
		}
		i--;
	}
}

bool check_freq(string txt, string alphabet, int lengthOfAlphabet, int lengthOfText) {
	//цикл на підрахунок усіх літер в тексті(від а до я)
	char symbol;
	int a_quantityOfSym[31];
	double a_frequencyOfSym[31];
	double frequencyOfSym;
	for (int i = 0; i < lengthOfAlphabet; i++) {
		symbol = alphabet[i];
		const auto count_symbol = count(txt.cbegin(), txt.cend(), symbol);
		a_quantityOfSym[i] = count_symbol;//запис кі-сті літер у масив
	}
	//цикл на підрахунок частоти кожної літери
	for (int i = 0; i < 31; i++) {
		frequencyOfSym = (a_quantityOfSym[i] * 1.0) / lengthOfText;
		a_frequencyOfSym[i] = frequencyOfSym;//запис частоти кожної літери у масив
	}
	double maximum = 0.0;
	double minimum = 1.0;
	for (int i = 0; i < lengthOfAlphabet; i++) {
		maximum = max(maximum, a_frequencyOfSym[i]);
		minimum = min(minimum, a_frequencyOfSym[i]);
	}
	//cout << "Max: " << maximum << endl;
	int most_freq, less_freq;
	for (int i = 0; i < lengthOfAlphabet; i++) {
		if (a_frequencyOfSym[i] == minimum) {
			less_freq = i;
		}
		if (a_frequencyOfSym[i] == maximum) {
			a_frequencyOfSym[i] = 0;
			most_freq = i;
			maximum = 0;
			//cout << "The most frequent letter: \"" << alphabet[i] << "\"" << endl;
		}
	}
	for (int i = 0; i < lengthOfAlphabet; i++) {
		maximum = max(maximum, a_frequencyOfSym[i]);
	}
	for (int i = 0; i < lengthOfAlphabet; i++) {
		if (a_frequencyOfSym[i] == maximum) {
			cout << "The most frequent letters: \"" << alphabet[most_freq] << "\" and \"" << alphabet[i] << "\" ";
			cout << " and the less is: \"" << alphabet[less_freq] << "\"" << endl;
			if ((alphabet[most_freq] == 'о' or alphabet[most_freq] == 'е' or alphabet[most_freq] == 'а') and (alphabet[i] == 'о' or alphabet[i] == 'е' or alphabet[i] == 'а') and (alphabet[less_freq] == 'ф' or alphabet[less_freq] == 'щ' or alphabet[less_freq] == 'э')) {
				cout << "RETURN \"" << alphabet[most_freq] << "\", \"" << alphabet[i] << "\" and \"" << alphabet[less_freq] << "\"" << endl;
				return true;
			}
			else {
				return false;
			}
		}
	}
}

bool check_bigr(string txt, int lengthOfText, vector<string> falseBigram, int lengthOfFalse) {
	string bigram;
	int count = 0;
	//цикл на підрахунок біграм (так як крок і=і+1 - біграми з перетином)
	for (int i = 0; i < lengthOfText; i++) {
		bigram = txt[i];
		bigram = bigram + txt[i + 1];
		for (int j = 0; j < lengthOfFalse; j++) {
			if (bigram == falseBigram[j]) {
				count++;
				break;
			}
		}
		if (count != 0) {
			break;
		}
	}
	if (count != 0) {
		return false;
	}
	else {
		return true;
	}
}

int main() {
	setlocale(LC_ALL, "Russian");
	ifstream f;
	ofstream f1;
	string file_name, txt_before, txt_after;
	cout << "Enter the root to .txt file: ";
	cin >> file_name;
	txt_before = inputf(f, file_name);
	//cout << txt_before << endl;
	string alphabet;
	int lengthOfText;
	lengthOfText = txt_before.length();
	alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя";
	int lengthOfAlphabet = alphabet.length();

	string a_bigram[31][31];
	string bigram = "";
	char sym1, sym2;
	//цикл на заповнення біграм алфавіту
	for (int r = 0; r < 31; ++r) {
		for (int c = 0; c < 31; ++c) {
			sym1 = alphabet[r];
			sym2 = alphabet[c];
			string bi1(1, sym1);
			string bi2(1, sym2);
			bigram = bi1 + bi2;
			a_bigram[r][c] = bigram;
		}
	}
	cout << endl;

	vector<int> y1, y2, x1, x2;
	vector<int> Y, X;
	//знаходження 5 найчастіших біграм в ШТ
	Y = bigram_freq(a_bigram, txt_before, lengthOfText, alphabet, y1, y2, Y);

	//5 найчастіших біграм в російській мові
	X.push_back(alphabet.find('с') * 31 + alphabet.find('т'));
	X.push_back(alphabet.find('н') * 31 + alphabet.find('о'));
	X.push_back(alphabet.find('т') * 31 + alphabet.find('о'));
	X.push_back(alphabet.find('н') * 31 + alphabet.find('а'));
	X.push_back(alphabet.find('е') * 31 + alphabet.find('н'));

	for (int i = 0; i < 5; i++) {
		cout << "X" << i << ": " << X[i] << endl;
	}

	//розв'язання лінійних порівнянь
	lin_comparison(Y, X);

	vector<int>().swap(y1);
	vector<int>().swap(y2);
	vector<int>().swap(Y);
	vector<int>().swap(X);
	int count_Y = 0;
	//розбиваємо текст на біграми
	for (int i = 0; i < lengthOfText; i=i+2) {
		y1.push_back(alphabet.find(txt_before[i]));
		y2.push_back(alphabet.find(txt_before[i+1]));
		Y.push_back(y1[count_Y] * 31 + y2[count_Y]);
		//cout << "Y: " << Y[count_Y] << endl;
		count_Y++;
	}

	vector<int> u_, v_, a_inv_v, a_, b_, x_;
	int a_inv, new_a_place;
	int a, b, m, x;
	m = 961;
	bool check_repeat = true;
	for (int i = 0; i < a_v.size(); i++) {
		if (a_v[i] != 0) {
			vector<int>().swap(q_v);
			u_ = { 1, 0 };
			v_ = { 0, 1 };
			check_repeat = true;

			a = a_v[i];
			b = b_v[i];
			a_.push_back(a);
			
			for (int j = a_.size() - 1; j >= 1; j--) {
				if (a_[i] == a_[j - 1]) {
					check_repeat = false;
					new_a_place = j - 1;
				}
			}
			if (check_repeat == true) {
				Euclid(m, a);
				a_inv = extra_Euclid(q_v, u_, v_, 2, a, Y[0]-b, m);
				//cout << "x_invert: " << x_invert << endl;
				a_inv_v.push_back(a_inv);
			}
			else {
				a_inv = a_inv_v[new_a_place];
				if (a_inv == 0) {
					Euclid(m, a);
					a_inv = extra_Euclid(q_v, u_, v_, 2, a, Y[0] - b, m);
				}
				//cout << "x_invert: " << x_invert << endl;
				a_inv_v.push_back(a_inv);
			}
			//cout << a << "^(-1) = " << a_inv << endl;
			b_.push_back(b);
		}
		else {
			a = a_v[i];
			a_.push_back(a);
		}
	}
	//знаходження порядок біграм Х
	for (int i = 0; i < Y.size(); i++) {
		x = (a_inv_v[0] * (Y[i] - b_[0])) % m;
		if (x < 0) {
			x = x + m;
		}
		//cout << "x = " << x << endl;
		X.push_back(x);
	}
	cout << endl;
	vector<vector<int>> X_all;
	for (int i = 0; i < a_inv_v.size(); i++) {
		vector<int>().swap(x_);
		for (int j = 0; j < Y.size(); j++) {
			x = (a_inv_v[i] * (Y[j] - b_[i])) % m;
			if (x < 0) {
				x = x + m;
			}
			//cout << "x[" << i << "] = " << x << endl;
			x_.push_back(x);
		}
		X_all.push_back(x_);
	}

	vector<string> all_text, filtered_text;
	//розбиття порядку біграми на порядок літер
	for (int i = 0; i < X_all.size(); i++) {
		for (int j = 0; j < x_.size(); j++) {
			//cout << "X"<<i<<"["<< j << "] = " << X_all[i][j] << endl;
			x1.push_back(X_all[i][j] / 31);
			x2.push_back(X_all[i][j] % 31);
			txt_after = txt_after + alphabet[x1[j]] + alphabet[x2[j]];
		}
		//cout << "///////Text " << i << "///////" << endl;
		//cout << txt_after << endl;
		all_text.push_back(txt_after);
		vector<int>().swap(x1);
		vector<int>().swap(x2);
		txt_after = "";
	}
	//автоматичний розпізнавач російської мови (частота літер)
	for (int i = 0; i < all_text.size(); i++) {
		if (check_freq(all_text[i], alphabet, lengthOfAlphabet, lengthOfText)) {
			filtered_text.push_back(all_text[i]);
		}
	}
	//cout << "size: " << filtered_text.size() << endl;
	vector<string> falseBigram = { "уь","еь", "ыь", "аь", "оь", "эь", "яь", "иь", "ьь", "юь" };
	int lengthOfFalse;
	lengthOfFalse = falseBigram.size();
	//автоматичний розпізнавач російської мови (хибні біграми)
	for (int i = 0; i < filtered_text.size(); i++) {
		if (check_bigr(filtered_text[i], lengthOfText, falseBigram, lengthOfFalse)) {
			txt_after = filtered_text[i];
		}
	}
	cout << endl;
	cout << txt_after << endl;
	cout << "New .txt is ready. Enter the root to it: ";
	cin >> file_name;
	outputf(f1, txt_after, file_name);
}