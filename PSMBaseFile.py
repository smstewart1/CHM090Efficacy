import csv
from sys import argv
from psmpy import PsmPy
from psmpy.functions import cohenD
from psmpy.plotting import *

# sets up global variables
StudentIDListX = []
StudentIDListY = []
IDC = []
GenderListX = []
GenderListY = []
GenderListC = []
EthListX = []
EthListY = []
EthListC = []
CourseX = []
CourseY = []
GradeX = []
GradeY = []
GradeC = []
DeliveryListX = []
DeliveryListY = []
DeliveryListC = []
EMIListX = []
EMIListY = []
EMIListC = []
DeliveryX = []
DeliveryY = []
TermC = []
TermT = []
OutputLaziness = ["A", "B", "C", "D", "F", "W/WE/WF/WP"]

# cutoff for the minimum number of data point for report by number of students
Cutoff = 50


def main():
    Start = 90
    Finish = 130
    psmpath = "130PSM.csv"
    # sets up global variables for sorter/swapping for output
    Grades = ["A", "B", "C", "D", "F", "W/WF/WP/WE"] # N max = 5
    DeliveryMethods = ["In Person", "Hybrid", "Online"] # N max = 2
    Gender = ["Female", "Male"] # N max = 1
    Eth = ["American Native", "Asian", "Black", "Hispanic", "Multiracial", "White"] # N max = 5
    EMI = ["Low", "Medium-Low", "Medium", "Medium-High", "High"] # N max = 4

    # import files
    try:
        input = open(argv[1], "r")
        secondinput = open(argv[2], "r")
    except:
        print("control first, treatment second")
                
    # reads in data for Grade Retention
    with secondinput as newfile:
        lines = csv.reader(newfile)
        next(lines)
        X = 0
        Y = 0
        for row in lines:
            # loads course information
            Course = row[2]
            if int(Course[4:7]) == Start and int(gradeswapper(row[3])) != 10:
                StudentIDListX.append(int(row[0]))
                #converts ethnicity to a numbrt
                EthListX.append(int(Ethswapper(row[5])))
                #give gender as number
                GenderListX.append(int(Genderswapper(row[4])))
                CourseX.append(int(Course[4:7]))
                DeliveryX.append(swapper(row[5]))
                GradeX.append(int(gradeswapper(row[3])))
                EMIListX.append(int(EMIswapper(row[8])))
                X += 1
            if int(Course[4:7]) == Finish and int(gradeswapper(row[3])) != 10:
                StudentIDListY.append(int(row[0]))
                CourseY.append(int(Course[4:7]))
                DeliveryY.append(swapper(row[5]))
                GradeY.append(int(gradeswapper(row[3])))
                EthListY.append(int(Ethswapper(row[5])))
                GenderListY.append(int(Genderswapper(row[4])))
                EMIListY.append(int(EMIswapper(row[8])))
                TermT.append(termswapper(row[1]))
                Y += 1

    # generates reports of grade retention
    # distr(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Start, Finish)
    # distrE(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Eth, EthListX, Start, Finish)
    # distrHRG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EthListX, Start, Finish)
    # distriG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Gender, GenderListX, Start, Finish)
    # distriEMI(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EMI, EMIListX, Start, Finish)

    # print(f"Reports were omitted if the number of students was less than {Cutoff} students")

    # setting up the propensity score matching base file
    PSMfile = open(psmpath, "w")
    with input as file:
        lines = csv.reader(file)
        PSMfile.write("treatment,SSID,Grade,Ethnicity,EMI,Term,Gender\n")
        next(lines)
        T = 0
        for row in lines:
            # loads course information
            if int(gradeswapper(row[3])) != 10:
                IDC.append(int(row[0]))
                #converts ethnicity to a numbrt
                EthListC.append(int(Ethswapper(row[5])))
                #give gender as number
                GenderListC.append(int(Genderswapper(row[4])))
                DeliveryListC.append(swapper(row[5]))
                GradeC.append(int(gradeswapper(row[3])))
                TermC.append(termswapper(row[1]))
                T += 1
                EMIListC.append(int(EMIswapper(row[5])))
        #writes the tretment groups
        for i in range(0, T - 1):
            if EthListC[i] != 10 and GenderListC[i] != 10 and DeliveryListC != 10 and GradeC[i] != 10 and EMIListC[i] != 0:
                PSMfile.write(f"0,{IDC[i]},{GradeC[i]},{EthListC[i]},{EMIListC[i]},{TermC[i]},{GenderListC[i]}")
                PSMfile.write("\n")
        for i in range(0, Y - 1):
            if EthListY[i] != 10 and GenderListY[i] != 10 and DeliveryListY != 10 and GradeY[i] != 10 and EMIListY[i] != 0:
                PSMfile.write(f"1,{StudentIDListY[i]},{GradeY[i]},{EthListY[i]},{EMIListY[i]},{TermT[i]},{GenderListY[i]}")
                PSMfile.write("\n")

    # start of PSM
    # reads in PSM data
    data = pd.read_csv(psmpath)
    
    #initialist the psm class
    psm = PsmPy(data, treatment = 'treatment', indx = 'SSID', exclude = ['Grade'])
    
    #calculates scores
    psm.logistic_ps(balance = True)
    
    #performs matching algorithm
    #method one
    psm.knn_matched(matcher = 'propensity_logit', replacement = False, caliper = None, drop_unmatched = True)
    
    #method two
    #psm.knn_matched_12n(matcher = 'propensity_logit', how_many = 1)
    
    #outputs a histogram of the matches
    psm.plot_match(Title = 'Side by side matched controls', Ylabel = 'Number of Students', Xlabel = 'Propensity logit', names = ['treatment', 'control'], colors = ['#E69F00', '#56B4E9'] ,save = True)
    
    #plots the effect size
    psm.effect_size_plot(title = 'Standardized Mean differences accross covariates before and after matching', before_color = '#FCB754', after_color = '#3EC8FB', save = True)
    
    #returns the matched pairs
    matches = psm.matched_ids
    matches.to_csv("MatchedPairs.csv")
    
    #returns the effect of each covariate
    matches = psm.effect_size
    matches.to_csv("EffectSize.csv")
    


