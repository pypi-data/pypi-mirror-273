# pywgraph

A library to manipulate weighted graphs in python. This library focus on directed graphs whose edges have weights. The weights of the graph can be any elements of a fixed mathematical group. By default, the underlying group is set to be the real numbers with the multiplication. Thus, when trasversing the graph, the weight of the path is the product of the weights of the edges, but in general, it is the product under the binary operation of the group.

For this reason, this package also includes a basic abstraction of a group. The group definition is base on:

* The a function of two variables that return one element (the binary operation of the group).

* The inverse function of an element. This is, the function that given an element of the group returns its inverse.

* The identity element of the group.

* Optional, a hash function for the elements of the group. By default it is taken the standard python hash function. If your group contains not hashable elements you should provide one.

* [New in `1.1.0`] Optional, a check function to check if an element belongs to the group.

## QUICKSTART

### Edges

The main object to construct the graph is the `WeightedDirectedEdge` class. This represents a directed edge with a weight. The construction basic construction is as follows:

```python
from pywgraph import WeightedDirectedEdge

edge = WeightedDirectedEdge("A", "B", 0.5)
```

The first two parameters are the nodes that the edge connects. The last parameter is the weight. It is important to notice that, since this is a directed edge, the order of the nodes is important. Since we do have not specify any group, the default group is the real numbers with the multiplication.

You can call the start and end nodes with `edge.start` and `edge.end`, respectevely. To get the weight, simply use `edge.weight`. You can also get the *inverse edge* with `edge.inverse`. This is, the edge that connects the end node of `edge` to the start node of `edge` and has `1/edge.weight` as weight (as said previously, in the future this is meant to be the inverse of the weight in the underlying group).

Also, this class is hashable and iterable, yielding the start node, end node and weight.

### Graph

The graph is represented by the `WeightedDirectedGraph` class. This is the main class of the package. The graph itself is a set of nodes and a set of `WeightedDirectedEdge`s. If you don`t specify it, the underlying group for the weights as said would be the real numbers with the multiplication.

It is also possible, and more comfortable, to create the graph using the `WeightedDirectedGraph.from_dict` method, which instantiates the graph from a dictionary. The keys of the dictionary are the starting nodes. The values must consists of another dictionary, where the keys are the ending nodes and the value is the weight of the edge. It is important that all nodes of the graph must be keys in the dictionary. If, for example, there is a node "C" that has no children nodes, then the dictionary must have a key "C" with a value of `{}`.
As always, if you want to use another group for the weights you should specify it here.

```python
from pywgraph import WeightedDirectedGraph

g = WeightedDirectedGraph.from_dict({
    "A": {"B": 0.5},
    "B": {"A": 0.5, "C": 1.0},
    "C": {}
})
```

The equivalent construction using set of nodes and set of edges is as follows:

```python
from pywgraph import WeightedDirectedGraph

graph = WeightedDirectedGraph(
    nodes={"A", "B", "C"},
    edges={
        WeightedDirectedEdge("A", "B", 0.5),
        WeightedDirectedEdge("B", "A", 0.5),
        WeightedDirectedEdge("B", "C", 1.0)
    }
)
```

You can instantiate a bad define graph by not writting all the nodes that appear in the edges in the nodes set. There is a method `check_defintion` that checks if the graph is well defined, but the check is not enforce. You can retrieve the nodes and edges by `graph.nodes` and `graph.edges`, respectively.

You can also acces the children and the parents of a nodes with the methods `children` and `parents`, respectively.

```python
graph.children("A")
# {"B"}

graph.parents("A")
# {}

graph.children("B")
# {"A", "C"}
```

The main use of this graph object is to work with their weights as group elements, so normally, you want that reverse edges of existing ones have the inverse weight of the existing edge weight. For this, there is the method `add_reverse_edges` that returns a new graph with the original graph with all the reverse edges added. You can also modify the graph directly with the paremeter `inplace=True`.

```python
graph_w_inverse_edges = graph.add_reverse_edges()

