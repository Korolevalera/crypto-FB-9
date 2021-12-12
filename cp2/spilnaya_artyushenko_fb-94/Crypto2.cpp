#include <iostream>
#include <fstream>
#include <Windows.h>
#include <algorithm>
#include <string>
#include <stdio.h>
#include <string.h>
#include <cstring>

using namespace std;

void print_menu() {
    system("cls"); // очищаем экран
    cout << "Что вы хотите сделать?" << endl;
    cout << "1. Закодировать шифром Виженера" << endl;
    cout << "2. Разкодировать шифр Виженера с помощью известного ключа" << endl;
    cout << "3. Посчитать индекс совпадений в шифрованом тексте" << endl;
    cout << "4. Посчитать индекс совпадений в открытом тексте" << endl;
    cout << "5. Посчитать индекс совпадений в 6 варианте" << endl;
    cout << "6. Поиск длины ключа" << endl;
    cout << "7. Поиск ключа" << endl;
    cout << "8. Разшифровать вариант 6" << endl;
    cout << "9. Exit" << endl;
    cout << ">"; 
}
int get_variant(int count) {
    int variant;
    string s; // строка для считывания введённых данных
    getline(cin, s); // считываем строку

    // пока ввод некорректен, сообщаем об этом и просим повторить его
    while (sscanf_s(s.c_str(), "%d", &variant) != 1 || variant < 1 || variant > count) {
        cout << "> : "; // выводим сообщение об ошибке
        getline(cin, s); // считываем строку повторно
    }

    return variant;
}
void EncryptVigenereСipher()
{
    string B, C, D = "";
    string A = "абвгдежзийклмнопрстуфхцчшщъыьэюя"; //наш алфавит
    setlocale(LC_ALL, "RUS");
    ifstream fin;
    fin.open("D:\\Crypto2\\text.txt");
    while (fin) {
        getline(fin, B);
    }
    fin.close();
    cout << "Введите ключ : " ;
    cin >> C;
    int* F = new int[B.size()];
    int* G = new int[B.size()];
    int c = C.size(); //делаем замену переменных для удобства
    int b = B.size();
    cout << "\nРазмер ключа : " << c <<endl;
    //Первое условие. Если длина вводимого слова болше, либо равна длине ключа
    if (b >= c)
    {
        for (int i = 0; i < (b / c); i++)
        {
            D = D + C; //Записываем целое количество ключа. Растягиваем ключ по длине слова.
        }
        for (int j = 0; j < (b % c); j++)
        {
            D = D + C[j];
        }
    }
    else
    {
        for (int s = 0; s < b; s++)
        {
            D = D + B[s];
        } //Иначе если ключ длинее слова, ускорачиваем ключ до длины слова.
    }
    for (int k = 0; k < b; k++)
    {
        for (int n = 0; n < 32; n++)
        {
            if (B[k] == A[n])
            {
                F[k] = n;
            }
            if (D[k] == A[n])
            {
                G[k] = n;
            } //Здесь мы уже начинаем щифровать. Смысл заключается а том, что мы ишем номер буквы 
              //вводимом ключе и номере, а после чего записываем
            //их в массив
        }
    }
    int e = 0;
    for (int u = 0; u < b; u++)
    {
        e = ((F[u] + G[u]) % 32);
        B[u] = A[e];
    }
    ofstream fout;
    fout.open("D:\\Crypto2\\encode.txt");
    fout << B ;
    fout.close();
}
void DecipherVigenereСipher()
{
    string B, C, D = "";
    string A = "абвгдежзийклмнопрстуфхцчшщъыьэюя"; //наш алфавит
    setlocale(LC_ALL, "RUS");
    ifstream fin;
    fin.open("D:\\Crypto2\\encode.txt");
    while (fin) {
        getline(fin, B);
    }
    fin.close();
    cout << "Введите ключ : ";
    cin >> C;
    int* F = new int[B.size()];
    int* G = new int[B.size()];
    int c = C.size(); //делаем замену переменных для удобства
    int b = B.size();
    cout << "\nРазмер ключа : " << c << endl;
    //Первое условие. Если длина вводимого слова болше, либо равна длине ключа
    if (b >= c)
    {
        for (int i = 0; i < (b / c); i++)
        {
            D = D + C; //Записываем целое количество ключа. Растягиваем ключ по длине слова.
        }
        for (int j = 0; j < (b % c); j++)
        {
            D = D + C[j];
        }
    }
    else
    {
        for (int s = 0; s < b; s++)
        {
            D = D + B[s];
        } //Иначе если ключ длинее слова, ускорачиваем ключ до длины слова.
    }
    for (int k = 0; k < b; k++)
    {
        for (int n = 0; n < 32; n++)
        {
            if (B[k] == A[n])
            {
                F[k] = n;
            }
            if (D[k] == A[n])
            {
                G[k] = n;
            } //Здесь мы уже начинаем щифровать. Смысл заключается а том, что мы ишем номер буквы 
              //вводимом ключе и номере, а после чего записываем
            //их в массив
        }
    }
    int e = 0;
    for (int u = 0; u < b; u++)
    {
        e = ((F[u] - G[u]));
        if (e < 0)
        {
            e = e + 32;
        }
        else
        {
            e = e % 32;
        }
        B[u] = A[e];
    }
    ofstream fout;
    fout.open("D:\\Crypto2\\decipher.txt");
    fout << B;
    fout.close();
}
void IndexTextEncode()
{
    double count = 0;
    double index = 0;
    char ch;
    double letter;
    double freque;
    const int SIZE = 32;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    fin.open("D:\\Crypto2\\encode.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        while (fin.get() != EOF)
        {
            count++;
        }
    }
    fin.close();
    for (int i = 0; i < SIZE; i++)
    {
        fin.open("D:\\Crypto2\\encode.txt");
        if (!fin.is_open())
        {
            cout << "Ошибка открытия файла!\n";
        }
        else
        {
            letter = 0;
            freque = 0;
            while (fin.get(ch))
            {
                if (ch == alph[i])
                {
                    letter++;
                }
            }
            freque = (letter) / (count);
            cout << alph[i] << " | " << letter << " -> " << freque << endl;
            index = index + (freque * freque);
        }
        fin.close();
    }
    cout << " Индекс соответствия : " << index << endl;
}
void IndexText()
{
    float count = 0;
    float index = 0;
    char ch;
    char ch1;
    float letter;
    float freque;
    const int SIZE = 32;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    fin.open("D:\\Crypto2\\text.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        while (fin.get() != EOF)
        {
            count++;
        }
    }
    fin.close();
    for (int i = 0; i < SIZE; i++)
    {
        fin.open("D:\\Crypto2\\text.txt");
        if (!fin.is_open())
        {
            cout << "Ошибка открытия файла!\n";
        }
        else
        {
            letter = 0;
            freque = 0;
            while (fin.get(ch1))
            {
                if (ch1 == alph[i])
                {
                    letter++;
                }
            }
            freque = (letter) / (count);
            cout << alph[i] << " | " << letter << " -> " << freque << endl;
            index = index + (freque * freque);
        }
        fin.close();
    }
    cout << " Индекс соответствия : " << index << endl;
}
void IndexVariant()
{
    double count = 0;
    double index = 0;
    char ch;
    double letter;
    double freque;
    const int SIZE = 32;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    fin.open("D:\\Crypto2\\variant6.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        while (fin.get() != EOF)
        {
            count++;
        }
    }
    fin.close();
    for (int i = 0; i < SIZE; i++)
    {
        fin.open("D:\\Crypto2\\variant6.txt");
        if (!fin.is_open())
        {
            cout << "Ошибка открытия файла!\n";
        }
        else
        {
            letter = 0;
            freque = 0;
            while (fin.get(ch))
            {
                if (ch == alph[i])
                {
                    letter++;
                }
            }
            freque = (letter) / (count);
            cout << alph[i] << " | " << letter << " -> " << freque << endl;
            index = index + (freque * freque);
        }
        fin.close();
    }
    cout << " Индекс соответствия : " << index << endl;
}
void FindLengthKey()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    const int SIZE = 32;
    char ch;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    int key;
    int c;
    int k = 0;
    cout << "Введите предпологаемый ключ : " << endl;
    cin >> key;
    ofstream fout;
    fout.open("D:\\Crypto2\\variant_key.txt");
    for (int i = 0; i < key; i++)
    {
        c = 0;
        fin.open("D:\\Crypto2\\variant6.txt");
        while (fin.get(ch))
        {
            if (c % key == k)
            {
                fout << ch;
            }
            c++;
        }
        k++;
        fin.close();
    }
    fout.close();
    int count = 0;
    fin.open("D:\\Crypto2\\variant_key.txt");
    while (fin.get() != EOF)
    {
        count++;
    }
    cout << "Количество символов в файле : " << count << endl;
    fin.close();
    int g = 0;
    double letter;
    double index;
    double index_mid = 0;
    int block = 0;
    int length = count / key;
    int block_text = length;
    for (int j = 0; j < key; j++)
    {
        for (int i = 0; i < SIZE; i++)
        {
            g = 0;
            letter = 0;
            index = 0;
            fin.open("D:\\Crypto2\\variant_key.txt");
            while (fin.get(ch))
            {
                if (block <= g && g <= block_text)
                {
                    if (ch == alph[i])
                    {
                        letter++;
                    }
                }
                g++;
            }
            fin.close();
            index = (letter * (letter - 1)) / (length * (length - 1));
            index_mid = index_mid + index;
        }
        block = block_text;
        block_text += length;
        cout << index_mid << endl;
        index_mid = 0;
    }
}
void FindKey()
{
    const int SIZE = 32;
    char ch;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    int count = 0;
    fin.open("D:\\Crypto2\\variant_key.txt");
    while (fin.get() != EOF)
    {
        count++;
    }
    cout << "Количество символов в файле : " << count << endl;
    fin.close();
    int g = 0;
    double letter;
    int block = 0;
    int length = count / 17;
    int block_text = length;
    double litter = 0;
    char mass[17];
    for (int j = 0; j < 17; j++)
    {
        g = 0;
        litter = 0;
        for (int i = 0; i < SIZE; i++)
        {
            fin.open("D:\\Crypto2\\variant_key.txt");
            letter = 0;
            g = 0;
            while (fin.get(ch))
            {
                if (block <= g && g <= block_text)
                {
                    if (ch == alph[i])
                    {
                        letter++;
                    }
                }
                g++;
            }
            if (litter <= letter)
            {
                litter = letter;
                mass[j] = alph[i];

            }
            fin.close();
        }
        block = block_text;
        block_text += length;
        cout << mass[j];
    }
    char o;
    int ind_o;
    char ans;
    cout << "\nВведите самую частую букву русского алфавита : ";
    cin >> o;
    for (int i = 0; i < SIZE; i++)
    {
        if (o == alph[i])
        {
            ind_o = i;
        }
    }
    for (int i = 0; i < 17; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            if (mass[i] == alph[j])
            {
                ans = (j - ind_o) + 32;
                ans %= 32;
                cout << alph[ans];
            }
        }
    }

}
void DecipherVariant6()
{
    string B, C, D = "";
    string A = "абвгдежзийклмнопрстуфхцчшщъыьэюя"; //наш алфавит
    setlocale(LC_ALL, "RUS");
    ifstream fin;
    fin.open("D:\\Crypto2\\variant6.txt");
    while (fin) {
        getline(fin, B);
    }
    fin.close();
    cout << "Введите ключ : ";
    cin >> C;
    int* F = new int[B.size()];
    int* G = new int[B.size()];
    int c = C.size(); //делаем замену переменных для удобства
    int b = B.size();
    cout << "\nРазмер ключа : " << c << endl;
    //Первое условие. Если длина вводимого слова болше, либо равна длине ключа
    if (b >= c)
    {
        for (int i = 0; i < (b / c); i++)
        {
            D = D + C; //Записываем целое количество ключа. Растягиваем ключ по длине слова.
        }
        for (int j = 0; j < (b % c); j++)
        {
            D = D + C[j];
        }
    }
    else
    {
        for (int s = 0; s < b; s++)
        {
            D = D + B[s];
        } //Иначе если ключ длинее слова, ускорачиваем ключ до длины слова.
    }
    for (int k = 0; k < b; k++)
    {
        for (int n = 0; n < 32; n++)
        {
            if (B[k] == A[n])
            {
                F[k] = n;
            }
            if (D[k] == A[n])
            {
                G[k] = n;
            } //Здесь мы уже начинаем щифровать. Смысл заключается а том, что мы ишем номер буквы 
              //вводимом ключе и номере, а после чего записываем
            //их в массив
        }
    }
    int e = 0;
    for (int u = 0; u < b; u++)
    {
        e = ((F[u] - G[u]));
        if (e < 0)
        {
            e = e + 32;
        }
        else
        {
            e = e % 32;
        }
        B[u] = A[e];
    }
    ofstream fout;
    fout.open("D:\\Crypto2\\deciphervar6.txt");
    fout << B;
    fout.close();
}
int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    int variant;
    do {
        print_menu();

        variant = get_variant(9); // получаем номер выбранного пункта меню

        switch (variant) {
        case 1:
            EncryptVigenereСipher();
            break;
        case 2:
            DecipherVigenereСipher();
            break;
        case 3:
            IndexTextEncode();
            break;
        case 4:
            IndexText();
            break;
        case 5:
            IndexVariant();
            break;
        case 6:
            FindLengthKey();
            break;
        case 7:
            FindKey();
            break;
        case 8:
            DecipherVariant6();
            break;
        }

        if (variant != 9)
            system("pause"); // задерживаем выполнение, чтобы пользователь мог увидеть результат выполнения выбранного пункта
    } while (variant != 9);
}