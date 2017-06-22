"""

"""

def min_heap_push(heap, item, cost):
    """
    Inserts an item into the heap
    and reheapifies according to min cost
    :param heap: The list of items
    :param item: The item to insert
    :param cost: The item priority
    :return: None
    """
    heap.append((cost, item))
    min_heap(heap)

def min_heap_pop(heap):
    """
    Pops an item from the heap
    and reheapifies according to
    min cost
    :param heap: The list to pop an item from
    :return: None
    """
    last_item = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = last_item
        min_heap(heap)
        return returnitem
    return last_item

def min_heap(heap):
    """
    Creates a min heap given a list of items with their priorities.
    :param heap: The list to "heapify"
    :return: None
    """
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
    """
    Pushes an item into the list and reheapifies that list
    :param heap: The list of items
    :param item: The item to insert
    :param cost: The item priority
    :return: None
    """
    heap.append((cost, item))
    max_heap(heap)

def max_heap_pop(heap):
    """
    Pops an item from the list and reheapifies that list
    :param heap: The list of items
    :return: None
    """
    last_item = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = last_item
        max_heap(heap)
        return returnitem
    return last_item


def max_heap(heap):
    """
    Creates a max heap given a list of items with their priorities.
    :param heap: The list of items
    :return: None
    """
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


