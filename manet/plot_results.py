import matplotlib.pyplot as plt
import pandas as pd
import xml.etree.ElementTree as ET

# Function to parse the XML file and extract data
def analyze_flowmon_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    
    # Initialize lists for the data we need
    times = []
    pdrs = []  # Packet Delivery Ratio
    throughputs = []  # Throughput (Mbps)
    
    # Extract data from the XML structure
    flow_stats = root.find(".//FlowStats")
    for flow in flow_stats.findall("Flow"):
        flow_id = flow.get("flowId")
        sent = int(flow.get("txPackets"))
        received = int(flow.get("rxPackets"))
        
        # Calculate PDR (Packet Delivery Ratio)
        if sent != 0:
            pdr = (received / sent) * 100
        else:
            pdr = 0
        pdrs.append(pdr)
        
        # Calculate throughput (in Mbps)
        tx_bytes = int(flow.get("txBytes"))
        duration = float(flow.get("timeLastTxPacket").replace('e+', 'e').replace('ns', '')) / 1e9  # Convert ns to seconds
        throughput = (tx_bytes * 8) / (duration * 1e6)  # Convert bytes to bits, and seconds to Mbps
        throughputs.append(throughput)

        # Collect the simulation time from the flow information (using timeLastTxPacket)
        times.append(duration)
    
    # Return the results as a DataFrame for easier plotting
    return pd.DataFrame({
        'Time (s)': times,
        'PDR (%)': pdrs,
        'Throughput (Mbps)': throughputs
    })

# Load and analyze the XML file
df = analyze_flowmon_xml("olsr-flowmon.xml")

# Plotting PDR vs Time
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(df['Time (s)'], df['PDR (%)'], marker='o', color='b', label="Packet Delivery Ratio")
plt.title("Packet Delivery Ratio (PDR) over Time")
plt.xlabel("Time (s)")
plt.ylabel("PDR (%)")
plt.grid(True)
plt.legend()

# Plotting Throughput vs Time
plt.subplot(2, 1, 2)
plt.plot(df['Time (s)'], df['Throughput (Mbps)'], marker='o', color='r', label="Throughput")
plt.title("Throughput over Time")
plt.xlabel("Time (s)")
plt.ylabel("Throughput (Mbps)")
plt.grid(True)
plt.legend()

# Show the plots
plt.tight_layout()
plt.show()
