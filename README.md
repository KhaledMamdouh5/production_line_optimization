# Machining Sequence & Production Line Optimizer

This Python tool optimizes the balancing of a production line by sequencing machining operations across multiple workstations. It uses a stochastic search algorithm to find valid machine layouts that satisfy cycle time limits, efficiency targets, and physical fixturing constraints.

## 🎯 Optimization Features

The script ensures that every generated solution adheres to the following industrial constraints:

* **Cycle Time Management**: No workstation exceeds the defined `CYCLE_TIME` (default: 28.4s).
* **Efficiency Balancing**: Machines are flagged as invalid if they fall below the `MIN_EFFICIENCY` threshold (default: 80%).
* **Fixturing Constraints**: Each machine is limited to a maximum of **two unique part faces** to minimize complex setup and re-clamping.
* **Automatic Penalty Calculation**:
    * **Tool Change**: Adds 3.3s when transitioning between different tools.
    * **Dynamic Indexing**: Adds 1.0s for rotations involving Face 1 and 1.5s for rotations between Face 2 and Face 3.

## 📊 Visual Analytics

The tool generates a comprehensive bar chart for each valid solution, providing:
* **Task Distribution**: Clear labeling of which process happens at which machine.
* **Overhead Visualization**: Distinctive hatching/coloring for Tool Changes and Indexing times.
* **Performance Metrics**: A "Stats Box" displaying the average, maximum, and minimum deviations from the target Cycle Time.
* **Compliance Lines**: Visual dashed lines for the Cycle Limit and Efficiency floor.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed along with the following libraries:
```bash
pip install pandas matplotlib numpy openpyxl
