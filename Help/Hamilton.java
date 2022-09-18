// Sean Szumlanski
// COP 3503, Fall 2021

// Hamilton.java
// =============
// This program reads a graph from a file (in 0-1 matrix format) and determines
// whether it has a Hamiltonian cycle. The solution uses backtracking. It
// attempts to form a path that uses every node in the graph. If it succeeds,
// it checks whether there is an edge from the last node in that path to the
// first node -- thus completing the cycle. If not, or if the algorithm reaches
// a dead end and cannot add any new nodes to the path it's constructing, it
// returns to the previous call and looks for other possible paths (i.e., it
// backtracks to the last decision point).
//
// The file format starts with the number of vertices in the graph, just like
// with Graph.java from earlier this semester. For example, here's the matrix
// multiplication graph we saw in class today (with one extra edge added so that
// it has a Hamiltonian cycle, not just a Hamiltonian path):
//
// 7
// 0 0 0 0 1 0 0
// 0 0 0 0 0 1 0
// 0 1 0 1 0 0 0
// 1 0 1 0 0 0 0
// 0 1 0 1 0 0 0
// 0 0 0 0 0 0 1
// 1 0 1 0 0 0 0
//
//  ^ Plunk that into an input file and give this thing a go.
//
// Note that I modified this program so that it takes a filename (the name of
// the file to read) as a command line argument.


import java.util.*;
import java.io.*;

public class Hamilton
{
	int n;
	boolean [][] matrix;
	
	public boolean hasHamiltonianCycle()
	{
		// We'll use this array to keep track of what vertices we add to the path
		// we're constructing.
		int [] cycle = new int[n];
		
		// We'll use this array to keep track of which vertices have already been
		// added to the path.
		boolean [] used = new boolean[n];
		
		// We'll start by adding vertex 0 to the path and marking it as visited.
		// Recall from class that if there is a Hamiltonian cycle, it contains
		// every vertex exactly once. Therefore, if we find a Hamiltonian cycle,
		// we can choose any vertex as its start vertex and follow along that same
		// cycle. Thus, we can start our search at vertex 0. If there is a
		// Hamiltonian cycle in this graph, there must necessarily be a Hamiltonian
		// cycle that starts at vertex 0.
		cycle[0] = 0;
		used[0] = true;
		
		// Pass things off to our recursive backtracking method.
		//
		// If we find a Hamiltonian cycle, print it out. The vertics are stored
		// in the 'cycle' array (except for the end vertex, which we can print
		// manually, since we know the cycle starts and ends at vertex 0).
		//
		// In class, I coded this print loop in the base case of the private
		// method. I want you to see that you can do it this way, too.
		if (hasHamiltonianCycle(cycle, used, 1))
		{
			for (int i = 0; i < n; i++)
				System.out.print("" + (char)(cycle[i] + 'A') + ", ");
			// Alternatively, we could print cycle[0] as a character below, and
			// our code would work no matter where we choose to start the cycle.
			System.out.println("A");

			return true;
		}
		
		// If we get down here, we did not find a Hamiltonian cycle.
		return false;
	}
	
	private boolean hasHamiltonianCycle(int [] cycle, boolean [] used, int k)
	{
		// The 'k' parameter indicates how many vertices have been placed in
		// the path so far. It also indicates the index where we want to place
		// the next vertex that we add to the 'cycle' array.
		
		// Thus, the vertex we just placed in the 'cycle' array is at position
		// (k - 1). I'm using 'v' here as a convenient short-hand way to refer
		// to that vertex throughout this method.
		int v = cycle[k - 1];
		
		// If we have filled up our path with 'n' vertices (n = matrix.length),
		// then see whether this last vertex has an edge to the start vertex
		// (vertex 0). If so, we have a Hamiltonian path (return true). If not,
		// we failed to find a Hamiltonian path (return false), and we need to
		// backtrack.
		//
		// Alternatively, we could write matrix[v][cycle[0]], which would allow
		// this code to work no matter where we start our search.
		if (k == n)
			return matrix[v][0];
		
		// Look for a vertex that is adjacent to 'v' and has not yet been added
		// to the path we're constructing. If we find such a vertex, add it to the
		// path and see if it leads to a solution.
		for (int i = 0; i < n; i++)
		{
			if (matrix[v][i] && !used[i])
			{
				used[i] = true;
				cycle[k] = i;
				
				if (hasHamiltonianCycle(cycle, used, k + 1))
					return true;
				
				// If we return from the recursive call without having found a
				// solution, remove this vertex from the path we're constructing and
				// move on to the next one.
				used[i] = false;
			}
		}
		// If we didn't find any fruitful paths (i.e., didn't find occassion to
		// return 'true' already), return 'false' to signify that the previous call
		// needs to continue searching for a solution.
		return false;
	}
	
	// Read the graph. This is pretty standard fare at this point. See Graph.java
	// from earlier in the semester if you seek elaboration on how this works.
	public Hamilton(String filename) throws IOException
	{
		Scanner in = new Scanner(new File(filename));
		
		n = in.nextInt();
		matrix = new boolean[n][n];
		
		for (int i = 0; i < n; i++)
			for (int j = 0; j < n; j++)
				matrix[i][j] = (in.nextInt() == 1);
	}
	
	public static void main(String [] args) throws IOException
	{
		if (args.length < 1)
		{
			System.out.println("Proper syntax: java Hamilton <filename>");
			return;
		}
		
		// The name of the file to open is supplied as a command line argument.
		Hamilton g = new Hamilton(args[0]);
		System.out.println(g.hasHamiltonianCycle());
	}
}