# Updating the graph 
graph.add_reverse_edges(inplace=True)
```

### Path finding

There is a method `find_paths` that finds all paths between two gven nodes. This method have many options to modify the behaviour of the search. Its parameters are:

* `start`: The node of the graph where the algorithm starts the search.
* `end`: The target node of the graph to reach.
* `general_max_visitations`: A non negative integer that specifies the maximum number of times that nodes can be visited along the path. By default is set to one.
* `specific_max_visitations`: A dictionary whose keys are nodes and values are non negative integers. This specifies the maximum number of times that the key node can be visited along the path, overriding what is set in the `genera_max_visitations` parameter. By default is set to the empty dictionary. You can use this parameter to find paths that avoid one node by setting `genera_max_visitations={"AvoidNode":0}`. You can also use it to find cycles by setting the same starting and ending node and allowing to visit it two times. There is an specific method to find cycles.
* `max_iter`: A non negative integer that limits the number of iterations of the search algorithm. The algorithm should always finish, but for large and complex paths it can take a lot of iterations. You can use this parameter to limit the amount of iterations to perform. By default is set to the factorial of the number of nodes in the graph. A warning will be raised if the maximum number of iterations is reached.
* `max_paths`: A non negative integer that limits the number of paths that the method will return. By default is set to infinity, so it will return all the possible paths. If you are interested in finding only one path you can set this parameter to one and the algorithm will finish after finding it.

The result of this method will be a list of `Paths` objects, which is just a direct subclass of `list[str]` that is used to represent a path. If no path was found the result will be an empty list.

```python
dictionary = {
    "A": {"B": 1},
    "B": {"C": 2.5, "A": 1},
    "C": {},
    "Z": {},
}
graph = WeightedDirectedGraph.from_dict(dictionary)

graph.find_paths("A", "B")
# [["A", "B]]

graph.find_paths("A", "Z")
# []

graph.find_paths("A", "C")
# [["A", "B", "C"]]

graph.find_paths("A", "A")
# [["A"]]

graph.find_paths("A", "A", general_max_visitations=2)
# [['A'], ['A','B','A'], ['A','B','C','B','A']]

graph.find_paths("A", "B", general_max_visitations=2)
# [['A','B'], ['A','B','A','B], ['A','B','C','B']]

graph.find_paths("A", "B", specific_max_visitations={"B":2})
# [['A','B'], ['A','B','C','B']
```

There is also a method to get the weight of following a path. This method is call `path_weight`. It receives a `Path` object or `list[str]` and returns the weight of the path (the product of the weights). You can set a default value (like the python `dict.get`) that will be return if the path is empty. By default it is set to `None`. If the given path does not exists an exception will be raised. If the given path consists of just one node, the identity element of the group (1.0 for standard graphs) will be return.

```python
graph.path_weight([], "Helo World")
# "Helo World"

graph.path_weight(["A", "B"])
# 1.0

graph.path_weight(["A", "B", "C"])
# 2.5

graph.path_weight(["Z"])
# 1.0
```

### Graphs and groups

#### Introduction to the `Group` class

As said in the introduction, there is also an abstraction of a mathematical group. This object is call simply `Group`. To initialize it you need to provide a description of the group (string), the binary operation, the inverse operation and the identity element. If the elements of the group are not hashable, you should provide a hash function. One example could be an implementation of $\mathbb{R^2}$ under addition. For this we could represent vectors with numpy arrays, which are not hashable. We can construct this group as follows.

```python
import numpy as np
from pywgraph import Group

group = Group(
    name="R^2 under addition",
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    identity=np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)
```

You can also provide a check function that checks if an object belongs to the group. In the above case, a checker function could be defined by:

```python
def r_2_check(weight: Any) -> bool:
    if not isinstance(weight, np.ndarray): 
        return False
    if len(weight) != 2:
        return False
    if not all(isinstance(x, (int, float)) for x in weight):
        return False
    return True
```

This group instance is callable. The call gets two variables as inputs and return the operation between them. Since there is no type checking, the user is responsible of using it with valid inputs. You can also call the group operation with the property `Group.operation` and the inverse operation by `Group.inverse_function`. The identity element is stored in the property `Group.identity`. If you need to, you can also get back the hash function with the property `Group.hash_function`. If provided a check function, you can check if an object belongs to the group with the method `Group.check`.

```python
import numpy as np 
vector_1 = np.array([1, 3])
vector_2 = np.arra([-1, 7])

group(vector_1, vector_2)
# np.array([0, 10])

group.operation(vector_1, vector_2)
# np.array([0, 10])

