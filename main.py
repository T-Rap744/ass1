def main():
    # List Courses
    courses = [{'Course code': 'EC205', 'Days': 'MM', 'Slots': '34', 'Quotas': 3, 'Participants': 0},
               {'Course code': 'EC48T', 'Days': 'MMM', 'Slots': '567', 'Quotas': 3, 'Participants': 0},
               {'Course code': 'EC48J', 'Days': 'TTT', 'Slots': '123', 'Quotas': 3, 'Participants': 0},
               {'Course code': 'EC331', 'Days': 'WWW', 'Slots': '567', 'Quotas': 3, 'Participants': 0},
               {'Course code': 'EC481', 'Days': 'ThTh', 'Slots': '12', 'Quotas': 2, 'Participants': 0},
               {'Course code': 'EC406', 'Days': 'ThTh', 'Slots': '34', 'Quotas': 2, 'Participants': 0},
               {'Course code': 'EC48Z', 'Days': 'ThTh', 'Slots': '67', 'Quotas': 2, 'Participants': 0},
               {'Course code': 'EC381', 'Days': 'TT', 'Slots': '34', 'Quotas': 1, 'Participants': 0},
               {'Course code': 'EC411', 'Days': 'WW', 'Slots': '45', 'Quotas': 1, 'Participants': 0},
               {'Course code': 'EC350', 'Days': 'TT', 'Slots': '34', 'Quotas': 3, 'Participants': 0}]
    # Student list and list for their courses
    students = []
    studentCourses = []
    # Add students
    addStudent(students, studentCourses, "Ahmet", 2115300000, '1234', 3.55, 7, 'Economics'),
    addStudent(students, studentCourses, 'Buse', 2015300001, '4321', 2.72, 5, 'Economics'),
    addStudent(students, studentCourses, 'Can', 2015300002, '3412', 3.14, 6, 'Management'),
    addStudent(students, studentCourses, 'Deniz', 2015300003, '1122', 2.56, 6, 'Political Science'),
    addStudent(students, studentCourses, 'Emmre', 2015300004, '1313', 3.70, 8, 'Economics')
    # Run program
    runProgram(students, courses, studentCourses)


# This function makes it easy to create a signup function or an admin account to add more students
def addStudent(studentList, studentCourses, name, studentID, password, gpa, semester, department):
    studentList.append({'Name': name, 'ID': int(studentID), 'Password': str(password),
                        'GPA': float(gpa), 'Semester': int(semester), 'Department': department})
    studentCourses.append([])  # Add spot in courses lis for student


def runProgram(students, courses, studentCourses):
    run = True
    while run:
        print('--- Welcome to BONDAGE REGISTRATION ---\n\n1. Login\n2. Exit\n')
        select = input()
        if select == '1':
            idInput = input('\nUser Name: ')
            password = input('\nPassword: ')
            result, pos = checkValidity(students, idInput, password)
            if result:
                logIn(students[pos], courses, studentCourses[pos])  # Pos = position for student in list
        elif select == '2':
            run = False
        else:
            print('Error: Invalid selection, please try again!\n\n\n')


def checkValidity(students, studentID, password):
    pos = 0
    result = False
    for i in range(len(students)):
        if students[i]['ID'] == int(studentID) \
                and students[i]['Password'] == str(password):
            result = True
            pos = i
    if not result:
        print('\nID or Password is incorrect!\n\n')

    return result, pos


def logIn(student, courses, studentCourses):
    stayLoggedIn = True
    while stayLoggedIn:
        print('Welcome ' + student['Name'] + '!\n')
        print('Please enter the number of the service:\n\n')
        print('\t1. Course List Preperation\n' +
              '\t2. Courses and Quotas\n' +
              '\t3. My Schedule\n' +
              '\t4. My Account Information\n' +
              '\t5. Logout\n')
        select = input()
        if select == '1':
            addOrDropCourse(courses, studentCourses)
        elif select == '2':
            coursesAndQuotas(courses)
        elif select == '3':
            schedule(courses, studentCourses)
        elif select == '4':
            accountInformation(student)
        elif select == '5':
            stayLoggedIn = False
        else:
            print('Error: Invalid selection, try again!\n\n\n')


