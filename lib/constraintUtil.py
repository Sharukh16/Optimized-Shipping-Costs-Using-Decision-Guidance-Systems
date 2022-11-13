'''
constraintSeq is a list of elements that are either
bool, pyomo atomic constraint, or a list of pyomo atomic constraints
The function returns either bool (True or False) or a non-empty sequence of pyomo atomic constraints
'''
def All(constraintSeq):
    constraint = []
    for c in constraintSeq:
        if c == True: pass
        elif c == False: return False
        elif type(c) == list:  # i.e., it is pyomo symbolic list
            constraint.extend(c)
        else:  # i.e., it is a pyomo atomic constraint
            constraint.append(c)
    if constraint == []: return True
    else: return constraint
