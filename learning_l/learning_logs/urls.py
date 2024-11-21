#contains urls for learning_logs

#import path from django
from django.urls import path

#. means from same directory
from . import views

app_name = 'learning_logs'

urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    
    #path for topic page.
    #!st argument is path 
    #2nd arguement is where to look for the method
    #3rd argument is the name assigned 
    path('topics/', views.topics, name='topics'),
    
    #enteries page
    path('topics/<int:topic_id>/', views.topic, name='topic' ),
    
    #add topic page
    path('new_topic/', views.new_topic, name='new_topic'),
    
    #add entry page
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    
    #editing entries
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),

    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
]
    


