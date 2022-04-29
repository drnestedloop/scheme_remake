class Frame:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.names = {}
    def lookup(self, name: str):
        if name in self.names:
            return self.names[name]
        else:
            if(not self.parent is None):
                return self.parent.lookup(name)
            else:
                assert False, f"Error unbound variable name {name}"
    def define(self, name: str, value: any):
        self.names[name] = value
    def make_child(self):
        return Frame(parent=self)
class Comment:
    def __init__(self, message='') -> None:
        self.message = message
class SchemeList:
    def __init__(self, first, rest) -> None:
        assert not rest is None, "Error: List must have two parts. You can always use nil!"
        self.first = first
        self.rest = rest
    def __str__(self) -> str:
        stringified_list = "(list"
        current_list = self
        while not current_list is nil:
            stringified_list += " " + str(current_list.first)
            current_list = current_list.rest
        return stringified_list + ")"
class Nil: #made to create the Nil object
    def __init__(self) -> None:
        pass
#define some important global variables
GLOBAL_FRAME = Frame()
nil = Nil()

#make it easy to add functions to the global frame
def define_in_global_frame(name:str):
    return lambda value: GLOBAL_FRAME.define(name, value)

@define_in_global_frame("+")
def scheme_add(args):
    total = 0
    for arg in args:
        total += arg
    return total
@define_in_global_frame("-")
def scheme_subtract(args):
    i = args[0]
    for arg in args[1:]:
        i -= arg
    return i
@define_in_global_frame("pow")
def scheme_exponentiate(args):
    assert len(args) == 2, "Error: Incorrect number of arguments passed to built-in function power"
    return args[0] ** args[1]
@define_in_global_frame("print")
def scheme_print(args):
    for arg in args:
        #ensure that True and False print as #t and #f
        if(arg == True): arg = "#t"
        if(arg == False): arg = "#f"
        print(">> ", arg)
@define_in_global_frame("car")
def scheme_car(args):
    assert len(args) == 1, "Error: Incorrect number of arguments passed to built-in function car"
    return args[0].first
@define_in_global_frame("cdr")
def scheme_cdr(args):
    assert len(args) == 1, "Error: Incorrect number of arguments passed to built-in function cdr"
    return args[0].rest
@define_in_global_frame("list")
def scheme_list(args):
    if(len(args) == 1):
        return SchemeList(args[0], nil)
    #For some reason the name 'scheme_list' is set to None in the current environment, I got around this by referencing the function by looking it up in GLOBAL_FRAME
    return SchemeList(args[0], GLOBAL_FRAME.lookup('list')(args[1:]))

#add some important constants to the global frame
define_in_global_frame("#t")(True)
define_in_global_frame("#f")(False)