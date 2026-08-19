// P3372 线段树 1
#include <bits/stdc++.h>
using namespace std;

class SegmentTree
{
private:
    int n;
    vector<long long> tree;
    vector<long long> lazy;

    void push_up(int node)
    {
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    void apply(int node, int left, int right, long long value)
    {
        tree[node] += 1LL * (right - left + 1) * value;
        lazy[node] += value;
    }

    void push_down(int node, int left, int right)
    {
        if (lazy[node] == 0 || left == right)
        {
            return;
        }

        int mid = (left + right) / 2;
        long long value = lazy[node];

        apply(node * 2, left, mid, value);
        apply(node * 2 + 1, mid + 1, right, value);

        lazy[node] = 0;
    }

    void build(
        int node,
        int left,
        int right,
        const vector<long long> &values)
    {
        if (left == right)
        {
            tree[node] = values[left];
            return;
        }

        int mid = (left + right) / 2;

        build(node * 2, left, mid, values);
        build(node * 2 + 1, mid + 1, right, values);

        push_up(node);
    }

    void update(
        int node,
        int left,
        int right,
        int ql,
        int qr,
        long long value)
    {
        if (ql <= left && right <= qr)
        {
            apply(node, left, right, value);
            return;
        }

        push_down(node, left, right);

        int mid = (left + right) / 2;

        if (ql <= mid)
        {
            update(node * 2, left, mid, ql, qr, value);
        }

        if (qr > mid)
        {
            update(node * 2 + 1, mid + 1, right, ql, qr, value);
        }

        push_up(node);
    }

    long long query(
        int node,
        int left,
        int right,
        int ql,
        int qr)
    {
        if (ql <= left && right <= qr)
        {
            return tree[node];
        }

        push_down(node, left, right);

        int mid = (left + right) / 2;
        long long result = 0;

        if (ql <= mid)
        {
            result += query(node * 2, left, mid, ql, qr);
        }

        if (qr > mid)
        {
            result += query(
                node * 2 + 1,
                mid + 1,
                right,
                ql,
                qr);
        }

        return result;
    }

public:
    explicit SegmentTree(const vector<long long> &values)
    {
        n = static_cast<int>(values.size()) - 1;
        tree.assign(n * 4 + 5, 0);
        lazy.assign(n * 4 + 5, 0);

        build(1, 1, n, values);
    }

    void range_add(int left, int right, long long value)
    {
        update(1, 1, n, left, right, value);
    }

    long long range_sum(int left, int right)
    {
        return query(1, 1, n, left, right);
    }
};

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<long long> values(n + 1);

    for (int i = 1; i <= n; i++)
    {
        cin >> values[i];
    }

    SegmentTree segment_tree(values);

    while (m--)
    {
        int operation;
        cin >> operation;

        if (operation == 1)
        {
            int left, right;
            long long value;

            cin >> left >> right >> value;
            segment_tree.range_add(left, right, value);
        }
        else
        {
            int left, right;
            cin >> left >> right;

            cout << segment_tree.range_sum(left, right) << '\n';
        }
    }

    return 0;
}