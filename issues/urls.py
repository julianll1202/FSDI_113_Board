from django.urls import path
from issues import views
urlpatterns = [
    path('', views.BoardView.as_view(), name='board'),
    path('<int:pk>', views.IssueDetailView.as_view(), name='detail'),
    path('new/', views.IssueCreateView.as_view(), name='new_issue'),
    path('delete/<int:pk>/', views.IssueDeleteView.as_view(), name='delete_issue'),
    path('update/<int:pk>/', views.IssueUpdateView.as_view(), name='update_issue'),
]