from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *

main_menu = [{'name': 'Лента', 'alt': '', 'logo_src': 'website/logos/home-alt.svg', 'href': 'pins'},
             {'name': 'Коллекции', 'alt': '', 'logo_src': 'website/logos/folder.svg', 'href': 'collections'},
             {'name': 'Создать', 'alt': '', 'logo_src': 'website/logos/plus.svg', 'href': 'add_project'},
             {'name': 'Поиск', 'alt': '', 'logo_src': 'website/logos/search.svg', 'href': 'search'},
             ]
user_menu = [{'name': 'Войти', 'alt': '', 'logo_src': 'website/logos/log-in.svg', 'href': 'users:login'},
             {'name': 'Регистрация', 'alt': '', 'logo_src': 'website/logos/sign_up.svg', 'href': 'users:sign_up'}
             ]
prof_menu = [
    {'name': 'Изменить профиль', 'alt': '', 'logo_src': 'website/logos/settings.svg', 'href': 'change_profile'},
    {'name': 'Изменить запись', 'alt': '', 'logo_src': 'website/logos/edit.svg', 'href': 'pin_update'},
    {'name': 'Удалить запись', 'alt': '', 'logo_src': 'website/logos/remove.svg', 'href': 'pin_delete'},
    {'name': 'Уведомления', 'alt': '', 'logo_src': 'website/logos/notification.svg', 'href': 'notifications_list'},
    {'name': 'Уведомления', 'alt': '', 'logo_src': 'website/logos/notification_notread.svg', 'href': 'notifications_list'},
]


class MainPage(ListView):
    model = Pins
    template_name = 'website/pins.html'
    context_object_name = 'pins'
    paginate_by = 6

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', 'time_create_desc')
        if sort_by == 'time_create_asc':
            return Pins.objects.all().order_by('time_create')
        elif sort_by == 'time_create_desc':
            return Pins.objects.all().order_by('-time_create')
        elif sort_by == 'likes_count':
            return Pins.objects.all().order_by('-likes_count')
        elif sort_by == 'title_asc':
            return Pins.objects.all().order_by('title')
        elif sort_by == 'title_desc':
            return Pins.objects.all().order_by('-title')
        return Pins.objects.all().order_by('-time_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Лента'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        context['comments_count'] = Pins.objects.annotate(comment_count=Count('comment'))
        return context


class ShowPin(DetailView):
    model = Pins
    template_name = 'website/pin.html'
    context_object_name = 'pin'
    pk_url_kwarg = 'pin_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['pin']
        context['main_menu'] = main_menu
        context['comments'] = Comment.objects.filter(pin=self.kwargs['pin_id']).order_by('-time_create')
        context['user_menu'] = user_menu
        if self.request.user.is_authenticated:
            likes = Likes.objects.filter(pin=self.kwargs['pin_id'], liked_by=self.request.user.profile)
            context['is_liked'] = likes.exists()
        else:
            context['is_liked'] = False
        context['prof_menu'] = prof_menu
        return context


@method_decorator(login_required, name='dispatch')
class CollectionsPage(ListView):
    model = Collections
    template_name = 'website/collections.html'
    context_object_name = 'collections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Коллекции'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def get_queryset(self):
        return Collections.objects.filter(author=self.request.user.profile)


class ShowCollection(ListView):
    model = Collections
    template_name = 'website/collection.html'
    context_object_name = 'collection'
    pk_url_kwarg = 'collection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['collection']
        context['pins'] = Pins.objects.filter(collection=self.kwargs['collection_id'],
                                              author=self.request.user.profile)
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def get_queryset(self):
        return Collections.objects.get(pk=self.kwargs['collection_id'])


class AddProject(CreateView):
    form_class = AddProjectForm
    template_name = 'website/add_project.html'
    success_url = reverse_lazy('pins')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создание проекта'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


@login_required
def follow(request, profile_id):
    user_profile = get_object_or_404(Profile, user=request.user)
    target_profile = get_object_or_404(Profile, id=profile_id)
    if user_profile != target_profile and not Follow.objects.filter(follower=user_profile,
                                                                    following=target_profile).exists():
        Follow.objects.create(follower=user_profile, following=target_profile)
    return redirect('profile', profile_id=profile_id)


@login_required
def unfollow(request, profile_id):
    user_profile = get_object_or_404(Profile, user=request.user)
    target_profile = get_object_or_404(Profile, id=profile_id)
    Follow.objects.filter(follower=user_profile, following=target_profile).delete()
    return redirect('profile', profile_id=profile_id)


class ProfilePage(DetailView):
    model = Profile
    template_name = 'website/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']
        context['page_title'] = profile
        context['pins'] = Pins.objects.filter(author=profile).annotate(count=Count('pk'))
        context['unread_notifications'] = Notification.objects.filter(recipient=self.request.user.profile, is_read=False).exists()
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        context['prof_menu'] = prof_menu

        context['followers_count'] = profile.followers.count()
        context['following_count'] = profile.following.count()

        if self.request.user.is_authenticated:
            context['is_following'] = Follow.objects.filter(follower=self.request.user.profile,
                                                            following=profile).exists()
        else:
            context['is_following'] = False

        context['is_online'] = profile.is_online

        return context

    def get_object(self, queryset=None, *args, **kwargs):
        return get_object_or_404(Profile, pk=self.kwargs['profile_id'])


