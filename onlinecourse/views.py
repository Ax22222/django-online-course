from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        
        # Look up or generate user enrollment validation context
        enrollment = get_object_or_404(Enrollment, course=course, user=request.user)
        
        # Instantiate a clean, traceable exam submission record
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Parse selected option checkbox values out of the payload
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        # Save relations to Many-to-Many field
        if selected_choice_ids:
            choices = Choice.objects.filter(id__in=selected_choice_ids)
            submission.choices.add(*choices)
            submission.save()
            
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Compile a flat sequence list of user-checked IDs
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    results = []
    
    for question in course.question_set.all():
        # Track the specific checked items matching this individual question block
        q_choices = question.choice_set.filter(id__in=selected_ids)
        is_correct = question.is_get_score(selected_ids)
        
        if is_correct:
            total_score += question.grade
            
        results.append({
            'question': question,
            'is_correct': is_correct,
            'selected_choices': q_choices
        })
        
    context = {
        'course': course,
        'total_score': total_score,
        'results': results,
    }
    return render(request, 'onlinecourse/exam_result.html', context)
