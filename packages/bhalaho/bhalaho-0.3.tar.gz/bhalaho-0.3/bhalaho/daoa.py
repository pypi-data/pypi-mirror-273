
prims='''
#include <stdio.h>
#include <conio.h>
#include <limits.h>

#define NODES 9
#define INF INT_MAX

int mst[NODES];
int adj[NODES][NODES] = {

	{0, 4, 0, 0, 0, 0, 0, 8, 0},
	{4, 0, 8, 0, 0, 0, 0, 11, 0},
	{0, 8, 0, 7, 0, 4, 0, 0, 2},
	{0, 0, 7, 0, 9, 14, 0, 0, 0},
	{0, 0, 0, 9, 0, 10, 0, 0, 0},
	{0, 0, 4, 14, 10, 0, 2, 0, 0},
	{0, 0, 0, 0, 0, 2, 0, 1, 6},
	{8, 11, 0, 0, 0, 0, 1, 0, 7},
	{0, 0, 2, 0, 0, 0, 6, 7, 0}
};

struct Vertices {
	int dist;
	int parent;
	int visited;
} V[NODES];

struct Graph {
	char nodes[NODES];
	int adjMatrix[NODES][NODES];
} G;

int extractMin() {
	int min = INF;
	int minIndex = -1;
	for (int i = 0; i < NODES; i++) {
		if (!V[i].visited && V[i].dist < min) {
			min = V[i].dist;
			minIndex = i;
		}
	}
	return minIndex;
}


void Prims(int start) {
	for (int i = 0; i < NODES; i++) {
		V[i].dist = INF;
		V[i].parent = -1;
		V[i].visited = 0;
	}
	V[start].dist = 0;
	for (int i = 0; i < NODES; i++) {
		int u = extractMin();
		V[u].visited = 1;
		for (int v = 0; v < NODES; v++) {
			if (G.adjMatrix[u][v] && !V[v].visited && V[v].dist > G.adjMatrix[u][v]) {
				V[v].parent = u;
				V[v].dist = G.adjMatrix[u][v];
			}
		}
	}
	for (int i = 0; i < NODES; i++) {
		mst[i] = V[i].parent;
	}
}

int main() {
	int totalCost = 0;
	for (int i = 0; i < NODES; i++) {
		for (int j = 0; j < NODES; j++) {
			G.adjMatrix[i][j] = adj[i][j];
		}
	}
	for (int i = 0; i < NODES; i++) {
		G.nodes[i] = 'a' + i;
	}
	Prims(0);
	printf("Minimum Spanning Tree: \\n");
	for (int i = 0; i < NODES; i++) {
		if (mst[i] != -1) {
			printf("%c - %c: %d\\n", G.nodes[mst[i]], G.nodes[i], G.adjMatrix[i][mst[i]]);
			totalCost += G.adjMatrix[i][mst[i]];
		}
	}
	printf("Total Cost: %d\\n", totalCost);
	return 0;
}
'''

