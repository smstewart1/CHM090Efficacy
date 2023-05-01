import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#Global functions
EMIDict = {"1" : "Low", "2" : "Medium-Low", "3" : "Medium", "4" : "Medium-High", "5" : "High"}
AgeDict = {"1" : "18-22", "2" : "23-26", "3" : "27-30", "4" : "31-34", "5" : "35-38", "6" : ">38"}

#main function
def main():
    #define variables
    course = "BIO-168"
    controlgroup = "168sans090Age.csv"
    treatmentgroup = "168with090Age.csv"
    EMI = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]
    AgeGroups = [18, 23, 27, 31, 35, 38]
    Grades = ["D", "F", "W", "WF", "WP", "WE", "NA"]
    GraphGroups = ["18-22", "23-26", "27-30", "31-34", "35-38", ">38"]
        #dictionary for EMI and Age Range

    
    #Nij is the number of students
        # i = EMI
        # j = age range
    NCij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    NT090ij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    NT168ij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    #Pij is the distribution of students not getting an A/B/C based on demographic ij
        # i = EMI
        # j = age range
    PCij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    PT090ij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    PT168ij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    PTij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    
    #difference matrix
    Dij = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
          
    # reads in the control group as a dataframe
    control = pd.read_csv(controlgroup, na_filter = True)
    treatment = pd.read_csv(treatmentgroup, na_filter = True)
    
    #populates matrices-------------------
    NT090ij = NFunction(treatment, NT090ij, "CHM-090", EMI, AgeGroups)
    PT090ij = PFunction(treatment, NT090ij, PT090ij, "CHM-090", EMI, AgeGroups, Grades)
    NT090ij = NFunction(treatment, NT168ij, course, EMI, AgeGroups)
    PT168ij = PFunction(treatment, NT168ij, PT168ij, course, EMI, AgeGroups, Grades)
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
        if updatedprob < 0.6:
            break
        Cutoff = Cutoff - 0.01
    
    #prints results
    string = PrintConditions(conditions, EMIDict, AgeDict, PCij) + "\nNew Bayesian Probability = " + str(round(updatedprob, 4)) + "\n Goal is 50% \n \n Number of Students sent to intervention = " + str(round(100 * NumberOfStudents(NCij, EMI, conditions, AgeGroups), 2)) + "% \nOriginal Bayesian Probability = " + str(round(100 * CurrentBayes(NCij, PCij, NT168ij, PT168ij, EMI, AgeGroups), 2)) + "%"
    string2 = matrices(PTij, PCij, EMI, AgeGroups)
    string = string2 + string
    outputfile = open("FinalResults.txt", "w")
    outputfile.write(string)
    outputfile.close()
    
    #generates plots of data
    xlab = "EMI"
    ylab = "Probability of Not Passing CHM168"
    plotting(PT168ij, xlab, ylab, GraphGroups, EMI, "Treatment")
    plotting(PCij, xlab, ylab, GraphGroups, EMI, "Control")
    xlab = "Age Ranges"
    ylab = "EMI"
    hotplocket(PTij, xlab, ylab, EMI, GraphGroups, "Treatment")
    hotplocket(PCij, xlab, ylab, EMI, GraphGroups, "Control")
    return 0

#special fuctions
    #return N matrix
def NFunction(db, Nij, course, EMI, AgeGroups):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            if j == len(AgeGroups) - 1:
                Nij[i][j] = float(len(db.loc[(db["EMI"] == EMI[i]) & (db["Age"] > AgeGroups[j]) & (db["CourseName"] == course)]))
            else:
                Nij[i][j] = float(len(db.loc[(db["EMI"] == EMI[i]) & (db["Age"] >= AgeGroups[j]) & (db["Age"] < AgeGroups[j + 1]) & (db["CourseName"] == course)]))
    return Nij

    #return P matrix
def PFunction(db, Nij, Pij, course, EMI, AgeGroups, Grades):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups)):
            if (Nij[i][j] == 0):
                Pij[i][j] = 0
            elif j == len(AgeGroups) - 1:
                Pij[i][j] = float(len(db.loc[(db["Grade"].isin(Grades)) & (db["EMI"] == EMI[i]) & (db["Age"] > AgeGroups[j]) & (db["CourseName"] == course)]) / Nij[i][j])
            else:
                Pij[i][j] = float(len(db.loc[(db["Grade"].isin(Grades)) & (db["EMI"] == EMI[i]) & (db["Age"] < AgeGroups[j + 1]) & (db["Age"] >= AgeGroups[j]) & (db["CourseName"] == course)]) / Nij[i][j])
    return Pij

    #populates difference matrix
