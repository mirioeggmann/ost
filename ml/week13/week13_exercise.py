import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits
from my_pca_sol import MyPca

###############################################################################
##
## Functions
##
###############################################################################

def example_1(data):
    """
    Function for example 1

    Parameters
    ----------
    data : pandas Dataframe
        Dataset to apply PCA to. Each row is considered as one observation and
        each column is considered as one feature.

    Returns
    -------
    None.

    """
    # Transform pandas Dataframe to numpy
    x = data.to_numpy()

    # Call own implementation of PCA
    pca = MyPca()
    pca.fit(x)
    pca.transform(x)

    # Print results
    print("Explained variances: \n\t{}\n".format(
          str(pca.eigen_vals).replace('\n', '\n\t')))
    print("Ccomponents: \n\t{}\n".format(
          str(pca.eigen_vecs).replace('\n', '\n\t')))
    print("Explained variance ratios: \n\t{}\n".format(
           str(pca.explained_variance_ratio_).replace('\n', '\n\t')))

    # Display explained variance
    plt.figure(figsize=(7, 5))
    x_plot = np.arange(x.shape[1]) + 1
    plt.plot(x_plot, pca.explained_variance_ratio_,
             '-o', label='Explained variance ratio')

    plt.plot(x_plot, np.cumsum(pca.explained_variance_ratio_), \
             '-s', label='Cumulative')

    plt.ylabel('Proportion of Variance Explained')
    plt.xlabel('Principal Component')
    plt.xlim(0.75, 4.25)
    plt.ylim(0, 1.05)
    plt.xticks(x_plot)
    plt.legend()
    plt.show()


def example_2(data):
    """
    Function for example 2

    Parameters
    ----------
    data : pandas Dataframe
        Dataset to apply PCA to. Each row is considered as one observation and
        each column is considered as one feature.

    Returns
    -------
    None.

    """
    # Call own implementation of PCA
    pca = MyPca()
    pca.fit(data.values)
    pca.transform(data.values)

    # Print results
    pca_loadings = pd.DataFrame(pca.components_,
                                index=data.columns,
                                columns=['V1', 'V2', 'V3', 'V4'])
    print("PCA Loadings:")
    print(pca_loadings)
    print('\n')

    df_plot = pd.DataFrame(pca.transform(data.values),
                           columns=['PC1', 'PC2', 'PC3', 'PC4'],
                           index=data.index)

    print("Transformed Data:")
    print(df_plot)
    print('\n')

    fig, ax1 = plt.subplots(figsize=(9, 7))
    ax1.set_xlim(-3.5, 3.5)
    ax1.set_ylim(-3.5, 3.5)

    # Plot Principal Components 1 and 2
    for i in df_plot.index:
        ax1.annotate(i, (df_plot.PC1.loc[i], -df_plot.PC2.loc[i]), ha='center')

    # Plot reference lines
    ax1.hlines(0, -3.5, 3.5, linestyles='dotted', colors='grey')
    ax1.vlines(0, -3.5, 3.5, linestyles='dotted', colors='grey')

    ax1.set_xlabel('First Principal Component')
    ax1.set_ylabel('Second Principal Component')

    # Plot Principal Component loading vectors, using a second
    # y-axis.
    ax2 = ax1.twinx().twiny()

    ax2.set_ylim(-1, 1)
    ax2.set_xlim(-1, 1)
    ax2.tick_params(axis='y', colors='orange')
    ax2.set_xlabel('Principal Component loading vectors', color='orange')

    # Plot labels for vectors. Variable 'a' is a small offset
    # parameter to separate arrow tip and text.
    a = 1.07
    for i in pca_loadings[['V1', 'V2']].index:
        ax2.annotate(i, (pca_loadings.V1.loc[i]*a, -pca_loadings.V2.loc[i]*a),
                     color='orange')

    ax2.arrow(0, 0, pca_loadings.V1[0], -pca_loadings.V2[0])
    ax2.arrow(0, 0, pca_loadings.V1[1], -pca_loadings.V2[1])
    ax2.arrow(0, 0, pca_loadings.V1[2], -pca_loadings.V2[2])
    ax2.arrow(0, 0, pca_loadings.V1[3], -pca_loadings.V2[3])
    plt.show()


def example_3(data):
    """
    Function for example 3

    Parameters
    ----------
    data : ndarray
        Dataset to apply PCA to. Each row is considered as one observation and
        each column is considered as one feature.

    Returns
    -------
    None.

    """
    # Plot original images
    plot_digits(data, 'Original images')

    # Add noise and plot resulting images
    np.random.seed(42)
    noisy = np.random.normal(data, 4)
    plot_digits(noisy, 'Noisy images')

    # Call own implementation of PCA
    pca = MyPca(12)
    pca.fit(noisy)

    # Apply inverse transformation and plot results
    components = pca.transform(noisy)
    filtered = pca.inverse_transform(components)
    plot_digits(filtered, 'Backtransformed images')


def plot_digits(data, title):
    fig, axes = plt.subplots(4, 10, figsize=(10, 4),
                             subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    plt.suptitle(title)
    for i, ax in enumerate(axes.flat):
        ax.imshow(data[i].reshape(8, 8),
                  cmap='binary', interpolation='nearest',
                  clim=(0, 16))
    plt.show()

###############################################################################
##
## Main
##
###############################################################################

if __name__ == "__main__":
    df = pd.read_csv('USArrests.csv', index_col=0)
    data_arrest = pd.DataFrame(scale(df), columns=df.columns, index=df.index)

    data_mnist = load_digits()

    example_1(data_arrest)
    example_2(data_arrest)
    example_3(data_mnist.data)
