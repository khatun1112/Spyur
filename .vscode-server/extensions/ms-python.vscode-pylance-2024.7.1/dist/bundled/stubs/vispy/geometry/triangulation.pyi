from collections import OrderedDict
from itertools import permutations

import numpy as np
from numpy.typing import ArrayLike

# -*- coding: utf-8 -*-

class Triangulation(object):
    def __init__(self, pts: ArrayLike, edges: ArrayLike): ...
    def _normalize(self): ...
    def _initialize(self): ...
    def triangulate(self): ...
    def _finalize(self): ...
    def _edge_event(self, i, j): ...
    def _find_cut_triangle(self, edge): ...
    def _edge_in_front(self, edge): ...
    def _edge_opposite_point(self, tri, i): ...
    def _adjacent_tri(self, edge, i): ...
    def _tri_from_edge(self, edge): ...
    def _edges_in_tri_except(self, tri, edge): ...
    def _edge_below_front(self, edge, front_index): ...
    def _is_constraining_edge(self, edge): ...
    def _intersected_edge(self, edges, cut_edge): ...
    def _find_edge_intersections(self): ...
    def _split_intersecting_edges(self): ...
    def _merge_duplicate_points(self): ...
    def _distances_from_line(self, edge, points): ...
    def _projection(self, a, b, c): ...
    def _cosine(self, A, B, C): ...
    def _iscounterclockwise(self, a, b, c): ...
    def _edges_intersect(self, edge1, edge2): ...
    def _intersect_edge_arrays(self, lines1, lines2): ...
    def _orientation(self, edge, point): ...
    def _add_tri(self, a, b, c): ...
    def _remove_tri(self, a, b, c): ...

def _triangulate_python(vertices_2d, segments): ...
def _triangulate_cpp(vertices_2d, segments): ...
def triangulate(vertices: ArrayLike) -> tuple[ArrayLike, ArrayLike]: ...
