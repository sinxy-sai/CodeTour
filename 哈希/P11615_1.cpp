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

class ChainHashMap {
private:
    int bucket_count;
    vector<int> head;
    vector<ull> keys;
    vector<ull> values;
    vector<int> next;

    int hash_func(ull key) const {
        return key % bucket_count;
    }

public:
    ChainHashMap(int size, int max_items) {
        bucket_count = size;
        head.assign(bucket_count, -1);
        keys.reserve(max_items);
        values.reserve(max_items);
        next.reserve(max_items);
    }

    ull get(ull key) const {
        int pos = hash_func(key);

        for (int i = head[pos]; i != -1; i = next[i]) {
            if (keys[i] == key) {
                return values[i];
            }
        }

        return 0;
    }

    void set(ull key, ull value) {
        int pos = hash_func(key);

        for (int i = head[pos]; i != -1; i = next[i]) {
            if (keys[i] == key) {
                values[i] = value;
                return;
            }
        }

        keys.push_back(key);
        values.push_back(value);
        next.push_back(head[pos]);
        head[pos] = (int)keys.size() - 1;
    }
};

int main() {
    FastScanner scanner;

    int n = (int)scanner.read_ull();
    ChainHashMap mp(n * 2 + 1, n);

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
