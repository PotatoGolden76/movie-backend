import pydot

(graph,) = pydot.graph_from_dot_file('pydt')
graph.write_png('somefile.png')