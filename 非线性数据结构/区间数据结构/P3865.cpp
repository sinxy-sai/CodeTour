#include <bits/stdc++.h>
using namespace std;

class SparseTable
{
private:
    int n;
    vector<int> logarithm;
    vector<vector<int>> table;

public:
    SparseTable(const vector<int> &values)
    {
        n = static_cast<int>(values.size()) - 1;

        logarithm.resize(n + 1, 0);

        for (int i = 2; i <= n; i++)
        {
            logarithm[i] = logarithm[i / 2] + 1;
        }

        int levels = logarithm[n] + 1;
        table.assign(levels, vector<int>(n + 1, 0));

        // 第 0 层：长度为 1 的区间
        table[0] = values;

        // 建表
        for (int k = 1; k < levels; k++)
        {
            int half = 1 << (k - 1);
            int length = 1 << k;

            for (int i = 1; i + length - 1 <= n; i++)
            {
                table[k][i] = max(
                    table[k - 1][i],
                    table[k - 1][i + half]);
            }
        }
    }

    int query_max(int left, int right) const
    {
        int length = right - left + 1;
        int k = logarithm[length];
        int block_length = 1 << k;

        return max(
            table[k][left],
            table[k][right - block_length + 1]);
    }
};

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<int> values(n + 1);

    for (int i = 1; i <= n; i++)
    {
        cin >> values[i];
    }

    SparseTable st(values);

    for (int i = 0; i < m; i++)
    {
        int left, right;
        cin >> left >> right;

        cout << st.query_max(left, right) << '\n';
    }

    return 0;
}