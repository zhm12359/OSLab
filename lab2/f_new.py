import re
from Process import Process

import sys

orig_stdout = sys.stdout
f = file('out.txt', 'w')
sys.stdout = f





##

def randomOS(U):
    n = random_list[0]
    print("Find burst when choosing ready process to run " + str(n))
    del random_list[0]
    return 1 + (n % U)

file_name = "input4.txt"
#set up random number list
f = open("random-numbers.txt", "r")
random_list = f.read().split("\n")
random_list = [int(x) for x in random_list if x.isdigit() ]
f.close()

#get the processes from the input file
pattern = r"\(\d+\s\d+\s\d+\s\d+\)"
f = open(file_name,"r")
data = f.read()

f.close()
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

    output = "Before cycle\t"+str(cycle)+":"
    for p in process_list:
        if p in ready:
            output += "\tready\t0"
        elif p in running:
            output += "\trunning\t" + str(p.cpuBurst)
            CPUuse += 1
        elif p in blocked:
            IOuse += 1
            output += "\tblocked\t" + str(p.IOBurst)
        elif p in finished:
            output += "   terminated 0"
        else:
            output += "     unstarted 0"
    output += "."
    print(output)

    #sort the blocked according to the appearance order in the sorted
    blocked = [p for p in process_list if p in blocked]
    i = 0
    while i < len(blocked):
        p = blocked[i]
        p.IOBurst -= 1
        p.IOTime += 1
        if p.IOBurst == 0:
            del blocked[i]
            #p.cpuBurst = randomOS(x.B)
            #p.IOBurst = p.cpuBurst * p.M
            ready.append(p)
            # if cycle == 262 or cycle==261:
            #     print("\n\n\n\n\n\n")
            #     for r in ready:
            #         print(r.toString)
        else:
            i = i+1

    #check if anything gets ready
    ready.extend([x for x in process_list if x.A == cycle and x not in ready])
    # for x in process_list:
    #     if x.A == cycle and x not in ready:
    #         x.cpuBurst = randomOS(x.B)
    #         x.IOBurst = x.cpuBurst * x.M
    #         ready.append(x)

    #everything is either unstarted or blocked
    if not ready and not running:
        cycle += 1
        continue
    # if nothing is running
    if not running:
        running.append(ready.pop(0))
        current = running[0]
        current.cpuBurst = randomOS(current.B)
        current.IOBurst = (current.cpuBurst) * current.M
    else:
        current = running[0]
        # if not current.cpuBurst:
        #     current.cpuBurst = randomOS(current.B)
        #     current.IOBurst = (current.cpuBurst) * current.M
        current.cpuBurst -= 1
        current.remainingTime -= 1

        if current.remainingTime == 0:
            current.finishTime = cycle
            current.turnAroundTime = cycle - current.A

            finished.append(current)
            running.pop()
            if ready:
                new =  ready.pop(0)
                new.cpuBurst = randomOS(new.B)
                new.IOBurst = (new.cpuBurst) * new.M
                running.append(new)

        elif current.cpuBurst == 0:
            blocked.append(current)
            running.pop()
            if ready:
                new =  ready.pop(0)
                new.cpuBurst = randomOS(new.B)
                new.IOBurst = (new.cpuBurst) * new.M
                running.append(new)

    for p in ready:
        p.waitingTime += 1
    cycle += 1
print("The scheduling algorithm used was First Come First Served\n")
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
sys.stdout = orig_stdout
f.close()