kruskal='''#include <stdio.h>
#include <stdlib.h>

// Structure to represent an edge in the graph
struct Edge {
    int src, dest, weight;
};

// Structure to represent a subset for union-find
struct Subset {
    int parent;
    int rank;
};

// Function prototypes
int find(struct Subset subsets[], int i);
void Union(struct Subset subsets[], int x, int y);
int compareEdges(const void* a, const void* b);
void KruskalMST(struct Edge edges[], int V, int E);

// Find set of an element i
int find(struct Subset subsets[], int i) {
    if (subsets[i].parent != i)
        subsets[i].parent = find(subsets, subsets[i].parent);
    return subsets[i].parent;
}

// Perform Union of two sets
void Union(struct Subset subsets[], int x, int y) {
    int xroot = find(subsets, x);
    int yroot = find(subsets, y);

    if (subsets[xroot].rank < subsets[yroot].rank)
        subsets[xroot].parent = yroot;
    else if (subsets[xroot].rank > subsets[yroot].rank)
        subsets[yroot].parent = xroot;
    else {
        subsets[yroot].parent = xroot;
        subsets[xroot].rank++;
    }
}

// Comparator function for sorting edges by weight
int compareEdges(const void* a, const void* b) {
    struct Edge* edge1 = (struct Edge*)a;
    struct Edge* edge2 = (struct Edge*)b;
    return edge1->weight - edge2->weight;
}

// Function to construct MST using Kruskal's algorithm
void KruskalMST(struct Edge edges[], int V, int E) {
    struct Edge result[V];
    int e = 0; // Index variable for result[] array
    int i = 0; // Index variable for sorted edges[] array

    // Step 1: Sort all edges in non-decreasing order of their weight
    qsort(edges, E, sizeof(edges[0]), compareEdges);

    // Allocate memory for creating V subsets
    struct Subset* subsets = (struct Subset*)malloc(V * sizeof(struct Subset));

    // Create V subsets with single elements
    for (int v = 0; v < V; v++) {
        subsets[v].parent = v;
        subsets[v].rank = 0;
    }

    // Number of edges to be taken is V-1
    while (e < V - 1 && i < E) {
        // Step 2: Pick the smallest edge. Increment index for next iteration
        struct Edge next_edge = edges[i++];

        int x = find(subsets, next_edge.src);
        int y = find(subsets, next_edge.dest);

        // If including this edge doesn't cause cycle, include it in the result and increment the index
        if (x != y) {
            result[e++] = next_edge;
            Union(subsets, x, y);
        }
    }

    // Print the result
    printf("Edges in the MST:\n");
    for (i = 0; i < e; ++i)
        printf("%d - %d: %d\n", result[i].src, result[i].dest, result[i].weight);

    // Free dynamically allocated memory
    free(subsets);
}

// Driver code
int main() {
    int V = 4; // Number of vertices
    int E = 5; // Number of edges

    // Example graph represented by its edges
    struct Edge edges[] = { {0, 1, 10}, {0, 2, 6}, {0, 3, 5}, {1, 3, 15}, {2, 3, 4} };

    // Function call to find MST
    KruskalMST(edges, V, E);

    return 0

'''

dijkstra = '''

#include <limits.h>
#include <stdbool.h>
#include <stdio.h>

// Number of vertices in the graph
#define V 9

// A utility function to find the vertex with minimum
// distance value, from the set of vertices not yet included
// in shortest path tree
int minDistance(int dist[], bool sptSet[])
{
    // Initialize min value
    int min = INT_MAX, min_index;

    for (int v = 0; v < V; v++)
        if (sptSet[v] == false && dist[v] <= min)
            min = dist[v], min_index = v;

    return min_index;
}

// A utility function to print the constructed distance
// array
void printSolution(int dist[])
{
    printf("Vertex \t\t Distance from Source\n");
    for (int i = 0; i < V; i++)
        printf("%d \t\t\t\t %d\n", i, dist[i]);
}

// Function that implements Dijkstra's single source
// shortest path algorithm for a graph represented using
// adjacency matrix representation
void dijkstra(int graph[V][V], int src)
{
    int dist[V]; // The output array.  dist[i] will hold the
                 // shortest
    // distance from src to i

    bool sptSet[V]; // sptSet[i] will be true if vertex i is
                    // included in shortest
    // path tree or shortest distance from src to i is
    // finalized

    // Initialize all distances as INFINITE and stpSet[] as
    // false
    for (int i = 0; i < V; i++)
        dist[i] = INT_MAX, sptSet[i] = false;

    // Distance of source vertex from itself is always 0
    dist[src] = 0;

    // Find shortest path for all vertices
    for (int count = 0; count < V - 1; count++) {
        // Pick the minimum distance vertex from the set of
        // vertices not yet processed. u is always equal to
        // src in the first iteration.
        int u = minDistance(dist, sptSet);

        // Mark the picked vertex as processed
        sptSet[u] = true;

        // Update dist value of the adjacent vertices of the
        // picked vertex.
        for (int v = 0; v < V; v++)

            // Update dist[v] only if is not in sptSet,
            // there is an edge from u to v, and total
            // weight of path from src to  v through u is
            // smaller than current value of dist[v]
            if (!sptSet[v] && graph[u][v]
                && dist[u] != INT_MAX
                && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }

    // print the constructed distance array
    printSolution(dist);
}

// driver's code
int main()
{
    /* Let us create the example graph discussed above */
    int graph[V][V] = { { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
                        { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
                        { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
                        { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
                        { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
                        { 0, 0, 4, 14, 10, 0, 2, 0, 0 },
                        { 0, 0, 0, 0, 0, 2, 0, 1, 6 },
                        { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
                        { 0, 0, 2, 0, 0, 0, 6, 7, 0 } };  // Function call
    dijkstra(graph, 0);
    return 0;
}

'''



