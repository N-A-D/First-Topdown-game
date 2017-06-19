def min_heap_push(heap, item, cost):
    heap.append((cost, item))
    min_heap(heap)

def min_heap_pop(heap):
    last_item = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = last_item
        min_heap(heap)
        return returnitem
    return last_item

def min_heap(heap):
    n = len(heap)
    for idx in range(n // 2, 0, -1):
        key = idx
        current = heap[key - 1]
        while True and (2 * key) <= n:
            child = 2 * key
            if child < n:
                if heap[child - 1][0] > heap[child][0]:
                    child += 1
            if current[0] < heap[child - 1][0]:
                break
            else:
                heap[key - 1] = heap[child - 1]
                key = child
        heap[key - 1] = current

def max_heap_push(heap, item, cost):
    heap.append((cost, item))
    max_heap(heap)

def max_heap_pop(heap):
    last_item = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = last_item
        max_heap(heap)
        return returnitem
    return last_item


def max_heap(heap):
    n = len(heap)
    for idx in range(n // 2, 0, -1):
        key = idx
        current = heap[key - 1]
        is_heap = False
        while not is_heap and (2 * key) <= n:
            child = 2 * key
            if child < n:
                if heap[child - 1][0] < heap[child][0]:
                    child += 1
            if current[0] >= heap[child - 1][0]:
                is_heap = True
            else:
                heap[key - 1] = heap[child - 1]
                key = child
        heap[key - 1] = current


