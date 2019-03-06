from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decoretors import enrollment_required


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
@enrollment_required
def announcements(request, slug):
    course = request.course
    template_name = 'announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentario foi enviado.')
    tamplate_name = 'announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form
    }
    return render(request, tamplate_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    template_name = 'lessons.html'
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template = 'lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.material_file.url)
    template_name = 'material.html'
    context = {
        'material': material,
        'lesson': lesson,
        'course': course
    }
    return render(request, template_name, context)
