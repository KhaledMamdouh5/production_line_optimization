# Machining Sequence & Production Line Optimizer

This Python tool optimizes the balancing of a production line by sequencing machining operations across multiple workstations. It uses a stochastic search algorithm to find valid machine layouts that satisfy cycle time limits, efficiency targets, and physical fixturing constraints.

## 🎯 Optimization Features

The script ensures that every generated solution adheres to the following industrial constraints:

* **Cycle Time Management**: No workstation exceeds the defined takt time `CYCLE_TIME`.
* **Efficiency Balancing**: Machines are flagged as invalid if they fall below the `MIN_EFFICIENCY` threshold to prevent bottlenecks.
* **Fixturing Constraints**: Each machine is limited to a maximum of **two unique part faces** to minimize complex setup and re-clamping.
* **Automatic Penalty Calculation**:
    * **Tool Change**: Adds tool change time when transitioning between different tools.
    * **Dynamic Indexing**: Adds indexing time for different rotations.

## 📊 Visual Analytics

The tool generates a comprehensive bar chart for each valid solution, providing:
* **Task Distribution**: Clear labeling of which process happens at which machine.
* **Overhead Visualization**: Distinctive hatching/coloring for Tool Changes and Indexing times.
* **Performance Metrics**: A "Stats Box" displaying the average, maximum, and minimum deviations from the target Cycle Time.
* **Compliance Lines**: Visual dashed lines for the Cycle Limit and Efficiency floor.
