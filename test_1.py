# import csv
# param_file = open('output.csv', "r")
#
# # writer = csv.writer(param_file)
# #
# # data = [None, 1, 2]
# # writer.writerow(data)
#
# reader = csv.reader(param_file)
#
# row = next(reader)
#
# row = [float(cell) if cell else None for cell in row ]
# print (row)
#

# condition = [None, None, 2, 2]
#
# counter = [0 if i else None for i in condition]
#
# # print (counter)
#
#
# def foo (value, counter, condition):
#     if value == len(condition):
#         return -1
#
#     result = foo (value + 1, counter, condition)
#
#     if counter[value] != None:
#         if result == -1:
#             print(counter)
#
#         counter[value] = counter[value] + 1
#
#         if counter[value] < condition[value]:
#             result = foo (value, counter, condition)
#             return result
#         else:
#             counter[value] = 0
#             return 0
#     else:
#         return result
#
#
# foo (0, counter, condition)

a = []

b = [1, 2]

a.append(b[:])

b[1] = 3
a.append(b[:])

print (a)