from collections import deque


def search(start_node, target='Elon Musk'):
    search_queue = deque()
    search_queue += graph[start_node]
    print(search_queue, 111)
    searched = set()
    while search_queue:
        person = search_queue.popleft()
        if person not in searched:
            if person == target:
                return True
            else:
                search_queue += graph[person]
                searched.add(person)
    return False


if __name__ == '__main__':
    graph = {
        "siz": ["olim", "fotima", "nurbek"],
        "Olim": ["AbdulKarim", "Jahongir"],
        "Javlon": ["...", "Jahongir","Elon Musk"]
    }

    print(search('siz', 'Jahongir'))
