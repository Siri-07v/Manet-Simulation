import xml.etree.ElementTree as ET

def parse_ns_value(value):
    """Converts strings like '+2.21409e+07ns' to float seconds."""
    if value is None:
        return 0.0
    value = value.replace('ns', '').replace('+', '')
    return float(value) / 1e9  # convert nanoseconds to seconds

def parse_time_ns(value):
    """Parses time like '+3e+09ns' safely."""
    if value is None:
        return 0.0
    value = value.replace('ns', '').replace('+', '').replace('e+', 'e')
    return float(value)

def analyze_flowmon_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()

    total_tx = 0
    total_rx = 0
    total_delay = 0.0
    total_throughput = 0.0
    valid_flows = 0

    for flow in root.findall(".//FlowStats/Flow"):
        tx = flow.get("txPackets")
        rx = flow.get("rxPackets")
        if tx is None or rx is None:
            continue  # skip incomplete entries

        tx = int(tx)
        rx = int(rx)
        delay = parse_ns_value(flow.get("delaySum"))
        rx_bytes = int(flow.get("rxBytes"))
        time_first_tx = parse_time_ns(flow.get("timeFirstTxPacket"))
        time_last_rx = parse_time_ns(flow.get("timeLastRxPacket"))
        duration = time_last_rx - time_first_tx

        if duration <= 0:
            throughput = 0.0
        else:
            throughput = (rx_bytes * 8) / duration / 1e6  # Mbps

        total_tx += tx
        total_rx += rx
        total_delay += delay
        total_throughput += throughput
        valid_flows += 1

    pdr = (total_rx / total_tx) * 100 if total_tx > 0 else 0.0
    avg_delay = total_delay / valid_flows if valid_flows > 0 else 0.0
    avg_throughput = total_throughput / valid_flows if valid_flows > 0 else 0.0

    print(f"✅ Packet Delivery Ratio (PDR): {pdr:.2f}%")
    print(f"✅ Average Delay: {avg_delay:.6f} seconds")
    print(f"✅ Average Throughput: {avg_throughput:.6f} Mbps")

# Run it
analyze_flowmon_xml("aodv-flowmon.xml")

