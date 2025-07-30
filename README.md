#  MANET Simulation Project

A simulation and performance comparison of two widely used routing protocols — **AODV** and **OLSR** — using the NS-3 network simulator.

This project evaluates their performance based on key metrics such as packet delivery ratio, average delay, throughput, and packet loss.

---

##  Tools & Technologies Used

- **NS-3** – For simulating Mobile Ad-hoc Network protocols  
- **Python** – For parsing and analyzing simulation results  
- **Flowmon** – For measuring network metrics like delay and delivery ratio  

---

##  Protocols Simulated

- **AODV**: A reactive (on-demand) protocol that creates routes only when needed.
- **OLSR**: A proactive protocol that maintains routing information at all times.

---

##  How to Run

1. Run the `.cc` files using NS-3 to simulate the network  
2. Analyze the `.xml` output using the provided Python scripts  
3. Use the Jupyter notebook or `plot_results.py` to visualize results  
