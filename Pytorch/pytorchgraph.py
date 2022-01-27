
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

model_name = 'model-1570822042'

def create_acc_loss_graph(model_name):
    contents = open('model.log', 'r').read().split('\n')

    times= []
    accuracies = []
    loss = []
    val_accs = []
    val_losses = []

    for c in contents:
        if model_name in c:
            name, timestamp, acc, loss, val_acc, val_loss = c.split(',')