matrix_chain_multiplication = '''
#include <stdio.h>
#include <limits.h>

// Function to find minimum number of multiplications needed to multiply matrices
int matrixChainOrder(int p[], int n) {
    // Create a 2D table to store the minimum number of multiplications
    int m[n][n];
    
    // Initialize m[i][j] as 0 where i == j (no multiplication needed for single matrix)
    for (int i = 1; i < n; i++)
        m[i][i] = 0;
    
    // 'l' is the chain length
    for (int l = 2; l < n; l++) {
        for (int i = 1; i < n - l + 1; i++) {
            int j = i + l - 1;
            m[i][j] = INT_MAX;
            for (int k = i; k <= j - 1; k++) {
                // Compute the number of multiplications needed for each combination of splits
                int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j])
                    m[i][j] = q;
            }
        }
    }
    
    // Return the minimum number of multiplications needed to multiply the matrices
    return m[1][n - 1];
}

// Driver code
int main() {
    int arr[] = {5, 4, 6, 2, 7}; // Array representing dimensions of matrices
    int size = sizeof(arr) / sizeof(arr[0]); // Number of matrices
    
    // Function call to find minimum number of multiplications
    printf("Minimum number of multiplications needed: %d", matrixChainOrder(arr, size));

    return 0;
}

'''

longest_common_subsequence='''
#include <stdio.h>
#include <string.h>

// Function to find the length of the longest common subsequence
int lcs(char* X, char* Y, int m, int n) {
    int dp[m + 1][n + 1];

    // Building the dp table in bottom-up manner
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0)
                dp[i][j] = 0;
            else if (X[i - 1] == Y[j - 1])
                dp[i][j] = dp[i - 1][j - 1] + 1;
            else
                dp[i][j] = (dp[i - 1][j] > dp[i][j - 1]) ? dp[i - 1][j] : dp[i][j - 1];
        }
    }

    return dp[m][n];
}

// Driver code
int main() {
    char X[] = "AGGTAB";
    char Y[] = "GXTXAYB";
    int m = strlen(X);
    int n = strlen(Y);

    printf("Length of LCS is %d\n", lcs(X, Y, m, n));

    return 0;
}
'''

knapsack = '''
#include<stdio.h>

int max(int a, int b) {
    return (a > b) ? a : b;
}

int knapsack(int W, int wt[], int val[], int n) {
    int i, w;
    int K[n + 1][W + 1];
    for (i = 0; i <= n; i++) {
        for (w = 0; w <= W; w++) {
            if (i == 0 || w == 0)
                K[i][w] = 0;
            else if (wt[i - 1] <= w)
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
            else
                K[i][w] = K[i - 1][w];
        }
    }
    return K[n][W];
}

int main() {
    int val[] = {60, 100, 120};
    int wt[] = {10, 20, 30};
    int W = 50;
    int n = sizeof(val) / sizeof(val[0]);
    printf("Maximum value: %d\\n", knapsack(W, wt, val, n));
    return 0;
}

'''

