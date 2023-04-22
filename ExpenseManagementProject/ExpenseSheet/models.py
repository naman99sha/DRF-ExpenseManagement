from django.db import models
from Users.models import User
# Create your models here.
transactTypes = (
    ("Debit","Debit"),
    ("Credit","Credit")
)

class ExpenseUserData(models.Model):
    userObj = models.ForeignKey(User, on_delete=models.CASCADE, related_name="EUD_userObj", unique=True, null=True)
    bankBalance = models.BigIntegerField(default=0)
    bankName = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.userObj.name or None} - {self.bankBalance} Rs"
    
class ExpenseEntry(models.Model):
    userObj = models.ForeignKey(ExpenseUserData, on_delete=models.CASCADE, related_name="EE_userObj", null=True)
    title = models.CharField(max_length=255, null=True)
    transactionType = models.CharField(max_length=255, choices=transactTypes, default="Debit")
    date = models.DateField(null=True)
    amount = models.BigIntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.userObj.userObj.name or None} - {self.title} - {self.transactionType} - {self.date} - {self.amount}"

    def save(self):
        obj = self.userObj
        if self.transactionType == "Debit":
            obj.bankBalance -= self.amount
        else:
            obj.bankBalance += self.amount
        obj.save()
        return super().save()