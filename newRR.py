import re
from Process import Process

import sys

# orig_stdout = sys.stdout
# f = file('out.txt', 'w')
# sys.stdout = f

def randomOS(U):
    n = random_list[0]
    print("Find burst when choosing ready process to run " + str(n))
    del random_list[0]
    return 1 + (n % U)

if len(sys.argv) not in [2,3]:
    print "Wrong Usage. Should be: python FCFS.py (--verbose) <file_name>"
    sys.exit(0)
elif sys.argv[1] == "--verbose":
    verbose = True
    try:
        file_name = sys.argv[2]
    except:
        print "Wrong Usage. Should be: python FCFS.py (--verbose) <file_name>"
        sys.exit(0)
else:
    verbose = False
    file_name = sys.argv[1]


#set up random number list
f = open("random-numbers", "r")
random_list = f.read().split("\n")
random_list = [int(x) for x in random_list if x.isdigit() ]
f.close()

#get the processes from the input file
pattern = r"\(\d+\s\d+\s\d+\s\d+\)"
try:
    f = open(file_name,"r")
    data = f.read()
    f.close()
except Exception, e:
    print e
    print "Error: Cannot open file. Please re-run this program and enter correct file name"
    sys.exit(0)



processes = re.findall(pattern, data)
process_list = [Process(x) for x in processes]
#map fields into ints
unsorted = "The original input was: " + str(len(process_list)) + " "
for p in process_list:
    p.A = int(p.A)
    p.B = int(p.B)
    p.C = int(p.C)
    p.M = int(p.M)
    p.remainingTime =int(p.remainingTime)
    unsorted += (p.toString.replace(",", " ") +" ")

print(unsorted)
#sort by arrival time
process_list.sort(key=lambda x: x.A)
ordered = "The (sorted) input is: " + str(len(process_list)) + "  "
for p in process_list:
    ordered += (p.toString.replace(",", " ") +" ")

print(ordered+"\n")

print("This detailed printout gives the state and remaining burst for each process\n")


total = len(process_list)

cycle = 0
ready = []
running = []
blocked = []
finished = []
current = None
CPUuse = 0
IOuse = 0
while len(finished) != total:

    for p in ready:
        p.waitingTime += 1
    new_ready = []
    if blocked:
        IOuse +=1

    output = "Before cycle\t"+str(cycle)+":"
    for p in process_list:
        if p in ready:
            output += "\tready\t0"
        elif p in running:
            output += "\trunning\t" + str(min(p.quantum, p.cpuBurst))
            CPUuse += 1
        elif p in blocked:
            output += "\tblocked\t" + str(p.IOBurst)
        elif p in finished:
            output += "   terminated 0"
        else:
            output += "     unstarted 0"
    output += "."
    if verbose: print(output)

    #sort the blocked according to the appearance order in the sorted
    blocked = [p for p in process_list if p in blocked]
    i = 0
    while i < len(blocked):
        p = blocked[i]
        p.quantum = 2
        p.IOBurst -= 1
        p.IOTime += 1
        if p.IOBurst == 0:
            del blocked[i]
            new_ready.append(p)
            ready.append(p)
        else:
            i = i+1

    # if nothing is running
    if not running:
        if ready:
            running.append(ready.pop(0))
            current = running[0]
            if not current.cpuBurst:
                current.cpuBurst = randomOS(current.B)
                current.IOBurst = (current.cpuBurst) * current.M
    else:
        current = running[0]
        # if not current.cpuBurst:
        #     current.cpuBurst = randomOS(current.B)
        #     current.IOBurst = (current.cpuBurst) * current.M
        current.quantum -= 1
        current.cpuBurst -= 1
        current.remainingTime -= 1

        if current.remainingTime == 0:
            current.finishTime = cycle
            current.turnAroundTime = cycle - current.A

            finished.append(current)
            running.pop()
            if ready:
                new =  ready.pop(0)
                if not new.cpuBurst:
                    new.cpuBurst = randomOS(new.B)
                    new.IOBurst = (new.cpuBurst) * new.M
                running.append(new)

        elif current.cpuBurst == 0:
            current.quantum = 2
            blocked.append(current)
            running.pop()
            if ready:
                new =  ready.pop(0)
                if not new.cpuBurst:
                    new.cpuBurst = randomOS(new.B)
                    new.IOBurst = (new.cpuBurst) * new.M
                running.append(new)

        elif current.quantum == 0:
            current.quantum = 2
            i = 0
            new_ready.append(current)
            new_ready.sort(key = lambda x: x.A)
            ready.append(current)
            running.pop()

            if ready:
                new =  ready.pop(0)
                if not new.cpuBurst:
                    new.cpuBurst = randomOS(new.B)
                    new.IOBurst = (new.cpuBurst) * new.M
                running.append(new)

    ready.extend([x for x in process_list if x.A == cycle and x not in ready])
    cycle += 1

print("The scheduling algorithm used was Round Robin\n")
totalTurnAround = 0
totalWaiting = 0
for i in range(0,len(process_list)):
    p = process_list[i]
    totalTurnAround += p.turnAroundTime
    totalWaiting += p.waitingTime

    print("Process " + str(i) + ":")
    print("\t\t(A,B,C,M) = " + p.toString)
    print("\t\tFinishing time: "+str(p.finishTime))
    print("\t\tTurnaround time: " + str(p.turnAroundTime))
    print("\t\tI/O time: " + str(p.IOTime))
    print("\t\tWaiting time: " + str(p.waitingTime) +"\n")

print("Summary Data: ")
print("\t\tFinishing time: " + str(cycle-1))
print("\t\tCPU Utilization: " + str(float(CPUuse)/(cycle-1)))
print("\t\tI/O Utilization: " + str(float(IOuse) / (cycle-1) ))
print("\t\tThroughput: " + str(( float(len(process_list)) / (cycle-1) * 100)) + " processes per hundred cycle")
print("\t\tAveratge turnaround time: "+ str( float(totalTurnAround)/len(process_list)))
print("\t\tAveratge waiting time: "+ str( float(totalWaiting)/len(process_list)))

# sys.stdout = orig_stdout
# f.close()
