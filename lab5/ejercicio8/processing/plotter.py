import matplotlib.pyplot as plt

def printResultsPlot(axis, iterations):
    (x_axis, y_axis) = axis
    plt.plot(x_axis, y_axis, 'ro')
    plt.axis([0, iterations - 1, -2, 2])
    plt.show()

def generateErrorSublist(iterations):
    if iterations <= 10:
        return list(range(0, iterations))
    elif iterations <= 100:
        return list(range(0, iterations, 10))
    else:
        return list(range(0, iterations, 100))

def printErrorPlot(plots, iterations):
    sublist = generateErrorSublist(iterations)
    sublistPlots = [x for x in plots if plots.index(x) in sublist]
    fig, ax = plt.subplots()
    for pairs in sublistPlots:
        (x_axis, y_axis) = pairs
        ax.plot(x_axis, y_axis, label="Iter " + str(sublistPlots.index(pairs)))
    ax.legend()

    plt.show()