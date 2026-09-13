"""Small fleet-routing example."""

from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from toroidal_routing.solver import ToroidalRouter


if __name__ == "__main__":
    delivery_nodes = np.random.rand(50, 2) * 100.0
    router = ToroidalRouter()
    route, cost = router.optimize_route(delivery_nodes)

    print("Optimized Fleet Route Sequence:", route[:10], "... (truncated)")
    print(f"Total Toroidal Path Cost Metric: {cost:.4f}")
