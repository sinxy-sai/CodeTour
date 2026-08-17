#include <bits/stdc++.h>
using namespace std;

const long long BASE = 300;
const long long MOD1 = 100000007;
const long long MOD2 = 100000009;

pair<long long, long long> get_hash(const string &s)
{
    long long h1 = 0;
    long long h2 = 0;

    for (char ch : s)
    {
        int x = ch;
        h1 = (h1 * BASE + x) % MOD1;
        h2 = (h2 * BASE + x) % MOD2;
    }

    return {h1, h2};
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<pair<long long, long long>> hashes;

    for (int i = 0; i < N; i++)
    {
        string s;
        cin >> s;
        hashes.push_back(get_hash(s));
    }

    sort(hashes.begin(), hashes.end());

    int ans = 0;

    for (int i = 0; i < N; i++)
    {
        if (i == 0 || hashes[i] != hashes[i - 1])
        {
            ans++;
        }
    }

    cout << ans;

    return 0;
}