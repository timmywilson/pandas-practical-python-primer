"""
Each new term in the Fibonacci sequence is generated by adding the previous
two terms. By starting with 1 and 2, the first 10 terms will be:

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

By considering the terms in the Fibonacci sequence whose values do not
exceed four million, find the sum of the even-valued terms.
"""


# Brute Force, with Generators and In-Place Multiple Variable Reassignment
def fibonacci(max_number):
    current_number = 1
    last_number = 0

    while current_number <= max_number:
        last_number, current_number = (current_number,
                                       current_number + last_number)

        if not current_number % 2:
            yield current_number


print(sum(fibonacci(4000000)))

# Dummy Line for Commit


# if __name__ == '__main__':
#     import timeit
#     print(timeit.repeat("sum(fibonacci(4000000))",
#                         setup="from __main__ import fibonacci",
#                         number=1000, repeat=3))
#
