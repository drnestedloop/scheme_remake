import sys
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
def do_define(code, env):
    assert len(code.children) == 2, "Error: malformed define statement"
    #evaluate value to be saved
    value = evaluate(code.children[1], env)
    return env.define(code.children[0][:], value)
def do_if(code, env):
    assert len(code.children) == 3, "Error: malformed if statement"
    predicate = code.children[0]
    if(scheme_boolify(evaluate(predicate, env))):
        return evaluate(code.children[1], env)
    else:
        return evaluate(code.children[2], env)

def do_call(code, env):
    if(type(code.children[0]) == lark.tree.Tree):
        opperator = evaluate(code.children[0], env)
    else:
        fname = code.children[0][:]
        opperator = env.lookup(fname)
    args = code.children[1:]
    evaled_args = []
    for arg in args:
        evaled = evaluate(arg, env)
        if(type(evaled) == Comment):
            pass
        else:
            evaled_args.append(evaled)
    return opperator(evaled_args)


def evaluate(code, env): 
    if(type(code) == lark.tree.Tree):
        if(code.data[:] == 'lambda_expr'):
            return do_lambda_expression(code.children, env)
        elif(code.data[:] == 'define'):
            return do_define(code, env)
        elif(code.data[:] == 'if'):
            return do_if(code, env)
        elif(code.data[:] == 'call'):
            return do_call(code, env)
        elif(code.data[:] == "multi_expr"):
            for expr in code.children:
                evaluate(expr, env)
        elif(code.data[:] == "comment"):
            return Comment(code.children[0][:]) #do nothing, it's a comment
    elif(type(code) == lark.lexer.Token):
        if(code.type == 'NUMBER'):
            try:
                intified_number = int(code[:])
            except ValueError:
                intified_number = None
            floatified_number = float(code[:])
            return intified_number if floatified_number == intified_number else floatified_number
        else:
            return env.lookup(code[:])


if __name__ == "__main__":
    filename = sys.argv[1]  #get the name of the file to execute -- from experiementation if you are running this script
                            #using python interpreter.py then 'interpreter.py' is the first in argv
    scheme_script = open(filename, 'r') #open file given in the command line arguments
    scheme_script = scheme_script.read() #convert file to string
    evaluate(parser.parse(scheme_script)) #run the code