import os
import sys

#object module class
class object_module(object):
    def __init__(self, definition_list = None, use_list = None, program_text = None):
        self.definition_list = definition_list
        self.use_list = use_list
        self.program_text = program_text

    def get_definition_list(self):
        return self.definition_list

    def get_use_list(self):
        return self.use_list

    def get_program_text(self):
        return self.program_text

def first_pass(data):

    lines = data.strip().split("\n")
    obj_count = int(lines[0])

    del lines[0]

    # make the data into a list of lists
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip().split(" ")
        lines[i] = [x for x in lines[i] if x]

    obj_list = []

    relative_address = 0
    for i in range(0, obj_count):

        #get definition_list
        if lines[0][0] == 0:
            definition_list = [0]
        else:
            def_count = int(lines[0][0])

            if(len(lines[0])>def_count+1):
                merge = lines[0] + lines[1]
                lines[0] = merge[0:def_count+1]
                lines[1] = merge[def_count+1:]

            #loop until we have enough entries for this line
            while len(lines[0]) < 2 * def_count + 1:
                lines[0] += [lines[1][0]]
                del lines[1][0]
                if not lines[1]: del lines[1]

        definition_list = lines[0]
        del lines[0]

        #print definition_list

        if lines[0][0] == 0:
            use_list = [0]
        else:
            use_count = int(lines[0][0])

            if(len(lines[0])>use_count+1):
                merge = lines[0] + lines[1]
                lines[0] = merge[0:use_count+1]
                lines[1] = merge[use_count+1:]

            while len(lines[0]) <  use_count + 1:
                lines[0] += [lines[1][0]]
                del lines[1][0]
                if not lines[1]: del lines[1]

        use_list = lines[0]
        del lines[0]

        #print use_list

        #get symbols
        for i in range(1,len(definition_list),2):
            if definition_list[i] not in symbols:
                symbols[definition_list[i]] = int(definition_list[i+1]) + relative_address
            else:
                print "Error: symbol %s is multiply defined; first value used." %  definition_list[i]

        #get program text
        if lines[0][0] == 0:
            program_text = [0]
        else:
            text_count = int(lines[0][0])
            relative_address += text_count

            if(len(lines[0])>text_count+1):
                merge = lines[0] + lines[1]
                lines[0] = merge[0:text_count+1]
                lines[1] = merge[text_count+1:]

            while len(lines[0]) <  text_count + 1:
                lines[0] += [lines[1][0]]
                del lines[1][0]
                if not lines[1]: del lines[1]

        program_text = lines[0]
        del lines[0]

        #check if deinition address exceed the size of the module
        for d in range(2,len(definition_list),2):
            if int(definition_list[d]) > int(program_text[0]):
                print(definition_list)
                print("Error:" + definition_list[d-1] + " has an address greater than the size of module %d" %i)
                definition_list[d] = 0

        #print(program_text)
        module = object_module(definition_list, use_list, program_text)
        obj_list.append(module)

    return obj_list

def second_pass(symbols, obj_list):
    relative_address = 0
    print("Memory Map")
    counter = 0
    symbols_used = []
    for ob in obj_list:
        for i in range(1,len(ob.program_text)):
            text = ob.program_text[i]
            if text[-1] == "1":
                result = text[0:4] #if int(text[1:4])<600 else text[0]+"000"+ "\tError: Absolute address exceeds machine size; zero used."
            elif text[-1] == "2":
                result = text[0:4] if int(text[1:4])<600 else text[0]+"000"+ "\tError: Absolute address exceeds machine size; zero used."
            elif text[-1] == "3":
                result =  str(int(text[0:4]) + relative_address)
                result = result if int(result[1:])<600 else result[0]+"000" + "\tError: Absolute address exceeds machine size; zero used."
                result = result if int(text[1:4])<= int(ob.program_text[0]) else result[0]+"000" + "\tError: Relative address exceeds module size zero used."
            elif text[-1] == "4":
                use_list = ob.use_list
                index = int(text[1:4]) + 1
                try:
                    symbol = use_list[index]
                    symbols_used.append(symbol)
                    symbol_value = symbols[symbol] if symbol in symbols else 0
                    result = str(int(text[0])*1000 + symbol_value)
                    result = result if int(result[1:])<600 else result[0]+"000" + "\tError: Absolute address exceeds machine size; zero used."
                    if symbol not in symbols:
                        result = str(int(text[0])*1000) + "\tError: "+ str(symbol) +" is not defined; zero used."
                except IndexError:
                    result = text[0:4] + "\tError: External address exceeds length of use list; treated as immediate."
            print str(counter)+":"+"\t" + result
            counter +=1
        relative_address += int(ob.program_text[0])

    #unused_symbols
    unused_symbols = list(set(symbols.keys()) - set(symbols_used))
    for s in unused_symbols:
        merge_definition_list = []

        for k in range(0,len(obj_list)):
            merge_definition_list += obj_list[k].definition_list

            if(s in obj_list[k].use_list):
                print("Warning: In module %d "%k +s+" is on use list but isn't used" )
                break
            elif (s in obj_list[k].definition_list):
                print("Warning: " + s + " was defined in module %d but never used." %k)
                break


if len(sys.argv) != 2:
    print("Error: Wrong Input. Usage: python linker.py <fileDirectory>")
else:
    input_file = sys.argv[1]


    #file read
    try:
        f_object = open(input_file,"r")
    except Exception, e:
        print e
        print "Error: Cannot open file. Please re-run this program and enter correct file name"

    all_data = f_object.read()
    f_object.close()

    #get rid empty line breaks
    cleaned_data = os.linesep.join([s for s in all_data.splitlines() if s]).strip()

    symbols = {}
    print("Symbol table: ")
    result = first_pass(cleaned_data)
    print(symbols)
    second_pass(symbols, result)
