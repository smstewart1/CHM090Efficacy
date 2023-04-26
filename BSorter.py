import csv
import sys
import pandas as pd

#main function
def main():
    #define variables
    course = "BIO-168"
    controlgroup = "168sans090.csv"
    treatmentgroup = "168with090.csv"
    EMI = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]
    AgeGroups = [18, 23, 27, 31, 35, 38, 100]
    Grades = ["D", "F", "W", "WF", "WP", "WE", "NA"]
    
        #dictionary for EMI and Age Range
    EMIDict = {"1" : "Low", "2" : "Medium-Low", "3" : "Medium", "4" : "Medium-High", "5" : "High"}
    AgeDict = {"1" : "<18", "2" : "18-22", "3" : "23-26", "4" : "27-30", "5" : "31-34", "6" : "35-38", "7" : ">38"}
    
    #Nij is the number of students
        # i = EMI
        # j = age range
    NCij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    NT090ij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    NT168ij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    
    #Pij is the distribution of students not getting an A/B/C based on demographic ij
        # i = EMI
        # j = age range
    PCij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    PT090ij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    PT168ij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    PTij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    
    #difference matrix
    Dij = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
          
    # reads in the control group as a dataframe
    control = pd.read_csv(controlgroup, na_filter = True)
    treatment = pd.read_csv(treatmentgroup, na_filter = True)
    
    #populates matrices-------------------
    NT090ij = NFunction(treatment, NT090ij, "CHM-090", EMI, AgeGroups)
    PT090ij = PFunction(treatment, NT090ij, PTij, "CHM-090", EMI, AgeGroups, Grades)
    NT168ij = MergedCounts(NT168ij, NT090ij, PT090ij, EMI, AgeGroups)
    PT168ij = PFunction(treatment, NT168ij, PTij, course, EMI, AgeGroups, Grades)
    PTij = MergedProbabilities(PTij, PT090ij, PT168ij, EMI, AgeGroups)
    NCij = NFunction(control, NCij, course, EMI, AgeGroups)
    PCij = PFunction(control, NCij, PCij, course, EMI, AgeGroups, Grades)
    Dij = DFunction(PCij, PTij, EMI, AgeGroups, Dij)

    #optimized Bayes probability
    updatedprob = 1
    Cutoff = 1.00
    while Cutoff > 0.2:
        conditions = FConditions(Dij, Cutoff, EMI, AgeGroups)
        updatedprob = Bayes(PTij, NCij, EMI, AgeGroups, conditions)
        if updatedprob < 0.53:
            break
        Cutoff = Cutoff - 0.01
    
    #prints results
    string = PrintConditions(conditions, EMIDict, AgeDict)
    print(string)
    print(f"New Bayesian Probability = {updatedprob}\n Goal is 50%\n")
    string = string + "\nNew Bayesian Probability = " + str(updatedprob) + "\n Goal is 50% \n"
    outputfile = open("FinalResults.txt", "w")
    outputfile.write(string)
    outputfile.close()
    return 0

#special fuctions
    #return N matrix
def NFunction(db, Nij, course, EMI, AgeGroups):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            if j == 0:
                Nij[i][j] = float(len(db.loc[(db["EMI"] == EMI[i]) & (db["Age"] < AgeGroups[j]) & (db["CourseName"] == course)]))
            elif j == len(AgeGroups) - 1:
                Nij[i][j] = float(len(db.loc[(db["EMI"] == EMI[i]) & (db["Age"] > AgeGroups[j - 1]) & (db["CourseName"] == course)]))
            else:
                Nij[i][j] = float(len(db.loc[(db["EMI"] == EMI[i]) & (db["Age"] >= AgeGroups[j - 1]) & (db["Age"] < AgeGroups[j]) & (db["CourseName"] == course)]))
    return Nij

    #return P matrix
def PFunction(db, Nij, Pij, course, EMI, AgeGroups, Grades):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            if j == 0:
                if (Nij[i][j] == 0):
                    Pij = 0
                else:
                    Pij[i][j] = float(len(db.loc[(db["Grade"].isin(Grades)) & (db["EMI"] == EMI[i]) & (db["Age"] < AgeGroups[j]) & (db["CourseName"] == course)]) / Nij[i][j])
            elif j == len(AgeGroups) - 1:
                if (Nij[i][j] == 0):
                    Pij = 0
                else:
                    Pij[i][j] = float(len(db.loc[(db["Grade"].isin(Grades)) & (db["EMI"] == EMI[i]) & (db["Age"] > AgeGroups[j - 1]) & (db["CourseName"] == course)]) / Nij[i][j])
            else:
                if (Nij[i][j] == 0):
                    Pij = 0
                else:
                    Pij[i][j] = float(len(db.loc[(db["Grade"].isin(Grades)) & (db["EMI"] == EMI[i]) & (db["Age"] >= AgeGroups[j - 1]) & (db["Age"] < AgeGroups[j]) & (db["CourseName"] == course)]) / Nij[i][j])
    return Pij

    #populates difference matrix
def DFunction(PCij, PTij, EMI, AgeGroups, Dij):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            Dij[i][j] = PCij[i][j] - PTij[i][j]
    return Dij

    #return conditions based on cutoff
def FConditions(Dij, Cutoff, EMI, AgeGroups):
    Conditions = []
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            if Dij[i][j] > Cutoff:
                temp = 10 * (i + 1) + (j + 1)
                Conditions.append(temp)
    return Conditions
                
    #returns merged probabilities
def MergedProbabilities(PTij, PT090ij, PT168ij, EMI, AgeGroups):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            PTij[i][j] = (1 - PT090ij[i][j]) * PT168ij[i][j]
    return PTij

    #returns merged numbers
def MergedCounts(NT168ij, NTij, PT090ij, EMI, AgeGroups):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            NT168ij[i][j] = (1 - PT090ij[i][j]) * NTij[i][j]
    return NTij

    #basic bayesian probability
def Bayes(PTij, NCij, EMI, AgeGroups, conditions):
    CGroup = 0
    TGroup = 0
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            check = 10 * (i + 1) + (j + 1)
            if (check in conditions):
                TGroup = TGroup + NCij[i][j] * PTij[i][j]
            else:
                CGroup = CGroup + NCij[i][j] * PTij[i][j]
    Prob = CGroup / (CGroup + TGroup)
    return Prob

    #returns groups that return the given Bayesian probability
def PrintConditions(conditions, EMIDict, AgeDict):
    string = "Conditions \n"
    for i in range(0, len(conditions)):
        temp = str(conditions[i])
        string1 = EMIDict[temp[0]]
        string2 = AgeDict[temp[1]]
        string = string + "EMI: " + string1 + " Age Range: " + string2 + "\n" 
    return string
    
#end of program
main()

