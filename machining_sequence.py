import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

# --- Configuration Constants ---
CYCLE_TIME = 28.4
MIN_EFFICIENCY = 0.80  
MAX_MACHINES = 6
TOOL_CHANGE = 3.3
INDEX_1_TO_ANY = 1.0  # Indexing involving Face 1
INDEX_2_TO_3 = 1.5    # Indexing between Face 2 and 3
MIN_TIME_ALLOWED = CYCLE_TIME * MIN_EFFICIENCY

def calculate_machine_stats(process_list):
    """Calculates total time and tracks transitions for a proposed machine."""
    if not process_list:
        return 0
    
    total_time = 0
    for i in range(len(process_list)):
        p = process_list[i]
        total_time += p['machining_time'] + p['travel_time']
        
        if i > 0:
            prev = process_list[i-1]
            # Tool Change
            if p['tool_index'] != prev['tool_index']:
                total_time += TOOL_CHANGE
            
            # Dynamic Indexing Logic
            if p['face'] != prev['face']:
                if prev['face'] == 1 or p['face'] == 1:
                    total_time += INDEX_1_TO_ANY
                else:
                    total_time += INDEX_2_TO_3
    return total_time

def get_multiple_solutions(processes, num_solutions=10, iterations=30000):
    """Searches for unique sequences satisfying the new face and indexing rules."""
    valid_solutions = []
    seen_combinations = set()

    print(f"Searching for up to {num_solutions} valid sequences...")
    
    for _ in range(iterations):
        if len(valid_solutions) >= num_solutions:
            break
            
        working_procs = processes.copy()
        random.shuffle(working_procs)
        
        current_layout = []
        temp_machine = []
        possible = True
        
        for p in working_procs:
            # Rule: No more than two unique faces per machine
            current_faces = {m['face'] for m in temp_machine}
            potential_faces = current_faces.union({p['face']})
            
            if len(potential_faces) > 2:
                # This machine cannot take a 3rd unique face
                is_compatible = False
            else:
                is_compatible = True
            
            test_machine = temp_machine + [p]
            time = calculate_machine_stats(test_machine)
            
            if time <= CYCLE_TIME and is_compatible:
                temp_machine = test_machine
            else:
                if not temp_machine:
                    possible = False; break
                
                if calculate_machine_stats(temp_machine) < MIN_TIME_ALLOWED:
                    possible = False; break
                
                current_layout.append(temp_machine)
                temp_machine = [p]
        
        if temp_machine:
            if calculate_machine_stats(temp_machine) < MIN_TIME_ALLOWED:
                possible = False
            else:
                current_layout.append(temp_machine)

        if possible and len(current_layout) <= MAX_MACHINES:
            signature = str([[p['process_name'] for p in m] for m in current_layout])
            if signature not in seen_combinations:
                valid_solutions.append(current_layout)
                seen_combinations.add(signature)
                
    return valid_solutions

def plot_production_line(machines, sol_index):
    """Generates the diagram with dynamic indexing and stats."""
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1']
    
    machine_times = []
    
    for m_idx, machine in enumerate(machines):
        bottom = 0
        m_label = f"M{m_idx+1}"
        
        for p_idx, proc in enumerate(machine):
            if p_idx > 0:
                prev = machine[p_idx-1]
                # Plot Tool Change
                if proc['tool_index'] != prev['tool_index']:
                    ax.bar(m_label, TOOL_CHANGE, bottom=bottom, color='lightgrey', edgecolor='black', hatch='//')
                    bottom += TOOL_CHANGE
                # Plot Indexing (Dynamic heights)
                if proc['face'] != prev['face']:
                    idx_dur = INDEX_1_TO_ANY if (prev['face'] == 1 or proc['face'] == 1) else INDEX_2_TO_3
                    ax.bar(m_label, idx_dur, bottom=bottom, color='darkgrey', edgecolor='black')
                    bottom += idx_dur

            duration = proc['machining_time'] + proc['travel_time']
            ax.bar(m_label, duration, bottom=bottom, color=colors[p_idx % len(colors)], edgecolor='black')
            ax.text(m_label, bottom + duration/2, f"{proc['process_name']}\n(F{proc['face']})", 
                    ha='center', va='center', weight='bold', fontsize=8)
            bottom += duration
        
        machine_times.append(bottom)

    # Statistics Calculation
    deviations = [abs(CYCLE_TIME - t) for t in machine_times]
    avg_dev, max_dev, min_dev = np.mean(deviations), np.max(deviations), np.min(deviations)

    # Threshold Lines
    plt.axhline(y=CYCLE_TIME, color='red', linestyle='--', label=f'Cycle Limit ({CYCLE_TIME}s)')
    plt.axhline(y=MIN_TIME_ALLOWED, color='orange', linestyle=':', 
                label=f'{int(MIN_EFFICIENCY*100)}% Efficiency ({MIN_TIME_ALLOWED:.2f}s)')
    
    # Stats Box
    stats_text = (f"STATS (Abs. Deviation)\nAvg: {avg_dev:.2f}s\nMax: {max_dev:.2f}s\nMin: {min_dev:.2f}s")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(1.02, 0.5, stats_text, transform=ax.transAxes, fontsize=10, bbox=props)

    plt.title(f"Solution {sol_index+1} | Faces Used: {len(set(p['face'] for m in machines for p in m))}", fontsize=14)
    plt.ylabel("Seconds")
    plt.ylim(0, CYCLE_TIME + 5)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.show()

# --- Main Runtime ---
try:
    # Look for "Machining Sequence.xlsx"
    df = pd.read_excel("Machining Sequence.xlsx")
    processes = df.to_dict('records')

    solutions = get_multiple_solutions(processes, num_solutions=10)

    if solutions:
        print(f"Found {len(solutions)} valid sequences.")
        for i, sol in enumerate(solutions):
            plot_production_line(sol, i)
    else:
        print(f"No sequences found for {int(MIN_EFFICIENCY*100)}% rule.")
except FileNotFoundError:
    print("Error: Could not find 'Machining Sequence.xlsx'. Please check the file name.")
except Exception as e:
    print(f"An error occurred: {e}")