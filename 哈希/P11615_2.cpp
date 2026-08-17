#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

class FastScanner {
private:
    static const int BUF_SIZE = 1 << 21;
    vector<char> buf;
    int idx = 0, size = 0;

    char gc() {
        if (idx == size) {
            size = fread(buf.data(), 1, BUF_SIZE, stdin);
            idx = 0;
            if (size == 0) return EOF;
        }
        return buf[idx++];
    }

public:
    FastScanner() : buf(BUF_SIZE) {}

    ull read_ull() {
        ull x = 0;
        char ch = gc();
        while (ch < '0' || ch > '9') ch = gc();
        while (ch >= '0' && ch <= '9') {
            x = x * 10 + (ch - '0');
            ch = gc();
        }
        return x;
    }
};

class OpenAddressHashMap {
private:
    int table_size;
    vector<ull> keys;
    vector<ull> values;
    vector<unsigned char> used;

    int hash_func(ull key) const {
        return key % table_size;
    }

    int find_slot(ull key) const {
        int pos = hash_func(key);

        while (used[pos]) {
            if (keys[pos] == key) {
                return pos;
            }

            pos++;
            if (pos == table_size) pos = 0;
        }

        return pos;
    }

public:
    OpenAddressHashMap(int size) {
        table_size = size;
        keys.assign(table_size, 0);
        values.assign(table_size, 0);
        used.assign(table_size, 0);
    }

    ull get(ull key) const {
        int pos = find_slot(key);

        if (used[pos]) {
            return values[pos];
        }

        return 0;
    }

    void set(ull key, ull value) {
        int pos = find_slot(key);

        if (!used[pos]) {
            used[pos] = 1;
            keys[pos] = key;
        }

        values[pos] = value;
    }
};

int main() {
    FastScanner scanner;

    int n = (int)scanner.read_ull();
    OpenAddressHashMap mp(n * 4 + 1);

    ull ans = 0;

    for (ull i = 1; i <= (ull)n; i++) {
        ull x = scanner.read_ull();
        ull y = scanner.read_ull();

        ull old = mp.get(x);
        ans += i * old;
        mp.set(x, y);
    }

    cout << ans;

    return 0;
}
