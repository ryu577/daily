import numpy as np


def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def check(arr):
    if arr[0] == 2 and arr[1] == 3 and arr[2] == 1:
        return True
    return False


class Perms():
    def __init__(self):
        self.recurse = True

    def gen_perms(self, arr, ix=0):
        if not self.recurse:
            return
        if ix == len(arr)-1:
            if check(arr):
                self.recurse = False
            print(arr)
            return
        for i in range(ix, len(arr)):
            swap(arr, i, ix)
            self.gen_perms(arr, ix+1)
            swap(arr, i, ix)


if __name__ == "__main__":
    p1 = Perms()
    p1.gen_perms([1, 2, 3])
