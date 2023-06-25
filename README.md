# Modified-Nodal-Analysis-Circuit-Solver

The code takes in a netlist in the form of a txt file and uses KCL aka the Junction law to solve the given circuit

Problem statement
- Write a linear equation solver that will take in matrices $A$ and $b$ as inputs, and return the vector $x$ that solves the equation $Ax=b$.  Your function should catch errors in the inputs and return suitable error messages for different possible problems.\n",
- Time your solver to solve a random $10\\times 10$ system of equations.  Compare the time taken against the `numpy.linalg.solve` function for the same inputs.\n",
- Given a circuit netlist, read it in from a file, construct the appropriate matrices, and use the solver you have written above to obtain the voltages and currents in the circuit.  If you find AC circuits hard to handle, first do this for pure DC circuits, but you should be able to handle both voltage and current sources.\n",
- (Small bonus): after reading in the netlist, allow some or all sources and impedances to be controlled interactively - either using widgets or other mechanisms.  On each change you should recompute the currents and voltages and display them.
- (Large bonus): make a solver that can do real-time transient simulations of a SPICE netlist and update the currents and voltages dynamically.  They should also be plotted as a function of time and react to changes. This is something along the lines of https://www.falstad.com/circuit/.  Ideally you should be able to do a real-time demo of some experiments you might conduct as part of a basic electronics lab, and simulate the behaviour of an oscilloscope and signal generator.
   
