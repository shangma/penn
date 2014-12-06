"""
Tournament.py
"""
from __future__ import division

# module imports
import sys
import numpy as np

# class imports
from optparse import OptionParser, OptionGroup

# library methods
from sklearn import cross_validation
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from KNN_DTW import knnDTW


# own methods
from merge_data import load_all

def main(options, args):
    """
    Main runs the machine learning algorithms
    and computes accuracy numbers each to be
    saved to a text file.

    Algorithms to compare:
        SVM
        LogReg
        Boosting
        Decision Trees
        DTW with K-NN
        PNN

    Methods for comparison:
        10-fold testing
        ROC curves for each letter.
    """
    X, Y, label_lookup = load_all(
        options.input_folder,
        5,
        options.prefix
    )
    n, d = X.shape

    if options.learning_algorithm == "svm":
        model = svm.SVC(
            C=options.C,
            kernel=options.kernel,
            degree=options.poly,
            gamma=options.gamma,
            tol=options.tol,
            max_iter=options.max_iter,
            verbose=options.verbose,
            probability=True,
        )
    elif options.learning_algorithm == "knn":
        model = knnDTW(
            n_neighbors=options.n_neighbors,
            max_warping_window=options.max_warping_window,
            subsample_step=options.subsample_step,
        )

    elif options.learning_algorithm == "logreg":
        model = LogisticRegression(
            penalty=options.penalty,
            C=options.C,
            tol=options.tol,
        )

    elif options.learning_algorithm == "boost":
        if options.base_estimator == "DecisionTreeClassifier":
            model = AdaBoostClassifier(
                DecisionTreeClassifier(
                    splitter=options.splitter,
                    max_features=options.max_features,
                    max_depth=options.max_depth,
                    min_samples_split=options.min_samples_split,
                    min_samples_leaf=options.min_samples_leaf,
                    max_leaf_nodes=options.max_leaf_nodes,
                ),
                n_estimators=options.n_estimators,
                learning_rate=options.learning_rate,
            )
        else:
            print "ERROR, must select learning algoritm"
            return

    elif options.learning_algorithm == "dt":
        model = DecisionTreeClassifier(
            splitter=options.splitter,
            max_features=options.max_features,
            max_depth=options.max_depth,
            min_samples_split=options.min_samples_split,
            min_samples_leaf=options.min_samples_leaf,
            max_leaf_nodes=options.max_leaf_nodes,
        )

    else:
        print "ERROR, must select learning algoritm"
        return

    kf = cross_validation.Kfold(
        n,
        folds=options.folds,
        shuffle=True,
        random_state=5,
    )



