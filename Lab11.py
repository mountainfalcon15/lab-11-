import os
import matplotlib.pyplot as plt

base_dir = os.path.dirname(__file__)
file_path_students = os.path.join(base_dir, 'data', 'students.txt')
file_path_assignments = os.path.join(base_dir, 'data', 'assignments.txt')
file_path_submissions = os.path.join(base_dir, 'data', 'submissions')

def get_id(name):
    with open(file_path_students) as f:
        lines = f.read().splitlines()
    for line in lines:
        if line[3:] == name:
            return line[:3]
    return False

def get_assignment_id(name):
    with open(file_path_assignments) as f:
        lines = f.read().splitlines()
        count, assignment_id = 0, ''
        for line in lines:
            if count == 0:
                assignment_name = line
            if count == 1:
                if name == assignment_name:
                    return line
            if count == 2:
                pass
                count = -1
            count += 1
    return False

with open(file_path_assignments) as f:
    lines = f.read().splitlines()
    count, assignment, weight = 0,0,0
    assignment_list = []
    for line in lines:
        if count == 0:
            pass
        if count == 1:
            assignment = line
        if count == 2:
            weight = line
            count = -1
            assignment_list.append((int(assignment),int(weight)/1000))
        count += 1

def get_weight(assignment_id):
    for assignment in assignment_list:
        if int(assignment[0]) == int(assignment_id):
            return assignment[1]
    return False

def get_average(id):
    grade = 0
    for file in os.scandir(file_path_submissions):
        with open(file) as f:
            line = f.readline()
            if int(line[:3]) == int(id):
                grade+=(get_weight(line[4:line[4:].index('|')+4]) * int(line[line[4:].index('|')+5:])) #weight(id) * grade
    return round(grade)

def get_assignment_average(assignment_id):
    grade_bank = [0,100, 0] #highest, lowest, average
    count = 0
    for file in os.scandir(file_path_submissions):
        with open(file) as f:
            line = f.readline()
            if (int(line[4:line[4:].index('|')+4]) == int(assignment_id)):
                grade = int(line[line[4:].index('|')+5:]) #weight(id) * grade
                grade_bank[2] += grade
                count += 1
                if grade < grade_bank[1]:
                    grade_bank[1] = grade
                if grade > grade_bank[0]:
                    grade_bank[0] = grade
    grade_bank[2] /= count
    return f"Min: {grade_bank[1]}%\nAvg: {(grade_bank[2])}%\nMax: {round(grade_bank[0])}%"

def get_assignment_scores(assignment_id):
    grades = []
    for file in os.scandir(file_path_submissions):
        with open(file) as f:
            line = f.readline()
            if (int(line[4:line[4:].index('|')+4]) == int(assignment_id)):
                grade = int(line[line[4:].index('|')+5:]) #weight(id) * grade
                grades.append(grade)
    return grades



while True:
    print('1. Student grade')
    print('2. Assignment statistics')
    print('3. Assignment graph')
    selection = int(input('\nEnter your selection: '))
    if selection == 1:
        name = input("What is the student's name: ")
        if get_id(name):
            print(f'{get_average(get_id(name))}%')
        else:
            print('Student not found')
    if selection == 2:
        name = input('What is the assignment name: ')
        if get_assignment_id(name):
            print(get_assignment_average(get_assignment_id(name)))
        else:
            print('Assignment not found')
    if selection == 3:
        name = input('What is the assignment name: ')
        if get_assignment_id(name):
            scores = get_assignment_scores(get_assignment_id(name))
            plt.hist(scores, bins=[50,55,60,65,70,75,80,85,90,95,100])
            plt.show()
        else:
            print('Assignment not found')
    break

