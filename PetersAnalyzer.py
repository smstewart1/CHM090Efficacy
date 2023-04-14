import csv
from sys import argv

# sets up global variables for input
Ethnicity = {}
Delivery = {}
CourseList = []
StudentsID = {}
StudentIDList = []
EthList = []
GenderList = []
GradeList = []
DeliveryList = []

# sets up global variables for sorter
GradeX = []
GradeY = []
DelX = []
DelY = []
Eth = []
Gen = []

OutputLaziness = ["A", "B", "C", "D", "F", "W/WE/WF/WP"]

# cutoff for the minimum number of data point for report by number of students
Cutoff = 10

def main():
    # Counts for the different courses
    N = 0

    # import files
    try:
        input = open(argv[1], "r")
    except:
        print("List the file to be read in")

    # reads in data
    with input as file:
        lines = csv.reader(file)
        next(lines)
        for row in lines:
            # loads student information
            StudentIDList.append(int(row[0]))
            EthList.append(row[7])
            GenderList.append(row[6])

            # loads course information
            Course = row[2]
            CourseList.append(int(Course[4:7]))
            GradeList.append(gradeswapper(row[8]))
            DeliveryList.append(swapper(row[5]))
            # Updates Counters
            N += 1
    # Creates lists of unique student IDs, Ethnicities, Courses, Course Numbers
    SSID = list(set(StudentIDList))
    Ethnics = list(set(EthList))

    # starts generating reports for overall performance
    for j in SSID:
        TempX = 0
        TempY = 0
        TX = 0
        TY = 0
        Teth = 0
        TGen = 0
        for i in range(0, N):
            if StudentIDList[i] == j and CourseList[i] == 151 and GradeList[i] < 4:
                TempX = GradeList[i]
                Teth = EthList[i]
                TX = DeliveryList[i]
                TGen = GenderList[i]
            if StudentIDList[i] == j and CourseList[i] == 152:
                TempY = GradeList[i]
                TY = DeliveryList[i]
        if TempX != 0 and TempY != 0:
            GradeX.append(TempX)
            GradeY.append(TempY)
            DelX.append(TX)
            DelY.append(TY)
            Eth.append(Teth)
            Gen.append(TGen)              
    print(f"Reports were omitted if the number of students was less than {Cutoff} students")
    OneFiftyOneDistribution(GradeX, CourseList)
    #distr(GradeX, GradeY)
    #distrE(GradeX, GradeY, Eth, Ethnics)
    #distrG(GradeX, GradeY, GenderList)


# converts old names for course delivery to the current definitions
def swapper(item):
    if (item == "IN"):
        string = "Online"
    elif (item == "HY" or item == "BL"):
        string = "Hybrid"
    else:
        string = "Inperson"
    return string

# converts grades to numbers
def gradeswapper(item):
    if (item == "A"):
        number = 1
    elif (item == "B"):
        number = 2
    elif (item == "C"):
        number = 3
    elif (item == "D"):
        number = 4
    elif (item == "F"):
        number = 5
    else:
        number = 6
    return number

def OneFiftyOneDistribution(GradeX, CourseList):
    N = len(GradeX)
    # gives the overall distribution for all courses given
    # sets up initial matrix
    Distribution = [0, 0, 0, 0, 0, 0, 0, 0]

    # searches for given criteria
    for i in range(0, N - 1):
        if CourseList[i] == 151:
            Distribution[GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    filename = "151GradeDistributions.txt"
    with open(filename, "w") as output:
        output.write("151 Grade Distribution")
        output.write(DistriScript(Distribution, N))
    return 0

# script for printing output to files
def DistriScript(Distribution, N):
    string = f"Grade Distribution\nN = {N}\n\nA B C D G W/WF/WP/WE\n"
    string = string + f"{Distribution[0]} {Distribution[1]} {Distribution[2]} {Distribution[3]} {Distribution[4]} {Distribution[5]}\n"
    return string


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


# the following generates the reports and are functions for specific filters
def distr(GradeX, GradeY):
    N = len(GradeX)
    # gives the overall distribution for all courses given
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N - 1):
        if (GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = "Allcourses.txt"
        with open(filename, "w") as output:
            output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
            output.write(Script(Distribution))
    return 0


# the following generates the reports based on ethnicity
def distrG(GradeX, GradeY, GenderList):
    N = len(GradeX)
    # searches for given criteria where gender is M
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
    for i in range(0, N - 1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and GenderList[i] == "M"):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = "CoursesByMale.txt"
        with open(filename, "w") as output:
            output.write("Restricted by Gender = Male\n")
            output.write(Script(Distribution))
    #female students        
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
    for i in range(0, N - 1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and GenderList[i] == "F"):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = "CoursesByFemale.txt"
        with open(filename, "w") as output:
            output.write("Restricted by Gender = Female\n")
            output.write(Script(Distribution))
    return 0


# the following generates the reports based on ethnicity
def distrE(GradeX, GradeY, Eth, Ethnics):
    N = len(GradeX)
    # searches for given criteria
    for k in Ethnics:
        Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]
        for i in range(0, N - 1):
            if (GradeX[i] < 4 and GradeY[i] < 7 and Eth[i] == k):
                # adds the student's grade to the distribution based on their grade in the subsequent course
                Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

                # counts the number of students who came in with an A, B, or C
                Distribution[3][GradeX[i] - 1] += 1

        # prints results to file ignoring if the number of data points is less than the cutoff
        if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
            filename = f"CoursesBy{k}.txt"
            with open(filename, "w") as output:
                output.write("Restricted by ethnicity\n")
                output.write(Script(Distribution))
        return 0

main()
