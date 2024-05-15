# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

import matplotlib.pyplot as plt
import matplotlib.figure
from typing import List
import numpy as np
import matplotlib
import io

matplotlib.use('Agg')

def figure2numpy(figure: matplotlib.figure.Figure) -> np.ndarray:
    """
    Converts a matplotlib.figure.Figure into a numpy 
    array so that it can be posted to tensorboard.
    
    Parameters
    ----------
        figure: matplotlib.figure.Figure
            This is the figure to convert to a numpy array.

    Returns
    -------
        figure: np.ndarray
            The figure that is represented as a numpy array.
    """
    io_buf = io.BytesIO()
    figure.savefig(io_buf, format='raw')
    io_buf.seek(0)
    nimage = np.reshape(
        np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
        newshape=(int(figure.bbox.bounds[3]), int(figure.bbox.bounds[2]), -1))
    io_buf.close()
    return nimage

def plot_classification_detection(
        class_histogram_data: dict, 
        model: str="Training Model") -> matplotlib.figure.Figure:
    """
    Plots the bar charts showing the precision, recall, and accuracy per class.
    It also shows the number of true positives, false positives, 
    and false negatives per class.
    
    Parameters
    ----------
        class_histogram_data: dict.
            This contains information about the metrics per class.

            .. code-block:: python

                {
                    'label_1': {
                        'precision': "The calculated precision at 
                                IoU threshold 0.5 for the class",
                        'recall': "The calculated recall at 
                                IoU threshold 0.5 for the class",
                        'accuracy': "The calculated accuracy at 
                                IoU threshold 0.5 for the class",
                        'tp': "The number of true positives for the class",
                        'fn': "The number of false negatives for the class",
                        'fp': "The number of localization and 
                                classification false positives for the class",
                        'gt': "The number of grounds truths for the class"
                    },
                    'label_2': ...
                }

        model: str
            The name of the model.

    Returns
    -------
        fig: matplotlib.pyplot
            This shows two histograms on the left that compares
            the precision, recall, and accuracy and on the right 
            compares the number of true positives, false positives,
            and false negatives for each class.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
    # Score = [[prec c1, prec c2, prec c3], [rec c1, rec c2, rec c3], [acc c1, acc c2, acc c3]]
    X = np.arange(len(class_histogram_data))
    labels, precision, recall, accuracy = list(), list(), list(), list()
    tp, fp, fn = list(), list(), list()

    for cls, value, in class_histogram_data.items():
        labels.append(cls)
        precision.append(round(value.get('precision') * 100, 2))
        recall.append(round(value.get('recall') * 100, 2))
        accuracy.append(round(value.get('accuracy') * 100, 2))
        tp.append(value.get('tp'))
        fn.append(value.get('fn'))
        fp.append(value.get('fp'))

    ax1.bar(X + 0.0, precision, color='m', width=0.25)
    ax1.bar(X + 0.25, recall, color='y', width=0.25)
    ax1.bar(X + 0.5, accuracy, color='c', width=0.25)

    ax2.bar(X + 0.0, tp, color='LimeGreen', width=0.25)
    ax2.bar(X + 0.25, fn, color='RoyalBlue', width=0.25)
    ax2.bar(X + 0.5, fp, color='OrangeRed', width=0.25)

    ax1.set_ylim(0, 100)

    ax1.set_ylabel('Score (%)')
    ax2.set_ylabel("Total Number")
    fig.suptitle(f"{model} Evaluation Table")

    ax1.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')
    ax2.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')

    colors = {'precision': 'm', 'recall': 'y', 'accuracy': 'c'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
                for label in labels]
    ax1.legend(handles, labels)
    colors = {'true positives': 'green',
              'false negatives': 'blue',
              'false positives': 'red'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
                for label in labels]
    ax2.legend(handles, labels)
    return fig

def plot_classification_segmentation(
        class_histogram_data: dict, 
        model: str="Training Model"
    ) -> matplotlib.figure.Figure:
    """
    Plots the bar charts showing the precision, recall, and accuracy per class.
    It also shows the number of true predictions and 
    false predictions per class.
    
    Parameters
    ----------
        class_histogram_data: dict.
            This contains information about the metrics per class.

            .. code-block:: python

                {
                    'label_1': {
                        'precision': "The calculated precision for the class",
                        'recall': "The calculated recall for the class",
                        'accuracy': "The calculated accuracy for the class",
                        'true_predictions': "The number of true prediction
                                            pixels of the class",
                        'false_predictions': "The number of false prediction
                                            pixels of the class",              
                        'gt': "The number of grounds truths for the class"
                    },
                    'label_2': ...
                }

        model: str
            The name of the model.

    Returns
    -------
        fig: matplotlib.pyplot
            This shows two histograms on the left that compares
            the precision, recall, and accuracy and on the right 
            compares the number of true prediction and 
            false prediction pixels for each class.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
    # Score = [[prec c1, prec c2, prec c3], [rec c1, rec c2, rec c3], [acc c1, acc c2, acc c3]]
    X = np.arange(len(class_histogram_data))
    labels, precision, recall, accuracy = list(), list(), list(), list()
    true_predictions, false_predictions = list(), list()

    for cls, value, in class_histogram_data.items():
        labels.append(cls)
        precision.append(round(value.get('precision') * 100, 2))
        recall.append(round(value.get('recall') * 100, 2))
        accuracy.append(round(value.get('accuracy') * 100, 2))
        true_predictions.append(value.get('true_predictions'))
        false_predictions.append(value.get('false_predictions'))

    ax1.bar(X + 0.0, precision, color='m', width=0.25)
    ax1.bar(X + 0.25, recall, color='y', width=0.25)
    ax1.bar(X + 0.5, accuracy, color='c', width=0.25)

    ax2.bar(X + 0.0, true_predictions, color='LimeGreen', width=0.25)
    ax2.bar(X + 0.25, false_predictions, color='OrangeRed', width=0.25)

    ax1.set_ylim(0, 100)

    ax1.set_ylabel('Score (%)')
    ax2.set_ylabel("Total Number")
    fig.suptitle(f"{model} Evaluation Table")

    ax1.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')
    ax2.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')

    colors = {'precision': 'm', 'recall': 'y', 'accuracy': 'c'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) 
               for label in labels]
    ax1.legend(handles, labels)
    colors = {'true predictions': 'green',
              'false predictions': 'red'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
                for label in labels]
    ax2.legend(handles, labels)
    return fig

