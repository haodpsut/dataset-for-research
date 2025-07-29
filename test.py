"""
======================================================================
My Final Comparison Test (Version 5) - The Correct Scientific Method
======================================================================
This script builds ONE single, correctly weighted graph and runs BOTH
algorithms on it for a fair and accurate comparison. This version
corrects the TypeError by properly adding edges to the graph.

"""
# --- Core Imports from the Simulator ---
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_entity.user as USER
import h5py
import networkx as nx
import numpy as np
from math import radians, cos, sin, asin, sqrt

# --- Utility Functions ---

def distance_between_satellite_and_user(groundstation, satellite, t):
    """
    Calculates the great-circle distance between a ground station and a satellite's subpoint.
    """
    longitude1, latitude1 = groundstation.longitude, groundstation.latitude
    # Assuming satellite longitude/latitude is 1-indexed for time t
    longitude2, latitude2 = satellite.longitude[t-1], satellite.latitude[t-1]
    
    longitude1, latitude1, longitude2, latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2), float(latitude2)])
    
    dlon, dlat = longitude2 - longitude1, latitude2 - latitude1
    a = sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    # Earth radius in km
    distance = 2 * asin(sqrt(a)) * 6371.0
    return np.round(distance, 3)

def build_graph_at_time_t(constellation_name, shell, time_slot):
    """
    Builds and returns a NetworkX graph 'G' for a specific shell and time slot.
    The graph's edges are weighted by the inter-satellite delay.
    """
    file_path = f"data/XML_constellation/{constellation_name}.h5"
    
    try:
        with h5py.File(file_path, 'r') as file:
            delay_group = file['delay']
            current_shell_group = delay_group[shell.shell_name]
            delay_matrix = np.array(current_shell_group[f'timeslot{time_slot}']).tolist()
    except KeyError:
        print(f"FATAL ERROR: 'delay' data not found in {file_path}. Please run a script that generates it first.")
        return None

    G = nx.Graph()
    # The number of satellites is the dimension of the matrix.
    # It's usually (num_sats + 1) because satellite IDs start from 1.
    num_sats_plus_one = len(delay_matrix)
    satellite_nodes = [f"satellite_{i}" for i in range(1, num_sats_plus_one)]
    G.add_nodes_from(satellite_nodes)

    # --- CORRECTED GRAPH BUILDING LOGIC ---
    for i in range(1, num_sats_plus_one):
        for j in range(i + 1, num_sats_plus_one):
            if delay_matrix[i][j] > 0:
                # Add edge directly with the 'weight' attribute.
                # 'weight' is the standard attribute name that NetworkX algorithms look for.
                G.add_edge(f"satellite_{i}", f"satellite_{j}", weight=delay_matrix[i][j])
    
    return G

def calculate_path_delay(path, G):
    """
    Calculates the total delay (sum of weights) of a given path on graph G.
    """
    # nx.path_weight is the most efficient way to do this.
    return nx.path_weight(G, path, weight='weight')

# --- Main Comparison Logic ---

def main_comparison():
    # --- 1. Scenario Setup ---
    constellation_name = "Telesat"
    source = USER.user(-122.42, 37.77, "San_Francisco")
    target = USER.user(151.21, -33.87, "Sydney")
    time_slot = 1

    print("======================================================================")
    print(f"Comparing routes from {source.user_name} to {target.user_name}")
    print(f"Constellation: {constellation_name}, Timeslot: {time_slot}")
    print("======================================================================")

    # --- 2. Pre-computation Step (Ensures 'delay' data exists) ---
    print("\nExecuting pre-computation step to generate delay data...")
    import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
    constellation = constellation_configuration.constellation_configuration(dT=5730, constellation_name=constellation_name)
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=5730)
    print("Pre-computation finished.")

    # --- 3. Build the Master Graph ---
    print("\nBuilding the master network graph...")
    shell = constellation.shells[0]
    G = build_graph_at_time_t(constellation_name, shell, time_slot)
    if G is None:
        return # Stop if graph building failed
    print("Graph built successfully.")

    # --- 4. Find Access Satellites ---
    print("Finding best access satellites...")
    nearest_sat_to_source, nearest_sat_to_target = None, None
    min_dist_source, min_dist_target = float('inf'), float('inf')

    # This can be slow, but it's the logic from the original scripts
    for orbit in shell.orbits:
        for sat in orbit.satellites:
            dist1 = distance_between_satellite_and_user(source, sat, time_slot)
            if dist1 < min_dist_source:
                min_dist_source = dist1
                nearest_sat_to_source = sat
            
            dist2 = distance_between_satellite_and_user(target, sat, time_slot)
            if dist2 < min_dist_target:
                min_dist_target = dist2
                nearest_sat_to_target = sat

    if not nearest_sat_to_source or not nearest_sat_to_target:
        print("ERROR: Could not find access satellites.")
        return
        
    start_node = f"satellite_{nearest_sat_to_source.id}"
    end_node = f"satellite_{nearest_sat_to_target.id}"
    print(f"Access nodes found: {start_node} -> {end_node}")

    # --- 5. Run and Analyze Algorithms on the SAME graph ---
    try:
        # --- Algorithm 1: Shortest Path (by delay) ---
        print("\n--- [Algorithm 1: Shortest Path (Lowest Latency)] ---")
        path1 = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        hops1 = len(path1) - 1
        delay1 = calculate_path_delay(path1, G)
        print(f"\tHop Count: {hops1}")
        print(f"\tTotal Delay (one-way): {delay1:.4f} s")

        # --- Algorithm 2: Least Hop Path ---
        print("\n--- [Algorithm 2: Least Hop Path] ---")
        # To find the least hop path, we run Dijkstra with weight=None
        # NetworkX will treat every edge as having a weight of 1
        path2 = nx.dijkstra_path(G, source=start_node, target=end_node, weight=None)
        hops2 = len(path2) - 1
        # Now, we calculate the DELAY of THIS least-hop path on the original graph
        delay2 = calculate_path_delay(path2, G)
        print(f"\tHop Count: {hops2}")
        print(f"\tTotal Delay (one-way): {delay2:.4f} s")
    
    except nx.NetworkXNoPath:
        print(f"\nERROR: No path could be found between {start_node} and {end_node}.")

    print("\n======================================================================")
    print("Comparison finished.")
    print("======================================================================")


if __name__ == "__main__":
    main_comparison()