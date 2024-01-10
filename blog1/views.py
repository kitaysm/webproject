from django.shortcuts import render, redirect # 렌더링. 다시 보내기
from django.views.generic import ListView, DetailView, CreateView, UpdateView # 리스트,디테일, 생성 수정 제너릭뷰
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # 유저 로그인 했는지 체크, 유저 스태프인지 admin 인지 ... 확인
from django.utils.text import slugify # slugify 함수는 문자열을 URL에 적합한 형태로 반환
from django.shortcuts import get_object_or_404 # 해당 객체가 존재하지 않을 경우 404 오류 페이지를 반환
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q # db에서 데이터를 검색, 필터링시, 다양한 조건을 조합하고 동적으로 쿼리를 작성하는 상황에서 유용
# CBV: Class Based View

class PostList(ListView):
    model = Post
    ordering = "-pk"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        # super 부모클래스 상속받는건데 PostList가 무엇을 상속받느냐하면 ListView를 상속받음
        # 즉, 부모 클래스의 cet_context_data() 호출함.
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    # fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]
    # fields 안에 tags 를 추가하면 태그 고를수 있게 포스트생성화면에 생김
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category", "tags"]

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form): # form_vaild 메서드는 폼 데이터가 유효할 때 호출되는 메서드
        current_user = self.request.user
        if current_user.is_authenticated and (
            current_user.is_staff or current_user.is_superuser
        ):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get("tags_str") # tags_str은 태그를 입력하는 폼에서 전달받은 데이터
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(",", ";") # ,은 db에서 사용되는 구분자이어서 오해의 문제가 될 수 있음.
                tags_list = tags_str.split(";")

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        
        else:
            return redirect("/blog/")
                    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category", "tags"]
    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context
    
    def dispatch(self, request, *args, **kwargs): # 부모 클래스의 dispatch 메서드를 호출
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response
        
def category_page(request, slug): # slug는 일반적으로 이미 얻은 데이터를 사용하여 유효한 url을 생성하는
    if slug == "no category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        "blog1/post_list.html",
        {
            "post_list": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category, # 현재 선택된 카테고리
        },
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug) # 해당 슬러그와 일치하는 Tag 객채를 가져옴
    post_list = tag.post_set.all() # tag에 속한 모든 Post 객체를 가져옴

    return render(
        request,
        "blog1/post_list.html",
        {
            "post_list": post_list, # 게시물 목록을 템플릿에 전달하여 해당 태그에 속한 게시물만 출력
            "tag" : tag, # 현재 선택된 태그
            "categories": Category.objects.all(), # 모든 카테고리 정보를 가져와 템플릿에 전달
            "no_category_post_count": Post.objects.filter(category=None).count(),
        },
    )

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk) # pk에 해당하는 Post 객체를 가져옴

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            # CommentForm(request.POST)를 사용하여 제출된 데이터로 댓글 폼의 인스턴스를 생성
            if comment_form.is_valid(): # 폼의 데이터가 유효한지 검사
                comment = comment_form.save(commit=False)
                # comment_form.save(commit=Flase)를 사용하여 Comment 객체를 생성하되, 데이터베이스에는 저장하지 않음
                comment.post = post # 댓글 객체에 post 속성을 할당
                comment.author = request.user # 댓글 객체에 author 속성을 할당
                comment.save()
                return redirect(comment.get_absolute_url())
            # 댓글 객체의 get_absolute_url 메서드를 호출하여 댓글 상세 페이지로 이동
        else:
            return redirect(post.get_absolute_url()) # 댓글 폼이 유효하지 않으면 post.get_absolute_url()로 이동
    else:
        raise PermissionDenied # 로그인하지 않은 사용자가 댓글을 작성하려고 하면 PermissionDenied 예외를 발생시킴
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment # Comment 모델을 사용
    form_class = CommentForm # 사용할 폼으로 CommentForm 을 지정

    def dispatch(self, request, *args, **kwargs): # HTTP 요청을 받아서 적절한 핸들러 메서드로 라우팅
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs) # 부모 클래스의 dispatch 메서드를 호출
        else: 
            raise PermissionDenied
        
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q) # 장고의 쿼리 표현식 더블언더바..
        ).distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context
# # FBV: Function Based View
# def index(request):
#     posts = Post.objects.all().order_by('-pk') # 모든 Post 객체를 가져와서 pk 역순으로 정렬

#     return render( # render 함수는 세 번째 인수로 전달된 딕셔너리 데이터를 템플릿 파일에 적용하여 HTML 코드로 변환
#         request, # 첫 번째 인수는 반드시 request
#         'blog/index.html',
#         {
#             'posts': posts, # posts 키에 posts 변수를 할당
#         }
#     )

# def single_post_page(request, pk): # pk는 URL에서 추출한 게시물의 고우 번호
#     post = Post.objects.get(pk=pk) # pk가 매개변수 pk와 같은 Post 객체를 post 변수에 할당

#     return render(
#         request,
#         'blog/single_post_page.html', # 템플릿 파일의 경로
#         {
#             'post': post,
#         }
#     )
# # Create your views here.