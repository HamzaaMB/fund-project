from django.urls import path, include
from .views import fund_list, upload_funds, delete_fund

urlpatterns = [
    # Template Paths #
    path('', fund_list, name='fund-list'),
    path('upload/', upload_funds, name='upload-funds'),
    path('delete/<uuid:fund_id>/', delete_fund, name='delete-fund'), 
    
    # API Paths #
    path('api/', include('funds.api.urls')),  
]
