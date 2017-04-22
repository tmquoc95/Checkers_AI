import random
import csv

def create_random_training_data(file, num_player):
    upper_bound = [40,      80,    15,     30,     30,      1.5]
    lower_bound = [15,      25,     0,     0,      0,       0]

    dataset =[[random.uniform(lower_bound[j], upper_bound[j]) for j in range(len(upper_bound))] for i in range(num_player)]

    writer = csv.writer(file)
    writer.writerows(dataset)

def create_defined_training_data (file):

    numberOfStep = [None, None, None, None, 6, 6, None, None]
    upper_bound = [None, None, None, None, 2, 2, None, None]
    lower_bound = [None, None, None, None, 0, 0, None, None]
    step = [(upper_bound[i] - lower_bound[i]) / numberOfStep[i] if (lower_bound[i] is not None) else None for i in range(len(lower_bound))]

    # print (step)

    dataset = []
    counter = [0 if i else None for i in numberOfStep]
    data = step[:]

    def foo(value, counter, condition):
        if value == len(condition):
            return -1

        result = foo(value + 1, counter, condition)

        if counter[value] is not None:
            if result == -1:
                dataset.append(data[:])

            counter[value] = counter[value] + 1
            data[value] = data[value] + step[value]

            if counter[value] < condition[value]:
                result = foo(value, counter, condition)
                return result
            else:
                counter[value] = 0
                data[value] = step[value]
                return 0
        else:
            return result


    foo(0, counter, numberOfStep )
    writer = csv.writer(file)
    writer.writerows(dataset)


if __name__ == "__main__":
    file = open('train_data/test_param_0.csv', 'w+', newline='')
    # random.seed(1211)
    # random.seed(1995)
    # random.seed(1909)
    # random.seed(3268)
    # random.seed(1234)create_defined_training_data
    random.seed(4321)
    # create_random_training_data(file, 4)

    create_defined_training_data(file)