def plot_pr(
        precision: np.ndarray, 
        recall: np.ndarray, 
        ap: np.ndarray, 
        names: list=[], 
        model: str="Training model",
        iou_threshold: float=0.50
    ) -> matplotlib.figure.Figure:
    """
    Version 1 Ploting precision and recall per class and the average metric.
    Use this method for deepview-validator implementation of precision recall
    curve.

    Parameters
    ----------
        precision: (NxM) np.ndarray
            N => number of classes and M is the number of precision values.
        
        recall: (NxM) np.ndarray
            N => number of classes and M is the number of recall values.

        ap: (NxM) np.ndarray
            N => number of classes, M => 10 denoting each IoU threshold
            from (0.5 to 0.95 at 0.05 intervals).

        names: list
            This contains the unique string labels captured in the order
            that respects the data for precision and recall.

        model: str
            The name of the model evaluated.

        iou_threshold: float
            The iou threshold used for the mAP calculation.

    Returns
    -------
        fig: matplotlib.pyplot
            The precision recall plot where recall is denoted
            on the x-axis and precision is denoted
            on the y-axis.
    """
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)
    if 0 < len(names) < 21:  # display per-class legend if < 21 classes
        for i, (p, r) in enumerate(zip(precision, recall)):
            # plot(recall, precision)
            ax.plot(r, p, linewidth=1, label=f'{names[i]} {ap[i, 0]:.3f}')
    else:
        # plot(recall, precision)
        for prec, rec in zip(precision, recall):
            ax.plot(rec, prec, linewidth=1, color='grey')

    ax.plot(
        np.mean(recall, axis=0),
        np.mean(precision, axis=0),
        linewidth=3,
        color='blue',
        label='all classes %.3f mAP@%.2f' % (ap[:, 0].mean(), iou_threshold))

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    ax.set_title(f'{model} Precision-Recall Curve')
    return fig

