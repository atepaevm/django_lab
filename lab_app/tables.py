import django_tables2 as tables
from .models import LabReport, LabUserReport, LabUser, LabComment

TEMPLATE = """
<form method="get">
    <select name='PreviousReceiver' record_id = '{{ record.id }}' onchange='if(this.value != 0) { this.form.submit(); }'>
        <option value="{{ record.id }}_0" selected disabled hidden>Поменять статус</option>
         <option value='{{ record.id }}_1'>Поступила</option>
         <option value='{{ record.id }}_2'>Передана в работу</option>
         <option value='{{ record.id }}_3'>Отклонена</option>
    </select>
</form>
"""

USER_TEMPLATE = """
<form method="get">
    <select name='PreviousReceiver' record_id = '{{ record.id }}' onchange='if(this.value != 0) { this.form.submit(); }'>
        <option value="{{ record.id }}_0" selected disabled hidden>Поменять статус</option>
         <option value='{{ record.id }}_1'>user</option>
         <option value='{{ record.id }}_2'>moderator</option>
         <option value='{{ record.id }}_3'>admin</option>
    </select>
</form>
"""

class LabReportTable(tables.Table):
    change_status = tables.TemplateColumn(TEMPLATE, extra_context={'record': lambda record: '{}'.format(record)})

    class Meta:
        model = LabReport
        template_name = "../templates/bootstrap.html"
        #fields = ('test', 'text', 'photo', 'lat', 'lng', 'status', 'comment')


class UserReportTable(tables.Table):
    change_status = tables.TemplateColumn(USER_TEMPLATE, extra_context={'record': lambda record: '{}'.format(record)})
    class Meta:
        model = LabUser
        template_name = "../templates/bootstrap.html"


class LikeReportTable(tables.Table):
    class Meta:
        model = LabUserReport
        template_name = "../templates/bootstrap.html"


class CommentTable(tables.Table):
    class Meta:
        model = LabComment
        template_name = "../templates/bootstrap.html"