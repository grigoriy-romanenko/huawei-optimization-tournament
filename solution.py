import sys

NUM_NODES = 10
NUM_TYPES = 3
MAX_BATCH_SIZE = 16
MAX_NUM_PACKETS = 100000

class Packet:
    def __init__(self):
        self.type = 0
        self.arriveTime = 0
        self.t = 0

packets = [Packet() for _ in range(MAX_NUM_PACKETS)]
cost = [[[0] * (MAX_BATCH_SIZE + 1) for _ in range(NUM_TYPES + 1)] for _ in range(NUM_NODES + 1)]
batchLimit = [[0] * (NUM_TYPES + 1) for _ in range(NUM_NODES + 1)]
ids = [[] for _ in range(NUM_NODES + 1)]
c4, c6, cr = 0, 0, 0
n, curTime, nout, queueTime = 0, 1, 0, 0

nextNode = {
    (1, 1): 2,
    (2, 1): 3,
    (3, 1): 4,
    (4, 1): 5,
    (5, 1): 6,
    (6, 1): 7,
    (7, 1): 8,
    (8, 1): 9,
    (9, 1): 10,
    (1, 2): 2,
    (2, 2): 3,
    (3, 2): 8,
    (8, 2): 9,
    (9, 2): 10,
    (1, 3): 2,
    (2, 3): 9,
    (9, 3): 10
}

def ReceivePackets(t):
    global curTime
    curTime = t + cr
    print(f"R {t}")
    sys.stdout.flush()
    p = int(input())
    if p == -1:
        sys.exit(0)

    for _ in range(p):
        id, type, a = map(int, input().split())
        packets[id].type = type
        packets[id].arriveTime = a
        packets[id].t = curTime
        ids[1].append(id)

def ExecuteTask(nodeId, arr, t):
    global curTime, queueTime, nout
    b = len(arr)
    type = packets[arr[0]].type
    print(f"E {t} {nodeId} {b} {' '.join(map(str, arr))}")
    sys.stdout.flush()

    p = int(input())
    if p == -1:
        sys.exit(0)

    curCost = cost[nodeId][type][b]
    curTime = t + curCost

    for i in arr:
        packets[i].t = curTime

    if (nodeId, type) in nextNode:
        nextNodeId = nextNode[(nodeId, type)]
        for i in arr:
            ids[nextNodeId].append(i)

    if nodeId == NUM_NODES:
        nout += b
        if nout == n:
            sys.exit(0)

    if nodeId == 4 or nodeId == 6:
        for i in arr:
            packets[i].t = max(curTime, queueTime) + (c4 if nodeId == 4 else c6)
            queueTime = packets[i].t

def TakeSinglePacket(i):
    arr = [ids[i][0]]
    ids[i].pop(0)
    ExecuteTask(i, arr, curTime)

def main():
    global c4, c6, cr, n
    for _ in range(20):
        line = list(map(int, input().split()))
        i, j, b = line[:3]
        batchLimit[i][j] = b
        for k in range(1, b + 1):
            cost[i][j][k] = line[3 + k - 1]

    c4, c6, cr = map(int, input().split())
    n = int(input())

    while True:
        any_packet = False
        for i in range(1, NUM_NODES + 1):
            if ids[i] and packets[ids[i][0]].t <= curTime:
                any_packet = True
                TakeSinglePacket(i)
        if any_packet:
            continue
        ReceivePackets(curTime)

if __name__ == "__main__":
    main()
