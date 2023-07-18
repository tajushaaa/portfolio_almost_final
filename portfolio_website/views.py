from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ProjectForm, ImageForm, AdditionalImageForm
from .models import Project, AdditionalImage
from django.forms import formset_factory, BaseFormSet, modelformset_factory
from django.http import HttpResponseBadRequest
from django.template.defaultfilters import slugify


class BaseImageFormSet(BaseFormSet):
    pass


def home(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='/login/')
def create_project(request):
    AdditionalImageFormSet = formset_factory(AdditionalImageForm, extra=1)


    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        formset = AdditionalImageFormSet(
            request.POST, request.FILES, prefix='image')

        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.save()

            for image_form in formset:
                image = image_form.cleaned_data.get('image')
                if image:
                    AdditionalImage.objects.create(
                        project=project, image=image)

            slug = slugify(project.name)
            return redirect('project_detail', project_slug=slug)
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = ProjectForm()
        formset = AdditionalImageFormSet(prefix='image')

    return render(request, 'base/create_project.html', {'form': form, 'formset': formset})


@login_required(login_url='/login/')
def edit_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    # Use modelformset_factory to create a formset for AdditionalImage
    ImageFormSet = modelformset_factory(
        AdditionalImage, form=ImageForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        additional_image_formset = ImageFormSet(
            request.POST, request.FILES, prefix='additional_image', queryset=project.additionalimages.all()
        )

        if form.is_valid() and additional_image_formset.is_valid():
            form.save()

            # Process the additional_image_formset to delete/clear images
            for additional_image_form in additional_image_formset.deleted_forms:
                if additional_image_form.instance.id:
                    additional_image_form.instance.delete()

            # Save additional images from the formset
            for additional_image_form in additional_image_formset:
                if 'image' in additional_image_form.cleaned_data:
                    image = additional_image_form.cleaned_data['image']
                    if image:
                        AdditionalImage.objects.create(
                            project=project, image=image)

            # Redirect using project name
            return redirect('project_detail', project_slug=project.slug)
    else:
        form = ProjectForm(instance=project)
        additional_image_formset = ImageFormSet(
            prefix='additional_image', queryset=project.additionalimages.all()
        )

    context = {
        'form': form,
        'additional_image_formset': additional_image_formset,
        'project': project,
    }
    return render(request, 'base/edit_project.html', context)


@login_required(login_url='/login/')
def add_image(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            for image in images:
                AdditionalImage.objects.create(project=project, image=image)
            return redirect('create_project')

    form = ImageForm()
    return render(request, 'base/create_project.html', {'form': form})


@login_required(login_url='/login/')
def delete_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            project.delete()
            return redirect('home')
        else:
            return HttpResponseBadRequest("Project ID not provided.")
    else:
        return HttpResponseBadRequest("Invalid request method.")


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'base/login.html', {})
    else:
        return render(request, 'base/login.html', {})


def project_detail(request, project_slug):
    project = get_object_or_404(
        Project, slug=project_slug)
    return render(request, 'base/project_detail.html', {'project': project})


def custom_logout(request):
    logout(request)
    return redirect('home')
