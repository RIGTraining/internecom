# Import necessary modules
from django.contrib import admin  
from django.urls import path       
from shop.views import *  
from django.conf import settings   # Application settings
from django.conf.urls.static import static

# Define URL patterns
urlpatterns = [
    path('home/', home, name="recipes"),      # Home page
    path("admin/", admin.site.urls),          # Admin interface
    path('login/', login_page, name='login_page'),    # Login page
    path('register/', register_page, name='register'),  # Registration page
    path('',shopview, name='shopview'), #Shop View
    path('addtowhitlist/', addtowhitlist, name='addtowhitlist'), #addtowhitlist
    path('addtocart/', addtocart, name='addtocart'), #addtocart
    path('whitelistview/', whitelistview, name='whitelistview'), #whitelistview
    path('cartview/', cartview, name='cartview'), #cartview
    path('clearcart/', clearcart, name='clearcart'), #clearcart
    path('processtocheck/', processtocheck, name='processtocheck'), #processtocheck

    path('adminlogin', UserLoginView.as_view(), name = 'UserLoginView'),
    path('logout/', UserLogoutView.as_view(), name='UserLogoutView'),

    #Admin

    path('AdminReportList/', AdminReportList.as_view(), name='AdminReportList'), #AdminReportList
    path('OrderDetailsView/<int:pk>/', OrderDetailsView.as_view(), name='OrderDetailsView'),  #OrderDetailsView
    path('Dash/', AdminDash.as_view(), name='AdminDash'),
    path('AdminProductManagement/', AdminProductManagement.as_view(), name='AdminProductManagement'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
