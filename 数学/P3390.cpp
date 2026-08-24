#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

const int64 MOD = 1000000007LL;

using Matrix = vector<vector<int64>>;

// 矩阵乘法：C = A * B
Matrix multiply(const Matrix &A, const Matrix &B, int n)
{
    Matrix C(n, vector<int64>(n, 0));

    for (int i = 0; i < n; ++i)
    {
        for (int k = 0; k < n; ++k)
        {
            int64 value = A[i][k];

            if (value == 0)
            {
                continue;
            }

            for (int j = 0; j < n; ++j)
            {
                C[i][j] = (C[i][j] + value * B[k][j]) % MOD;
            }
        }
    }

    return C;
}

// 矩阵快速幂：计算 A^exponent
Matrix matrixPower(Matrix base, long long exponent, int n)
{
    Matrix result(n, vector<int64>(n, 0));

    // 构造单位矩阵
    for (int i = 0; i < n; ++i)
    {
        result[i][i] = 1;
    }

    while (exponent > 0)
    {
        // 当前指数为奇数
        if (exponent & 1)
        {
            result = multiply(result, base, n);
        }

        // base 平方
        base = multiply(base, base, n);

        // 指数除以 2
        exponent >>= 1;
    }

    return result;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;

    cin >> n >> k;

    Matrix matrix(n, vector<int64>(n));

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            cin >> matrix[i][j];

            matrix[i][j] %= MOD;

            // 处理可能的负数
            if (matrix[i][j] < 0)
            {
                matrix[i][j] += MOD;
            }
        }
    }

    Matrix answer = matrixPower(matrix, k, n);

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            if (j > 0)
            {
                cout << ' ';
            }

            cout << answer[i][j];
        }

        cout << '\n';
    }

    return 0;
}