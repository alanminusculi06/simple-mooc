from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Announcement
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
        user=request.user,
        course=course
    )
    if created:
        enrollment.active()
        messages.success(request, 'Inscrição realizada com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito neste curso!')
    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)


@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment,
                                       user=request.user,
                                       course=course
                                       )
        if not enrollment.is_approved():
            messages.error(request, 'A sua incrição está pendente.')
            return redirect('accounts:dashboard')
    template_name = 'announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)


@login_required
def announcement(request, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment,
                                       user=request.user,
                                       course=course
                                       )
        if not enrollment.is_approved():
            messages.error(request, 'A sua incrição está pendente.')
            return redirect('accounts:dashboard')
    tamplate_name = 'announcement.html'
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    context = {
        'course': course,
        'announcement': announcement
    }
    return render(request, tamplate_name, context)
