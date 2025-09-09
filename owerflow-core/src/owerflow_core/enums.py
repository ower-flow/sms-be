from django.db import models


class SchoolTypeEnum(models.TextChoices):
    PRIMARY = 'Primary', 'Primary'
    SECONDARY = 'Secondary', 'Secondary'
    HIGH_SCHOOL = 'High School', 'High School'


class GenderEnum(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class UserRoleEnum(models.TextChoices):
    SCHOOL_ADMIN = "schooladmin", "School Admin"
    TEACHER = "teacher", "Teacher"
    STUDENT = "student", "Student"


class ClassEnum(models.TextChoices):
    NURSERY = 'Nursery', 'Nursery'
    PREP = 'Prep', 'Prep'
    KG = 'KG', 'KG'
    CLASS_1 = '1', 'Class 1'
    CLASS_2 = '2', 'Class 2'
    CLASS_3 = '3', '3rd'
    CLASS_4 = '4', '4th'
    CLASS_5 = '5', '5th'
    CLASS_6 = '6', '6th'
    CLASS_7 = '7', '7th'
    CLASS_8 = '8', '8th'
    CLASS_9 = '9', '9th'
    CLASS_10 = '10', '10th'
