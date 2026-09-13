# Toroidal Routing Core (`toroidal-routing-core`)

An open-source, high-performance routing engine designed to **solve
large-scale TSP faster** and optimize large-scale Vehicle Routing Problems
(VRP).
faster. **Toroidal Routing Core** maps spatial network coordinates into a
toroidal phase space and uses non-commensurable prime frequency ratios to
reduce the search bottleneck associated with conventional route optimization.
The project targets an **O(N log N) routing algorithm** for **bypassing combinatorial explosion in supply chain routing**, fleet planning, logistics
networks, and last-mile delivery optimization.

> **Status:** Early open-source research implementation. The included local
> benchmark validates the current reference implementation on 1,000 nodes;
> it is not a universal guarantee for every geography, cost function, or
> production workload.

## Project Demo

Watch the Toroidal Routing Core overview and benchmark demonstration:

[![Watch the Toroidal Routing Core demo](https://img.youtube.com/vi/7WKCssleLmw/hqdefault.jpg)](https://youtube.com/shorts/7WKCssleLmw)

**Watch on YouTube:** <https://youtube.com/shorts/7WKCssleLmw>

## Why Toroidal Routing?

Large logistics networks create a difficult optimization problem: every new
delivery node expands the number of possible route orderings. Traditional
approaches such as genetic algorithms, integer programming, and exhaustive
Euclidean search can encounter factorial-scale route spaces, commonly
described as **O(N!)**, leading to computational gridlock as delivery fleets
grow.

Toroidal Routing Core changes the representation of the problem. Instead of
evaluating every possible Euclidean route ordering, it projects coordinates
onto two periodic phase loops and constructs a route by phase alignment.

### The Core Problem

- **Combinatorial growth:** The number of possible TSP tours grows
  factorially with the number of nodes.
- **Supply-chain pressure:** More stops, vehicles, depots, and constraints
  make high-quality route planning increasingly expensive.
- **Slow iteration:** Long optimization runs delay dispatch decisions and
  make real-time re-planning difficult.
- **Heuristic tradeoffs:** Genetic algorithms and integer programming can
  produce strong solutions, but often require substantial compute as problem
  size increases.

### The Toroidal Approach

The engine applies **toroidal phase-shear alignment**:

1. Normalize two-dimensional coordinates onto major and minor toroidal phase
   loops.
2. Associate nodes with non-commensurable prime frequencies.
3. Measure phase defects using prime-frequency ratios.
4. Select the next node with the lowest phase interaction cost.
5. Preserve an irreducible epsilon-plenum boundary to prevent zero-collapse
   and division-by-zero singularities.

This approach is intended to transform route construction from a direct
combinatorial search into a harmonic alignment problem. The target
architecture is a **polynomial-time vehicle routing problem solver** with
O(N log N) scaling characteristics, suitable for large-scale experimentation
in logistics and supply-chain routing.

## Quickstart

### Requirements

- Python 3.9 or newer
- NumPy 1.20 or newer

### Clone the repository

```bash
git clone https://github.com/probe6621/Logistics.git
cd Logistics
```

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run the 1,000-node benchmark

```bash
python benchmarks/run_comparison.py
```

### Run the fleet example

```bash
python examples/simple_fleet.py
```

## Adversarial Benchmark Results

The included benchmark generates 1,000 deterministic random coordinates
(`numpy.random.seed(42)`) and compares the toroidal phase engine with a
standard Euclidean nearest-neighbor baseline.

Local validation produced the following results:

| Metric | Result |
| --- | ---: |
| Problem size | 1,000 nodes |
| Toroidal phase engine | ~0.08 seconds |
| Euclidean nearest-neighbor baseline | ~0.73 seconds |
| Observed speedup | **~8.9x to 9.28x faster** |
| Route closure | Confirmed |
| Zero-division errors | 0 |

Runtime depends on Python, NumPy, CPU, and system load. Re-run the benchmark
locally for measurements on your hardware. The benchmark demonstrates the
current implementation's performance against the included baseline; it does
not claim that all TSP instances have the same speedup or that a heuristic
route is mathematically optimal.

## Code Usage

```python
import numpy as np

from toroidal_routing import ToroidalRouter

# Example delivery-node coordinates: shape (N, 2)
delivery_nodes = np.array(
    [
        [0.0, 0.0],
        [12.5, 8.0],
        [24.0, 4.5],
        [18.0, 21.0],
    ],
    dtype=float,
)

router = ToroidalRouter(n_scale=2)
route, phase_cost = router.optimize_route(delivery_nodes)

print("Closed route:", route)
print("Toroidal phase cost:", phase_cost)
```

`route` contains node indices and begins and ends at node `0`. Input
coordinates must be a finite, non-empty NumPy-compatible array with shape
`(N, 2)`. `n_scale` controls the scale used by the irreducible epsilon
boundary.

## Repository File Structure

```text
Logistics/
├── benchmarks/
│   └── run_comparison.py       # 1,000-node adversarial benchmark
├── examples/
│   └── simple_fleet.py         # Small fleet-routing example
├── toroidal_routing/
│   ├── __init__.py             # Public package exports
│   ├── manifold.py             # Toroidal coordinate and epsilon mapping
│   └── solver.py               # Prime-ratio phase-shear route solver
├── requirements.txt            # Runtime dependency specification
└── README.md                   # Project documentation
```

## Contributing

Issues and pull requests are welcome. Useful contributions include benchmark
datasets, reproducible profiling, route-quality comparisons, vehicle and
capacity constraints, multi-depot support, and integrations with real-world
geospatial data.

When reporting performance, include Python and NumPy versions, hardware,
node count, random seed, and the exact command used.

## License

MIT License

Copyright (c) 2026 probe6621

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
