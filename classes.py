# # class Person:
# #     def __init__(self, name, age, gender):
# #         self.name =name
# #         self.age=age
# #         self.gender=gender
# #
# #     def speak(self, word):
# #         print(f"{self.name } said {word}")
# #
# # Anna= Person("Anna",15,"Female")
# #
# # print(Anna.age)
# # Anna.speak("HIII")
#
#
# class Person:
#     def __init__(self, name, age, group, faculty):
#         self.name=name
#         self.age=age
#         self.group=group
#         self.faculty=faculty
#     def info(self):
#         print(f"{self.name} age {self.age}  group of {self.group}  faculty {self.faculty}")
#
#
# Students=[
#     Person("Anna",17,"DINJ","Information Technologies"),
#     Person("Jhon",20,"KIDT","Information Technologies"),
#     Person("Ali",22,"DINJ","Information Technologies"),
#     Person("Vali",29,"KIDT","Information Technologies"),
#     Person("Khan",19,"DINJ","Information Technologies")
# ]
# count=0
# for student in Students:
#     # student.info()
#     if student.faculty=="Information Technologies":
#         count+=1
# print(count)


# class Test:
#     def __init__(self, x):
#         self.x = x
#
#     def change(self, x):
#         self.x = x
#
# a = Test(5)
# b = Test(10)
#
# a.change(20)
# print(a.x, b.x)


#
# class device:
#     def __init__(self, name ):
#         self.name = name
#
#     def off(self):
#         print(f"{self.name} o'chirildi")
#
#     def on(self):
#         print(f"{self.name} yonodindi")
#
# class Phone(device):
#     def __init__(self, brand, mp):
#         super().__init__(brand)
#         self.mp=mp
#
#     def Photo(self):
#         print(f"{self.name} rasmga oldi pikseli {self.mp}")
#
#
# class Laptop(device):
#     def __init__(self,brand, ram):
#         super().__init__(brand)
#         self.ram=ram
#
#     def info(self):
#         print(f"{self.name} ning tezkor xotirasi {self.ram}")
#
#
# hp=Laptop("HP",16)
# hp.info()
#

#
#
#
# class Person:
#     def __init__(self,name , age, pasportid):
#         self.name =name
#         self.age=age
#         self.pasportid=pasportid
#
#     def info(self):
#         print(f"""Ism: {self.name}
#             Yoshi: {self.age}
#             Pasport malumoti: {self.pasportid}""" )
#
#
# class Student(Person):
#     def __init__(self,name,age,pasportid,group,gpi,subjects):
#         super().__init__(name,age,pasportid)
#         self.group=group
#         self.gpi=gpi
#         self.subjects=subjects
#
#     def info(self):
#         print(f"{self.name}  {self.group} guruhida o'qiydi va {self.age} yoshda PassportId {self.pasportid} ")
#
#
# class Teacher(Person):
#     def __init__(self,name,age,subject,pasportid,experienceyear):
#         super().__init__(name,age,pasportid)
#         self.subject=subject
#         self.experienceyear=experienceyear
#
#     def info(self):
#         print(f"O'qituvchi : {self.name}  {self.subject} fanidan {self.experienceyear} yillik tajribaga ega ")


def my_decorator(func):
    def wrapper(name):
        print("Boshladi")
        func(name)
        print("Tugadi")
    return wrapper

@my_decorator
def greet(name):
    print(f"Salom {name}")

greet("Ali")