######################################### Start of Functions ##########################################################
def distriEMI(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EMI, EMIList, Start, Finish):
    # searches for given criteria
    for k in range(0, len(EMI) - 1):
        # sets up initial matrix
        Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
        for i in range(0, X - 1):
            #finds all the A, B, and C grades from 090
            if GradeX[i] < 3 and EMIList[i] == k:
                for j in range(0, Y - 1):
                    if StudentIDListX[i] == StudentIDListY[j]:
                        # adds the student's grade to the distribution based on their grade in the subsequent course
                        Distribution[GradeX[i]][GradeY[j]] += 1
                        # counts the number of students who came in with an A, B, or C
                        Distribution[3][GradeX[i]] += 1
        # prints results to file ignoring if the number of data points is less than the cutoff
        if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
            filename = f"{Start}_to_{Finish}_EMI_{EMI[k]}.txt"
            with open(filename, "w") as output:
                output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
                output.write(Script(Distribution))
    return 0

def distriG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Gender, GenderList, Start, Finish):
    # searches for given criteria
    for k in range(0, 2):
        # sets up initial matrix
        Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
        for i in range(0, X - 1):
            #finds all the A, B, and C grades from 090
            if GradeX[i] < 3 and GenderList[i] == k:
                for j in range(0, Y - 1):
                    if StudentIDListX[i] == StudentIDListY[j]:
                        # adds the student's grade to the distribution based on their grade in the subsequent course
                        Distribution[GradeX[i]][GradeY[j]] += 1
                        # counts the number of students who came in with an A, B, or C
                        Distribution[3][GradeX[i]] += 1
        # prints results to file ignoring if the number of data points is less than the cutoff
        if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
            filename = f"{Start}_to_{Finish}_Eth_{Gender[k]}.txt"
            with open(filename, "w") as output:
                output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
                output.write(Script(Distribution))
    return 0

# the following generates the reports and are functions for specific filters
def distrE(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Eth, EthList, Start, Finish):
    # searches for given criteria
    for k in range(0, 6):
        # sets up initial matrix
        Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
        for i in range(0, X - 1):
            #finds all the A, B, and C grades from 090
            if GradeX[i] < 3 and EthList[i] == k:
                for j in range(0, Y - 1):
                    if StudentIDListX[i] == StudentIDListY[j]:
                        # adds the student's grade to the distribution based on their grade in the subsequent course
                        Distribution[GradeX[i]][GradeY[j]] += 1
                        # counts the number of students who came in with an A, B, or C
                        Distribution[3][GradeX[i]] += 1
        # prints results to file ignoring if the number of data points is less than the cutoff
        if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
            filename = f"{Start}_to_{Finish}_Eth_{Eth[k]}.txt"
            with open(filename, "w") as output:
                output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
                output.write(Script(Distribution))
    return 0

