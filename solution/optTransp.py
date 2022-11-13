#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import copy
# replace path below with a path to aaa_dgalPy
sys.path.append("./lib")
#sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/cs787_ha3_supp_manuf_transp_sn_solution")
# import aaa_dgalPy.lib.dgalPy as dgal
import dgalPy as dgal
import ams

dgal.startDebug()

f = open("example_input_output/combined_transp_in_var.json","r")
varInput = json.loads(f.read())

def constraints(o):
    outFlow = o["services"]["combinedTransport"]["outFlow"]
    
    #mat1 = outFlow["mat1_manuf1"]["qty"]
    #mat2 = outFlow["mat2_manuf1"]["qty"]

    mat1 = sum([
        outFlow[o]["qty"]
        for o in outFlow
        if outFlow[o]["item"] == "mat1"
    ])

    mat2 = sum([
        outFlow[o]["qty"]
        for o in outFlow
        if outFlow[o]["item"] == "mat2"
    ])

    return (dgal.all([ o["constraints"], mat1 >= 1000, mat2 >= 2000]))


optAnswer = dgal.min({
    "model": ams.combinedTransp,
    "input": varInput,
    "obj": lambda o: o["cost"],
    "constraints": constraints,
    "options": {"problemType": "mip", "solver":"glpk","debug": True}
})
optOutput = ams.combinedTransp(optAnswer["solution"])
dgal.debug("optOutput",optOutput)
dgal.debug("constraints", optOutput["constraints"])

output = {
#    "input":input,
#    "varInput":varInput,
    "optAnswer": optAnswer,
    "optOutput": optOutput
}
f = open("answers/outOptTransp.json","w")
#f.write(str(output))
f.write(json.dumps(output))
#f.write(str(output))

#print("\n dgal opt output \n", optAnswer)
#print(json.dumps(optAnswer))
