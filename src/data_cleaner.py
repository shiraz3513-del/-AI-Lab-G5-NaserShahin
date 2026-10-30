"""
Clean and analyze routing graph data for AI Lab G5.

Author: Naser Shahin (Coding / Step 3)

The input graph must be a NetworkX MultiDiGraph.
Coordinates use x=longitude and y=latitude.
Edge length is measured in meters.
"""

from __future__ import annotations

import copy
import math
from typing import Any

import networkx as nx


def _valid_number(value: Any) -> bool:
    """Check whether a value is a finite number."""
    try:
        number = float(value)
        return math.isfinite(number)
    except (TypeError, ValueError):
        return False


def _valid_coordinates(attributes: dict) -> bool:
    """Check longitude and latitude values and their valid ranges."""
    if "x" not in attributes or "y" not in attributes:
        return False

    if not _valid_number(attributes["x"]):
        return False

    if not _valid_number(attributes["y"]):
        return False

    longitude = float(attributes["x"])
    latitude = float(attributes["y"])

    return -180 <= longitude <= 180 and -90 <= latitude <= 90


def clean_graph(graph: nx.MultiDiGraph) -> tuple[nx.MultiDiGraph, dict]:
    """
    Clean a copy of the input graph.

    Invalid-coordinate nodes and invalid-length edges are removed.
    The original graph remains unchanged.
    """

    if not isinstance(graph, nx.MultiDiGraph):
        raise TypeError("Input must be a NetworkX MultiDiGraph.")

    cleaned = copy.deepcopy(graph)

    original_nodes = cleaned.number_of_nodes()
    original_edges = cleaned.number_of_edges()

    invalid_nodes = []

    # Check node coordinates.
    for node_id, attributes in list(cleaned.nodes(data=True)):
        if not _valid_coordinates(attributes):
            invalid_nodes.append(node_id)
        else:
            attributes["x"] = float(attributes["x"])
            attributes["y"] = float(attributes["y"])

    # Remove nodes with invalid coordinates.
    cleaned.remove_nodes_from(invalid_nodes)

    invalid_edges = []

    # Check edge lengths. Parallel edges are checked separately.
    for u, v, key, attributes in list(
        cleaned.edges(keys=True, data=True)
    ):
        length = attributes.get("length")

        # Use weight as a fallback if length is missing.
        if length is None:
            length = attributes.get("weight")

        if not _valid_number(length) or float(length) < 0:
            invalid_edges.append((u, v, key))
        else:
            attributes["length"] = float(length)
            attributes["weight"] = float(length)

    # Remove invalid edges.
    for u, v, key in invalid_edges:
        cleaned.remove_edge(u, v, key)

    # Find isolated nodes.
    isolated_nodes = [
        node for node in cleaned.nodes()
        if cleaned.degree(node) == 0
    ]

    # Analyze graph connectivity.
    if cleaned.number_of_nodes() > 0:
        weak_components = list(
            nx.weakly_connected_components(cleaned)
        )
        strong_components = list(
            nx.strongly_connected_components(cleaned)
        )
    else:
        weak_components = []
        strong_components = []

    report = {
        "original_node_count": original_nodes,
        "original_edge_count": original_edges,
        "cleaned_node_count": cleaned.number_of_nodes(),
        "cleaned_edge_count": cleaned.number_of_edges(),
        "removed_node_count": len(invalid_nodes),
        "removed_edge_count": len(invalid_edges),
        "isolated_node_count": len(isolated_nodes),
        "weak_component_count": len(weak_components),
        "strong_component_count": len(strong_components),
        "invalid_nodes": invalid_nodes,
        "invalid_edges": invalid_edges,
        "isolated_nodes": isolated_nodes,
        "valid": (
            cleaned.number_of_nodes() > 0
            and cleaned.number_of_edges() > 0
        ),
    }

    return cleaned, report


def analyze_graph_quality(graph: nx.MultiDiGraph) -> dict:
    """
    Analyze graph quality without changing the original graph.
    """

    _, report = clean_graph(graph)
    return report
