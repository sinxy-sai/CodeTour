import sys

def main():
    N = int(sys.stdin.readline())

    s = set()

    for _ in range(N):
        s.add(sys.stdin.readline().strip())

    sys.stdout.write(str(len(s)))

if __name__ == '__main__':
    main()
