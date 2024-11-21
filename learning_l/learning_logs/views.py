from django.shortcuts import render, redirect, get_object_or_404

from .models import Topic, Entry
# Create your views here.

from .form import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

from django.http import Http404

def index(request):
    
    return render(request, 'learning_logs/index.html')

#method for topics
@login_required
def topics(request):

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    #creates a dictionary that can be accessible with the name in html file
    context = {'topics': topics}
    
    #return the template topics.html and context is passed
    return render(request, 'learning_logs/topics.html', context)
    
    
#method for enteries
@login_required
def topic(request, topic_id):
    
    #getting topic_id
    topic = Topic.objects.get(id=topic_id)
    enteries = topic.entry_set.order_by('-date_added')
    if topic.owner != request.user:
        raise Http404
    
    context = {'topic': topic , 'enteries': enteries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    
    if request.method != 'POST':
        #create blank page
        form = TopicForm()
        
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            
            return redirect('learning_logs:topics')
        
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
        
        
#method for adding entries
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
        raise Http404 
    
    #display empty form if "get"
    if request.method != 'POST':
        form = EntryForm()
        
    #if data is filled, process data
    else:
        form = EntryForm(data=request.POST)
        
        #store new entry without saving it in database
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.topic.owner = request.user
        new_entry.save()
        return redirect("learning_logs:topic", topic_id=topic_id)
    
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

#method for editing entries
@login_required
def edit_entry(request, entry_id):
    
    #getting access to the entry and topic
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    #if statements for get and post
    if request.method != "POST":
        form = EntryForm(instance=entry) #prefilled with entry
        
    else:
        form = EntryForm(instance=entry, data=request.POST)
        form.save()
        return redirect('learning_logs:topic', topic_id=topic.id)
    
    
    context = {'topic': topic, 'entry':entry, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topics')
    return redirect('learning_logs:topics')
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    return redirect('learning_logs:topics')