def DFunction(PCij, PTij, EMI, AgeGroups, Dij):
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups) - 1):
            Dij[i][j] = PCij[i][j] - PTij[i][j]
    return Dij

    #return conditions based on cutoff
def FConditions(Dij, Cutoff, EMI, AgeGroups):
    Conditions = []
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups) - 1):
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
        for j in range(0, len(AgeGroups) - 1):
            NT168ij[i][j] = (1 - PT090ij[i][j]) * NTij[i][j]
    return NTij

    #basic bayesian probability
def Bayes(PTij, NCij, EMI, AgeGroups, conditions):
    CGroup = 0
    TGroup = 0
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups) - 1):
            check = 10 * (i + 1) + (j + 1)
            if (check in conditions):
                TGroup = TGroup + NCij[i][j] * PTij[i][j]
            else:
                CGroup = CGroup + NCij[i][j] * PTij[i][j]
    Prob = CGroup / (CGroup + TGroup)
    return Prob

    #returns groups that return the given Bayesian probability
def PrintConditions(conditions, EMIDict, AgeDict, PCij):
    string = "Conditions \n"
    for i in range(0, len(conditions)):
        temp = str(conditions[i])
        string1 = EMIDict[temp[0]]
        string2 = AgeDict[temp[1]]
        string3 = str(round(PCij[int(temp[0]) - 1][int(temp[1]) - 1], 3))
        string = string + "EMI: " + string1 + " Age Range: " + string2 + " Original Probability of Not Passing: " + string3 + "\n" 
    return string
    
def matrices(PTij, PCij, EMI, AgeGroups):
    string = "Treatment Groups - final matrix \n"
    string = string + printmatrix(PTij, EMI, AgeGroups)
    string = string + "\nControl Group\n"
    string = string + printmatrix(PCij, EMI, AgeGroups) + "\n"
    return string  
    
    
def printmatrix(PTij, EMI, AgeGroups):
    string = "      "
    for j in range(1, len(AgeGroups) + 1):
        string = string + str(AgeDict[str(j)]) + " "
    string = string +  "\n"
    for i in range(0, len(EMI)):
        string = string + str(EMIDict[str(i + 1)]) + " "
        for j in range(0, len(AgeGroups)):
            string = string + " " + str(round(PTij[i][j], 3))
        string = string + "\n"
    string = string + "\n"
    return string

def plotting(dataset, xlab, ylab, xrange, labels, group):
    for i in range(0, len(labels)):
        title = f"For the {group} Success Rate vs Age Range" + "\n" + f"for Economic Mobility Index = {labels[i]}"
        plt.figure()
        plt.bar(xrange, dataset[i], )
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.ylim(0, 1)
        figtitle = f"{group}AgeRangevs{labels[i]}.png"
        plt.savefig(figtitle)
        plt.clf()
    return 0

def hotplocket(dataset, xlab, ylab, EMI, AgeGroups, Group):
    title = "Probability of Not Passing BIO168\n Based on Demographic Pairing: " + f"{Group} Group"
    plt.cla()
    plt.imshow(dataset, interpolation = "hanning", vmin = 0, vmax = 1, aspect = "auto")
    plt.colorbar(location = "bottom")
    plt.xticks(range(len(AgeGroups)), AgeGroups)
    plt.yticks(range(len(EMI)), EMI)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.tight_layout()
    plotname = f"{Group}HeatPlot.png"
    plt.savefig(plotname)
    plt.clf()
    return 0

def NumberOfStudents(Nij, EMI, conditions, AgeGroups):
    Ntotal = 0
    NConverted = 0
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups) - 1):
            Ntotal = Nij[i][j] + Ntotal
            check = 10 * (i + 1) + (j + 1)
            if (check in conditions):
                NConverted = NConverted + Nij[i][j]
    return NConverted/Ntotal    

def CurrentBayes (NCij, PCij, N168ij, P168ij, EMI, AgeGroups):
    N168 = 0
    N090 = 0
    for i in range(0, len(EMI)):
        for j in range(0, len(AgeGroups) - 1):
            N168 = N168 + NCij[i][j] * PCij[i][j]
            N090 = N090 + N168ij[i][j] * P168ij[i][j]
    return N168/(N090 + N168)


#end of program
main()

