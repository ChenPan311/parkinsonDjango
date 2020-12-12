from django.urls import path

from dashboard import views as d_views
from registration import views as r_views

urlpatterns = [
    # path("<int:id>", views.index, name="index"),
    path('', d_views.postsign, name="login"),
    path('register/', r_views.register_new_doctor, name="register"),
    path('home/', d_views.home, name="home"),
    path('logout/', d_views.user_logout, name="logout"),
    # path("myaccount/",views.my_account,name="my_account"),
    # path("addcontact/", views.add_contact, name="add_contact"),
    # path("edit/<int:contact_id>", views.editcontact, name="edit_contact"),
    # path('home/', views.home, name="home"),
    # path('logout/', views.user_logout, name="home"),
]
