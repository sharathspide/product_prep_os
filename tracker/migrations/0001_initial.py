from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(unique=True)),
                ('target_days', models.PositiveIntegerField(default=7)),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='StudySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('minutes', models.PositiveIntegerField(default=0)),
                ('problems_solved', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
            ],
            options={'ordering': ['-date']},
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField()),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='tracker.phase')),
            ],
            options={'ordering': ['phase__order', 'order']},
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('difficulty', models.CharField(choices=[('easy','Easy'),('medium','Medium'),('hard','Hard')], max_length=10)),
                ('points', models.PositiveIntegerField(default=10)),
                ('source', models.URLField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('last_reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('next_review_at', models.DateTimeField(blank=True, null=True)),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('confidence', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='tracker.chapter')),
            ],
            options={'ordering': ['id']},
        ),
        migrations.AddConstraint(
            model_name='chapter',
            constraint=models.UniqueConstraint(fields=('phase','order'), name='unique_chapter_order'),
        ),
    ]
