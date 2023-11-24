class Student:
    _registry = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self._registry.append(self)

    @classmethod

    def all_instances(cls):
        return cls._registry

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lectors(self, lector, course, grade):
        if isinstance(lector, Lecturer) and course in lector.courses_attached and course in self.courses_in_progress:
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_avg(self, list_of_list_grades):
        list_grades = []
        for grades in list_of_list_grades:
            list_grades.append(sum(grades) / len(grades))
        return round(sum(list_grades) / len(list_grades), 1)

    def __lt__(self, other):
        return self.get_avg(list(self.grades.values())) < other.get_avg(list(other.grades.values()))

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за "
                f"домашние задания: {self.get_avg(list(self.grades.values()))} \n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}"
                f"\nЗавершенные курсы: {', '.join(self.finished_courses)} ")


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    _registry = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self._registry.append(self)

    @classmethod

    def all_instances(cls):
        return cls._registry

    def get_avg(self, list_of_list_grades):
        list_grades = []
        for grades in list_of_list_grades:
            list_grades.append(sum(grades) / len(grades))
        return round(sum(list_grades) / len(list_grades), 1)

    def __lt__(self, other):
        return self.get_avg(list(self.grades.values())) < other.get_avg(list(other.grades.values()))

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self.get_avg(list(self.grades.values()))}")


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# функции по п.4 д.з.
def get_avg_cours(list_students, cours_name):
    sum_1, count_1 = 0, 0
    for student in list_students:
        for grade in list(student.grades.get(cours_name)):
            sum_1 += grade
            count_1 += 1

    return round(sum_1 / count_1, 1)


def get_avg_lectors(list_lectors, cours_name):
    sum_2, count_2 = 0, 0
    for lector in list_lectors:
        for grade in list(lector.grades.get(cours_name)):
            sum_2 += grade
            count_2 += 1

    return round(sum_2 / count_2, 1)


# Основной код.
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.finished_courses += ['Git']
best_student.courses_in_progress += ['Python']
best_student.grades['Git'] = [10, 5, 10, 5, 10]
best_student.grades['Python'] = [10, 10]

cool_mentor = Reviewer('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
cool_mentor.rate_hw(best_student, 'Python', 7)
cool_mentor.rate_hw(best_student, 'Python', 8)
cool_mentor.rate_hw(best_student, 'Python', 9)

cool_lector = Lecturer('Jon', 'Smith')
cool_lector.courses_attached += ['Python']

best_student.rate_lectors(cool_lector, 'Python', 10)
best_student.rate_lectors(cool_lector, 'Python', 5)
best_student.courses_in_progress += ['Meditation']

second_student = Student('Oleg', 'Barygin', 'your_gender')
second_student.finished_courses += ['Git']
second_student.courses_in_progress += ['Python']
second_student.grades['Git'] = [1, 2, 1, 5, 3]
second_student.grades['Python'] = [4, 4]

second_lector = Lecturer('Andrew', 'Second')
second_lector.courses_attached += ['Python']

best_student.rate_lectors(second_lector, 'Python', 1)
best_student.rate_lectors(second_lector, 'Python', 2)

print('переназначение _str_ и печать студентов')
print(best_student)
print()
print(second_student)
print()

print('переназначение _str_ и печать менторов')
print(cool_mentor)
print()
print(cool_lector)
print()

print('переназначение оператора и сравнение экземпляров класса')
print(f'результат сравнения студентов {second_student.surname} < {best_student.surname}:'
      f' {second_student < best_student}')
print(f'результат сравнения студентов {best_student.surname} < {second_student.surname}:'
      f' {best_student < second_student}')
print(f'результат сравнения лекторов {second_lector.surname} < {cool_lector.surname}:'
      f' {second_lector < cool_lector}')
print(f'результат сравнения лекторов {cool_lector.surname} < {second_lector.surname}:'
      f' {cool_lector < second_lector}')
print()

# 4.1. функция подсчета средней оценки за домашние задания по всем студентам в рамках курса.
cours_name = 'Git'
list_students = []
for student in Student.all_instances():
    list_students.append(student)
print(f'средний бал студентов по курсу {cours_name} {get_avg_cours(list_students, cours_name)}')

# 4.2. функция подсчета средней оценки за лекции всех лекторов в рамках курса.
cours_name = 'Python'
list_lectors = []
for lector in Lecturer.all_instances():
    list_lectors.append(lector)
print(f'средний бал лекторов по курсу {cours_name} {get_avg_lectors(list_lectors, cours_name)}')