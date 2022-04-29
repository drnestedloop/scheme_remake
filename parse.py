import lark
from builtin_items import *

grammar = open("grammarfile.lark", "r")
grammar = grammar.read()

parser = lark.Lark(grammar)


def do_lambda_expression(parts:list, env):
    formals = parts[0]
    assert formals.data[:] == 'call', "Error: Malformed Lambda Expression"
    formals = formals.children
    body_expressions = parts[1:]
    lambda_frame = env.make_child()
    def lambda_call(args):
        assert len(args)  == len(formals), "Error: incorrect number of arguments passed to lambda"
        #bind args to their names 
        for i in range(len(formals)):
            lambda_frame.define(formals[i][:], args[i])
        for expr in body_expressions[:-1]:
            evaluate(expr, lambda_frame)
        return evaluate(body_expressions[-1], lambda_frame)
    return lambda_call
#ensure that the only falsy thing in scheme is the litteral #f (False)
def scheme_boolify(value):
    if(value is False):
        return False
    else:
        return True
def do_define(AST, env):
    assert len(AST.children) == 2, "Error: malformed define statement"
    #evaluate value to be saved
    value = evaluate(AST.children[1], env)
    return env.define(AST.children[0][:], value)
def do_if(AST, env):
    assert len(AST.children) == 3, "Error: malformed if statement"
    predicate = AST.children[0]
    if(scheme_boolify(evaluate(predicate, env))):
        return evaluate(AST.children[1], env)
    else:
        return evaluate(AST.children[2], env)

def do_call(AST, env):
    if(type(AST.children[0]) == lark.tree.Tree):
        opperator = evaluate(AST.children[0], env)
    else:
        fname = AST.children[0][:]
        opperator = env.lookup(fname)
    args = AST.children[1:]
    evaled_args = []
    for arg in args:
        evaled = evaluate(arg, env)
        if(type(evaled) == Comment):
            pass
        else:
            evaled_args.append(evaled)
    return opperator(evaled_args)


def evaluate(AST, env): #TODO rename parameter from AST since the input is not always an AST
    if(type(AST) == lark.tree.Tree):
        if(AST.data[:] == 'lambda_expr'):
            return do_lambda_expression(AST.children, env)
        elif(AST.data[:] == 'define'):
            return do_define(AST, env)
        elif(AST.data[:] == 'if'):
            return do_if(AST, env)
        elif(AST.data[:] == 'call'):
            return do_call(AST, env)
        elif(AST.data[:] == "multi_expr"):
            for expr in AST.children:
                evaluate(expr, env)
        elif(AST.data[:] == "comment"):
            return Comment(AST.children[0][:]) #do nothing, it's a comment
    elif(type(AST) == lark.lexer.Token):
        if(AST.type == 'NUMBER'):
            try:
                intified_number = int(AST[:])
            except ValueError:
                intified_number = None
            floatified_number = float(AST[:])
            return intified_number if floatified_number == intified_number else floatified_number
        else:
            return env.lookup(AST[:])
