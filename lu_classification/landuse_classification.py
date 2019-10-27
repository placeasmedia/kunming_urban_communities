# -*- coding: utf-8 -*-
############################################################################
# System requirements:
#   Python 3.X distribution from Anaconda (Anaconda 3)
############################################################################

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import seaborn as sns
import pickle as pk
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score


## --- Load DataSet from CSV file
def loadFrCSVFile(filename):
    print(filename)
    col_names = ["lu_assmt","year_lcc", "landuse1","landuse2", 
                 "nyt", "rat", "nightt", "morningt", "endt", "dayt",
                 "dist2s1","dist2s2","dist2s3","dist2s4","dist2s5","dist2s6",
                 "dist2rec","dist2tr","dist2ma","dist2res","dist2gov","dist2of","dist2ot","dist2co",
                 "num2s1", "num2s2", "num2s3", "num2s4", "num2s5", "num2s6", 
                 "num2rec","num2tr","num2ma","num2res","num2gov","num2of","num2ot","num2co",
                 "area"]
    dataset = pd.read_csv(filename, names=col_names, encoding='utf8', header=1)
    print(dataset.shape)
    dataset['year_lcc'] = dataset['year_lcc'].astype(float)
    dataset['soso1'] = dataset['landuse1'].astype('category').cat.codes
    dataset['soso2'] = dataset['landuse2'].astype('category').cat.codes
    dataset['nyt'] = dataset['nyt'].astype(float)
    dataset['rat'] = dataset['rat'].astype(float)
    dataset['nightt'] = dataset['nightt'].astype(float)
    dataset['morningt'] = dataset['morningt'].astype(float)
    dataset['endt'] = dataset['endt'].astype(float)
    dataset['dayt'] = dataset['dayt'].astype(float)
    # set label
    # reduce number of categories
    dataset['lu_assmt'] = dataset['lu_assmt'].map(
        {'gc':'res', 
         'oc':'res', 
         'us': 'co', 
         'res':'res',
         'rec':'re',
         'co': 'co', 
         'of':'of',
         'gov':'of', 
         'ma':'ma', 
         'ot':'ot', 
         'uu':'uu',
         'tr':'tr', 
         're':'re'})
    dataset['lu_assmt'] = dataset['lu_assmt'].astype('category')
    return dataset


## Descriptive Statistics
def summariseDataset(dataset):
    cols1 = ["lu_assmt","year_lcc","area"]
    cols2 = ["dist2s1","dist2s2","dist2s3","dist2s4","dist2s5","dist2s6"]
    cols3 = ["dist2rec","dist2tr","dist2ma","dist2res","dist2gov","dist2of","dist2ot","dist2co"]
    cols4 = ["num2s1", "num2s2", "num2s3", "num2s4", "num2s5", "num2s6"]
    cols5 = ["num2rec","num2tr","num2ma","num2res","num2gov","num2of","num2ot","num2co"]
    cols6 = ["nyt", "rat", "nightt", "morningt", "endt", "dayt"]
    # types
    print(dataset.dtypes)
    dataset.describe(include='all')
    # shape
    print(dataset[cols1].shape)
    print(dataset[cols2].shape)
    print(dataset[cols3].shape)
    print(dataset[cols4].shape)
    print(dataset[cols5].shape)
    print(dataset[cols6].shape)
    # head
    print(dataset[cols1].head(5))
    print(dataset[cols2].head(5))
    print(dataset[cols3].head(5)) 
    print(dataset[cols4].head(5))
    print(dataset[cols5].head(5)) 
    print(dataset[cols6].head(5)) 
    # descriptions
    print(dataset[cols1].describe())
    print(dataset[cols2].describe())    
    print(dataset[cols3].describe())
    print(dataset[cols4].describe())    
    print(dataset[cols5].describe())
    print(dataset[cols6].describe())
    # class distribution
    print(dataset.groupby('lu_assmt').size())
    

