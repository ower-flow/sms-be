from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from owerflow_core.enums import UserRoleEnum
from owerflow_core.models import BaseModel

# def teacher_avatar_upload_path(instance, filename):
#     return f"teacher/avatars/{instance.employee_id}/{filename}"


class Teacher(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    school = models.ForeignKey(
        "school.School",
        on_delete=models.CASCADE,
        related_name="teachers",
    )
    employee_id = models.CharField(
        max_length=32,
        help_text="Unique per school.",
        unique=True,
        db_index=True,
    )

    class Meta:
        # Per-tenant uniqueness
        constraints = [
            models.UniqueConstraint(
                fields=["school", "employee_id"],
                name="teacher_unique_employee_id_per_school",
            ),
            models.UniqueConstraint(
                fields=["school", "user"],
                name="teacher_unique_user_per_school",
            ),
        ]
        indexes = [
            models.Index(fields=["school", "employee_id"]),
            models.Index(fields=["school"]),
        ]
        ordering = ["user__first_name", "user__last_name"]

    def clean(self):
        super().clean()
        # Ensure the linked user has the TEACHER role
        if getattr(self.user, "role", None) != UserRoleEnum.TEACHER:
            raise ValidationError("Linked user must have role 'teacher'.")
        # If you also link users to schools elsewhere, enforce match here if applicable.

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    @property
    def full_name(self):
        return (self.user.get_full_name() or self.user.username or "").strip()



# class AssignClassToTeacher(models.Model):
#     teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)
#     # klasses = models.ManyToManyField('academic.Klass')
#     assigned_on = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.teacher} → Classes: {', '.join(k.name for k in self.klasses.all())}"
#
# class AssignSubjectToTeacher(models.Model):
#     teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)
#     # subjects = models.ManyToManyField('subject.Subject')
#     assigned_on = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.teacher} → Subjects: {', '.join(s.name for s in self.subjects.all())}"
#
#
#
# class AttendanceStatus(models.Model):
#     name = models.CharField(
#         max_length=255,
#         unique=True,
#         help_text='"Present" will not be saved but show as an option for admins.',
#     )
#     code = models.CharField(
#         max_length=10,
#         unique=True,
#         help_text="Short code used on attendance reports. Example: 'A' might be the code for 'Absent'.",
#     )
#     present = models.BooleanField(default=False)
#     excused = models.BooleanField(default=False)
#     absent = models.BooleanField(
#         default=False, help_text="Used for different types of absent statuses."
#     )
#     late = models.BooleanField(
#         default=False, help_text="Used for tracking late statuses."
#     )
#     half = models.BooleanField(
#         default=False,
#         help_text="Indicates half-day attendance. Do not check absent, otherwise it will double count.",
#     )
#
#     class Meta:
#         verbose_name_plural = "Attendance Statuses"
#
#     def __str__(self):
#         return self.name
#
# class TeachersAttendance(models.Model):
#     school = models.ForeignKey(
#         'school.School',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='teacher_attendance'
#     )
#     date = models.DateField(blank=True, null=True, validators=[no_future_date])
#     teacher = models.ForeignKey(Teacher, blank=True, on_delete=models.CASCADE)
#     time_in = models.TimeField(blank=True, null=True)
#     time_out = models.TimeField(blank=True, null=True)
#     status = models.ForeignKey(
#         AttendanceStatus,
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#         help_text="Select status like Present, Absent, Late etc.",
#     )
#     notes = models.CharField(max_length=500, blank=True)
#     edit_count = models.PositiveIntegerField(default=0)
#     last_edit_date = models.DateField(null=True, blank=True)
#
#     class Meta:
#         unique_together = (("teacher", "date"),)
#         ordering = ("-date", "teacher")
#
#     def __str__(self):
#         return f"{self.teacher} - {self.date} {self.status}"
#
#     @property
#     def edit(self):
#         return f"Edit {self.teacher} - {self.date}"
#
#     @property
#     def editable(self):
#         """Check if this attendance is editable (within 3 days)"""
#         return self.date >= datetime.date.today() - datetime.timedelta(days=3)
#
#
#     @property
#     def is_late(self):
#         """
#         Returns True if status is Present and time_in is after 7:00 AM.
#         """
#         present_status = AttendanceStatus.objects.filter(name__iexact="Present").first()
#         return (
#             self.status == present_status
#             and self.time_in
#             and self.time_in > datetime.time(7, 0)
#         )
#
# class AttendanceEditLog(models.Model):
#     attendance = models.ForeignKey("teacher.TeachersAttendance", on_delete=models.CASCADE, related_name='edit_logs')
#     edited_at = models.DateTimeField(auto_now_add=True)
#     changes = models.TextField()  # plain text summary or JSON if preferred
#
#     class Meta:
#         ordering = ['-edited_at']
