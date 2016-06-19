'''

The file containing all build in functions / keywords in LOGIC

'''

def echo(args):
    string = ""
    for arg in args:
        string += str(arg)
    print (string)









functions = {
    "ECHO"  :   echo
}