#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append(r'//Users/alexbrodsky/Documents/OneDrive\ -\ George\ Mason\ University\ -\ O365\ Production/aaa_python_code')
sys.path.append(r'/lib')
import copy
import pyomo.environ as pyo
from pyomo.environ import *
import json
import ams
# import aaa_dgalPy.lib.dgalPy as dgal
# import importlib.util
# spec = importlib.util.spec_from_file_location("dgal", "/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/aaa_dgalPy/lib/dgalPy.py")
# dgal = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(dgal)

f = open("example_input_output/shared.json", "r")
shared = json.loads(f.read())

input = json.loads(sys.stdin.read())
# answer = ams.supplierMetrics(input)
# answer = ams.manufMetrics(input)
# answer = ams.transportMetrics(input,shared)
# answer = ams.combinedSupply(input)
# answer = ams.combinedManuf(input)
# answer = ams.combinedTransp(input)
answer = ams.am(input)
sys.stdout.write(json.dumps(answer))

# f = open("out.json","w")
# f.write(json.dumps(answer))

#print("\n dgal opt output \n", optAnswer)
#print(json.dumps(optAnswer))
