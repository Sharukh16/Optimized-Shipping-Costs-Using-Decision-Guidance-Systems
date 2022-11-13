#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import copy
# replace path below with a path to aaa_dgalPy
# sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code")
sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/cs787_ha3_supp_manuf_transp_sn_solution")
# import aaa_dgalPy.lib.dgalPy as dgal
import lib.dgalPy as dgal

import ams

dgal.startDebug()
#f = open("exampleSCinput.json", "r")
#input = json.loads(f.read())
f = open("example_input_output/sn_in_var.json","r")
varInput = json.loads(f.read())

def constraints(o):
    outFlow = o["services"]["mySupplyChain"]["outFlow"]
    prod1Qty = outFlow["prod1_manuf2"]["qty"]
    prod2Qty = outFlow["prod2_manuf2"]["qty"]
    return (dgal.all([ o["constraints"], prod1Qty >= 1000, prod2Qty >= 2000]))

optAnswer = dgal.min({
    "model": ams.am,
    "input": varInput,
    "obj": lambda o: o["cost"],
#    "constraints": lambda o: o["constraints"],
    "constraints": constraints,
    "options": {"problemType": "mip", "solver":"glpk","debug": True}
})
optOutput = ams.am(optAnswer["solution"])
dgal.debug("optOutput",optOutput)
dgal.debug("constraints", optOutput["constraints"])

output = {
#    "input":input,
#    "varInput":varInput,
    "optAnswer": optAnswer,
    "optOutput": optOutput
}
f = open("answers/outOptSN.json","w")
#f.write(str(output))
f.write(json.dumps(output))
#f.write(str(output))

#print("\n dgal opt output \n", optAnswer)
#print(json.dumps(optAnswer))
