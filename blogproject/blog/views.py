from django.shortcuts import render, redirect,get_object_or_404
from .models import Post
from django.http import Http404
from django.utils import timezone
from .forms import LoginForm,CreateUserForm,CreateRecordForm,UpdateRecordForm,ReviewForm
from django.core.mail import send_mail
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login
from django.contrib import messages 
from django.contrib.auth.decorators import login_required


# Create your views here.

#THE LANDING PAGE
def landing(request):
  template_name='landing.html'
  return render(request, template_name)



# HOME PAGE
@login_required
def home(request):
    template_name="home.html"
    posts = Post.objects.all().order_by('-created')
    popular_posts = [post for post in posts if post.is_popular()]
    context = {
        'posts': posts,
        'popular_posts': popular_posts
    }
    return render(request, template_name, context)


#ABOUT PAGE
def about(request):
  print()
  return render(request, 'about.html')

#DETAILS PAGE
@login_required
def details(request, pk):
    post = get_object_or_404(Post, id=pk)
    reviews = post.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'like_post' in request.POST:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return redirect('blog:details', pk=post.id)
        
  
        elif 'add_review' in request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.post = post
                review.user = request.user
                review.save()
                return redirect('blog:details', pk=post.id)
    else:
        form = ReviewForm()
    
    context = {
        'post': post,
        'reviews': reviews,
        'form': form,
        'user_has_liked': request.user in post.likes.all()
    }
    return render(request, 'details.html', context)
  
  
#CONTACT US PAGE
def contact(request):
  return render(request, 'contact.html')


#CONTACT SUBMISSION PAGE
def contact_submit(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        thoughts = request.POST.get('thoughts')
        email = request.POST.get('email')
        
        # Prepare email content
        subject = f"New Contact Form Submission from {first_name} {last_name}"
        message = f"""
        From: {first_name} {last_name}
        Email: {email}
        
        Message:
        {thoughts}
        """
        sender_email = email
        recipient_email = 'girltogirl427@gmail.com'  # Your email address
        
        try:
            # Send email
            send_mail(
                subject,
                message,
                sender_email,
                [recipient_email],
                fail_silently=False,
            )
            
            # Notify user of success
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        except Exception as e:
            # Notify user of error
            messages.error(request, 'There was an error sending your message. Please try again later.')
            # You might want to log this error in production
        
        return redirect('blog:contact')
    
    return redirect('blog:contact')

#ARCHIVED POSTS PAGE
@login_required
def archives(request):
  template_name='archive.html'
  one_week_ago = timezone.now() - timezone.timedelta(days=7)
  
  archived_posts = Post.objects.filter(
        created__lt=one_week_ago
    ).order_by('-created')
    
  context = {
        'archived_posts': archived_posts,
        'title': 'Archived Posts'
    }
  return render(request, template_name, context)

# POPULAR POSTS PAGE
@login_required
def popular_posts(request):
    template_name='popular.html'
    posts = Post.objects.all()
    popular_posts = [post for post in posts if post.is_popular()]
    context = {
        'popular_posts': popular_posts,
        'title': 'Popular Posts'
    }
    return render(request, template_name, context)

#LOGIN A USER

def login(request):
  form=LoginForm()
  template_name = 'login.html'
  if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('blog:home')
        messages.error(request, 'Invalid username or password.')
  context={'form':form}
  return render(request, template_name,context)

#USER LOGOUT
def logout(request):
    auth.logout(request)
    
    messages.success(request,"Logout success! See you soon")
  
    return redirect("blog:login")
  
  

#REGISTER A USER
def register(request):
  form=CreateUserForm()
  
  if request.method=='POST':
    form = CreateUserForm(request.POST)
    
    if form.is_valid():
      new_form = form.save(commit=False)
      new_form.is_staff = True
      new_form.save()
      
      messages.success(request, "Account created successfully!")
      return redirect("blog:login")
  
  context ={'form':form}
  return render(request,'register.html',context)

#CREATE A POST
@login_required(login_url='login')
def create_post(request):
  template_name='create.html'
  form=CreateRecordForm()
   
  if request.method=="POST":
     form = CreateRecordForm(request.POST, request.FILES, user=request.user)
     
     if form.is_valid():
       form.save()
       
       
       messages.success(request, "Your blog post was created!")
       return redirect("blog:home")
  else: 
    form= CreateRecordForm(user=request.user)
  context ={'form': form}
  return render(request,template_name, context)  

 #--Update a record
@login_required(login_url='login')
def update(request, pk):
  post = Post.objects.get(id=pk)
  template_name='update.html'
  form = UpdateRecordForm(instance=post)
  
  if request.method=='POST':
    form = UpdateRecordForm(request.POST, request.FILES, instance=post)
    
    if form.is_valid():
      form.save()
      messages.success(request,"Your record was updated successfully!")
      
      return redirect("blog:home")
  context={'form': form}
  return render(request, template_name, context) 


#--Delete Record
@login_required(login_url='login')
def delete_post(request, pk):     
     post= Post.objects.get(id=pk)
     post.delete()
     
     messages.success(request,"Your record was deleted!")
     return redirect("blog:home")
   
#--Like a POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  
    else:
        post.likes.add(request.user)  
    return redirect('details', post_id=post.id)   
  
#--Review a Post
@login_required
def add_review(request, post_id):
  template_name='details.html'
  post = get_object_or_404(Post, id=post_id)
  if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.post = post
            review.user = request.user
            review.save()
            return redirect('blog:details', post_id=post.id)
  else:
        form = ReviewForm()
  return render(request, template_name, {'form': form})