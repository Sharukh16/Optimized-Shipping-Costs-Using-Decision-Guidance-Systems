'''
check balancing constraints in SN AM
the input example seems to have a problem
'''

import copy
import json
import importlib.util
import sys
sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/aaa_dgalPy")
import lib.dgalPy as dgal
'''
spec = importlib.util.spec_from_file_location("dgal", "/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/aaa_dgalPy/lib/dgalPy.py")
dgal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dgal)
# import aaa_dgalPy.lib.dgalPy as dgal
'''
#--------------------------------------------------------------
def flowBoundConstraint(flowBounds,flow):

    c = dgal.all([  dgal.all([flow[f]["qty"] >= 0, flow[f]["qty"] >= flowBounds[f]["lb"]])
                    for f in flow
    ])
    dgal.debug("flowBoundConstraints", c)
    return c

#--------------------------------------------------------------
def atomicSeqDiff(setA,setB):
    return [a for a in setA if all([b != a for b in setB])]
#--------------------------------------------------------------
'''
must be cleaned up from debug statements + simplified handling of union.
Why did not it work?
'''

def am(input):
    shared = input["shared"]
    root = input["rootService"]
    services = input["services"]

    serviceMetrics = computeMetrics(shared,root,services)

    cost = serviceMetrics[root]["cost"]
    constraints = serviceMetrics[root]["constraints"]

    return {
        "cost": cost, "constraints": constraints,
        "rootService": root, "services": serviceMetrics
    }
#--------------------------------------------------------------------
#assumptions on input data for ns:computeMetrics:
#1. root service inFlows and outFlows are disjoint
#2. every inFlow of every subService must have a corresponding root inFlow
#   and/or a corresponding subService outFlow (i.e., an inFlow of a subService can't
#   come from nowhere)
#3. every outFlow of every subService must have a corresponding root outFlow
#   and/or a corresponding subService inFlows (i.e., an outFlow of a subService can't
#  go nowhere)
#4. every root outFlow must have at least one corresponding subService outFlow
#5. every root inFlow must have at least one corresponding subService inFlow
#----------------------------------------------------------------

def computeMetrics(shared,root,services):
    type = services[root]["type"]
    inFlow = services[root]["inFlow"]
    outFlow = services[root]["outFlow"]

    if type == "supplier":
        return {root: supplierMetrics(services[root])}
    elif type == "manufacturer":
        return {root: manufMetrics(services[root])}
    elif type == "transport":
        return {root: transportMetrics(services[root],shared)}
    else:
        subServices = services[root]["subServices"]
        subServiceMetrics = dgal.merge([computeMetrics(shared,s,services) for s in subServices])
        cost = sum([subServiceMetrics[s]["cost"] for s in subServices])

        dgal.debug("computeMetricsRoot",root)
        inOutFlowKeysSet = set().union(inFlow,outFlow)
        flowKeysList = [ k for k in inOutFlowKeysSet]

        for s in subServices:
            flowKeysList.extend(services[s]["inFlow"])
            flowKeysList.extend(services[s]["inFlow"])

#        dgal.debug("flowKeysList after loop", flowKeysList)
        flowKeysSet = set(flowKeysList)
#        dgal.debug("flowKeysSet_after_loop",flowKeysSet)

        internalOnlyFlowKeysSet = set(flowKeysSet).difference(inOutFlowKeysSet)
#        dgal.debug("internalOnlyFlowKeysSet",internalOnlyFlowKeysSet)

        subServicesFlowSupply = dict()
        for f in flowKeysSet:
            supply = sum([ subServiceMetrics[s]["outFlow"][f]["qty"]
                           for s in subServices
                           for ff in subServiceMetrics[s]["outFlow"]
                           if ff == f
                     ])
            subServicesFlowSupply.update({f: supply})
#        dgal.debug("subServicesFlowSupply", subServicesFlowSupply)

        subServicesFlowDemand = dict()
        for f in flowKeysSet:
            supply = sum([ subServiceMetrics[s]["inFlow"][f]["qty"]
                           for s in subServices
                           for ff in subServiceMetrics[s]["inFlow"]
                           if ff == f
                     ])
            subServicesFlowDemand.update({f: supply})
#        dgal.debug("subServicesFlowDemand", subServicesFlowDemand)

        newInFlow = dict()
        for f in inFlow:
            qty = subServicesFlowDemand[f] - subServicesFlowSupply[f]
            newInFlow.update({f:{"qty":qty, "item": inFlow[f]["item"]}})
#        dgal.debug("newInFlow",newInFlow)

        newOutFlow = dict()
        for f in outFlow:
            qty = subServicesFlowSupply[f] - subServicesFlowDemand[f]
            newOutFlow.update({f:{"qty":qty, "item": outFlow[f]["item"]}})
#        dgal.debug("newInFlow",newInFlow)

        internalSupplySatisfiesDemand = dgal.all([
            subServicesFlowSupply[f] >= subServicesFlowDemand[f]
            for f in internalOnlyFlowKeysSet
        ])
