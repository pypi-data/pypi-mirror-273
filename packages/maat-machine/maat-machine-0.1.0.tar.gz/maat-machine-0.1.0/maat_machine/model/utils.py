from matplotlib import pyplot as plt


def plot_training_history(history):
    plt.plot(history["accuracy"], label="Доля верных ответов на обучающем наборе")
    plt.plot(history["val_accuracy"], label="Доля верных ответов на проверочном наборе")
    plt.xlabel("Эпоха обучения")
    plt.ylabel("Доля верных ответов")
    plt.legend()
    plt.show()

    plt.plot(history["loss"], label="Ошибка на обучающем наборе")
    plt.plot(history["val_loss"], label="Ошибка на проверочном наборе")
    plt.xlabel("Эпоха обучения")
    plt.ylabel("Ошибка")
    plt.legend()
    plt.show()