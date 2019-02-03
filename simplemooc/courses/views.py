from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment
from .forms import ContactCourse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    template_name = 'index.html'
    return render(request, template_name, context)


def detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():            
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form
    template_name = 'detail.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    enrollment, created = Enrollment.objects.get_or_create(
        user = request.user,
        course = course
    )
    if created:
        enrollment.active()
        messages.success(request, 'Inscrição realizada com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito neste curso!')
    return redirect('accounts:dashboard')
    