#        dgal.debug("internalSupplySatisfiesDemand", internalSupplySatisfiesDemand)
        inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
        outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
        subServiceConstraints = dgal.all([ subServiceMetrics[s]["constraints"]
                                        for s in subServices
                                ])
        constraints = dgal.all([ internalSupplySatisfiesDemand,
                            inFlowConstraints,
                            outFlowConstraints,
                            subServiceConstraints
                      ])
        dgal.debug("constraints", constraints)
        rootMetrics = {
            root : {
                "type": type,
                "cost": cost,
                "constraints": constraints,
                "inFlow": newInFlow,
                "outFlow": newOutFlow,
                "subServices": subServices
            }
        }
        return dgal.merge([ subServiceMetrics , rootMetrics ])
'''

    "debug": {
        "flowKeysSet": list(flowKeysSet),
        "internalOnlyFlowKeysSet": list(internalOnlyFlowKeysSet),
        "subServicesFlowSupply": subServicesFlowSupply,
        "subServicesFlowDemand": subServicesFlowDemand,
        "internalSupplySatisfiesDemand": internalSupplySatisfiesDemand,
        "inFlowConstraints": inFlowConstraints,
        "outFlowConstraints": outFlowConstraints,
        "subServiceConstraints": subServiceConstraints
    }
'''
# end of Compute Metrics function
# ------------------------------------------------------------------------------
def supplierMetrics(supInput):
    type = supInput["type"]
    inFlow = supInput["inFlow"]
    outFlow = supInput["outFlow"]

    dgal.debug("outFlowInSupMetrics", outFlow)
    cost = sum([ outFlow[o]["ppu"] * outFlow[o]["qty"] for o in outFlow ])

    newOutFlow = dict()
    for f in outFlow:
        newOutFlow.update({f: {"qty": outFlow[f]["qty"], "item": outFlow[f]["item"]}})
    constraints = flowBoundConstraint(outFlow,newOutFlow)
    return {
        "type": type,
        "cost": cost,
        "constraints": constraints,
        "inFlow": dict(),
        "outFlow": newOutFlow
    }
#---------------------------------------------------------------------------------------
# simple manufacturer
# assumption: there is an input flow for every inQtyPer1out

def manufMetrics(manufInput):
    type = manufInput["type"]
    inFlow = manufInput["inFlow"]
    outFlow = manufInput["outFlow"]
    qtyInPer1out = manufInput["qtyInPer1out"]

    cost = sum([ outFlow[f]["ppu"] * outFlow[f]["qty"] for f in outFlow ])
    newInFlow = dict()
    newOutFlow = dict()
    for f in inFlow:
        qty = sum([qtyInPer1out[o][f] * outFlow[o]["qty"]
                            for o in qtyInPer1out
                            for i in qtyInPer1out[o]
                            if i == f
              ])
        newInFlow.update({f: {"qty":qty, "item": inFlow[f]["item"]}})


    newOutFlow = dgal.merge([
        {f: {"qty": outFlow[f]["qty"], "item": outFlow[f]["item"]}}
        for f in outFlow
    ])

    inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
    outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
    constraints = dgal.all([ inFlowConstraints, outFlowConstraints])

    return { "type": type,
             "cost": cost,
             "constraints": constraints,
             "inFlow": newInFlow,
             "outFlow": newOutFlow
    }
# end of manufMetrics
def transportMetrics(transportInput, shared):
    type = transportInput["type"]
    inFlow = transportInput["inFlow"]
    outFlow = transportInput["outFlow"]
    pplbFromTo = transportInput["pplbFromTo"]
    orders = transportInput["orders"]

    newInFlow = dict()
    for f in inFlow:
        qty = sum([ o["qty"] for o in orders if o["in"] == f ])
        newInFlow.update({f: {"qty": qty, "item": inFlow[f]["item"]} })

    newOutFlow = dict()
    for f in outFlow:
        qty = sum([ o["qty"] for o in orders if o["out"] == f ])
        newOutFlow.update({f: {"qty": qty, "item": outFlow[f]["item"]} })
    dgal.debug("busEntities",shared["busEntities"])
    dgal.debug("orders",orders)

    sourceLocations = set([shared["busEntities"][o["sender"]]["loc"] for o in orders])

    destsPerSource = dict()
    for s in sourceLocations:
        dests = set()
        for o in orders:
            senderLoc = shared["busEntities"][o["sender"]]["loc"]
            recipientLoc = shared["busEntities"][o["recipient"]]["loc"]
            if senderLoc == s:
                dests.add(recipientLoc)
        destsPerSource.update({s: list(dests)})

    weightCostPerSourceDest = list()
    for s in sourceLocations:
        for d in destsPerSource[s]:
            weight = sum([
                unitWeight * o["qty"]
                for o in orders
                if (shared["busEntities"][o["sender"]]["loc"] == s
                    and shared["busEntities"][o["recipient"]]["loc"])
                for unitWeight in [shared["items"][inFlow[o["in"]]["item"]]["weight"]]
            ])
            cost = pplbFromTo[s][d] * weight
            weightCostPerSourceDest.append({"source": s, "dest": d, "weight": weight, "cost": cost })

    cost = sum([ sd["cost"] for sd in weightCostPerSourceDest ])

    inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
    outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
    constraints = dgal.all([inFlowConstraints,outFlowConstraints])
    return { "type": type,
             "cost": cost,
             "constraints": constraints,
             "inFlow": newInFlow,
             "outFlow": newOutFlow,
             "debug": { "busEntities": shared["busEntities"],
                        "sourceLocations": list(sourceLocations),
                        "destsPerSource": destsPerSource
             }

    }
