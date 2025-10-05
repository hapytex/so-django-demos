from django.urls import path

from app_name.views import FileImportView, MatchView, DryRunView, RunView

urlpatterns = [
    path('upload/', FileImportView.as_view(), name='file-import'),
    path('upload/<int:pk>/match', MatchView.as_view(), name='file-match'),
    path('upload/<int:pk>/dry-run', DryRunView.as_view(), name='dry-run'),
    path('upload/<int:pk>/run', RunView.as_view(), name='run'),
]