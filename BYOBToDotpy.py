import scratch
s = scratch.Scratch(host='127.0.0.1', port=42001)

def listen():
    while True:
        try:
           yield s.receive()
        except scratch.ScratchError:
           raise StopIteration

def addindent(line):
    global indent
    if indent > 0:
        for loop in range(indent):
            line = "    " + line
    return line

#s.broadcast("Hello, Scratch!")
#print "rcv",s.receive()
while True:
    masterlist = []
    for msg in listen():
        print msg
        if msg[0] == 'broadcast':
            inputlist = msg[1].split(',')
            print inputlist
            masterlist.append(inputlist)
            if inputlist[0] == "pythonend":
                break


    print masterlist
    print "-------"

    indent = 0
    dotpy = "#!/usr/bin/env python\n"
    dotpy += "import time as time\n"

    value = masterlist

    for item in value:
        print "type len  item",type(item),len(item),item
        #print
        if 'time.sleep' in item:
            dotpy += addindent("time.sleep(" + str(item[1]) + ")\n")
        elif 'while' in item:
            dotpy += addindent("while " + str(item[1]) + ":\n")
            indent += 1
        elif 'if' in item:
            dotpy += addindent("if " + str(item[1]) + ":\n")
            indent += 1
        elif 'else' in item:
            dotpy += addindent("else:\n")
            indent += 1
        elif 'forstart' in item:
            dotpy += addindent("for " + str(item[1]) + " in range(" +str(item[2]) +" ," +str(item[3]) +"):\n")
            indent += 1
        elif ('forend' in item) or ("ifend" in item) or ("elseend" in item) or ("elifend" in item):
            indent -= 1
        elif('defend' in item) :
            indent -= 1
            dotpy += "\n"

        elif "print" in item:
            dotpy += addindent("print(" + str(item[1]) + ")\n")

        elif "#" in item:
            dotpy += addindent("#" + str(item[1]) + "\n")
        elif 'defstart' in item:
            dotpy += "\n" + addindent("def " + str(item[1]) + "(")
            for loop in item[2:]:
                if loop != "defstart":
                    dotpy += str(loop) + ","
            dotpy = dotpy.rstrip(",")
            dotpy += "):\n"
            indent += 1
        elif ("pythonstart" not in item ) and ("pythonend" not in item ) and ("defstart" not in item ):
            if len(item) > 1:
                dotpy += addindent(str(item[0]))
                for loop in item[1:]:
                    dotpy += str(loop) + ","
                dotpy = dotpy.rstrip(",")
                dotpy +="\n"

        print
        print "dotpy.y\n\n",dotpy
        print




    with open("dotpy.py","w") as dotpyfile:
        print>>dotpyfile, dotpy

