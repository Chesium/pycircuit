# pycircuit

Python reference implementation for prototyping a DC circuit simulator used in the NUS EE2026 Digital Design Course Project.

The primary artifact in this repo is [`circuitsim.ipynb`](./circuitsim.ipynb), which contains:

- implementation code for Modified Nodal Analysis (MNA) stamping
- rich-text notes and equations for each stamp type
- test circuits with expected outputs and reference diagrams

## Project Goals

- Provide a clear software reference for hardware/FPGA simulator design.
- Validate stamping behavior before translating logic to RTL.
- Keep the implementation small and readable for rapid iteration.

## Current Scope

This prototype currently supports DC operating-point solving with:

- resistors (`add_r`)
- independent current sources (`add_constant_i`)
- independent voltage sources (`add_constant_v`)
- VCVS (voltage-controlled voltage source) (`add_v_ctrl_v`)
- a simple NPN BJT approximation (`add_npn_bjt`)

Core solver flow:

1. Initialize MNA system (`init`)
2. Stamp each component into matrix `A` and RHS vector `J`
3. Solve `A x = J` with NumPy (`solve`)

## Repository Structure

```text
.
├── circuitsim.ipynb      # Main reference notebook (implementation + notes + tests)
├── assets/               # Circuit figures used in notebook/README
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Locked dependency versions
└── main.py               # Minimal placeholder entry point
```

## Setup

Requirements:

- Python >= 3.14

Install dependencies:

```bash
uv sync
```

If you do not use `uv`, install manually:

```bash
pip install numpy ipykernel
```

## Running the Reference Notebook

Launch Jupyter and open the notebook:

```bash
jupyter notebook circuitsim.ipynb
```

Run all cells to execute the built-in tests (Test 1 to Test 6) and compare against the expected values in notebook comments.

## Notes and References

- Main theory reference in notebook:
  - Lawrence T. Pillage, R. A. Rohrer, C. Visweswariah, *Electronic Circuit and System Simulation Methods* (1995)
- Additional teaching references are cited inline in notebook markdown cells.

## Limitations

This is intentionally a compact reference model, not a production SPICE replacement. Current limitations include:

- DC analysis only (no transient/AC analysis)
- linear stamping plus a simple hand-crafted BJT approximation
- no netlist parser yet (circuits are constructed directly in Python)

## Next Steps

- Split notebook code into importable Python modules.
- Add automated regression tests (e.g., `pytest`) for all example circuits.
- Add more nonlinear device models and iterative solvers.
