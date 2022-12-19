from django.urls import path
from .views import addView,homeView,loginView,signUpView,logoutView,cartView,profileView,checkoutView,ordersView,storeView,paginatorView,updateprofileView,resetpasswordView,changepasswordView,render_pdf_view,sendotpView,ajaxdataView #,searchView

urlpatterns=[
    path('add/',addView,name='add'),
    path('home/',homeView,name='home'),
    path('store/',storeView,name='store'),
    path('login/',loginView,name='login'),
    path('logout/',logoutView,name='logout'),
    path('signup/',signUpView,name='signup'),
    path('cart/',cartView,name='cart'),
    path('profile/',profileView,name='profile'),
    path('update/',updateprofileView,name='update'),
    path('check-out/',checkoutView,name='check-out'),
    path('orders/',ordersView,name='orders'),
# ,placeorderView   path('placeorder/',placeorderView,name='placeorder'),
    path('paginator/',paginatorView,name='paginator'),
    path('resetpassword/',resetpasswordView,name='resetpassword'),
    path('changepassword/',changepasswordView,name='changepassword'),
    path('renderpdf/<int:i>',render_pdf_view,name='renderpdf'),
    # path('search/',searchView,name='search'),
    path('sendotp',sendotpView,name='sendotp'),
    path('ajaxdata',ajaxdataView,name='ajaxdata')

]