class ShowFollowers(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'website/followers.html'
    context_object_name = 'followers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Подписчики'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu

        followers_count = Follow.objects.filter(following=self.request.user.profile).count()
        context['followers_count'] = followers_count
        return context

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user.profile)


class ShowFollowing(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'website/following.html'
    context_object_name = 'following'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Подписки'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu

        following_count = self.request.user.profile.following.count()
        context['following_count'] = following_count
        return context

    def get_queryset(self):
        return self.request.user.profile.following.all()


class SearchPage(ListView):
    model = Pins
    template_name = 'website/search.html'
    context_object_name = 'pins'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Поиск'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context

    def post(self, request):
        search_term = request.POST.get('search')

        if search_term:
            pins = Pins.objects.filter(Q(title__icontains=search_term.lower()) |
                                       Q(title__icontains=search_term.upper()) |
                                       Q(title__icontains=search_term.capitalize()) |
                                       Q(description__icontains=search_term))
        else:
            pins = Pins.objects.all()

        return render(request,
                      template_name='website/search_results.html',
                      context={
                          'query': search_term,
                          'pins': pins,
                          'main_menu': main_menu,
                          'user_menu': user_menu,
                          'page_title': 'Результаты поиска'})


class ChangeProfile(UpdateView):
    form_class = ChangeProfileForm
    template_name = 'website/change_profile.html'

    def get_success_url(self):
        profile_id = self.object.id
        return reverse_lazy('profile', kwargs={'profile_id': profile_id})

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Изменение профиля'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class UpdatePin(UpdateView):
    model = Pins
    template_name = 'website/update_project.html'
    success_url = reverse_lazy('pins')
    form_class = UpdateProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user.profile})
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Изменение записи'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class DeletePin(DeleteView):
    model = Pins
    success_url = reverse_lazy('pins')
    template_name = 'website/pin_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удалить запись'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class LikePin(LoginRequiredMixin, View):
    def post(self, request, pin_id):
        pin = get_object_or_404(Pins, pk=pin_id)
        like, created = Likes.objects.get_or_create(liked_by=request.user.profile, pin=pin)
        if not created:
            like.delete()
        pin.likes_count = pin.likes_set.count()
        pin.save()
        return redirect('pin', pin_id=pin_id)


class AddCollection(CreateView):
    model = Collections
    form_class = AddCollectionForm
    template_name = 'website/add_collection.html'
    success_url = reverse_lazy('collections')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создание коллекции'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


class DeleteCollection(DeleteView):
    model = Collections
    success_url = reverse_lazy('collections')
    template_name = 'website/pin_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удалить коллекцию'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


def add_comment(request):
    pin_id = request.POST.get('pin_id')
    comment = Comment.objects.create(author=request.user.profile,
                                     pin=Pins.objects.get(pk=pin_id),
                                     content=request.POST.get('content'))
    comment.save()
    return redirect(f'/pin/{pin_id}/')


class DeleteComment(DeleteView):
    model = Comment
    # success_url = reverse_lazy('pins')
    template_name = 'website/pin_delete.html'

    def get_success_url(self):
        pin_id = self.object.pin.pk
        return reverse_lazy('pin', kwargs={'pin_id': pin_id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удалить комментарий'
        context['main_menu'] = main_menu
        context['user_menu'] = user_menu
        return context


@login_required
def notifications_list(request):
    notifications = request.user.profile.notifications.all().order_by('-created_at')
    return render(request, 'website/list_notifications.html',
                  {
                      'main_menu': main_menu,
                      'page_title': 'Уведомления',
                      'notifications': notifications
                  })


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user.profile)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')


def report_view(request, pin_id):
    pin = get_object_or_404(Pins, pk=pin_id)

    if request.method == "POST":
        form = ReportForm(request.POST, pin)

        if form.is_valid():
            print(form.cleaned_data)
            report = Report.objects.create(post=pin,
                                           reporter=request.user,
                                           reason=form.cleaned_data['reason']).save()

            return redirect("pins")

    else:
        form = ReportForm()

    return render(request, "website/report_complaint.html",
                  {"form": form, "main_menu": main_menu, "user_menu": user_menu, "page_title": 'Пожаловаться'})


def about_project(request):
    return render(request, 'website/about.html',
                  {
                      'user_menu': user_menu,
                      'main_menu': main_menu,
                      'page_title': 'О проекте',
                  })