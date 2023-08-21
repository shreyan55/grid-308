from django.urls import path
from .views import SimulationView, ProductListView, CreateInteractionAPIView, ResultView,HistoryView,ReportsView

app_name='interaction'

urlpatterns = [
    path('<int:user_id>/', SimulationView.as_view(), name='index'),
    path('list/', ProductListView.as_view(), name='list'),
    path('create/<int:user_id>/', CreateInteractionAPIView.as_view(), name='create_interaction'),
    path('result/<int:result_id>',ResultView.as_view(),name='result'),
    path('history/<int:user_id>',HistoryView.as_view(),name='history'),
    path('reports/<int:user_id>',ReportsView.as_view(),name='reports')
]
