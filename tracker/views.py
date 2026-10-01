from datetime import timedelta
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Phase, Chapter, Problem, StudySession


def stats():
    total = Problem.objects.aggregate(v=Sum('points'))['v'] or 0
    earned = Problem.objects.filter(completed=True).aggregate(v=Sum('points'))['v'] or 0
    total_problems = Problem.objects.count()
    solved = Problem.objects.filter(completed=True).count()
    return {
        'total_points': total, 'earned_points': earned,
        'percent': round(earned / total * 100) if total else 0,
        'total_problems': total_problems, 'solved': solved,
        'pending': total_problems - solved,
    }


def dashboard(request):
    phases = list(Phase.objects.prefetch_related('chapters__problems'))
    context = stats()
    context.update({
        'phases': phases,
        'review_due': Problem.objects.filter(completed=True, next_review_at__lte=timezone.now()).count(),
        'upcoming_reviews': Problem.objects.filter(completed=True, next_review_at__gt=timezone.now()).order_by('next_review_at')[:5],
        'sessions': StudySession.objects.all()[:7],
    })
    return render(request, 'tracker/dashboard.html', context)


def roadmap(request):
    phases = Phase.objects.prefetch_related('chapters__problems')
    return render(request, 'tracker/roadmap.html', {'phases': phases, **stats()})


def phase_detail(request, phase_id):
    phase = get_object_or_404(Phase.objects.prefetch_related('chapters__problems'), id=phase_id)
    return render(request, 'tracker/phase.html', {'phase': phase, **stats()})


def toggle_problem(request, problem_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    problem = get_object_or_404(Problem, id=problem_id)
    was_complete = problem.completed
    problem.completed = not problem.completed
    problem.save()
    if problem.completed and not was_complete:
        messages.success(request, f'Completed: {problem.title} (+{problem.points} points)')
    elif was_complete:
        messages.info(request, f'Reopened: {problem.title}')
    return redirect(request.POST.get('next') or 'dashboard')


def review_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        confidence = int(request.POST.get('confidence', 3))
        days = int(request.POST.get('days', 7))
        problem.confidence = max(1, min(5, confidence))
        problem.review_count += 1
        problem.last_reviewed_at = timezone.now()
        problem.next_review_at = timezone.now() + timedelta(days=max(1, days))
        problem.save(update_fields=['confidence','review_count','last_reviewed_at','next_review_at','updated_at'])
        messages.success(request, f'Review scheduled for {problem.next_review_at.strftime("%d %b %Y")}.')
    return redirect(request.POST.get('next') or 'dashboard')


def update_notes(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        problem.notes = request.POST.get('notes', '')
        problem.save(update_fields=['notes','updated_at'])
        messages.success(request, 'Notes saved.')
    return redirect(request.POST.get('next') or 'dashboard')


def save_session(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        minutes = int(request.POST.get('minutes', 0) or 0)
        problems_solved = int(request.POST.get('problems_solved', 0) or 0)
        notes = request.POST.get('notes', '')
        StudySession.objects.update_or_create(date=date, defaults={'minutes': minutes, 'problems_solved': problems_solved, 'notes': notes})
        messages.success(request, 'Study session saved.')
    return redirect('dashboard')


def reset_progress(request):
    if request.method == 'POST':
        Problem.objects.update(completed=False, completed_at=None, last_reviewed_at=None, next_review_at=None, review_count=0, confidence=0)
        StudySession.objects.all().delete()
        messages.warning(request, 'Progress reset. Your roadmap and problems were kept.')
    return redirect('dashboard')
