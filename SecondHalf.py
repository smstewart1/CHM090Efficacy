import csv
from sys import argv

# sets up global variables
StudentIDListX = []
StudentIDListY = []
StudentIDList = []
GenderList = []
EthList = []
CourseX = []
CourseY = []
GradeX = []
GradeY = []
DeliveryList = []
EMIList = []
DeliveryX = []
DeliveryY = []
StudentID = []
OutputLaziness = ["A", "B", "C", "D", "F", "W/WE/WF/WP"]

# cutoff for the minimum number of data point for report by number of students
Cutoff = 50


def main():
    Start = 90
    Finish = 168
    # sets up global variables for sorter/swapping for output
    Grades = ["A", "B", "C", "D", "F", "W/WF/WP/WE"] # N max = 5
    DeliveryMethods = ["In Person", "Hybrid", "Online"] # N max = 2
    Gender = ["Female", "Male"] # N max = 1
    Eth = ["American Native", "Asian", "Black", "Hispanic", "Multiracial", "White"] # N max = 5
    EMI = ["Low", "Medium-Low", "Medium", "Medium-High", "High"] # N max = 4

    # import files
    try:
        input = open(argv[1], "r")
    except:
        print("List the file to be read in")

    # reads in data
    with input as newfile:
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
                EthList.append(int(Ethswapper(row[5])))
                #give gender as number
                GenderList.append(int(Genderswapper(row[4])))
                CourseX.append(int(Course[4:7]))
                DeliveryX.append(swapper(row[5]))
                GradeX.append(int(gradeswapper(row[3])))
                X += 1
            if int(Course[4:7]) == Finish and int(gradeswapper(row[3])) != 10:
                StudentIDListY.append(int(row[0]))
                CourseY.append(int(Course[4:7]))
                DeliveryY.append(swapper(row[5]))
                GradeY.append(int(gradeswapper(row[3])))
                Y += 1
            #converts EMI to an integer
            EMIList.append(int(EMIswapper(row[8])))
            # Updates Counters
    print(f"{X} {Y}")
    # starts generating reports for overall performance
    distr(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Start, Finish)
    distrE(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Eth, EthList, Start, Finish)
    distrHRG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EthList, Start, Finish)
    distriG(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, Gender, GenderList, Start, Finish)
    distriEMI(X, Y, GradeX, GradeY, StudentIDListX, StudentIDListY, EMI, EMIList, Start, Finish)

    print(f"Reports were omitted if the number of students was less than {Cutoff} students")


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
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
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


main()
