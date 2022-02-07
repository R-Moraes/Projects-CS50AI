import csv
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import collections 

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def convertMonth(month:str):
    if month == 'Jan':
        return 0
    elif month == 'Feb':
        return 1
    elif month == 'Mar':
        return 2
    elif month == 'Apri':
        return 3
    elif month == 'May':
        return 4
    elif month == 'Jun':
        return 5
    elif month == 'Jul':
        return 6
    elif month == 'Aug':
        return 7
    elif month == 'Sep':
        return 8
    elif month == 'Oct':
        return 9
    elif month == 'Nov':
        return 10
    elif month == 'Dec':
        return 11
    else:
        return -1
 
def convertVisitorType(vt):
    if vt == 'Returning_Visitor':
        return 1
    else:
        return 0
     
def convertWeekend(week):
    if week == 'TRUE':
        return 1
    else:
        return 0

def convertRevenue(rev):
    if rev == 'TRUE':
        return 1
    else:
        return 0

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following varaise NotImplementedErrorstrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    with open('shopping.csv','r') as file:
        read = csv.DictReader(file)
        for r in read:
            aux = list()
            for l in r:
                if l != 'Revenue':
                    if l == 'Month':
                        r[l] = convertMonth(r[l])
                    if l == 'VisitorType':
                        r[l] = convertVisitorType(r[l])
                    if l == 'Weekend':
                        r[l] = convertWeekend(r[l])
                    if l == 'Administrative':
                        r[l] = int(r[l])
                    if l == 'Informational':
                        r[l] = int(r[l])
                    if l == 'ProductRelated':
                        r[l] = int(r[l])
                    if l == 'Month':
                        if r[l] != None: r[l] = int(r[l])
                    if l == 'Informational':
                        r[l] = int(r[l])
                    if l == 'OperatingSystems':
                        r[l] = int(r[l])
                    if l == 'Browser':
                        r[l] = int(r[l])
                    if l == 'Region':
                        r[l] = int(r[l])
                    if l == 'TrafficType':
                        r[l] = int(r[l])
                    if l == 'VisitorType':
                        r[l] = int(r[l])
                    if l == 'Weekend':
                        r[l] = int(r[l])
                    if l == 'Administrative_Duration':
                        r[l] = float(r[l])
                    if l == 'Informational_Duration':
                        r[l] = float(r[l])
                    if l == 'ProductRelated_Duration':
                        r[l] = float(r[l])
                    if l == 'BounceRates':
                        r[l] = float(r[l])
                    if l == 'ExitRates':
                        r[l] = float(r[l])
                    if l == 'PageValues':
                        r[l] = float(r[l])
                    if l == 'SpecialDay':
                        r[l] = float(r[l])
                    aux.append(r[l])
                if l == 'Revenue':
                    r[l] = convertRevenue(r[l])
                    labels.append(r[l])    
            evidence.append(aux)
            
    return np.array(evidence),np.array(labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    kb = KNeighborsClassifier(n_neighbors=1)
    kb.fit(evidence, labels)
    
    return kb

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sen = 0
    spe = 0
   
    for i,value in enumerate(labels):
        if value == 1:
            if predictions[i] == value:
                sen += 1
        if value == 0:
            if predictions[i] == value:
                spe += 1       
    col = collections.Counter(labels)
    true_pos = col[1]
    true_neg = col[0]
    
    return sen/true_pos, spe/true_neg
        


if __name__ == "__main__":
    main()
