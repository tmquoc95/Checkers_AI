import random
import csv

def create_train_data(file, num_player):
    upper_bound = [40,      80,    15,     30,     30,      1.5]
    lower_bound = [15,      25,     0,     0,      0,       0]

    dataset =[[random.uniform(lower_bound[j], upper_bound[j]) for j in range(len(upper_bound))] for i in range(num_player)]

    writer = csv.writer(file)
    writer.writerows(dataset)

if __name__ == "__main__":
    file = open('train_data/test_param_0.csv', 'w+', newline='')
    # random.seed(1211)
    # random.seed(1995)
    # random.seed(1909)
    # random.seed(3268)
    # random.seed(1234)
    random.seed(4321)
    create_train_data(file, 4)