# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by 6.034 Staff

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')


################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################


#### Part 1A: Classifying points ###############################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    while not id_tree.is_leaf():
        id_tree = id_tree.apply_classifier(point)

    return id_tree.get_node_classification()

#### Part 1B: Splitting data with a classifier #################################

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    result = {}
    for D in data:
        classification = classifier.classify(D)
        if classification not in result:
            result[classification] = [D]
        else:
            result[classification].append(D)

    return result


#### Part 1C: Calculating disorder #############################################

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    split = split_on_classifier(data, target_classifier)

    num_points = len(data)
    branch_points = lambda x: len(split[x])

    disorder = lambda x: 0 if branch_points(x) == 0 else -1 * branch_points(x) / num_points * log2(branch_points(x) / num_points)
    total_disorder = sum(disorder(x) for x in split)

    return total_disorder

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    split = split_on_classifier(data, test_classifier)

    result = sum(len(split[x]) / len(data) * branch_disorder(split[x], target_classifier) for x in split)
    return result


## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:

#for classifier in tree_classifiers:
#    print(classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type")))


#### Part 1D: Constructing an ID tree ##########################################

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    options = list((average_test_disorder(data, C, target_classifier), C) for C in possible_classifiers)

    result = None
    M = 0
    for val in options:
        if result == None or val[0] < M:
            M = val[0]
            result = val[1]

    # If the best classifier has only one branch, raises NoGoodClassifiersError.
    if all(result.classify(A) == result.classify(B) for A,B in zip(data, data[1:])):
        raise NoGoodClassifiersError

    return result

## To find the best classifier from 2014 Q2, Part A, uncomment:
# print(find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type")))

def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""

    if id_tree_node == None:
        id_tree_node = IdentificationTreeNode(target_classifier)
   
    if not data:
        raise 'I dunno how to deal with no data'

    first_datum = target_classifier.classify(data[0])

    is_homogenous = all(target_classifier.classify(D) == first_datum for D in data)

    if is_homogenous:
        id_tree_node.set_node_classification(first_datum)
    else:
        try:
            C = find_best_classifier(data, possible_classifiers, target_classifier)

            split = split_on_classifier(data, C)
            id_tree_node.set_classifier_and_expand(C, list(s for s in split))
            for branch in id_tree_node.get_branches():
                construct_greedy_id_tree(split[branch], list(p for p in possible_classifiers if p != C), target_classifier, id_tree_node.get_branches()[branch])
        except:
            pass

    return id_tree_node

## To construct an ID tree for 2014 Q2, Part A:
# print(construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type")))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
# tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
# print(id_tree_classify_point(tree_test_point, tree_tree))

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
# print(construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification")))
# print(construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class")))


#### Part 1E: Multiple choice ##################################################

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


#### OPTIONAL: Construct an ID tree with medical data ##########################

## Set this to True if you'd like to do this part of the lab
DO_OPTIONAL_SECTION = False

if DO_OPTIONAL_SECTION:
    from parse import *
    medical_id_tree = construct_greedy_id_tree(heart_training_data, heart_classifiers, heart_target_classifier_discrete)


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### Part 2A: Drawing Boundaries ###############################################

BOUNDARY_ANS_1 = None
BOUNDARY_ANS_2 = None

BOUNDARY_ANS_3 = None
BOUNDARY_ANS_4 = None

BOUNDARY_ANS_5 = None
BOUNDARY_ANS_6 = None
BOUNDARY_ANS_7 = None
BOUNDARY_ANS_8 = None
BOUNDARY_ANS_9 = None

BOUNDARY_ANS_10 = None
BOUNDARY_ANS_11 = None
BOUNDARY_ANS_12 = None
BOUNDARY_ANS_13 = None
BOUNDARY_ANS_14 = None


#### Part 2B: Distance metrics #################################################

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    raise NotImplementedError

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    raise NotImplementedError

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    raise NotImplementedError

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    raise NotImplementedError

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    raise NotImplementedError

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    raise NotImplementedError


#### Part 2C: Classifying points ###############################################

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    raise NotImplementedError

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    raise NotImplementedError


## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
# print(knn_classify_point(knn_tree_test_point, knn_tree_data, 1, euclidean_distance))


#### Part 2C: Choosing k #######################################################

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    raise NotImplementedError

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    raise NotImplementedError


## To find the best k and distance metric for 2014 Q2, part B, uncomment:
# print(find_best_k_and_metric(knn_tree_data))


#### Part 2E: More multiple choice #############################################

kNN_ANSWER_1 = None
kNN_ANSWER_2 = None
kNN_ANSWER_3 = None

kNN_ANSWER_4 = None
kNN_ANSWER_5 = None
kNN_ANSWER_6 = None
kNN_ANSWER_7 = None


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