group.inverse(vector_1)
# np.array([-1, -3])

group.identity
# np.array([0, 0])

group.check(vector_1)
# True

group.check(23)
# False
```

#### General weights for edges

Now that we introduce how to construct a group we will se how to use it to provide elements of an arbitrary group as weights of an edge. To do so you just need to create the group and add it as a parameter in the constructor of edge.

```python
from pywgraph import WeightedDirectedEdge, Group
import numpy as np 
group = Group(
    name="R^2 under addition",
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    identity=np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)
weight_of_edge = np.array([1, 2])

edge = WeightedDirectedEdge("A", "B", weight_of_edge, group)
```

With the group information given, now this edge instance knows how to construct the inverse edge.

```python
edge.inverse
# WeightedDirectedEdge("B", "A", np.array([-1, -2]), group)
```

Is important to notice that there is no checking of wether the provide weight is a valid element of the given group.

#### General weighted graphs

Now, for constructing a weighted directed graph whose weights are elements of a specific group you just need to define the group and create the graph adding the group as parameter. The edges of the graph need to include the group as well, as seen before. A better way to construct the graph is to use the method `WeightedDirectedGraph.from_dict`. Now this works exactly the same but adding the group as a new parameter.

With this implementation any method that concerns weights uses the group operation to handle it. For example, the weight of a given path that the `WeightedDirectedGraph.path_weight` yields is obtain with the consecutive application of the group operation. The same happens with the `WeightedDirectedGraph.weight_between` method.

```python
from pywgraph import WeightedDirectedGraph, Group
import numpy as np 
group = Group(
    "R^2 under addition",
    lambda x, y: x + y,
    lambda x, y: x - y,
    np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)

dictionary = {
    "A": {"B": np.array([1, 2.5]), "C": np.array([-1, 3.4])},
    "B": {"C": np.array([2.5, -1])},
    "C": {"A": np.array([1 / 2.5, 1 / 3.4]), "D": np.array([1.3, 3.4])},
    "D": {"E": np.array([3.4, 1.3])},
    "E": {},
}

graph = WeightedDirectedGraph.from_dict(dictionary, group)
# Creates the graph

graph.path_weight(["A", "C"])
# np.array([-1, 3.4])

graph.path_weight(["A", "B", "C"])
# np.array([1, 2.5]) + np.array([2.5, -1]) = np.array([3.5, 1.5])
```

Notice that this graph is not conmutative since the weight of the path `["A", "C"]` is different from the weight of the path `["A", "B", "C]`.

## Release Notes

### Version 1.0.1 (2024-05-07)

* Added a method to `WeightedDirectedGraph` to add a new node.
* Added a method to `WeightedDirectedGraph` to add a new edge. This can be doned given the desire weight, given a path between the nodes to connect and use the product of the weights or just let the graph find a path between nodes and use the product of the weights.

### Version 1.0.2 (2024-05-09)

* Added a method to `WeightedDirectedGraph` to remove a node.
* Added a method to `WeightedDirectedGraph` to remove an edge.

### Version 1.1.0 (2024-05-15)

* The `Group` class now has a `group_checker` optional parameter that consists of a function to check wether an element belongs to the group or not.

* Add the method `WeightedDirectedGraph.find_paths` to find all paths between two given nodes.
* The method `WeightedDirectedGraph.find_path` is deprecated and will be removed, use `find_paths` with `max_paths=1` to replicate `WeightedDirectedGraph.find_path` behaviour.
* Add `Path` and `Cycle` classes to represent an abstraction of a node path and a node cycle.
* Add method `WeightedDirectedGraph.get_node_cycles` to find all cycles that contains the node.
* Add property `WeightedDirectedGraph.cycles` that returns the set of all simple cycles of the graph.
* Add the property `WeightedDirectedGraph.is_conmutative` that checks it the graph is conmutative.
* The method `WeightedDirectedGraph.weight_between` is deprecated and will be removed. Combine `WeightedDirectedGraph.find_paths` with `WeightedDirectedGraph.path_weight` to replicate `WeightedDirectedGraph.weight_between` behaviour.
* The behaviour of `WeightedDirectedGraph.add_edge` when no weight and path is given is deprecated and will be removed. Either give a weight or seach for a path.
