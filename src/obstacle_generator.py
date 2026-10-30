"""
Generate obstacle scenarios for AI Lab G5 routing experiments.

Author: Naser Shahin (Coding / Step 3)

All scenarios are applied to a copy of the input graph.
The original graph is never modified.
"""

from __future__ import annotations

import copy
import math
from typing import Any

import networkx as nx


def _get_edge_keys(
    graph: nx.MultiDiGraph,
    u: Any,
    v: Any,
    key: Any = None,
) -> list:
    """Return matching edge keys between two nodes."""

    if not graph.has_edge(u, v):
        return []

    available_keys = list(graph[u][v].keys())

    if key is None:
        return available_keys

    return [key] if key in available_keys else []


def _collect_edges(
    graph: nx.MultiDiGraph,
    edges: list[tuple],
    bidirectional: bool,
) -> list[tuple]:
    """Find existing edges, including optional reverse directions."""

    selected = []

    for edge in edges:
        if len(edge) not in (2, 3):
            raise ValueError(
                "Each edge must be (u, v) or (u, v, key)."
            )

        u, v = edge[0], edge[1]
        key = edge[2] if len(edge) == 3 else None

        if u not in graph or v not in graph:
            raise ValueError(f"Unknown node in edge: {edge}")

        directions = [(u, v)]

        if bidirectional and u != v:
            directions.append((v, u))

        found = False

        for start, end in directions:
            keys = _get_edge_keys(graph, start, end, key)

            for edge_key in keys:
                selected.append((start, end, edge_key))
                found = True

        if not found:
            raise ValueError(f"Edge not found in graph: {edge}")

    # Remove duplicate edge references.
    return list(dict.fromkeys(selected))


def generate_obstacle_scenario(
    graph: nx.MultiDiGraph,
    scenario: str,
    edges: list[tuple],
    *,
    bidirectional: bool = True,
    penalty_factor: float = 5.0,
) -> tuple[nx.MultiDiGraph, dict]:
    """
    Apply an obstacle scenario to a copy of the graph.

    Supported scenarios:
    - single_closure
    - multiple_closures
    - high_cost

    Edge formats:
    - (u, v): all parallel edges between two nodes
    - (u, v, key): one specific parallel edge

    Returns:
        A modified graph and a scenario report.
    """

    if not isinstance(graph, nx.MultiDiGraph):
        raise TypeError("Input must be a NetworkX MultiDiGraph.")

    if not edges:
        raise ValueError("At least one edge must be provided.")

    allowed_scenarios = {
        "single_closure",
        "multiple_closures",
        "high_cost",
    }

    if scenario not in allowed_scenarios:
        raise ValueError(
            f"Unknown scenario. Choose one of: {sorted(allowed_scenarios)}"
        )

    if scenario == "single_closure" and len(edges) != 1:
        raise ValueError("single_closure requires exactly one edge.")

    if scenario == "multiple_closures" and len(edges) < 2:
        raise ValueError("multiple_closures requires at least two edges.")

    if scenario == "high_cost":
        try:
            penalty_factor = float(penalty_factor)
        except (TypeError, ValueError) as exc:
            raise ValueError("penalty_factor must be numeric.") from exc

        if not math.isfinite(penalty_factor) or penalty_factor <= 1:
            raise ValueError("penalty_factor must be finite and greater than 1.")

    # Work on a separate copy to protect the original graph.
    modified_graph = copy.deepcopy(graph)

    selected_edges = _collect_edges(
        modified_graph,
        edges,
        bidirectional,
    )

    changed_edges = []

    if scenario in {"single_closure", "multiple_closures"}:

        # Remove the selected edges from the copied graph.
        for u, v, key in selected_edges:
            if modified_graph.has_edge(u, v, key):
                modified_graph.remove_edge(u, v, key)
                changed_edges.append((u, v, key))

    elif scenario == "high_cost":

        # Increase the routing cost without closing the roads.
        for u, v, key in selected_edges:
            attributes = modified_graph[u][v][key]

            length = attributes.get("length")

            try:
                length = float(length)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid length on edge ({u}, {v}, {key})."
                ) from exc

            if not math.isfinite(length) or length < 0:
                raise ValueError(
                    f"Invalid length on edge ({u}, {v}, {key})."
                )

            new_length = length * penalty_factor

            attributes["length"] = new_length
            attributes["weight"] = new_length
            attributes["obstacle_penalty"] = penalty_factor

            changed_edges.append((u, v, key))

    report = {
        "scenario": scenario,
        "requested_edges": len(edges),
        "changed_edge_count": len(changed_edges),
        "changed_edges": changed_edges,
        "bidirectional": bidirectional,
        "penalty_factor": (
            penalty_factor if scenario == "high_cost" else None
        ),
        "original_graph_preserved": True,
    }

    return modified_graph, report
