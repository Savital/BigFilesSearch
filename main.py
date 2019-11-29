from random import randint
from heapq import merge
from itertools import count, islice
from contextlib import ExitStack

max_length = 5


def binary_search(lst, x):
    lst.sort()
    p = 0
    r = len(lst) - 1
    answer = False
    while p <= r:
        q = (p + r) // 2
        if lst[q] == x:
            answer = True
            break
        elif lst[q] > x:
            r = q - 1
        elif lst[q] < x:
            p = q + 1

    return answer


def find_start(fp, pos):
    start = pos
    fp.seek(start, 0)
    line = fp.read(1)
    while start != 0 and line != "\n":
        start -= 1
        fp.seek(start, 0)
        line = fp.read(1)

    return start + 1


def binary_search_file(filename, search_x):
    x = int(search_x)
    fp = open(filename)
    fp.seek(0, 2)
    begin = 0
    end = fp.tell()
    answer = False

    old_pos = 0
    while begin < end:
        pos = (end + begin) // 2

        if pos == old_pos:
            break

        start = find_start(fp, pos)
        fp.seek(start, 0)
        line = fp.readline().strip()
        if line == "":
            break
        line_key = int(line)

        if x == line_key:
            answer = True
            break
        elif x > line_key:
            begin = start
        else:
            end = start

        length = len(line)
        print(length)
        old_pos = pos

    return answer


def generate_file(filename):
    with open(filename, 'w') as result:
        for i in range(1, 10):
            d = randint(0, 10000)
            print('{}'.format(d), file=result)


def read_file(filename):
    with open(filename, "r") as result:
        for line in result:
            print(line.strip())


def sort_big_file(filename):
    chunk_names = []

    with open(filename) as input_file:
        for chunk_number in count(1):
            sorted_chunk = sorted(islice(input_file, max_length))
            if not sorted_chunk:
                break

            chunk_name = 'chunk_{}.chk'.format(chunk_number)
            chunk_names.append(chunk_name)
            with open(chunk_name, 'w') as chunk_file:
                chunk_file.writelines(sorted_chunk)

    with ExitStack() as stack, open('searched_file_sorted.txt', 'w') as output_file:
        files = [stack.enter_context(open(chunk)) for chunk in chunk_names]
        output_file.writelines(merge(*files))


# direct variant (simple)
def file_intersection(filename1, filename2):
    with open("result", 'w') as result:
        with open(filename1, "r") as origin:
            for line in origin:
                origin_num = int(line.strip())
                with open(filename2, "r") as searched_file:
                    for ptr_line in searched_file:
                        print(origin_num, "vs", ptr_line)
                        if origin_num == int(ptr_line.strip()):
                            result.write(ptr_line)
                            print(ptr_line)


# for not big data
def file_intersection_binary_simple(filename1, filename2):
    with open("result", 'w') as result:
        with open(filename1, "r") as origin:
            lst_origin = origin.readlines()
        sort_big_file(filename2)
        with open("searched_file_sorted.txt", "r") as searched_file_sorted:
            lst_searched = searched_file_sorted.readlines()
        for elem in lst_origin:
            if binary_search(lst_searched, elem):
                result.write(elem)


# for big data
def file_intersection_binary(filename1, filename2):
    sort_big_file(filename2)
    with open("result", 'w') as result:
        with open(filename1, "r") as origin:
            for line in origin:
                origin_num = int(line.strip())
                if binary_search_file("searched_file_sorted.txt", origin_num):
                    result.write(line)

def main():
    #generate_file("file1")
    #generate_file("file2")
    #read_file("file1")
    #read_file("file2")
    #sort_big_file("file2")
    #file_intersection("file1", "file2")
    #file_intersection_binary_simple("file1", "file2")
    file_intersection_binary("file1", "file2")


if __name__ == "__main__":
    main()