fractional_knapsack = '''
#include <stdio.h>
#include <stdlib.h>

struct Item {
    int value;
    int weight;
};

int compare(const void *a, const void *b) {
    double ratio1 = (double)((struct Item *)a)->value / ((struct Item *)a)->weight;
    double ratio2 = (double)((struct Item *)b)->value / ((struct Item *)b)->weight;
    return ratio2 > ratio1 ? 1 : -1;
}

double fractionalKnapsack(int capacity, struct Item items[], int n) {
    qsort(items, n, sizeof(struct Item), compare);
    double totalValue = 0.0; 
    int currentWeight = 0;  
    for (int i = 0; i < n; i++) {
        if (currentWeight + items[i].weight <= capacity) {
            totalValue += items[i].value;
            currentWeight += items[i].weight;
        } else {
            int remainingWeight = capacity - currentWeight;
            totalValue += (double)items[i].value / items[i].weight * remainingWeight;
            break; 
        }
    }
    return totalValue;
}

int main() {
    int capacity = 50;
    struct Item items[] = {{60, 10}, {100, 20}, {120, 30}};
    int n = sizeof(items) / sizeof(items[0]);

    double maxValue = fractionalKnapsack(capacity, items, n);
    printf("Maximum value in knapsack = %.2f\\n", maxValue);

    return 0;
}

'''

n_queens = '''
#include<stdio.h>
#include<stdbool.h>
#include<math.h>

#define N 20

int board[N][N];
int count = 0;

void printSolution(int n);
bool isSafe(int row, int col, int n);
bool solveNQueensUtil(int col, int n);
bool solveNQueens(int n);

int main() {
    int n;
    printf("Enter number of Queens : ");
    scanf("%d", &n);
    if (solveNQueens(n))
        printf("\\nTotal solutions: %d\\n", count);
    else
        printf("\\nNo solution exists for %d queens.\\n", n);
    return 0;
}

void printSolution(int n) {
    int i, j;
    printf("\\n\\nSolution : %d\\n\\n", ++count);
    for (i = 0; i < n; ++i) {
        for (j = 0; j < n; ++j) {
            if (board[i][j] == 1)
                printf("Q ");
            else
                printf(". ");
        }
        printf("\\n");
    }
}

bool isSafe(int row, int col, int n) {
    int i, j;
    for (i = 0; i < col; i++) {
        if (board[row][i])
            return false;
    }
    for (i = row, j = col; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j])
            return false;
    }
    for (i = row, j = col; j >= 0 && i < n; i++, j--) {
        if (board[i][j])
            return false;
    }
    return true;
}

bool solveNQueensUtil(int col, int n) {
    if (col == n) {
        printSolution(n);
        return true;
    }
    bool res = false;
    for (int i = 0; i < n; i++) {
        if (isSafe(i, col, n)) {
            board[i][col] = 1;
            res = solveNQueensUtil(col + 1, n) || res;
            board[i][col] = 0;
        }
    }
    return res;
}

bool solveNQueens(int n) {
    if (n <= 0 || n > N) {
        printf("Invalid input.\\n");
        return false;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            board[i][j] = 0;
        }
    }
    return solveNQueensUtil(0, n);
}
'''

