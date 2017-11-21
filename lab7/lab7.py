# MIT 6.034 Lab 7: Support Vector Machines
# Written by 6.034 staff

from svm_data import *
from functools import reduce


#### Part 1: Vector Math #######################################################

def dot_product(u, v):
    """Computes the dot product of two vectors u and v, each represented 
    as a tuple or list of coordinates. Assume the two vectors are the
    same length."""
    return sum(a*b for a,b in zip(u,v))

import math
def norm(v):
    """Computes the norm (length) of a vector v, represented 
    as a tuple or list of coords."""
    return math.sqrt(dot_product(v, v))


#### Part 2: Using the SVM Boundary Equations ##################################

def positiveness(svm, point):
    """Computes the expression (w dot x + b) for the given Point x."""
    return dot_product(svm.w, point) + svm.b

def classify(svm, point):
    """Uses the given SVM to classify a Point. Assume that the point's true
    classification is unknown.
    Returns +1 or -1, or 0 if point is on boundary."""
    p = positiveness(svm, point) / norm(svm.w)
    if p == 0:
        return 0
    elif p > 0:
        return 1
    elif p < 0:
        return -1

def margin_width(svm):
    """Calculate margin width based on the current boundary."""
    return 2 / norm(svm.w)

def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification, for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    result = set()
    for p in svm.training_points:
        w_distance = positiveness(svm, p)
        gutter_constraint = p in svm.support_vectors and w_distance != p.classification
        between_gutters = -1 < w_distance < 1
        if (gutter_constraint or between_gutters):
            result.add(p)

    return result


#### Part 3: Supportiveness ####################################################

def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    result = set()
    for p in svm.training_points:
        if p in svm.support_vectors:
            if p.alpha <= 0:
                result.add(p)
        else:
            if p.alpha != 0:
                result.add(p)
    return result

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False. Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    equilibrium = 0
    for p in svm.training_points:
        equilibrium += classify(svm, p) * p.alpha
    
    eq_4 = equilibrium == 0
   
    test_w = scalar_mult(0, svm.w)
    for p in svm.training_points:
        test_w = vector_add(test_w, scalar_mult(classify(svm,p) * p.alpha, p))

    eq_5 = all(a == b for a,b in zip(svm.w, test_w))

    a = eq_4
    b = eq_5
    return a and b


#### Part 4: Evaluating Accuracy ###############################################

def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    return set(p for p in svm.training_points if classify(svm, p) != p.classification)
    return result


#### Part 5: Training an SVM ###################################################

def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b. Return the updated SVM."""
    # print(svm)
    svm.support_vectors = [p for p in svm.training_points if p.alpha > 0]

    new_w = scalar_mult(0, svm.training_points[0])
    for p in svm.support_vectors:
        new_w = vector_add(new_w, scalar_mult(p.alpha * p.classification, p))

    # print (svm.support_vectors)
    min_b = max_b = None
    for p in svm.support_vectors:
        b = p.classification - dot_product(p, new_w)
        # print (p, b)
        if p.classification < 0 and (min_b == None or b < min_b):
            min_b = b

        if p.classification > 0 and (max_b == None or b > max_b):
            max_b = b

    new_b = (min_b + max_b) / 2

    svm.w = new_w
    svm.b = new_b

    return svm


#### Part 6: Multiple Choice ###################################################

ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A', 'D']
ANSWER_6 = ['A', 'B', 'D']
ANSWER_7 = ['A', 'B', 'D']
ANSWER_8 = []
ANSWER_9 = ['A', 'B', 'D']
ANSWER_10 = ['A', 'B', 'D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1, 3, 6, 8]
ANSWER_18 = [1, 2, 4, 5, 6, 7, 8]
ANSWER_19 = [1, 2, 4, 5, 6, 7, 8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