def extract_options(args):
    parser = OptionParser()
    usage = "usage: %prog  [options]"
    """
    options:
        algorithm
            SVC
                C,
                kernel, (rbf, sigmoid, precomputed, poly, linear)
                gamma,
                max_iter,
                tol
            logistic regression
                C
                penalty (l1, l2)
                tol
            ADABoostClassifier
                base estimator (DecisionTreeClassifier)
                n_estimators
                learning_rate,
            DecisionTreeClassifier
                splitter (best, random)
                max_features (number of features explored)
                    int: only look at max_features features
                    float: look at percent of n_features
                    auto: n_features
                    sqrt: look at sqrt(n_features)
                    log2: look at log2(n_features)
                min_samples_split: min numbers of samples required to split
                min_samples_leaf: minimum samples required to be at a leaf
                    random_state
                max_depth

            KNN_DTW
                n_neighbors
                max_warping_window
                subsample_step
    """

    parser.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        help="Enable verbose output. Note that this setting takes advantage of a per-process runtime setting in libsvm that, if enabled, may not work properly in a multithreaded context.",
        default=False,
        action="store_true",
    )
    ###################################
    #
    #     begin file I/O options
    #
    ###################################

    file_options = OptionGroup(
        parser,
        "File I/O options",
        "file system options"
    )

    file_options.add_option(
        "-i","--input_folder",
        dest="input_folder",
        help="path to training data location"
    )

    file_options.add_option(
        "-o","--output_path",
        dest="output_path",
        help="output path for dump files",
        default=4,
    )

    file_options.add_option(
        "-p","--prefix",
        dest="prefix",
        help="prefix for the training data files",
        default="proc_"
    )

    file_options.add_option(
        "-s","--suffix",
        dest="suffix",
        help="suffix for the training data files",
        default=".txt",
    )

    parser.add_option_group(file_options)

    ###################################
    #
    #     end file I/O options
    #
    ###################################

    ###################################
    #
    #     begin algorithm options
    #
    ###################################


    algo_opt = OptionGroup(parser, "Algorithm Options:","Choosing the right algorithm is really important in life.")

    algo_opt.add_option(
        "-a", "--algorithm",
        dest="learning_algorithm",
        help="Select learning algorithm. one of: svm, logreg, boost, dt, knn",
        default=None,
        action="store",
        type="string",
    )

    algo_opt.add_option(
        "-k","--k_folds",
        dest="folds",
        help="number of folds for K-folds",
        default=4,
    )



    parser.add_option_group(algo_opt)


    ###################################
    #
    #     end algorithm options
    #
    ###################################


    ###################################
    #
    #     begin SVC options
    #
    ###################################

    svc_opt = OptionGroup(
        parser,
        "SVM.svc specific options",
        "options for SVM svc classifiers",
    )

    svc_opt.add_option(
        "--svc_C",
        dest="C",
        help="Value of C: Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.",
        action="store",
        type="float",
        default=1.,
    )

    svc_opt.add_option(
        "--kernel",
        dest="kernel",
        help="kernel for SVC (rbf, sigmoid, precomputed, poly, linear)",
        action="store",
        type="string",
        default="linear",
    )
    svc_opt.add_option(
        "--degree",
        dest="degree",
        help="optional (default=3) Degree of the polynomial kernel function ('poly'). Ignored by all other kernels.",
        action="store",
        type="int",
        default="3",
    )
    svc_opt.add_option(
        "--max_iter",
        dest="max_iter",
        help="max_iterations before halting",
        action="store",
        type="int",
        default=-1,
    )
    svc_opt.add_option(
        "--gamma",
        dest="gamma",
        help="Kernel coefficient for 'rbf', 'poly' and 'sigmoid'. If gamma is 0.0 then 1/n_features will be used instead.",
        action="store",
        type="float",
        default=0.0,
    )
    svc_opt.add_option(
        "--tolerance",
        dest="tol",
        help="tolerance for halting",
        action="store",
        type="float",
        default=1e-3,
    )

    parser.add_option_group(svc_opt)
    ###################################
    #
    #     end SVC options
    #
    ###################################


    ###################################
    #
    #     Begin Log Reg options
    #
    ###################################

    log_reg_opt = OptionGroup(
        parser,
        "Logistic Regression specific options",
        ""
    )

    log_reg_opt.add_option(
        "--penalty",
        dest="penalty",
        help="Used to specify the norm used in the penalization. {l1, l2}",
        action="store",
        type="string",
        default='l2',
    )

    log_reg_opt.add_option(
        "--C_lr",
        dest="C",
        help="Value of C: Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.",
        action="store",
        type="float",
        default=1.,
    )

    log_reg_opt.add_option(
        "--tolerance_lr",
        dest="tol",
        help="tolerance for halting",
        action="store",
        type="float",
        default=1e-3,
    )

    parser.add_option_group(log_reg_opt)



    ###################################
    #
    #     End Log Reg options
    #
    ###################################



    ###################################
    #
    #     Begin AdaBoost options
    #
    ###################################

    ada_opt = OptionGroup(
        parser,
        "AdaBoost specific options",
        "NOTE: AdaBoost will also use options from DecisionTreeClassifier options if base_estimator = DecisionTreeClassifier"
    )

    ada_opt.add_option(
        "--base_estimator",
        dest="base_estimator",
        help="AdaBoost only The base estimator from which the boosted ensemble is built. Support for sample weighting is required, as well as proper classes_ and n_classes_ attributes.\n {eg.DecisionTreeClassifier}",
        action="store",
        default=None,
    )

    ada_opt.add_option(
        "--n_estimators",
        dest="n_estimators",
        help="The maximum number of estimators at which boosting is terminated. In case of perfect fit, the learning procedure is stopped early.(default=50)",
        action="store",
        type="int",
        default=50,
    )

    ada_opt.add_option(
        "--learning_rate",
        dest="learning_rate",
        help="Learning rate shrinks the contribution of each classifier by learning_rate. There is a trade-off between learning_rate and n_estimators.",
        action="store",
        type="float",
        default=1.,
    )



    parser.add_option_group(ada_opt)

    ###################################
    #
    #     End Ada Boost options
    #
    ###################################


    ###################################
    #
    #     Begin DT options
    #
    ###################################

    dt_opt = OptionGroup(
        parser,
        "DecisionTreeClassifier specific options",
        "NOTE: DecisionTreeClassifier options will also affect ADABoostClassifier if ADABoostClassifier is selected and base_estimator = DecisionTreeClassifier"
    )
    dt_opt.add_option(
        "--splitter",
        dest="splitter",
        help="The strategy used to choose the split at each node. Supported strategies are 'best' to choose the best split and 'random' to choose the best random split.",
        action="store",
        type="string",
        default='best',
    )
    dt_opt.add_option(
        "--max_features",
        dest="max_features",
        help="number of features explored \n\t int: only look at max_features features \n\t float: look at percent of n_features \n\t auto: n_features \n\tsqrt: look at sqrt(n_features) \n\tlog2: look at log2(n_features)",
        action="store",
        default=None,
    )
    dt_opt.add_option(
        "--max_depth",
        dest="max_depth",
        help="The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples. Ignored if max_samples_leaf is not None.",
        action="store",
        default=None,
    )
    dt_opt.add_option(
        "--min_samples_split",
        dest="min_samples_split",
        help="The minimum number of samples required to split an internal node.",
        action="store",
        type="int",
        default=2,
    )
    dt_opt.add_option(
        "--min_samples_leaf",
        dest="min_samples_leaf",
        help="The minimum number of samples required to be at a leaf node.",
        action="store",
        type="int",
        default=1,
    )

    dt_opt.add_option(
        "--max_leaf_nodes",
        dest="max_leaf_nodes",
        help="Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes. If not None then max_depth will be ignored.",
        action="store",
        default=None,
    )

    parser.add_option_group(dt_opt)

    ###################################
    #
    #  End DecisionTreeClassifier opts
    #
    ###################################


    ###################################
    #
    #     Begin KNN DTW options
    #
    ###################################

    knn_opt = OptionGroup(
        parser,
        "KNN DTW specific options",
        "",
    )

    knn_opt.add_option(
        "--n_neighbors",
        dest="n_neighbors",
        help="int, optional (default=5) Number of neighbors to use by default for KNN",
        action="store",
        type="int",
        default=5,
    )
    knn_opt.add_option(
        "--max_warping_window",
        dest="max_warping_window",
        help="int, optional (default = 1000000) Maximum warping window allowed by the DTW dynamic programming function",
        action="store",
        type="int",
        default=1000000,
    )
    knn_opt.add_option(
        "--subsample_step",
        dest="subsample_step",
        help="int, optional (default = 1) Step size for the timeseries array. By setting subsample_step = 2, the timeseries length will be reduced by half because every second item is skipped. Implemented by x[:, ::subsample_step]",
        action="store",
        type="int",
        default=1,
    )
    parser.add_option_group(knn_opt)

    ###################################
    #
    #  End KNN DTW opts
    #
    ###################################


    return parser.parse_args(args)



if __name__ == '__main__':
    opt_args = extract_options(sys.argv)
    if not opt_args is None:
        main(options=opt_args[0], args=opt_args[1])