def plot_pr_curve( #NOSONAR
    precision: np.ndarray, 
    recall: np.ndarray, 
    ap: np.ndarray, 
    names: list=[], 
    model: str="Training model",
    iou_threshold: float=0.50
) -> matplotlib.figure.Figure:
    """
    Version 2 Ploting precision and recall per class and the average metric.
    Use this method for YoloV5 implementation of precision recall
    curve.

    Parameters
    ----------
        precision: (NxM) np.ndarray
            N => number of classes and M is the number of precision values.
        
        recall: (NxM) np.ndarray
            N => number of classes and M is the number of recall values.

        ap: (NxM) np.ndarray
            N => number of classes, M => 10 denoting each IoU threshold
            from (0.5 to 0.95 at 0.05 intervals).

        names: list
            This contains the unique string labels captured in the order
            that respects the data for precision and recall.

        model: str
            The name of the model evaluated.

        iou_threshold: float
            The iou threshold used for the mAP calculation.

    Returns
    -------
        fig: matplotlib.pyplot
            The precision recall plot where recall is denoted
            on the x-axis and precision is denoted
            on the y-axis.
    """
    # Precision-recall curve
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)
    if len(precision) == 0:
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        ax.set_title(f'{model} Precision-Recall Curve')
        return fig
    
    precision = np.stack(precision, axis=1)
    if (0 < len(names) < 21):  # display per-class legend if < 21 classes
        for i, y in enumerate(precision.T):
            ax.plot(recall, y, linewidth=1, label=f"{names[i]} {ap[i, 0]:.3f}")  # plot(recall, precision)
    else:
        ax.plot(recall, precision, linewidth=1, color="grey")  # plot(recall, precision)

    ax.plot(
        recall, 
        precision.mean(1), 
        linewidth=3, 
        color="blue", 
        label="all classes %.3f mAP@%.2f" % (ap[:, 0].mean(), iou_threshold))
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    ax.set_title(f'{model} Precision-Recall Curve')
    return fig

def plot_confusion_matrix(
        confusion_data: np.ndarray, 
        labels: list, 
        model: str="Training Model"
    ) -> matplotlib.figure.Figure:
    """
    Plots the confusion matrix using the method defined below:
    https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python/74152927#74152927

    Parameters
    ----------
        confusion_data: np.ndarray
            This is a square matrix representing the confusion matrix data
            where the rows are the predictions and the columns are the 
            ground truth.

        labels: list
            This contains the unique string labels in the dataset.

        model: str
            The name of the model being validated.

    Returns
    --------
        fig: matplotlib.pyplot
            The confusion matrix plot. 
    """
    norm_conf = []
    for i in confusion_data:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            try:
                tmp_arr.append(float(j)/float(a))
            except ZeroDivisionError:
                tmp_arr.append(0.)
        norm_conf.append(tmp_arr)

    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
                    interpolation='nearest')
    width, height = confusion_data.shape

    for x in range(width):
        for y in range(height):
            ax.annotate(str(int(confusion_data[x][y])), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')
    fig.colorbar(res)
    plt.xticks(range(width), labels[:width], rotation="vertical")
    plt.yticks(range(height), labels[:height])
    plt.ylabel("Prediction")
    plt.xlabel("Ground Truth")
    plt.title(f"{model} Confusion Matrix")
    return fig

def close_figures(figures: List[matplotlib.figure.Figure]):
    """
    Closes the matplotlib figures opened to prevent 
    errors such as "Fail to allocate bitmap."

    Parameters
    ----------
        figures: list
            Contains matplotlib.pyplot figures.
    """
    if len(figures) > 0:
        for figure in figures:
            plt.close(figure)