# the following generates the reports and are functions for specific filters
def distrHRG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EthList, Start, Finish):
    # gives the overall distribution for all courses given
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, X - 1):
        #finds all the A, B, and C grades from 090
        if (GradeX[i] < 3 and (EthList[i] == 0 or EthList[i] == 3 or EthList[i] == 2 or EthList[i] == 4)):
            for j in range(0, Y - 1):
                if StudentIDListX[i] == StudentIDListY[j]:
                    # adds the student's grade to the distribution based on their grade in the subsequent course
                    Distribution[GradeX[i]][GradeY[j]] += 1
                    # counts the number of students who came in with an A, B, or C
                    Distribution[3][GradeX[i]] += 1
    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{Start}_to_{Finish}_HRG.txt"
        with open(filename, "w") as output:
            output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
            output.write(Script(Distribution))
    return 0

# the following generates the reports and are functions for specific filters
def distr(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Start, Finish):
    # gives the overall distribution for all courses given
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, X - 1):
        #finds all the A, B, and C grades from 090
        if (GradeX[i] < 3):
            for j in range(0, Y - 1):
                if StudentIDListX[i] == StudentIDListY[j]:
                    # adds the student's grade to the distribution based on their grade in the subsequent course
                    Distribution[GradeX[i]][GradeY[j]] += 1
                    # counts the number of students who came in with an A, B, or C
                    Distribution[3][GradeX[i]] += 1
    # prints results to file ignoring if the number of data points is less than the cutoff
    if (Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff):
        filename = f"{Start}_to_{Finish}_all.txt"
        with open(filename, "w") as output:
            output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
            output.write(Script(Distribution))
    return 0


# converts old names for course delivery to the current definitions
def swapper(item):
    if (item == "IN"):
        value = 0
    elif (item == "HY" or item == "BL"):
        value = 1
    else:
        value = 2
    return value


# script for printing output to files
def Script(array):
    string = f"Grade in First Course Followed by Grade in Next Course \nN = {array[3][0] + array[3][1] + array[3][2]}\nn = "
    string = string + f"{array[3][0]} {array[3][1]} {array[3][2]}\nGrade A B C \n"
    for i in range(0, 6):
        string = string + f"{OutputLaziness[i]} "
        for j in range(0, 3):
            if array[3][j] == 0:
                string = string + "-- "
            else:
                string = string + f"{array[j][i]/array[3][j] * 100:.2f}% "
        string = string + "\n"
    return string


#converts ethnicity to a number
def EMIswapper(item):
    if item == "Low":
        value = 0
    elif item == "Medium-Low": 
        value = 1
    elif item == "Medium":
        value = 2
    elif item == "Medium-High":
        value = 3
    elif item == "High":
        value = 4
    else:
        value = 10
    return value

#Converts EMI to a number 0 (lowest) to 4 (highest)
def Ethswapper(item):
    if item == "AN":
        value = 0
    elif item == "AS": 
        value = 1
    elif item == "BL":
        value = 2
    elif item == "HIS":
        value = 3
    elif item == "MULTI":
        value = 4
    elif item == "WH":
        value = 5
    else:
        value = 10
    return value

#converts gender to a number
def Genderswapper(item):
    if item == "M":
        value = 0
    elif item == "F": 
        value = 1
    else:
        value = 10
    return value

# converts grades to numbers
def gradeswapper(item):
    if (item == "A"):
        number = 0
    elif (item == "B"):
        number = 1
    elif (item == "C"):
        number = 2
    elif (item == "D"):
        number = 3
    elif (item == "F"):
        number = 4
    elif (item == "W" or item == "WP" or item == "WF" or item == "WE"):
        number = 5
    else:
        number = 10
    return number

# converts semesters to numbers
def termswapper(item):
    partone = item[2:4]
    if item[4:6] == "SP":
        parttwo = 0
    elif item[4:6] == "SU":
        parttwo = 3
    elif item[4:6] == "FA":
        parttwo = 6
    number = int(partone)*10 + parttwo
    return number


main()
