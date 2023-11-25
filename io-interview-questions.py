test_case_1 = [12, 23, 30, 40]
test_case_2 = [1, 2, 3, 4]
test_case_3 = [0, 2, 3, 4]

def solve(arr: list) -> list:
    product = 1
    zeros = 0

    for num in arr:
        if num != 0:
            product *= num
        else:
            zeros += 1

    if zeros > 1:
        return [0 for _ in arr]
    elif zeros == 1:
        return [(0 if num != 0 else product) for num in arr]
    else:
        return [(int(product / num) if num != 0 else product) for num in arr]

j = 331200

assert solve(test_case_1) == [j/12, j/23, j/30, j/40]
assert solve(test_case_2) == [24, 12, 8, 6]
assert solve(test_case_3) == [24, 0, 0, 0]