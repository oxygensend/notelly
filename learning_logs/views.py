from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import TopicAccessForm, TopicForm, EntryForm
from .models import Topic, Entry
# Create your views here.

def check_topic_owner(request, topic):
    return True if request.user == topic.owner else False
  
def index(request):
    """Home page for Learning logs app."""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """ Display all topics."""
    topics_public = Topic.objects.filter(access=False).exclude(owner=request.user).order_by('date_added')
    topics_private = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics_public': topics_public,
               'topics_private': topics_private}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """ Display one topic and all his entries."""
    
    changed = False
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic) and \
       topic.access:
        raise Http404
    

    entries = topic.entry_set.order_by('-date_added')

    if not check_topic_owner(request, topic):
        context = { 'topic': topic,
                'entries': entries,
                
                }
        return render(request, 'learning_logs/topic.html', context)
    
    if request.method != 'POST':
        form = TopicAccessForm(instance=topic)
    else:
        form = TopicAccessForm(instance=topic,data=request.POST)
        changed = True
        if form.is_valid():
            form.save()
        
    context = { 'topic': topic,
                'entries': entries,
                'form': form,
                'changed': changed
            }
    return render(request, 'learning_logs/topic.html', context)
    
@login_required
def new_topic(request):
    """ Adding new topic from user """

    if request.method != 'POST':
        form = TopicForm(request.user)
    else:
        form = TopicForm(request.user, data=request.POST)
        if form.is_valid():

            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    """ Deleting topic """

    topic = get_object_or_404(Topic, pk=topic_id);

    if not check_topic_owner(request,topic):
        raise Http404

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')    
    
    return render(request,'learning_logs/delete_topic.html', {'topic': topic})


@login_required
def new_entry(request, topic_id):
    """ Adding new entry to specific topic"""
    
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic) and \
        topic.access:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic)
    else:
        form = EntryForm(topic,data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.creator = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id)
        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit entry of topic"""
    
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic

    if not check_topic_owner(request, topic) and \
        topic.access or request.user != entry.creator:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic, instance=entry)
    else:
        form = EntryForm(topic, instance=entry, data=request.POST)
        if form.is_valid():
        
            form.save()
            return redirect('learning_logs:topic', topic.id)

    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
    

@login_required
def delete_entry(request, entry_id):
    """Delete entry of topic"""

    entry= get_object_or_404(Entry, pk=entry_id);
    topic = entry.topic
    if request.user != entry.creator:
        raise Http404
        
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic.id)    
    
    return render(request,'learning_logs/delete_entry.html', {'topic': topic})
