from django.urls import path
from core.views import ProcessCreate, ProcessList, \
    ProcessUpdate, ProcessDelete, ProcessDetail, SearchPart

app_name = 'core'

urlpatterns = [
    path('', ProcessList.as_view(), name="list"),
    path('create/', ProcessCreate.as_view(), name="create"),
    path('search/part/', SearchPart.as_view(), name="search-part"),
    path('update/<int:pk>/', ProcessUpdate.as_view(), name="update"),
    path('delete/<int:pk>/', ProcessDelete.as_view(), name="delete"),
    path('detail/<int:pk>/', ProcessDetail.as_view(), name="detail"),
]
