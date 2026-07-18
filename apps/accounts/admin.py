from django.contrib import admin
from .models import UserAccount,UserRole, PasswordResetToken


admin.site.register(UserAccount)
admin.site.register(PasswordResetToken)