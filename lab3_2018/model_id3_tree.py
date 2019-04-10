# Dependencies
# --------------------------------------------------------------------------------
import os
import sys
import math
import operator
import pdb
import preprocessor as pre

# Tree class
# --------------------------------------------------------------------------------

class Tree:

    def __init__(self, attribute, childs = None, most_likely = None):

        # String identifying node's attribute
        self.attribute = attribute

        # String with most likely value for tree's attribute
        # It is used when a new example comes with missing value
        self.most_likely = most_likely

        # Dictionary with keys from attribute's options
        # If is not leaf, values are children nodes,
        # Else, values are booleans giving the answer
        if childs is None:
            self.options = {}
        else:
            self.options = childs


    # Main methods
    # ----------------------------------------------------------------------------

    # Adds a "result" with key "option" to options dictionary
    # If option is to be a leaf, result is a boolean. Else, it is a child node
    def add_option(self, option, result):
        self.options[option] = result

    # Returns the value for "option", could be an answer or a child node
    def get_option(self, option):
        return self.options[option]


    # Auxiliar methods
    # ----------------------------------------------------------------------------

    def print_tree(self, n):

        for x in range(0,n):
            print ('-', end="")
        print (self.attribute)

        for key, value in self.options.items():

            (node,p) = value

            for x in range(0, n+1):
                print ('-', end="")

            if p == -1:
                print(key)
            else:
                print((key,p))

            if type(node) == Tree:
                node.print_tree(n+2)
            else:
                for x in range(0, n+2):
                    print('-', end="")
                print(node)


# Main methods
# --------------------------------------------------------------------------------

# Using a dataset "ds" of training examples and a list "attributes" of attributes, generates a decision tree using ID3
# This version of ID3 adds an strategy for continuous and missing values. The arguments "continuousOption" and "missingOption"
# are for choosing which strategy will be used. There are 2 and 3 possible values for each respectively:
# -------------------------------------------------------------------------------------------------------------------------
# Continuous 1: Splits the continuous range in 3 fixed intervals based on its min and max values
# Continuous 2: Splits the continuous range in intervals based on when the result function changes its value, adding a branch for each one
# Continuous different than 1,2: Does not support continuous values
# -------------------------------------------------------------------------------------------------------------------------
# Missing 1: Adds to the missing values the most likely value in the current dataset for that attribute
# Missing 2: Adds a probability to each branch of the attribute if it has missing values, which will be used to classify
# Missing different than 1,2: Does not support empty values
# -------------------------------------------------------------------------------------------------------------------------
def id3_train(ds, attributes, continuousOption = 0, missingOption = 0):

    # Border Case: Every example is labeled true
    # Returns true (dont care if is root or not, ID3 is recursive)
    if proportion_examples_true(ds) == 1:
        return True

    # Border Case: Every example is labeled false
    # Returns false (dont care if is root, ID3 is recursive)
    elif proportion_examples_true(ds) == 0:
        return False

    # Border Case: There are no more attributes
    # Returns the most likely value between true and false
    elif len(attributes) == 0:
        if proportion_examples_true(ds) > 0.5:
            return True
        else:
            return False

    # No Border Case
    else:

        # 0. Fill missing values if option determines so
        if missingOption == 1:
            pre.fill_missing_values(ds, attributes)

        # 1. Get the attribute that best classifies ds (highest information gain)
        att = get_best_attribute(ds, attributes, continuousOption == 2, continuousOption == 1)

        # Aux: Delete the chosen attribute, it will not be used in further iterations
        new_attributes = list(attributes)
        new_attributes.remove(att)

        # 2. Create an empty dictionary which will have the children nodes for the tree (booleans or nodes)
        options = {}

        # 3. Get possible values for "att" in "ds"
        possible_values = []
        if continuousOption == 2 and pre.get_continuity(ds, att):
            possible_values = pre.get_possible_continuous_values(ds, att)
        elif continuousOption == 1 and pre.get_continuity(ds, att):
            possible_values = pre.get_possible_fixed_continuous_values(ds,att)
        else:
            possible_values = pre.get_possible_values(ds, att)

        # 4. Iterate through them
        for value in possible_values:

            # 4.1. Get a list of examples that match value "value" in attribute "att"
            examples_vi = []
            if continuousOption == 2 and pre.get_continuity(ds, att):
                if missingOption == 2:
                    new_ds = [x for x in ds if x not in pre.get_unknown_examples_for_value(ds, att)]
                    examples_vi = pre.get_examples_for_interval(new_ds, att, value, possible_values)
                else:
                    examples_vi = pre.get_examples_for_interval(ds, att, value, possible_values)

            elif continuousOption == 1 and pre.get_continuity(ds, att):
                if missingOption == 2:
                    new_ds = [x for x in ds if x not in pre.get_unknown_examples_for_value(ds, att)]
                    examples_vi = pre.get_examples_for_interval(new_ds, att, value, possible_values)
                else:
                    examples_vi = pre.get_examples_for_interval(ds, att, value, possible_values)

            else:
                examples_vi = pre.get_examples_for_value(ds, att, value)

            # 4.2 Calculates probability of current attribute (default -1, when missingOption != 2)
            # It will be used when to classify a new example with missing values
            total_examples = 1
            cant_examples = -1
            if missingOption == 2:
                total_examples = len(ds) - len(pre.get_unknown_examples_for_value(ds,att))
                cant_examples = len(examples_vi)

            # 4.3. If there are no examples for the value, the answer is the most likely value between true and false
            if len(examples_vi) == 0:
                if proportion_examples_true(ds) > 0.5:
                    options[value]= (True, cant_examples/total_examples)
                else:
                    options[value] = (False, cant_examples/total_examples)

            # 4.4. If there are still examples for the value, triggers recursive execution
            # This time using the set of examples with value "value" in "att" as dataset
            # and excluding "att" from the list of attributes
            else:

                node = id3_train(examples_vi, new_attributes, continuousOption, missingOption)
                options[value] = (node, cant_examples/total_examples)

        # 5. Create and return the tree node
        if missingOption == 1:
            return Tree(att, options, pre.get_most_likely_value(ds,att))
        else:
            return Tree(att, options)

