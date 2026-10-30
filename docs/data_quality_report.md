# Data Quality Report

**Project:** AI Lab G5 - AI Urban Routing for Shiraz  
**Author:** Naser Shahin  
**Role:** Data & Evaluation  
**Date:** 2026-10-30

## 1. Introduction

This report describes the data quality checks used in the
AI urban routing project.

The project uses a directed and weighted NetworkX MultiDiGraph.
Node coordinates are stored as longitude (x) and latitude (y).
Edge lengths are stored in meters.

Two types of road networks may be used:

- Real road network downloaded from OpenStreetMap.
- Synthetic grid network generated for testing.

The synthetic network is not a representation of actual Shiraz streets.

## 2. Data Quality Checks

The following checks are performed by data_cleaner.py:

### 2.1 Node Coordinates

- Check for missing longitude and latitude.
- Check whether coordinates are numeric.
- Check longitude range: -180 to 180.
- Check latitude range: -90 to 90.
- Identify nodes with invalid coordinates.

### 2.2 Edge Lengths

- Check whether edge length exists.
- Check whether edge length is numeric.
- Reject negative and non-finite values.
- Synchronize the length and weight attributes.

### 2.3 Graph Connectivity

- Identify isolated nodes.
- Count weakly connected components.
- Count strongly connected components.

### 2.4 Graph Statistics

The report records:

- Original node count.
- Original edge count.
- Cleaned node count.
- Cleaned edge count.
- Removed node count.
- Removed edge count.
- Isolated node count.
- Connected component counts.

## 3. Data Cleaning Method

The cleaning process works on a copy of the original graph.

Nodes with invalid coordinates are removed.
Edges with missing or invalid lengths are removed.
Valid edge lengths are converted to numeric values.

The original graph remains unchanged.

## 4. Obstacle Scenarios

The obstacle generator supports three scenarios:

1. Single road closure.
2. Multiple road closures.
3. Increased road travel cost.

All obstacle scenarios are applied to a copy of the graph.

## 5. Test Data

Test cases are stored in:

`data/test/test_cases.csv`

The initial test cases use the synthetic 8x8 grid.

The synthetic grid contains:

- 64 nodes.
- 224 directed edges.
- 120 meters spacing between adjacent nodes.

Test results are marked as pending until the tests are executed.

## 6. Results

| Metric | Result |
|---|---|
| Graph source | Synthetic grid |
| Original nodes | Pending |
| Original edges | Pending |
| Removed nodes | Pending |
| Removed edges | Pending |
| Isolated nodes | Pending |
| Weak components | Pending |
| Strong components | Pending |
| Validation status | Pending |

## 7. Limitations

- The synthetic network does not represent real streets.
- Real map boundaries and travel mode require team confirmation.
- Test results have not yet been verified.
- Real-world routing performance requires testing with OSM data.

## 8. Conclusion

A data cleaning and quality analysis module has been prepared
to identify invalid coordinates, invalid edge lengths,
isolated nodes, and graph connectivity issues.

The obstacle generator provides controlled scenarios
for evaluating routing behavior.

Final quality metrics will be added after running the
modules on the selected road network.
