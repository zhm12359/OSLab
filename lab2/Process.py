class Process:
    def __init__(self, string=None):
        ABCM = self.parse(string)
        self.A = ABCM[0]
        self.B = ABCM[1]
        self.C = ABCM[2]
        self.M = ABCM[3]
        self.cpuBurst = None
        self.IOBurst = None
        self.finishTime = None
        self.turnAroundTime = None
        self.waitingTime = 0
        self.IOTime = 0
        self.remainingTime = self.C
        self.quantum = 2
        self.toString = "(" + ",".join(ABCM) + ")"

    def parse(self, string):
        p = string.replace("(","").replace(")","")
        abcm = p.split(" ")
        return abcm