## Data Visualisation
def visualiseDataset(dataset):
    cols1 = ["year_lcc","area", "soso1", "soso2"]
    cols2 = ["dist2s1","dist2s2","dist2s3","dist2s4","dist2s5","dist2s6"]
    cols3 = ["dist2rec","dist2tr","dist2ma","dist2res","dist2gov","dist2of","dist2ot","dist2co"] 
    cols4 = ["num2s1", "num2s2", "num2s3", "num2s4", "num2s5", "num2s6"]
    cols5 = ["num2rec","num2tr","num2ma","num2res","num2gov","num2of","num2ot","num2co"]
    cols6 = ["nyt", "rat", "nightt", "morningt", "endt", "dayt"]
    
    # pairplot with the two classes in different color using the attribute hue
    sns.pairplot(dataset, hue='lu_assmt')
    sn = sns.heatmap(dataset.corr(), annot=True)
    fig = sn.get_figure()
    fig.savefig('./heatmap.png', dpi=300)
    
    # box and whisker plots
    dataset[cols1].plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()
    dataset[cols2].plot(kind='box', subplots=True, layout=(3,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()
    dataset[cols3].plot(kind='box', subplots=True, layout=(4,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()  
    dataset[cols4].plot(kind='box', subplots=True, layout=(3,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()
    dataset[cols5].plot(kind='box', subplots=True, layout=(4,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()
    dataset[cols6].plot(kind='box', subplots=True, layout=(4,2), sharex=False, sharey=False, figsize=(12,12))
    pyplot.show()
    # histograms
    dataset[cols1].hist(figsize=(12,12))
    pyplot.show()
    dataset[cols2].hist(figsize=(12,12))
    pyplot.show()
    dataset[cols3].hist(figsize=(12,12))
    pyplot.show() 
    dataset[cols4].hist(figsize=(12,12))
    pyplot.show()
    dataset[cols5].hist(figsize=(12,12))
    pyplot.show()
    dataset[cols6].hist(figsize=(12,12))
    pyplot.show()
    # scatter plot matrix
    scatter_matrix(dataset[cols1], figsize=(12,12))
    pyplot.show()
    scatter_matrix(dataset[cols2], figsize=(12,12))
    pyplot.show()
    scatter_matrix(dataset[cols3], figsize=(12,12))
    pyplot.show()
    scatter_matrix(dataset[cols4], figsize=(12,12))
    pyplot.show()
    scatter_matrix(dataset[cols5], figsize=(12,12))
    pyplot.show()
    scatter_matrix(dataset[cols6], figsize=(12,12))
    pyplot.show()
    
## Data Pre-Processing
def preProcessingData(dataset):

    # Feature Selection
    cols_X = ["year_lcc",
              "area",
              "soso1",
              "dist2s1",
              "dist2s3",
              "dist2rec",
              "dist2tr",
              "dist2ma",
              "dist2of",
              "dist2ot", 
              "num2s4", 
              "num2s5", 
              "num2s6", 
              "num2rec",
              "num2tr",
              "num2ma",
              "num2res",
              "num2gov",
              "num2of",
              "num2ot",
              "num2co"]
    cols_Y = "lu_assmt"
    
    # Split out train : test datasets
    train_X, test_X, train_Y, test_Y = train_test_split(dataset.loc[:, cols_X], 
                                                        dataset.loc[:, cols_Y], 
                                                        test_size=0.20,
                                                        random_state=42,
                                                        shuffle=True
                                                        )
    
    return train_X, test_X, train_Y, test_Y

## Deep learning model
# def create_model():
#     classifier = Sequential()
#     #First Hidden Layer, input_dim equals the dimension of features in training sample
#     classifier.add(Dense(15, activation='relu', kernel_initializer='random_normal', input_dim=24))
#     #Second  Hidden Layer
#     classifier.add(Dense(10, activation='relu', kernel_initializer='random_normal'))
#     #Output Layer
#     classifier.add(Dense(7, activation='sigmoid', kernel_initializer='random_normal'))
#     #Compiling the neural network
#     classifier.compile(optimizer ='adam',loss='categorical_crossentropy', metrics =['accuracy'])
    
#     return classifier


## Applied Machine Learning Algorithm
def evaluateAlgorithm(train_X, test_X, train_Y, test_Y):  
    model_List = []
    model_List.append(('LR',    'Logistic Regression',          LogisticRegression()))
    model_List.append(('LDA',   'Linear Discriminant Analysis', LinearDiscriminantAnalysis()))
    model_List.append(('KNN',   'K Neighbors Classifier',       KNeighborsClassifier()))
    model_List.append(('CART',  'DecisionTreeClassifier',       DecisionTreeClassifier()))
    model_List.append(('NB',    'Naive Bayes',                  GaussianNB()))
    model_List.append(('SVM',   'Support Vector Machine ',      SVC(kernel="linear", C=0.025)))
#     model_List.append(('RBF',   'Support Vector Machine with RBF ',      SVC(gamma=2, C=1)))
    model_List.append(('GPC',   'Gaussian Process Classifier ',      GaussianProcessClassifier(1.0 * RBF(1.0))))
    model_List.append(('RMF',   'Random Forest ',      RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)))
#     model_List.append(('Ada',   'Adaboost ',      AdaBoostClassifier()))
#     model_List.append(('NN',   'Neural Network ',      MLPClassifier(alpha=1, max_iter=1000)))
#     model_List.append(('NN',   'Neural Network ',      MLPClassifier(hidden_layer_sizes=(50,100,50), max_iter=1000,activation = 'relu',solver='adam',random_state=1)))
#     model_List.append(('DL',   'Deep-learning Neural Network ',      KerasClassifier(build_fn=create_model, epochs=200, batch_size=5, verbose=0)))
    
    ##Cross Validation
    print("Cross Validation Results ")
    outcomes = []
    description = []
    shortDescription = []
    for shtDes, des, model in model_List:
        cv_results = cross_val_score(model, train_X, train_Y, cv = 3, 
                                     scoring='accuracy', n_jobs = -1, verbose = 0)
        outcomes.append(cv_results)
        description.append(des)
        shortDescription.append(shtDes)
        prt_string = "\n %s:\n \tMean Accuracy: %f (Std: %f)" % (des, cv_results.mean()
                                                                    , cv_results.std())
        print(prt_string)
        
    ##Visualise the outcomes / results from Cross Validation
    fig = pyplot.figure(figsize = (12,12))
    fig.suptitle('Cross Validation Results (Algorithm Comparison)')
    ax = fig.add_subplot(111)
    pyplot.boxplot(outcomes)
    ax.set_xticklabels(shortDescription)
#     pyplot.show()
    pyplot.savefig('./lu_classification_comparison.png', dpi=300)
    
    ##Training & Fitting of each Algorithm with training Dataset
    print('\nEvaluate Algorithms (Accuracy, Classification Report, Confusion Matrix) ... ... ... ')
    
    for shtDes, des, model in model_List:   
        
        #model fitting or training
        trained_Model = model.fit(train_X, train_Y)
        
        ##Evaluation of trained Algorithm (or Model) and result
        pred_Class          = trained_Model.predict(test_X)
        acc         = accuracy_score(test_Y, pred_Class)
        classReport = classification_report(test_Y, pred_Class)
        confMatrix  = confusion_matrix(test_Y, pred_Class) 
        kappa = cohen_kappa_score(test_Y, pred_Class)

        print("\n%s: " % (des))
        print('The accuracy: {}'.format(acc))
        print('The Classification Report:\n {}'.format(classReport))
        print('The Confusion Matrix:\n {}'.format(confMatrix))
        print('The Kappa Score:\n {}'.format(kappa))

        #Save the trained Model
        with open('model_'+shtDes+'.pickle', 'wb') as f:
                pk.dump(trained_Model, f)

## Load a new dataset to make predictions 
def loadPredictionDataset(filename):
    col_names = ["gid","year_lcc", "landuse1","landuse2", 
                 "nyt", "rat", "nightt", "morningt", "endt", "dayt",
                 "dist2s1","dist2s2","dist2s3","dist2s4","dist2s5","dist2s6",
                 "dist2rec","dist2tr","dist2ma","dist2res","dist2gov","dist2of","dist2ot","dist2co",
                 "num2s1", "num2s2", "num2s3", "num2s4", "num2s5", "num2s6", 
                 "num2rec","num2tr","num2ma","num2res","num2gov","num2of","num2ot","num2co",
                 "area"]
    dataset = pd.read_csv(filename, names=col_names, encoding='utf8', header=1)
    print(dataset.shape)
    dataset['year_lcc'] = dataset['year_lcc'].astype(float)
    dataset['soso1'] = dataset['landuse1'].astype('category').cat.codes
    dataset['soso2'] = dataset['landuse2'].astype('category').cat.codes
    dataset['nyt'] = dataset['nyt'].astype(float)
    dataset['rat'] = dataset['rat'].astype(float)
    dataset['nightt'] = dataset['nightt'].astype(float)
    dataset['morningt'] = dataset['morningt'].astype(float)
    dataset['endt'] = dataset['endt'].astype(float)
    dataset['dayt'] = dataset['dayt'].astype(float)
    
    return dataset

## --- Load the trained model and make prediction
def loadTrainedModelForPrediction(pred_dataset):
    cols_X = ["year_lcc",
              "area",
              "soso1",
              "dist2s1",
              "dist2s3",
              "dist2rec",
              "dist2tr",
              "dist2ma",
              "dist2of",
              "dist2ot",
              "num2s4", 
              "num2s5", 
              "num2s6", 
              "num2rec",
              "num2tr",
              "num2ma",
              "num2res",
              "num2gov",
              "num2of",
              "num2ot",
              "num2co"]
    pred_dataset2 = pred_dataset.loc[:, cols_X]
    f = open('model_LR.pickle', 'rb')
    model = pk.load(f); f.close();
    pred_Class = model.predict(pred_dataset2)
    pred_dataset.loc[:, 'classResult'] = pred_Class
    return pred_dataset

## Finalise the results 
def finaliseResult(result):
    
    #Save Result in a CSV file
    result.to_csv('LR_finalResult.csv', index = False)
    print("\n\nSave Result in a CSV file ... ... Done ...")                   
                

if __name__ == '__main__':
    filename = 'lu_training.csv'

    # Load Dataset to which Machine Learning Algorithm to be applied
    dataset = loadFrCSVFile(filename)

    
    # Summarisation of Data to understand dataset (Descriptive Statistics)
#     summariseDataset(dataset)
    
    # Visualisation of Data to understand dataset (Plots, Graphs etc.)
#     visualiseDataset(dataset)
    
    # Data pre-processing and Data transformation (split into train-test datasets)
    train_X, test_X, train_Y, test_Y = preProcessingData(dataset)
    
    # Application of a Machine Learning Algorithm to training dataset 
    evaluateAlgorithm(train_X, test_X, train_Y, test_Y)
    
    # Load the saved model and apply it to new dataset for prediction 
    pred_Dataset = loadPredictionDataset('lu_prediction.csv')
    result = loadTrainedModelForPrediction(pred_Dataset)
    finaliseResult(result)
    
    print('\ndone\n')