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
    cout << "1. Перевод в нижний регистр" << endl;
    cout << "2. Убрать все символы и числа из файла" << endl;
    cout << "3. Убрать повторяющиеся пробелы" << endl;
    cout << "4. Убрать все пробелы" << endl;
    cout << "5. Подсчитать частоту букв в тексте с пробелами" << endl;
    cout << "6. Подсчитать частоту букв в тексте без пробелов" << endl;
    cout << "7. Подсчитать количество биграм в тексте с пробелами(с пересечения)" << endl;
    cout << "8. Подсчитать количество биграм в тексте без пробелами(с пересечения)" << endl;
    cout << "9. Подсчитать количество биграм в тексте c пробелами(без пересечения)" << endl;
    cout << "10. Подсчитать количество биграм в тексте без пробелами(без пересечения)" << endl;
    cout << "11. Exit" << endl;
    cout << ">";
}
int get_variant(int count) {
    int variant;
    string s; // строка для считывания введённых данных
    getline(cin, s); // считываем строку

    // пока ввод некорректен, сообщаем об этом и просим повторить его
    while (sscanf_s(s.c_str(), "%d", &variant) != 1 || variant < 1 || variant > count) {
        cout << "Некорректный ввод, попробуйте еще раз : "; // выводим сообщение об ошибке
        getline(cin, s); // считываем строку повторно
    }

    return variant;
}
void Register()
{
    const int SIZE = 34;
    ifstream fin;
    ofstream fout;
    string str;
    fin.open("D:\\Crypto1\\text.txt");
    fout.open("D:\\Crypto1\\register.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        if (!fout.is_open())
        {
            cout << "Ошибка открытия файла для записи!\n";
        }
        else
        {
            char ch;
            char reg;
            while (fin.get(ch))
            {
                reg = tolower(ch);
                fout << reg;
            }
            cout << "Текст переведено в нижний регистр!\n";
        }
    }
    fin.close();
    fout.close();
}
void DeleteSymbols()
{
    ifstream fin;
    ofstream fout;
    fin.open("D:\\Crypto1\\register.txt");
    fout.open("D:\\Crypto1\\space.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        cout << "Файл открыт!\n";
        if (!fout.is_open()) //перевірка на коректне відкритя файлу
        {
            cout << "Ошибка открытия файла для записи!\n";
        }
        else
        {
            const int SIZE = 34;
            const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к',
                                  'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                                  'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' ' };
            char ch;
            while (fin.get(ch))
            {
                for (int i = 0; i < SIZE; i++)
                {
                    if (ch == alph[i])
                    {
                        if (ch == 'ё')
                        {
                            fout << 'е';
                        }
                        else
                        {
                            fout << ch;
                        }
                    }
                }

            }
            cout << "Текст записан в файл!\n";
        }
    }
    fin.close();
    fout.close();
}
void Space()
{
    ifstream fin;
    ofstream fout;
    fin.open("D:\\Crypto1\\space.txt");
    fout.open("D:\\Crypto1\\space1.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        cout << "Файл открыт!\n";
        if (!fout.is_open())
        {
            cout << "Ошибка открытия файла для записи!\n";
        }
        else
        {
            char ch;
            char prb = ' ';
            int probel = 0;
            while (fin.get(ch))
            {
                if (ch == prb)
                {
                    probel++;
                }
                else
                {
                    probel = 0;
                }
                if (probel < 2)
                {
                    fout << ch;
                }
            }
            cout << "Все повторяющиеся пробелы удалены!\n";
        }
    }
    fin.close();
    fout.close();
}
void NotSpace()
{
    ifstream fin;
    ofstream fout;
    fin.open("D:\\Crypto1\\space1.txt");
    fout.open("D:\\Crypto1\\Notspace.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        cout << "Файл открыт!\n";
        if (!fout.is_open())
        {
            cout << "Ошибка открытия файла для записи!\n";
        }
        else
        {
            char ch;
            char prb = ' ';
            int probel = 0;
            while (fin.get(ch))
            {
                if (ch != prb)
                {
                    fout << ch;
                }
            }
            cout << "Все пробелы удалены!\n";
        }
    }
    fin.close();
    fout.close();
}
void FrequencyLettersSpace()
{
    double count = 0;
    char ch;
    char ch1;
    double letter;
    double freque;
    const int SIZE = 32;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ' };
    ifstream fin;
    fin.open("D:\\Crypto1\\space1.txt");
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
        fin.open("D:\\Crypto1\\space1.txt");
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
        }
        fin.close();
    }
}
void FrequencyLettersNotSpace()
{
    double count = 0;
    char ch;
    char ch1;
    double letter;
    double freque;
    const int SIZE = 31;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    fin.open("D:\\Crypto1\\Notspace.txt");
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
        fin.open("D:\\Crypto1\\Notspace.txt");
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
        }
        fin.close();
    }
}
void BigramSpace()
{
    setlocale(LC_ALL, "Russian");
    const char alfb[] = "абвгдежзийклмнопрстуфхцчшщыьэюя ";
    const int setlen = (sizeof(alfb) - 1);
    int count[setlen][setlen];
    double k = 0;
    int b = 0;
    char* p0 = NULL;
    int c1;
    FILE* plain;
    ofstream fout;
    fout.open("D:\\Crypto1\\bigramspace.txt");
    fopen_s(&plain, "D:\\Crypto1\\space1.txt", "r");
    memset(count, 0, sizeof(count));

    if (plain != NULL) {
        while ((c1 = getc(plain)) != EOF) {
            char* p1 = (char*)memchr(alfb, c1, setlen);
            if (p1 != NULL && p0 != NULL) {
                count[p0 - alfb][p1 - alfb]++;
                k++;
            }
            p0 = p1;
        }
        fclose(plain);
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    b++;
                }
            }
        }
        cout << "Количество биграм: " << b << endl;
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    fout << "[" << alfb[i] << "," << alfb[j] << "] :" << n << " -> " << n / k << endl;
                }
            }
        }
    }
}
void BigramNotSpace()
{
    setlocale(LC_ALL, "Russian");
    const char alfb[] = "абвгдежзийклмнопрстуфхцчшщыьэюя";
    const int setlen = (sizeof(alfb) - 1);
    int count[setlen][setlen];
    char* p0 = NULL;
    int c1;
    double k = 0;
    int b = 0;
    FILE* plain;
    ofstream fout;
    fout.open("D:\\Crypto1\\bigramnotspace.txt");
    fopen_s(&plain, "D:\\Crypto1\\Notspace.txt", "r");
    memset(count, 0, sizeof(count));

    if (plain != NULL) {
        while ((c1 = getc(plain)) != EOF) {
            char* p1 = (char*)memchr(alfb, c1, setlen);
            if (p1 != NULL && p0 != NULL) {
                count[p0 - alfb][p1 - alfb]++;
                k++;
            }
            p0 = p1;
        }
        fclose(plain);
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    b++;
                }
            }
        }
        cout << "Количество биграм: " << b << endl;
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    fout << "[" << alfb[i] << "," << alfb[j] << "] :" << n << " -> " << n / k << endl;
                }
            }
        }
    }
}
void BigramSpaceCross()
{
    setlocale(LC_ALL, "Russian");
    const char alfb[] = "абвгдежзийклмнопрстуфхцчшщыьэюя ";
    const int setlen = (sizeof(alfb) - 1);
    int count[setlen][setlen];
    double k = 0;
    int b = 0;
    char* p0 = NULL;
    int c1;
    FILE* plain;
    ofstream fout;
    fout.open("D:\\Crypto1\\bigramspacenotcross.txt");
    fopen_s(&plain, "D:\\Crypto1\\space1.txt", "r");
    memset(count, 0, sizeof(count));
    int sh = 0;
    if (plain != NULL) {
        while ((c1 = getc(plain)) != EOF) {
            char* p1 = (char*)memchr(alfb, c1, setlen);
            if (p1 != NULL && p0 != NULL) {
                if (sh == 0)
                {
                    count[p0 - alfb][p1 - alfb]++;
                    k++;
                    sh++;
                }
                else if (sh == 1)
                {
                    sh = 0;
                }
            }
            p0 = p1;
        }
        fclose(plain);
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    b++;
                }
            }
        }
        cout << "Количество биграм: " << b << endl;
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    fout << "[" << alfb[i] << "," << alfb[j] << "] :" << n << " -> " << n / k << endl;
                }
            }
        }
    }
}
void BigramNotSpaceCross()
{
    
    setlocale(LC_ALL, "Russian");
    const char alfb[] = "абвгдежзийклмнопрстуфхцчшщыьэюя";
    const int setlen = (sizeof(alfb) - 1);
    int count[setlen][setlen];
    double k = 0;
    int b = 0;
    char* p0 = NULL;
    int c1;
    FILE* plain;
    ofstream fout;
    fout.open("D:\\Crypto1\\bigramnotspacenotcros.txt");
    fopen_s(&plain, "D:\\Crypto1\\Notspace.txt", "r");
    memset(count, 0, sizeof(count));
    int sh = 0;
    if (plain != NULL) {
        while ((c1 = getc(plain)) != EOF) {
            char* p1 = (char*)memchr(alfb, c1, setlen);
            if (p1 != NULL && p0 != NULL) {
                if (sh == 0)
                {
                    count[p0 - alfb][p1 - alfb]++;
                    k++;
                    sh++;
                }
                else if (sh == 1)
                {
                    sh = 0;
                }
            }
            p0 = p1;
        }
        fclose(plain);
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    b++;
                }
            }
        }
        cout << "Количество биграм: " << b << endl;
        for (size_t i = 0; i < setlen; i++) {
            for (size_t j = 0; j < setlen; j++) {
                double n = count[i][j];
                if (n > 0) {
                    fout << "[" << alfb[i] << "," << alfb[j] << "] :" << n << " -> " << n / k << endl;
                }
            }
        }
    }
}
int main()
{
    setlocale(LC_ALL, "Russian");
    int variant;

    do {
        print_menu();

        variant = get_variant(11); // получаем номер выбранного пункта меню

        switch (variant) {
        case 1:
            Register();
            break;

        case 2:
            DeleteSymbols();
            break;

        case 3:
            Space();
            break;

        case 4:
            NotSpace();
            break;
        case 5:
            FrequencyLettersSpace();
            break;
        case 6:
            FrequencyLettersNotSpace();
            break;
        case 7:
            BigramSpace();
            break;
        case 8:
            BigramNotSpace();
            break;
        case 9:
            BigramSpaceCross();
            break;
        case 10:
            BigramNotSpaceCross();
        }

        if (variant != 11)
            system("pause"); // задерживаем выполнение, чтобы пользователь мог увидеть результат выполнения выбранного пункта
    } while (variant != 11);
}