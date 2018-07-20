from django.contrib import admin
from .models import Question
from enron.models import Email, ToEmail, CcEmail, BccEmail, Sender, ReceiverTo, ReceiverCC, ReceiverBCC, StaffName, StaffEmail
from  enron.models import AnalysisResult
# Register your models here.

class EnronAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(Question,EnronAdmin)
admin.site.register(Email,EnronAdmin)
admin.site.register(ToEmail,EnronAdmin)
admin.site.register(CcEmail,EnronAdmin)
admin.site.register(BccEmail,EnronAdmin)
admin.site.register(Sender,EnronAdmin)
admin.site.register(ReceiverTo,EnronAdmin)
admin.site.register(ReceiverCC,EnronAdmin)
admin.site.register(ReceiverBCC,EnronAdmin)
admin.site.register(StaffName,EnronAdmin)
admin.site.register(StaffEmail,EnronAdmin)
admin.site.register(AnalysisResult,EnronAdmin)