def addOrDropCourse(courses, studentCourses):
    print('1. Add course\n' +
          '2. Drop course\n')
    select = input()
    if select == '1':
        addCourse(courses, studentCourses)
    elif select == '2':
        dropCourse(courses, studentCourses)
    else:
        print('Error: Invalid selection, try again!\n\n\n')
    backToMain()


def addCourse(courses, studentCourses):
    courseCode = input('Please enter the course code you want to add: ')
    if checkNotInList(studentCourses, courseCode) \
            and checkNoCollision(courses, studentCourses, courseCode) \
            and checkQuota(courses, courseCode):
        canAdd = True
    else:
        if not courseExists(courses, courseCode):
            print('\nCourse with name \'' + courseCode + '\' does not exist and will not be added!')
        canAdd = False
    if canAdd:
        studentCourses.append(courseCode)
        addParticipant(courses, courseCode)
        print('Course added\n\n\n')


def courseExists(courses, courseCode):
    exists = False  # Assume it does not exist
    for i in range(len(courses)):
        if courseCode in courses[i].values():
            exists = True  # Find that it does exist
    return exists


def checkNoCollision(courses, studentCourses, courseCode):
    courseCodeDays, courseCodePeriods = getCourseDaysAndPeriods(courses, courseCode)
    for i in range(len(studentCourses)):
        for j in range(len(courses)):
            if studentCourses[i] == courses[j]['Course code']:
                days = returnListOfDays(courses[j]['Days'])
                periods = list(courses[i]['Slots'])
                # Only check first day and period as this dataset will not overlap anyway
                if courseCodeDays[0] == days[0]:
                    if periodCollision(courseCodePeriods, periods):
                        print(courseCode + ' is in conflict with ' + studentCourses[i] +
                              ' and will not be added!\n\n\n')
                        return False
    return True


def periodCollision(courseCodePeriods, periods):
    for i in range(len(courseCodePeriods)):
        for j in range(len(periods)):
            if courseCodePeriods[i] == periods[j]:
                return True
    return False


def getCourseDaysAndPeriods(courses, courseCode):
    days = ['n']  # Adding reference to avoid errors
    periods = ['0']
    for i in range(len(courses)):
        if courses[i]['Course code'] == courseCode:
            days = returnListOfDays(courses[i]['Days'])
            periods = list(courses[i]['Slots'])
    return days, periods


def returnListOfDays(days):  # Need this to filter out Thursday as Th
    listOfDays = list(days)
    newListOfDays = []
    for i in range(len(listOfDays)):
        isItThursday = False
        if i < len(listOfDays) - 1:  # Avoid going out of bounds
            if listOfDays[i + 1] == 'h':
                isItThursday = True
                i += 1
        if isItThursday:
            newListOfDays.append('Th')
        else:
            newListOfDays.append(listOfDays[i])
    return newListOfDays


def checkNotInList(studentCourse, courseCode):
    for i in range(len(studentCourse)):
        if studentCourse[i] == courseCode:
            print(courseCode + ' is already in your list.\n\n\n')
            return False
    return True


def checkQuota(courses, courseCode):
    for i in range(len(courses)):
        if courses[i]['Course code'] == courseCode:
            if courses[i]['Participants'] >= courses[i]['Quotas']:
                print('There is no quota left')
                return False
            else:
                return True


def addParticipant(courses, courseCode):
    for i in range(len(courses)):
        if courses[i]['Course code'] == courseCode:
            courses[i]['Participants'] += 1
            break


def dropCourse(courses, studentCourse):
    drop = input('Please enter the course you would like to drop: ')
    if isCourseOnList(studentCourse, drop):
        studentCourse.remove(drop)
        removeParticipant(courses, drop)
    print('Course dropped!\n\n\n')


def removeParticipant(courses, drop):
    for i in range(len(courses)):
        if courses[i]['Course code'] == drop:
            courses[i]['Participants'] -= 1
        break


def isCourseOnList(studentCourse, courseCode):
    for i in range(len(studentCourse)):
        if studentCourse[i] == courseCode:
            return True
    print(courseCode + ' is not on your list.\n\n\n')
    return False


