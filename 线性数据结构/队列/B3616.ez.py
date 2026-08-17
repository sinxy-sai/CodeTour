import sys

def main():
    n = int(sys.stdin.buffer.readline())

    queue = []
    head = 0
    out = []

    for _ in range(n):
        op = sys.stdin.buffer.readline().strip().split()

        if op[0] == b'1':
            queue.append(int(op[1]))

        elif op[0] == b'2':
            if head == len(queue):
                out.append('ERR_CANNOT_POP')
            else:
                head += 1

        elif op[0] == b'3':
            if head == len(queue):
                out.append('ERR_CANNOT_QUERY')
            else:
                out.append(str(queue[head]))
            
        elif op[0] == b'4':
            out.append(str(len(queue)-head))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()