# Using a decision tree "tree", classifies a valid example, taking into account same parameters than id3_generate_better
def id3_classify(tree, example, continuousOption = 0, missingOption = 0):

    # 1. Choose the current attribute in the tree
    current_att = tree.attribute

    # 2. Get the value in the example for the current attribute
    example_att = example[current_att]

    valueIsKnown = False
    for key in tree.options.keys():
        if key == example_att:
            valueIsKnown = True

    if not valueIsKnown:
        example_att = '?'

    # Aux: Cast to number if it is intended to be
    if type(example_att) != float and example_att.replace('.','',1).isdigit():
        example_att = float(example_att)

    # Aux: Check if new example's value in "att" is unknown
    # If it is and missingOption = 0, it is substituted by the most likely value for "att"
    if example_att == '?' and missingOption == 1:
        example_att = tree.most_likely

    # Aux: Check if new example's value in "att" is unknown
    # If it is and missingOption = 1, from now on answer will be calculated based on probability
    elif example_att == '?' and missingOption == 2:

        prob_pos = 0
        prob_neg = 0

        # Starting in this node, probability for each branch has to be calculated and added
        for key, value in tree.options.items():

            node,p = value

            # If it is a leaf node, just adds probability to the corresponding positive or negatuve value
            if type(node) == bool:
                if node == True:
                    prob_pos += 1 * p
                else:
                    prob_neg += 1 * p

            # If it is not, gets recursive probability taking into account probability in all next branches
            else:
                recursion = id3_classify(node, example, continuousOption, missingOption)
                prob_pos += recursion[0] * p
                prob_neg += recursion[1] * p

        return (prob_pos, prob_neg)


    # 3. If there are no missing values for this attribute, get the subtree for that value
    #try:
    # Aux: Used for getting the right value when there are intervals
    if type(example_att) == float and (continuousOption == 1 or continuousOption == 2):
        for x in tree.options:
            if x == 'bigger' or example_att <= float(x):
                example_att = x
                break

    # Get correct branch and its probability
    (branch, p) = tree.options[example_att]
    
    # If it is a tree, recursive call using subtree as root
    if type(branch) == Tree:
        return id3_classify(branch, example, continuousOption, missingOption)

    # Otherwise, the branch is the answer
    else:
        # Aux: If missingOption = 2, classifier must handle probabilities. There is a chance that some value
        # for the example is missing, so the result must be returned in a correct way for the upper recursion
        # to handle it. The returned pair corresponds to (positive_prob, negative_prob).
        if missingOption == 2:
            if branch:
                return (1,0)
            else:
                return (0,1)
        else:
            return (branch,p)

    #except:
        #return False

# Auxiliar methods
# --------------------------------------------------------------------------------


# Given a dataset "ds" of training examples, returns the proportion of the ones labeled as positive
def proportion_examples_true(ds):
    if len(ds) == 0:
        return 0.5
    positives = [x for x in ds if x['truth'] == True]
    return len(positives) / len(ds)

# Given a dataset "ds" and a list "attributes", returns the attribute that gives the highest information gain
def get_best_attribute(ds, attributes, continuous = False, continuousFixed = False):
    ret = attributes[0]
    for att in attributes:
        isContinuousAtt = pre.get_continuity(ds,att) and continuous
        isContinuousRet = pre.get_continuity(ds,ret) and continuous
        isContinuousFixedAtt = pre.get_continuity(ds,att) and continuousFixed
        isContinuousFixedRet = pre.get_continuity(ds,ret) and continuousFixed
        if get_gain(ds, att, isContinuousAtt, isContinuousFixedAtt) > get_gain(ds, ret, isContinuousRet, isContinuousFixedRet):
            ret = att
    return ret

# Given a dataset "ds" and an attribute "att", returns the information gain in "ds" for "attribute"
# If isContinuous is true, takes into account that att is continuous and gets its intervals
def get_gain(ds, att, isContinuous = False, isContinuousFixed = False):
    entropia = 0
    split = 0
    cant_ejemplos = len(ds)

    possible_values = []
    if isContinuous:
        possible_values = pre.get_possible_continuous_values(ds,att)
    else:
        if isContinuousFixed:
            possible_values = pre.get_possible_fixed_continuous_values(ds,att)
        else:
            possible_values = pre.get_possible_values(ds,att)

    for value in possible_values:
        subset = pre.get_examples_for_value(ds, att, value)
        entropia += ((len(subset)/cant_ejemplos) * entropy(subset))

    return (entropy(ds) - entropia)

# Given a dataset "ds", returns its entropy
def entropy(ds):
    pos_prop = proportion_examples_true(ds)
    neg_prop = 1 - pos_prop
    if pos_prop == 0 or neg_prop == 0:
        return 0
    entropia = - pos_prop * math.log(pos_prop,2) - neg_prop * math.log(neg_prop,2)
    return entropia
