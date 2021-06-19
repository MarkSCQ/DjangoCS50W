from django.urls import path, re_path
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [path("", views.index, name="index"),
               path("bid_with_detail",
                    views.bid_with_detail, name="bid_with_detail"),
               path("bid_with_detail/biditem",
                    views.biditem, name="biditem"),
               path("login", views.login_view, name="login"),
               path("logout", views.logout_view, name="logout"),
               path("register", views.register, name="register"),
               path("categories", views.categories, name="categories"),

               path("mypanel", views.mypanel, name="mypanel"),
               path("editbid", views.editbid, name="editbid"),
               path("biddelete", views.biddelete, name="biddelete"),
               path("bidprice", views.bidprice, name="bidprice"),

               path("editauction", views.editauction, name="editauction"),
               path("executeauction", views.executeauction, name="executeauction"),

               path("createnewitem", views.createnewitem, name="createnewitem"),
               path("createnewbidauction", views.createnewbidauction,
                    name="createnewbidauction"),
               path("categorysub/<str:categoryname>",
                    views.categorysub, name="categorysub"),
               path("watchinglist", views.watchinglist, name="watchinglist"),
               path("watchinglist/watchinglistsub/<str:itemname>",
                    views.watchinglistsub, name="watchinglistsub"),
               path("watchinglist/addWatchinglist",
                    views.addWatchinglist, name="addWatchinglist"),
               path("watchinglist/deleteWatchinglist",
                    views.deleteWatchinglist, name="deleteWatchinglist"),
               #     path("watchinglist/watchinglistsub/<str:itemname>",
               #          views.watchinglistsubContent, name="watchinglistsubContent")
               path("submitcomments/",views.submitcomments,name="submitcomments"),
               path("oneacution/<str:auction_item>",views.oneacution,name="oneacution"),

               path("myitems/",views.myitems,name="myitems"),
               path("wantit",views.wantit,name="wantit"),
               path("addWatchinglist_inlisting",views.addWatchinglist_inlisting,name="addWatchinglist_inlisting"),

               ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