sum_of_subset = '''
#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 100

// Function to print subset elements
void printSubset(int subset[], int size) {
    printf("{ ");
    for (int i = 0; i < size; i++) {
        printf("%d ", subset[i]);
    }
    printf("}\n");
}

// Function to find subsets with given sum using backtracking
void findSubsetsWithSum(int arr[], int size, int sum, int currentSum, int start, int subset[], int subsetSize) {
    // If current sum equals the target sum, print the subset
    if (currentSum == sum) {
        printSubset(subset, subsetSize);
        return;
    }

    // If the current sum exceeds the target sum or all elements are processed, return
    if (currentSum > sum || start == size) {
        return;
    }

    // Include the current element in the subset
    subset[subsetSize] = arr[start];
    findSubsetsWithSum(arr, size, sum, currentSum + arr[start], start + 1, subset, subsetSize + 1);

    // Exclude the current element from the subset
    findSubsetsWithSum(arr, size, sum, currentSum, start + 1, subset, subsetSize);
}

// Function to find subsets with given sum and initialize backtracking
void findSubsets(int arr[], int size, int sum) {
    int subset[MAX_SIZE]; // Array to store the subset elements
    findSubsetsWithSum(arr, size, sum, 0, 0, subset, 0);
}

// Main function
int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    int sum = 10;

    printf("Subsets with sum %d:\n", sum);
    findSubsets(arr, size, sum);

    return 0;
}
'''


kmp = '''
#include <stdio.h>
#include <string.h>

void prefixSuffixArray(char *pat, int M, int *pps) {
    int length = 0;
    pps[0] = 0;
    int i = 1;
    while (i < M) {
        if (pat[i] == pat[length]) {
            length++;
            pps[i] = length;
            i++;
        }
        else {
            if (length != 0)
                length = pps[length - 1];
            else {
                pps[i] = 0;
                i++;
            }
        }
    }
}

void KMPAlgorithm(char *text, char *pattern) {
    int M = strlen(pattern);
    int N = strlen(text);
    int pps[M];
    prefixSuffixArray(pattern, M, pps);
    int i = 0;
    int j = 0;
    int flag = 0;
    while (i < N) {
        if (pattern[j] == text[i]) {
            j++;
            i++;
        }
        if (j == M) {
            flag = 1;
            printf("Found pattern at index %d\\n", i - j);
            j = pps[j - 1];
        }
        else if (i < N && pattern[j] != text[i]) {
            if (j != 0)
                j = pps[j - 1];
            else
                i = i + 1;
        }
    }
    if (flag == 0){
        printf("Pattern not found\\n");
    }
}

int main() {
    char text[100], pattern[100];
    
    printf("Enter the text: ");
    scanf("%s", text);

    printf("Enter the pattern: ");
    scanf("%s", pattern);

    KMPAlgorithm(text, pattern);
    return 0;
}
'''


coin_change_greedy= '''
#include <stdio.h>
#define COINS 9
#define MAX 20
 
// All denominations of Indian Currency
int coins[COINS] = { 1, 2, 5, 10, 20,
                     50, 100, 200, 2000 };
 
void findMin(int cost)
{
    int coinList[MAX] = { 0 };
    int i, k = 0;
 
    for (i = COINS - 1; i >= 0; i--) {
        while (cost >= coins[i]) {
            cost -= coins[i];
            // Add coin in the list
            coinList[k++] = coins[i];
        }
    }
 
    for (i = 0; i < k; i++) {
        // Print
        printf("%d ", coinList[i]);
    }
    return;
}
 
int main(void)
{
    // input value
    int n = 93;
 
    printf("Following is minimal number"
           "of change for %d: ",
           n);
    findMin(n);
    return 0;
}

'''

