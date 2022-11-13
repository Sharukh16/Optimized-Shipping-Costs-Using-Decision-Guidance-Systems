# Optimized-Shipping-Costs-Using-Decision-Guidance-Systems
An analytical model using Python to provide optimized shipping costs for a shipping company involving suppliers and manufacturers and their transportation orders, by selecting the best combination of the involved entities depending upon the shipping cost per pound for a particular item for a sender/receiver pair.

 To run the implemented functions in Problem 1 below, use solution/main.py
a. In terminal, make the downloaded folder your current folder
b. In main.py uncomment invocation of the function you want to run, e.g.
answer = ams.supplierMetrics(input) and comment other invocations
c. Run main.py in Python w/ stdin being the model input stdout being the model output.
Example:
python solution/main.py < example_input_output/sn_in.json > answers/out.json to get answers in out.json which you can compare with the correct answer, e.g., in example_input_output/sn_out.json


To optimize the service network, with input captured in
example_input_output/sn_in_var.json, run: python solution/optSN.py
