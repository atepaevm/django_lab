# Generated by Django 3.0.4 on 2020-05-02 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab_app', '0002_auto_20200326_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='labuser',
            name='role',
            field=models.TextField(default='user'),
        ),
        migrations.AlterField(
            model_name='labreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lab_app.LabUser'),
        ),
        migrations.CreateModel(
            name='LabComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time', models.DateTimeField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lab_app.LabReport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lab_app.LabUser')),
            ],
        ),
    ]