TSP_dp = '''
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define V 4 // Number of vertices in the graph

// Function to find minimum of two numbers
int min(int x, int y) {
    return (x < y) ? x : y;
}

// Function to find the minimum weight Hamiltonian Cycle
int tsp(int graph[][V], int mask, int pos, int dp[][V]) {
    // If all vertices have been visited
    if (mask == (1 << V) - 1)
        return graph[pos][0];

    // If sub-problem has been solved before, return the result from dp array
    if (dp[mask][pos] != -1)
        return dp[mask][pos];

    int ans = INT_MAX;

    // Try all possible next vertices
    for (int city = 0; city < V; city++) {
        // If city is not visited and not same as current city
        if ((mask & (1 << city)) == 0 && graph[pos][city]) {
            int newAns = graph[pos][city] + tsp(graph, mask | (1 << city), city, dp);
            ans = min(ans, newAns);
        }
    }

    // Save the result in dp array and return the result
    return dp[mask][pos] = ans;
}

// Driver code
int main() {
    // Example graph represented by its adjacency matrix
    int graph[][V] = {{0, 10, 15, 20},
                      {10, 0, 35, 25},
                      {15, 35, 0, 30},
                      {20, 25, 30, 0}};

    // Initialize dp array with -1
    int dp[1 << V][V];
    for (int i = 0; i < (1 << V); i++) {
        for (int j = 0; j < V; j++) {
            dp[i][j] = -1;
        }
    }

    // Starting from vertex 0
    int start = 0;

    // Function call to find minimum weight Hamiltonian Cycle
    printf("Minimum cost of the Hamiltonian Cycle: %d\n", tsp(graph, 1 << start, start, dp));

    return 0;
}

'''
a15_puzzle = '''
#include<stdio.h>
#include<stdlib.h>

#define N 4

int getInvCount(int *arr){
    int inv_count = 0;
    for (int i = 0; i < N*N - 1; i++)
    {
        for (int j = i+1; j < N*N; j++)
        {
            if (arr[j] && arr[i] && arr[i] > arr[j])
            {
                inv_count++;
            }
            
        }
        
    }
    return inv_count;
}

int findPosition( int puzzle[N][N]){
    for (int i = N -1; i>= 0; i--)
    {
        for (int j = N - 1; j >= 0; j --)
        {
            if (puzzle[i][j] == 0)
            {
                return N - i;
            }
        }
    }
}
int isSolvable(int puzzle[N][N]){
    int invcount =  getInvCount((int *)puzzle);
    if (N  & 1)
        return !(invcount & 1);
    else
    {
        int pos = findPosition(puzzle);
        if (pos & 1)
        {
            return !(invcount & 1);
        }
        else
        {
            return invcount & 1;
        }
    }
}
int getManhattanDistance(int value,int row,int col){
    if (value == 0)
    {
        return 0;
    }
    int goalRow = (value -1) / N;
    int goalCol = (value - 1) % N;
    return abs(row - goalRow) + abs(col - goalCol);
}

int calculateTotalCost(int puzzle[N][N]){
    int totalCost = 0;
    totalCost += getInvCount((int *) puzzle);
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            totalCost += getManhattanDistance(puzzle[i][j],i,j);
        }
    }
    return totalCost;
}

int main()
{
    int puzzle[N][N] = {
        {1, 2, 3, 4},
        {5, 6, 0, 8},
        {9, 10, 7, 11},
        {13, 14, 15, 12},
    };

    if (!isSolvable(puzzle))
    {
        printf("Not Solvable\n");
        return 0;
    }

    int totalCost = calculateTotalCost(puzzle);
    printf("Total Cost: %d\n", totalCost);
    return 0;
}
'''

