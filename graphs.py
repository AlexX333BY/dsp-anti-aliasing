from matplotlib import pyplot
from collections import namedtuple

Graph = namedtuple('Graph', ['ox', 'oy', 'name'])
NamedDrawGraphCallback = namedtuple('GraphDrawer', ['callback', 'name'])


class GraphDrawer:
    def __init__(self):
        self.__graph_drawers = []

    def add_plot(self, graph):
        self.__graph_drawers.append(NamedDrawGraphCallback(lambda axes: axes.plot(graph.ox, graph.oy), graph.name))

    def add_stem(self, graph):
        self.__graph_drawers.append(NamedDrawGraphCallback(lambda axes: axes.stem(graph.ox, graph.oy), graph.name))

    def draw(self):
        graphs_count = len(self.__graph_drawers)
        new_figure = pyplot.figure()

        for i, graph_drawer in enumerate(self.__graph_drawers):
            new_axes = new_figure.add_subplot(1, graphs_count, i + 1)
            pyplot.title(graph_drawer.name)
            graph_drawer.callback(new_axes)

    @staticmethod
    def show():
        pyplot.show()
