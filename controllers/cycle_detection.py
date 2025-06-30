def is_cycle_util(adjacent, u, visited, rec_stack):
  
    if not visited[u]:
      
        # Mark the current node as visited
        # and part of recursion stack
        visited[u] = True
        rec_stack[u] = True

        # Recur for all the vertices 
        # adjacent to this vertex
        for x in adjacent[u]:
            if not visited[x] and is_cycle_util(adjacent, x, visited, rec_stack):
                return True
            elif rec_stack[x]:
                return True

    # Remove the vertex from recursion stack
    rec_stack[u] = False
    return False

def is_cyclic(adjacent, V):
    visited = [False] * V
    rec_stack = [False] * V

    # Call the recursive helper function to
    # detect cycle in different DFS trees
    for i in range(V):
        if not visited[i] and is_cycle_util(adjacent, i, visited, rec_stack):
            return True

    return False

# Driver function
if __name__ == "__main__":
    V = 4
    adjacent = [[] for _ in range(V)]

    # Adding edges to the graph
    adjacent[0].append(1)
    adjacent[0].append(2)
    adjacent[1].append(2)
    adjacent[2].append(0)
    adjacent[2].append(3)
    adjacent[3].append(3)

    # Function call
    if is_cyclic(adjacent, V):
        print("Contains Cycle")
    else:
        print("No Cycle")