strassens_detail = '''
#include <stdio.h>
#include <stdlib.h>

// Function to add two matrices
void add(int n, int A[][n], int B[][n], int C[][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
}

// Function to subtract two matrices
void subtract(int n, int A[][n], int B[][n], int C[][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }
}

// Function to multiply two matrices using Strassen's algorithm
void strassen(int n, int A[][n], int B[][n], int C[][n]) {
    if (n == 1) {
        C[0][0] = A[0][0] * B[0][0];
        return;
    }

    int newSize = n / 2;

    // Creating sub-matrices
    int A11[newSize][newSize], A12[newSize][newSize], A21[newSize][newSize], A22[newSize][newSize];
    int B11[newSize][newSize], B12[newSize][newSize], B21[newSize][newSize], B22[newSize][newSize];
    int C11[newSize][newSize], C12[newSize][newSize], C21[newSize][newSize], C22[newSize][newSize];
    int M1[newSize][newSize], M2[newSize][newSize], M3[newSize][newSize], M4[newSize][newSize], M5[newSize][newSize], M6[newSize][newSize], M7[newSize][newSize];
    int temp1[newSize][newSize], temp2[newSize][newSize];

    // Dividing matrices into sub-matrices
    for (int i = 0; i < newSize; i++) {
        for (int j = 0; j < newSize; j++) {
            A11[i][j] = A[i][j];
            A12[i][j] = A[i][j + newSize];
            A21[i][j] = A[i + newSize][j];
            A22[i][j] = A[i + newSize][j + newSize];

            B11[i][j] = B[i][j];
            B12[i][j] = B[i][j + newSize];
            B21[i][j] = B[i + newSize][j];
            B22[i][j] = B[i + newSize][j + newSize];
        }
    }

    // Calculating M1 to M7
    add(newSize, A11, A22, temp1);
    add(newSize, B11, B22, temp2);
    strassen(newSize, temp1, temp2, M1); // M1 = (A11 + A22) * (B11 + B22)

    add(newSize, A21, A22, temp1);
    strassen(newSize, temp1, B11, M2); // M2 = (A21 + A22) * B11

    subtract(newSize, B12, B22, temp1);
    strassen(newSize, A11, temp1, M3); // M3 = A11 * (B12 - B22)

    subtract(newSize, B21, B11, temp1);
    strassen(newSize, A22, temp1, M4); // M4 = A22 * (B21 - B11)

    add(newSize, A11, A12, temp1);
    strassen(newSize, temp1, B22, M5); // M5 = (A11 + A12) * B22

    subtract(newSize, A21, A11, temp1);
    add(newSize, B11, B12, temp2);
    strassen(newSize, temp1, temp2, M6); // M6 = (A21 - A11) * (B11 + B12)

    subtract(newSize, A12, A22, temp1);
    add(newSize, B21, B22, temp2);
    strassen(newSize, temp1, temp2, M7); // M7 = (A12 - A22) * (B21 + B22)

    // Calculating C11, C12, C21, C22
    add(newSize, M1, M4, temp1);
    subtract(newSize, temp1, M5, temp2);
    add(newSize, temp2, M7, C11); // C11 = M1 + M4 - M5 + M7

    add(newSize, M3, M5, C12); // C12 = M3 + M5

    add(newSize, M2, M4, C21); // C21 = M2 + M4

    add(newSize, M1, M3, temp1);
    subtract(newSize, temp1, M2, temp2);
    add(newSize, temp2, M6, C22); // C22 = M1 - M2 + M3 + M6

    // Combining C11, C12, C21, C22 into C
    for (int i = 0; i < newSize; i++) {
        for (int j = 0; j < newSize; j++) {
            C[i][j] = C11[i][j];
            C[i][j + newSize] = C12[i][j];
            C[i + newSize][j] = C21[i][j];
            C[i + newSize][j + newSize] = C22[i][j];
        }
    }
}

// Function to print a matrix
void printMatrix(int n, int matrix[][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d\t", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
     const int n = 4; // Size of matrices
    int A[n][n] = {{1, 2, 3, 4},
                   {5, 6, 7, 8},
                   {9, 10, 11, 12},
                   {13, 14, 15, 16}};
    int B[n][n] = {{17, 18, 19, 20},
                   {21, 22, 23, 24},
                   {25, 26, 27, 28},
                   {29, 30, 31, 32}};
    int C[n][n]; // Resultant matrix

    // Perform Strassen's Matrix Multiplication
    strassen(A, B, C, n);

    // Print the result
    printf("Resultant Matrix C:\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d ", C[i][j]);
        }
        printf("\n");
    }

    return 0;
}
'''
coin_change_dp = '''
#include <stdio.h>

// Function to find the number of ways to make a certain amount using given coins
int coinChange(int coins[], int n, int amount) {
    // Create a table to store results of subproblems
    int dp[amount + 1];
    
    // Initialize all table values as 0
    for (int i = 0; i <= amount; i++)
        dp[i] = 0;
 
    // Base case (if given amount is 0)
    dp[0] = 1;
 
    // Pick all coins one by one and update the dp[] values after the index
    for (int i = 0; i < n; i++)
        for (int j = coins[i]; j <= amount; j++)
            dp[j] += dp[j - coins[i]];
 
    return dp[amount]; // Value in the last cell of dp[] represents the number of ways to make the given amount
}

int main() {
    int coins[] = {1, 2, 5}; // Types of coins available
    int n = sizeof(coins) / sizeof(coins[0]); // Number of different coin types
    int amount = 12; // Target amount

    printf("Number of ways to make %d using the given coins: %d\n", amount, coinChange(coins, n, amount));
    
    return 0;
}

'''
job_sequencing = '''
// C program for the above approach
 
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
 
// A structure to represent a job
typedef struct Job {
   
    char id; // Job Id
    int dead; // Deadline of job
    int profit; // Profit if job is over before or on
                // deadline
} Job;
 
// This function is used for sorting all jobs according to
// profit
int compare(const void* a, const void* b)
{
    Job* temp1 = (Job*)a;
    Job* temp2 = (Job*)b;
    return (temp2->profit - temp1->profit);
}
 
// Find minimum between two numbers.
int min(int num1, int num2)
{
    return (num1 > num2) ? num2 : num1;
}
 
// Returns maximum profit from jobs
void printJobScheduling(Job arr[], int n)
{
    // Sort all jobs according to decreasing order of profit
    qsort(arr, n, sizeof(Job), compare);
 
    int result[n]; // To store result (Sequence of jobs)
    bool slot[n]; // To keep track of free time slots
 
    // Initialize all slots to be free
    for (int i = 0; i < n; i++)
        slot[i] = false;
 
    // Iterate through all given jobs
    for (int i = 0; i < n; i++) {
       
        // Find a free slot for this job (Note that we start
        // from the last possible slot)
        for (int j = min(n, arr[i].dead) - 1; j >= 0; j--) {
           
            // Free slot found
            if (slot[j] == false) {
                result[j] = i; // Add this job to result
                slot[j] = true; // Make this slot occupied
                break;
            }
        }
    }
 
    // Print the result
    for (int i = 0; i < n; i++)
        if (slot[i])
            printf("%c ", arr[result[i]].id);
}
 
// Driver's code
int main()
{
    Job arr[] = { { 'a', 2, 100 },
                  { 'b', 1, 19 },
                  { 'c', 2, 27 },
                  { 'd', 1, 25 },
                  { 'e', 3, 15 } };
    int n = sizeof(arr) / sizeof(arr[0]);
    printf(
        "Following is maximum profit sequence of jobs \n");
 
    // Function call
    printJobScheduling(arr, n);
    return 0;
}

'''

time_complexity = '''
abhi baki hai daalna bhai , sabar rakho
'''

daoaexp = {
    'Prims.c' : prims,
    'Kruskal.c' : kruskal,
    'Dijkstra.c' : dijkstra,
    'Matrix Chain Multiplication.c' : matrix_chain_multiplication,
    'Longest_Common_Subsequence.c' : longest_common_subsequence,
    'job_sequencing.c' : job_sequencing,
    'Fractional greedy Knapsack.c' : fractional_knapsack,
    'N-Queens.c' : n_queens,
    'Sum_of_Subset.c' : sum_of_subset,
    'KMP.c' : kmp,
    'Coin Change Greedy.c' : coin_change_greedy,
    'TSP_dp.c' : TSP_dp,
    '15 Puzzle.c' : a15_puzzle,
    'Strassens_detail.c' : strassens_detail,
    'Coin Change DP.c' : coin_change_dp,
    'time_complexity.txt' : time_complexity,
}

def daa_():
    for filename, content in daoaexp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(daoaexp[exp])