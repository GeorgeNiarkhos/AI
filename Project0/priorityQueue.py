import heapq

class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        heapq.heappush(self.heap, [priority, item])
        self.count = self.count + 1

    def isEmpty(self):
        if self.count:
            return False
        else:
            return True

    def pop(self):
        if self.isEmpty():
            print ('PriorityQueue is Empty')
            return None
        else:
            self.count = self.count - 1
            item = heapq.heappop(self.heap)
            return item[1]
    
    def update(self, item, priority):
        flag = 1
        for i  in self.heap:
            if (item == i[1]):
                flag = 0
                if(priority < i[0]):
                    i[0] = priority     # MESSING WITH HEAPLIKE FORM
                    flag = 0
        heapq.heapify(self.heap)        # CALL HEAPIFY TO ACHIEVE HEAPLIKE FORM
        if (flag):
            self.push(item, priority)

def PQSort(intList):
    q = PriorityQueue()
    sortedList = []
    for i in intList:
        q.push(str(i), i)              # PUSH ALL NUMBERS WITH i PRIORITY AND "i" AS ITEM
    for i in range(len(intList)):
        number = q.pop()
        sortedList.append(int(number))  # POP THEM ALL APPEND AS INT
    return sortedList

if __name__ == '__main__':
    intList = [4,3,5,6,2,1]
                                        #HARDCODED EXAMPLE
    result = PQSort(intList)

    print(result)
