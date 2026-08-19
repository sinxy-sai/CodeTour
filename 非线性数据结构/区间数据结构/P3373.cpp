#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

class SegmentTree
{
private:
    int n;
    int64 mod;
    vector<int64> tree;
    vector<int64> lazyMul;
    vector<int64> lazyAdd;

    void pushUp(int node)
    {
        tree[node] = (tree[node * 2] + tree[node * 2 + 1]) % mod;
    }

    void apply(int node, int left, int right,
               int64 mul, int64 add)
    {
        int64 length = right - left + 1;

        tree[node] =
            (tree[node] * mul + length * add) % mod;

        lazyMul[node] =
            lazyMul[node] * mul % mod;

        lazyAdd[node] =
            (lazyAdd[node] * mul + add) % mod;
    }

    void pushDown(int node, int left, int right)
    {
        if (lazyMul[node] == 1 && lazyAdd[node] == 0)
        {
            return;
        }

        int mid = (left + right) / 2;

        int64 mul = lazyMul[node];
        int64 add = lazyAdd[node];

        apply(node * 2, left, mid, mul, add);
        apply(node * 2 + 1, mid + 1, right, mul, add);

        lazyMul[node] = 1;
        lazyAdd[node] = 0;
    }

    void build(int node, int left, int right,
               const vector<int64> &values)
    {
        if (left == right)
        {
            tree[node] = values[left] % mod;
            return;
        }

        int mid = (left + right) / 2;

        build(node * 2, left, mid, values);
        build(node * 2 + 1, mid + 1, right, values);

        pushUp(node);
    }

    void update(int node, int left, int right,
                int ql, int qr,
                int64 mul, int64 add)
    {
        if (ql <= left && right <= qr)
        {
            apply(node, left, right, mul, add);
            return;
        }

        pushDown(node, left, right);

        int mid = (left + right) / 2;

        if (ql <= mid)
        {
            update(node * 2, left, mid,
                   ql, qr, mul, add);
        }

        if (qr > mid)
        {
            update(node * 2 + 1, mid + 1, right,
                   ql, qr, mul, add);
        }

        pushUp(node);
    }

    int64 query(int node, int left, int right,
                int ql, int qr)
    {
        if (ql <= left && right <= qr)
        {
            return tree[node];
        }

        pushDown(node, left, right);

        int mid = (left + right) / 2;
        int64 result = 0;

        if (ql <= mid)
        {
            result += query(node * 2, left, mid, ql, qr);
        }

        if (qr > mid)
        {
            result += query(node * 2 + 1,
                            mid + 1, right,
                            ql, qr);
        }

        return result % mod;
    }

public:
    SegmentTree(const vector<int64> &values, int64 modulus)
        : n(static_cast<int>(values.size()) - 1),
          mod(modulus),
          tree(n * 4 + 5, 0),
          lazyMul(n * 4 + 5, 1),
          lazyAdd(n * 4 + 5, 0)
    {
        build(1, 1, n, values);
    }

    void rangeMultiply(int left, int right, int64 value)
    {
        update(1, 1, n,
               left, right,
               value % mod, 0);
    }

    void rangeAdd(int left, int right, int64 value)
    {
        update(1, 1, n,
               left, right,
               1, value % mod);
    }

    int64 rangeSum(int left, int right)
    {
        return query(1, 1, n, left, right);
    }
};

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    int64 mod;

    cin >> n >> q >> mod;

    vector<int64> values(n + 1);

    for (int i = 1; i <= n; i++)
    {
        cin >> values[i];
    }

    SegmentTree segmentTree(values, mod);

    while (q--)
    {
        int op;
        cin >> op;

        if (op == 1)
        {
            int left, right;
            int64 k;

            cin >> left >> right >> k;

            segmentTree.rangeMultiply(left, right, k);
        }
        else if (op == 2)
        {
            int left, right;
            int64 k;

            cin >> left >> right >> k;

            segmentTree.rangeAdd(left, right, k);
        }
        else
        {
            int left, right;
            cin >> left >> right;

            cout << segmentTree.rangeSum(left, right)
                 << '\n';
        }
    }

    return 0;
}