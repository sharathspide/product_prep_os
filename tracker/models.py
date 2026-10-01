from django.db import models
from django.utils import timezone

class Phase(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(unique=True)
    target_days = models.PositiveIntegerField(default=7)

    class Meta:
        ordering = ['order']

    @property
    def total_points(self):
        return sum(c.total_points for c in self.chapters.all())

    @property
    def earned_points(self):
        return sum(c.earned_points for c in self.chapters.all())

    @property
    def percent(self):
        return round((self.earned_points / self.total_points) * 100) if self.total_points else 0

    @property
    def complete(self):
        return self.total_points > 0 and self.earned_points >= self.total_points

class Chapter(models.Model):
    phase = models.ForeignKey(Phase, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['phase__order', 'order']
        constraints = [models.UniqueConstraint(fields=['phase', 'order'], name='unique_chapter_order')]

    @property
    def total_points(self):
        return sum(p.points for p in self.problems.all())

    @property
    def earned_points(self):
        return sum(p.points for p in self.problems.filter(completed=True))

    @property
    def percent(self):
        return round((self.earned_points / self.total_points) * 100) if self.total_points else 0

    @property
    def complete(self):
        return self.total_points > 0 and self.earned_points >= self.total_points

class Problem(models.Model):
    DIFFICULTIES = [('easy','Easy'), ('medium','Medium'), ('hard','Hard')]
    chapter = models.ForeignKey(Chapter, related_name='problems', on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    points = models.PositiveIntegerField(default=10)
    source = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    next_review_at = models.DateTimeField(null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0)
    confidence = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        if not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)

class StudySession(models.Model):
    date = models.DateField(unique=True)
    minutes = models.PositiveIntegerField(default=0)
    problems_solved = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