def coursesAndQuotas(courses):
    selectCourse = input('Please enter the course code: ')
    for i in range(len(courses)):
        if courses[i]['Course code'] == selectCourse:
            print('\n\n' + courses[i]['Course code'] + '\n\n' +
                  'Total Quota: ' + str(courses[i]['Quotas']) + '\n\n' +
                  'Registered: ' + str(courses[i]['Participants']) + '\n\n' +
                  'Days ' + returnDaysForCourse(courses, i) + '\n\n' +
                  'Slots ' + returnPeriodsForCourse(courses, i) + '\n\n')
    backToMain()


def returnDaysForCourse(courses, iteration):
    dayList = list(courses[iteration]['Days'])
    returnString = ''
    for i in range(len(dayList)):
        returnString += dayList[i]
        if i < len(dayList) - 1:
            if dayList[i + 1] == 'h':
                returnString += dayList[i]
                i += 1
        if i < len(dayList) - 1:
            returnString += ','
    return returnString


def returnPeriodsForCourse(courses, iteration):
    periodList = list(courses[iteration]['Slots'])
    returnString = ''
    for i in range(len(periodList)):
        returnString += str(periodList[i])
        if i < len(periodList) - 1:
            returnString += ','
    return returnString


def schedule(courses, studentCourses):
    listOfDays = [('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'),
                  ('Th', 'Thursday'), ('F', 'Friday')]
    for i in range(len(listOfDays)):
        printDayInfo(courses, studentCourses, listOfDays[i])
    backToMain()


def printDayInfo(courses, studentCourses, day):
    listOfThisDaysCourses = findCurrentDayCourses(courses, studentCourses, day)
    buildString = '\n\n' + day[1] + ':'
    if len(listOfThisDaysCourses) > 0:
        for i in range(len(listOfThisDaysCourses)):
            buildString += ' ' + listOfThisDaysCourses[i] + '(' + \
                           returnPeriodsForDay(courses, listOfThisDaysCourses[i]) + ')'
            if i < len(listOfThisDaysCourses) - 1:
                buildString += ','
    print(buildString)


def returnPeriodsForDay(courses, thisCourse):
    slots = ''
    for i in range(len(courses)):
        if courses[i]['Course code'] == thisCourse:
            slots = list(courses[i]['Slots'])
            break
    formattedSlots = ''
    for i in range(len(slots)):
        formattedSlots += slots[i]
        if i < len(slots) - 1:
            formattedSlots += ','
    return formattedSlots


def findCurrentDayCourses(courses, studentCourses, day):
    coursesOfTheDay = []
    slots = []
    for i in range(len(courses)):
        for j in range(len(studentCourses)):
            if courses[i]['Course code'] == studentCourses[j]:
                if returnListOfDays(courses[i]['Days'])[0] == day[0]:
                    coursesOfTheDay.append(courses[i]['Course code'])
                    slots.append(courses[i]['Slots'])
    if len(coursesOfTheDay) == 0:
        coursesOfTheDay = []  # Create empty list to avoid None in print
    if len(coursesOfTheDay) > 1:
        coursesOfTheDay = sortCoursesByPeriod(coursesOfTheDay, slots)
    return coursesOfTheDay


def sortCoursesByPeriod(coursesOfTheDay, slotsOfTheDay):
    indexes = []
    sortedCourses = []
    for i in range(len(coursesOfTheDay)):
        smallest = 999
        for j in range(len(coursesOfTheDay)):
            if int(list(slotsOfTheDay[j])[0]) < smallest and j not in indexes:
                smallest = int(list(slotsOfTheDay[j])[0])  # Only need to check for first period, non of them overlap
                loopIndex = j  # unless they start at the same period
        indexes.append(loopIndex)
        sortedCourses.append(coursesOfTheDay[loopIndex])
    return sortedCourses


def accountInformation(student):
    print('Student ID: ' + str(student['ID']) + '\n\n' +
          'Name: ' + student['Name'] + '\n\n' +
          'GPA: ' + str(student['GPA']) + '\n\n' +
          'Semester: ' + str(student['Semester']) + '\n\n' +
          'Department: ' + student['Department'] + '\n\n')
    backToMain()


def backToMain():
    print('\nGoing back to main menu!\n\n\n')


main()
