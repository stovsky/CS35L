#!/usr/bin/env python3

import os
import sys
import zlib

def topo_order_commits():
    return print_topo()

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


# Returns a string that contains the top level git directory
def find_top_level_git_directory():
    # Get the current working directory
    path = os.getcwd() 

    # If we're at the root, then we couldn't find a .git directory
    while (path != os.path.dirname(path)): 

        # If we find a .git directory, then return
        if (os.path.isdir(path + '/.git')):
       	    return os.path.join(path, '.git')
    
        # Otherwise, set the path to the parent directory
        path = os.path.dirname(path)

    sys.exit("Not inside a Git repository")

# Returns a dictionary that pairs the name of a branch with its commit ID
def get_local_branches():

    # Go to the directory containing the branches
    git_directory = find_top_level_git_directory()
    branch_directory = os.path.join(git_directory, 'refs', 'heads')
    branches = []

    # Walk through each file
    for root, dirs, files in os.walk(branch_directory):
        for file in files:
            # Append each branch to a list of branches
            branch_path = os.path.join(root, file)
            branches.append(branch_path[len(branch_directory) + 1:])

    hashes = {}

    # Walk through each branch
    for branch in branches:

        # Open the branch to get its commit ID
        branch_path = os.path.join(branch_directory, branch)
        hash = open(branch_path, 'r').read()
        hash = hash.replace('\n', '')

        # Add the branch and commit ID pairing to the dictionary
        hashes[branch] = hash
        
    return hashes

# Returns a list of all parents of a commit
def get_parents(id):

    # Go into the object directory that contains the commit ID and open it
    top_level = find_top_level_git_directory()
    path = os.path.join(os.path.join(top_level, 'objects'),  id[:2], id[2:])
    parents = []
    decompressed = zlib.decompress(open(path, 'rb').read())

    # If it's a commit
    if (decompressed[:6] == b'commit'):

        # Decode it and split it up based on newlines
        decompressed = decompressed.decode().split('\n')

        # If the line contains parent, then append that ID to the parent list
        for message in sorted(decompressed):
            if(message[:6] == 'parent'): parents.append(message[7:])

    return parents

# Create the commit graph that returns a dictionary that pairs a commit ID with its CommitNode
def create_graph():

    # Get all the branches and create an empty graph
    branches = get_local_branches()
    graph = {}

    # Loop through every commit
    for id in sorted(branches.values()):

        # Go into the object directory that contains the commit ID and open it
        top_level = find_top_level_git_directory()
        path = os.path.join(os.path.join(top_level, 'objects'),  id[:2], id[2:])
        decompressed = zlib.decompress(open(path, 'rb').read())

        # If it's a commit
        if (decompressed[:6] == b'commit'):

            # Create a stack and add the id
            stack = [id]

            while(stack != []):

                commit = stack.pop()

                # If the commit is already in the graph, then get that node
                if commit in graph:
                    node = graph[commit]
                # Otherwise, create a new node
                else:
                    node = CommitNode(commit)

                # Find all the parents of the commit
                parents = get_parents(commit)

                for parent in sorted(parents):

                    # Add the parent to the CommitNode's parent set
                    node.parents.add(parent)

                    # If the parent is already in the graph, then get that node
                    if parent in graph:
                        pnode = graph[parent]
                    # Otherwise, we need to create a new node and append the parent to the stack so we can repeat the process
                    else:
                        stack.append(parent)
                        pnode = CommitNode(parent)

                    # Add the current commit to the CommitNode's children set
                    pnode.children.add(commit)

                    graph[parent] = pnode

                graph[commit] = node
    return graph


# This function uses DFS to return a list of the commits in topological ordering  
def create_topo():


    # Create the graph
    graph = create_graph()
    root_commits = []
    seen = set()
    topo = []

    # Find all the root commits
    for id in sorted(graph):
        if len(graph[id].parents) == 0:
            root_commits.append(id)

    for root in root_commits:
        # Add every root to the stack
        if root not in seen:
            stack = [root]

        while (stack != []):

            # Get one of the roots
            commit = stack.pop()

            # If we haven't seen the commit yet
            if commit not in seen:
                
                # If a commit has 2 or more parents, we need to search through each parent
                if len(graph[commit].parents) >= 2:

                    parent_stack = []
                    parent_seen = []

                    # Loop through every parent
                    for parent in sorted(graph[commit].parents):

                        # If we haven't seen the parent yet
                        if parent not in seen:
                            parent_stack = [parent]

                            # We now have seen one of the parents
                            seen.add(parent)
                            while (parent_stack != []):
                                parent_commit = parent_stack.pop()

                                # Search through the parent's parent
                                for parent in sorted(graph[parent_commit].parents):
                                    if parent not in seen:
                                        parent_stack.append(parent)
                                    parent_seen.append(parent_commit)
                                    seen.add(parent_commit)
                    
                    # Add the parents to the topological order
                    for node in reversed(parent_seen):
                        topo.append(node)

                # Search the children next
                for child in sorted(graph[commit].children):
                    if child not in seen:
                        stack.append(child)

                topo.append(commit)
                seen.add(commit)
    return topo

# This function will print the commit hashes, using sticky ends
def print_topo():

    graph = create_graph()
    topo = create_topo()[::-1]
    branches = get_local_branches()
    sticky = False
    topo_len = len(topo)

    # Loop through the topological ordering
    for i in range(topo_len):
        id = topo[i]
        node = graph[id]

        # If the commit is sticky, the output is different
        if sticky:
            sticky = False
            print_sticky = "="

            # Print the children of the sticky commit
            for child in sorted(node.children):
                print_sticky += f'{child} '
            print(print_sticky.rstrip())
        print(id, end='')

        # If the branch matches the id, the commit is associated with that branch
        for branch in sorted(branches.keys()):
            if branches[branch] == id:
                output = ' ' + branch
                print(output, end='')
        print()

        # If we aren't at the last element
        if i  != topo_len - 1:

            # Move to the next node
            id_next = topo[i + 1]
            node_next = graph[id_next]

            # If the current id isn't a child of the next node
            if id not in node_next.children:
                output = ""

                # Print the parents
                for parent in sorted(node.parents):
                    output += f'{parent} '
                output = output.strip()
                print(output + '=')
                print()
                sticky = True



if __name__ == '__main__':
    topo_order_commits()

# I used strace to verify that my implementation does not use other commands by combining strace -f with grep.  I searched for 'git' and also 'exec' in the output of strace -f, so this confirmed I didn't use any outside commands.  The only call to exec was executing pytest.
