#include <iostream>
#include <stdlib.h>
using namespace std;

int main()
{
	//linear binary code [n, k]

	int n, k;
	cout << "Enter row size Of Matrix : ";
	cin >> k;
	cout << "Enter column size Of Matrix : ";
	cin >> n;

	int **matrixG = 0; // matrix G_{k*n}
	matrixG = new int*[k];
	for (int i = 0; i < k; ++i)
		matrixG[i] = new int[n];

	int **copymatrixG = 0; //copy of matrix G
	copymatrixG = new int*[k];
	for (int i = 0; i < k; ++i)
		copymatrixG[i] = new int[n];

	int **parity = 0; // matrix H_{n-k*n}
	parity = new int*[n - k];
	for (int i = 0; i < n - k; ++i)
		parity[i] = new int[n];

	int p = 0;
	int **swap = 0; // matrix swap_{2*n}
	swap = new int*[2];
	for (int i = 0; i < 2; ++i)
		swap[i] = new int[n];


	//‌دریافت ماتریس G
	cout << "\nEnter matrix G row by row:\n";
	for (int i = 0; i < k; i++)
	{
		for (int j = 0; j < n; j++)
		{
			cin >> matrixG[i][j];
		}
	}

	//چاپ ماتریس G
	//cout << "\nmatrix G:\n";

	for (int i = 0; i < k; i++)
	{
	for (int j = 0; j < n; j++)
	{
	copymatrixG[i][j] = matrixG[i][j];
	//cout << matrixG[i][j] << " ";
	}
	//cout << "\n";
	}

	//صفر کردن ماتریس H
	for (int i = 0; i < n - k; i++)
	{
		for (int j = 0; j < n; j++)
		{
			parity[i][j] = 0;
		}
	}



	// G استاندارد سازی ماتریس 
	// با استفاده از عملیات سطری مقدماتی
	int lead = 0;
	int rowCount = k;
	int columnCount = n;

	for (int r = 0; r < rowCount; r++)
	{
		int i;
		if (columnCount <= lead)
			break;
		else
		{
			i = r;
			while (matrixG[i][lead] == 0)//پیدا کدن اولین عنصر نا صفر ستون 
			{
				i = i + 1;
				if (rowCount == i)
				{
					i = r;
					lead = lead + 1;
					if (columnCount == lead)
						break;
				}
			}

		}
		for (int j = 0; j < columnCount; j++) // انتقال سطر شامل اولین عنصر ناصفر ستون به سطر مورد نظر 
		{
			int temp = matrixG[r][j];
			matrixG[r][j] = matrixG[i][j];
			matrixG[i][j] = temp;
		}
		int div = matrixG[r][lead]; // عملیات های یک کردن اولین عنصر
		if (div != 0)
			for (int j = 0; j < columnCount; j++)
				matrixG[r][j] /= div;
		for (int j = 0; j < rowCount; j++)
		{
			if (j != r)
			{
				int sub = matrixG[j][lead];
				for (int k = 0; k < columnCount; k++)
					matrixG[j][k] -= (sub * matrixG[r][k]);
			}
		}
		lead++;
	}



	//  G‌ چاپ ماتریس کاهش یافته سطری 
	//cout << "\nReduced row echelon form of matrix G:" << "\n";

	for (int i = 0; i < rowCount; ++i)
	{
		for (int j = 0; j < columnCount; ++j)
		{
			if (matrixG[i][j] % 2 == 0)
				matrixG[i][j] = 0;
			else
				matrixG[i][j] = 1;
			//cout << matrixG[i][j] << '\t';

		}
		cout << "\n";
	}

	// جابه جایی ستون ها در ماتریس G
	for (int i = 0; i < rowCount; ++i)
	{
		for (int j = 0; j < columnCount; ++j)
		{
			if (matrixG[i][j] == 1 & i == j)
				break;
			if (matrixG[i][j] == 1 & i != j)
			{
				swap[0][p] = i;
				swap[1][p] = j;
				p = p + 1;
				for (int s = 0; s < rowCount; s++)
				{
					int temp = matrixG[s][j];
					matrixG[s][j] = matrixG[s][i];
					matrixG[s][i] = temp;
				}
				break;
			}
		}
	}


	//  G‌ چاپ ماتریس استانداردشده 
	cout << "\nstandard matrix G:" << "\n";

	for (int i = 0; i < rowCount; ++i)
	{
		for (int j = 0; j < columnCount; ++j)
		{
			if (matrixG[i][j] % 2 == 0)
				matrixG[i][j] = 0;
			else
				matrixG[i][j] = 1;
			cout << matrixG[i][j] << '\t';

		}
		cout << "\n";
	}


	//  H ساخت ماتریس 
	for (int i = 0; i < k; ++i)
	{
		for (int j = 0; j < n - k; ++j)
			parity[j][i] = matrixG[i][j + k];
	}

	for (int i = 0; i < n - k; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			if (j - k == i)
				parity[i][j] = 1;
		}
	}


	//جابه جایی ستونها در ماتریس H
	for (int i = p-1; i >=0 ; i--)
	{
		int x = swap[0][i];
		int y = swap[1][i];
		for (int s = 0; s < rowCount; s++)
		{
			int temp = parity[s][x];
			parity[s][x] = parity[s][y];
			parity[s][y] = temp;
		}

	}


	//  H چاپ ماتریس 
	cout << "\nmatrix parity check H:" << "\n";

	for (int i = 0; i < n - k; ++i)
	{
		for (int j = 0; j < n; ++j)
			cout << parity[i][j] << '\t';
		cout << "\n";
	}


	//تست درستی ماتریس H
	cout << "\ntest parity check H, GH^T=0?" << "\n";
	for (int i = 0; i < k; i++)
	{
		for (int j = 0; j < n - k; j++)
		{
			int temp = 0;
			for (int r = 0; r < n; r++)
			{
				temp += copymatrixG[i][r] * parity[j][r];
			}
			if (temp % 2 == 0)
				temp = 0;
			if (temp % 2 != 0)
				temp = 1;
			cout << temp << '\t';

		}
		cout << "\n";
	}

	getchar();
	getchar();

	return 0;
}
