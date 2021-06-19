# Author:   https://github.com/MarkSCQ/

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, item_info, bid_info, comments, auction_list, category, watchlists
import datetime
import uuid
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models import Q

ITEM_STATE = (("1", "Not Available"), ("2", "For Sale"))
AUCTION_STATE = (("1", "Not Available"), ("2", "Available"))

CATEGORIES = [i.category_item for i in category.objects.all()]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)[0].comment_content


@register.filter
def get_user(dictionary, key):
    return dictionary.get(key)[0].comment_user


def makecatetuples(categories):
    retval = []
    for i in range(len(categories)):
        retval.append((str(i), categories[i]))
    return tuple(retval)


CATEGORIES_CHOICE = makecatetuples(CATEGORIES)

# assume date1 is less then dates


def dateTimeCmp(date_start, date_end):
    start_time = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    if start_time < end_time:
        return True
    else:
        return False


def dateTimeTodayCmp(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    today_date = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time())
    if date < today_date:
        return True
    else:
        return False


def userPk(request):
    name = request.user
    return User.objects.all().get(username=name).pk


def watchinglistDupMsg(duplicateArr):
    msgHead = "Auctions: "
    msgContnet = ""
    msgTail = " exist in current watching list"
    for i in duplicateArr:
        msgContnet += str(i.auction_item.item_name)
        msgContnet += " "
    msg = msgHead+msgContnet+msgTail
    return msg


def whetherIn(item, target):
    pass
    # class itemForm(forms.Form):

    #     item_name = forms.CharField(label="Item Name")
    #     item_description = forms.CharField(label="Description")
    #     item_category = forms.ChoiceField(
    #         label="Category", choices=CATEGORIES_CHOICE)
    #     item_origin_price = forms.IntegerField(label="Base Price")
    #     # active or not / on auction or off auction
    #     item_publisher = forms.CharField(label="Description")
    #     item_img = forms.ImageField(upload_to='pictures/')


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


'''
def flights(request, flight_id):
    f = flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": f,
        "passengers": f.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=f).all()

    })


def book(request, flight_id):
    if request.method == "POST":
        flight = flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
'''

# class bid_info_manager(bid_info):
#     def create_book(self, title):
#         book = self.bid_info()
#         return book
    
def index(request):
    a_lists = auction_list.objects.all()
    state = auction_list.objects.only('auction_state')
    # al is a list of objects that contains all the targets
    # al = auction_list.objects.all().filter(auction_state=str("2"))
    al = auction_list.objects.all().filter(Q(auction_state=str("2")) | Q(auction_state=str("1")))
    # img_add is a list contains img targets that contains all the targets
    # theoracally, they will shall the same order, but need to be check or modify
    img_add = []
    bids = []
    alitems = [i.auction_item for i in al]
    maxdic = {}
    for i in alitems:
        tmp = bid_info.objects.filter(bid_item=item_info.objects.get(item_name=str(i)))
        if len(tmp)==0:
            curr_item = item_info.objects.get(item_name=i)
            tmp = bid_info.objects.create(bid_item=curr_item, 
                                          bid_user=curr_item.item_publisher, 
                                          bid_price=curr_item.item_origin_price)

        bids.append(tmp)
    for one in bids:
        for i in one:
            if i.bid_item.item_name not in maxdic:
                maxdic[i.bid_item.item_name] = i.bid_price
            if maxdic[i.bid_item.item_name] <= i.bid_price:
                maxdic[i.bid_item.item_name] = i.bid_price

    for i in range(len(al)):
        img_add.append(item_info.objects.get(item_name=al[i].auction_item))

    # for i in al:

    retarr = []
    for i in range(len(al)):
        retarr.append(
            [al[i], img_add[i], maxdic[al[i].auction_item.item_name]])
    # item_info.objects.all().filter()
    for i in al:
        updateAuctionBid(i.auction_item)

    comment_dic = {}
    # cl = comments.objects.all().filter(comment_auction=auction_list.objects.all().get(auction_id=a_lists[0].auction_id).pk)
    for i in a_lists:
        comment_dic[i.auction_id] = comments.objects.all().filter(
            comment_auction=auction_list.objects.all().get(auction_id=i.auction_id).pk)

    return render(request, "auctions/index.html", {
        "activelist": retarr,
        "len": retarr[0][0].get_num_bid_info(),
        "signal": 1,
        "comments": comment_dic
    })


def updateAuctionBid(auctionItem):
    t = auction_list.objects.get(auction_item=auctionItem)
    t.value = t.get_num_bid_info()  # change field
    t.save()  # this will update only


# def updateAuctionBidFromBidList(auctionitem, auction):

#     # check the auctions by categories


def categories(request):
    categorylist = category.objects.all()
    retarr = []
    # for i in range(len(categorylist)):
    #     retarr.append()
    return render(request, "auctions/categories.html", {
        "categorylist": categorylist
    })
    # show categroies in index page
    # . item_1
    # . item_2
    # . item_3
    # ........
    #  each has an url to its auction list


def categorysub(request, categoryname):
    # cat_name_index = category.objects.all().get(category_item=categoryname).pk
    # ai result is below.
    # <QuerySet [<item_info: American Truck Simulator>,
    #            <item_info: War Thunder>, <item_info: UBOAT>,
    #            <item_info: Silent Hunter®: Wolves of the Pacific>]>
    ai = item_info.objects.filter(
        item_category=category.objects.all().get(category_item=str(categoryname)))
    act = auction_list.objects.all()
    # return an auction with item category == categoryname
    # u = item_info.objects.all().get(item_category=category.objects.get(category_item=cat_name_index))
    retval = []
    for i in range(len(ai)):
        for j in range(len(act)):
            if ai[i].item_name == act[j].auction_item.item_name:
                retval.append([act[j], ai[i]])
    # u = item_info.objects.filter(item_category=category.objects.all().get(category_item=def categoriesSub(request, categoryname)))
    # idx = item_info.objects.get(item.item_category=category).pk
    # u = auction_list.objects.all().get(
    #     auction_item=item_info.objects.get(item_category=category))
    # item_info.objects.filter(item_category=(category.objects.get(category_item="Simulation").pk))
    #  u = auction_list.objects.filter(auction_item=(item_info.objects.filter(item_category=(category.objects.get(category_item="Simulation").pk))))
    return render(request, "auctions/categorysub.html", {
        "retval": retval,
        "len": int(len(retval))
    })

# # TODO give out all the information in that auction


def mypanel(request):
    return render(request, "auctions/mypanel.html")

# TODO Three creation functions are used to create new items, new bid, new auctions

# TODO createNewItem.
# TODO If needed, create new item, pay attention to the duplicated item


class createnewitemclass(forms.ModelForm):
    # item_publisher = forms.CharField(label='Publisher')

    class Meta:
        model = item_info
        fields = ['item_name', 'item_description', 'item_category',
                  'item_origin_price', 'item_img']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'input'}),
            'item_description': forms.TextInput(attrs={'class': 'input'}),
            # 'item_category': forms.SelectDateWidget(),
            #             'items_start_date': forms.SelectDateWidget(),
            'item_origin_price': forms.TextInput(attrs={'class': 'input'})
        }
        
    def __init__(self, *args, **kwargs):
        super(createnewitemclass, self).__init__(*args, **kwargs)
        self.fields['item_img'].required = True
        
    def clean(self):
        super(createnewitemclass, self).clean()
        item_name = self.cleaned_data.get('item_name')
        all_item_name = [i.item_name for i in item_info.objects.all()]
        if item_name in all_item_name:
            self._errors['item_name'] = self.error_class([
                'Item existed! Add another one!'])
        # return any errors if found
        return self.cleaned_data


def createnewitem(request):
    # user = request.user
    if request.method == 'POST':
        form = createnewitemclass(request.POST, request.FILES)
        if form.is_valid():
            
            
            st = form.save()
            if st.item_img is None:
                form = createnewitemclass()
                return render(request, 'auctions/createnewitem.html', {'form': form,'form_flag':True})
            st.item_publisher = request.user
            st.save()
            # return redirect('success')
            return render(request, 'auctions/createnewitem.html', {'alert_flag': True,'form_flag':False})
    else:
        form = createnewitemclass()
    return render(request, 'auctions/createnewitem.html', {'form': form,'form_flag':True})


# def createnewitem(request):
#     # user = request.user
#     if request.method == 'POST':
#         form = createnewitemclass(request.POST, request.FILES)
#         if form.is_valid():
#             st = form.save()
#             st.item_publisher = request.user
            
#             st.save()
#             # return redirect('success')
#             return render(request, 'auctions/createnewitem.html', {'alert_flag': True,'form_flag':False})
#     else:
#         form = createnewitemclass()
#     return render(request, 'auctions/createnewitem.html', {'form': form,'form_flag':True})


class createnewbidclass(forms.ModelForm):
 
    class Meta:
        model = bid_info
        fields = ['bid_item', 'bid_price']
        # fields = ['bid_item', 'bid_price']

        # widgets = {
        # 'bid_item': forms.TextInput(attrs={'class': 'input'}),
        # 'bid_price': forms.TextInput(attrs={'class': 'input'}),
        # }

    def clean(self):
        super(createnewbidclass, self).clean()
        # auction_item = self.cleaned_data.get('auction_item')
        # all_item_name = [
        #     i.auction_item.item_name for i in auction_list.objects.all()]
        # if auction_item in all_item_name:
        #     self._errors['auction_item'] = self.error_class([
        #         'Auction existed! Add another one!'])
        # msg1 = str(items_start_date)+str(type(items_start_date))
        # msg2 = str(items_end_date)+str(type(items_end_date))
        # if items_start_date:
        #     self._errors['items_start_date'] = self.error_class([
        #         'Warning '+msg1])
        # if items_end_date:
        #     self._errors['items_end_date'] = self.error_class([
        #         'Warning '+msg2])
        # return any errors if found
        return self.cleaned_data

# TODO createAuction.
# TODO create new auctions, when create new auction,
# TODO need to input the first bid as main bid,
# TODO need to create time and any other auction at the same time



class createnewauctionclass(forms.ModelForm):

    items_start_date = forms.DateField(
        label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    items_end_date = forms.DateField(
        label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = auction_list
        fields = ('auction_item','auction_owner','auction_state',
                  'items_start_date', 'items_end_date')
        widgets = {
            'items_start_date': forms.SelectDateWidget(),
            'items_end_date': forms.SelectDateWidget(),
        }

    def clean(self):
        super(createnewauctionclass, self).clean()
        # auction_owner = self.user
        auction_item = self.cleaned_data.get('auction_item')
        all_item_name = [i.auction_item.item_name for i in auction_list.objects.all()]
        # all_item_name = [i.auction_item.item_name for i in auction_list.objects.all().filter(auction_owner=user)]
        if auction_item in all_item_name:
            self._errors['auction_item'] = self.error_class([
                'Auction existed! Add another one!'])

        items_start_date = self.cleaned_data.get('items_start_date')
        items_end_date = self.cleaned_data.get('items_end_date')

        isd = str(items_start_date)
        ied = str(items_end_date)
        # msg1 = str(items_start_date)+str(type(items_start_date))
        # msg2 = str(items_end_date)+str(type(items_end_date))
        errmsg = 'Start Date should be earlier than End Date'
        errmsg1 = 'Start Date should not be earlier than Today'
        errmsg2 = 'End Date should not be earlier than Today'

        if not dateTimeCmp(isd, ied):
            self._errors['items_start_date'] = self.error_class([
                errmsg])
            self._errors['items_end_date'] = self.error_class([
                errmsg])
        if dateTimeTodayCmp(isd):
            self._errors['items_start_date'] = self.error_class([
                errmsg1])
        if dateTimeTodayCmp(ied):
            self._errors['items_end_date'] = self.error_class([
                errmsg2])
        # if items_start_date > items_end_date:
        #     self._errors['items_start_date'] = self.error_class([
        #         'Wrong Date Settings!'])
        #     self._errors['items_end_date'] = self.error_class([
        #         'Wrong Date Settings!'])
        # return any errors if found
        return self.cleaned_data

# TODO createBid.
# TODO create new bid based on the items existed in database or user created by createNewItem


def createnewbidauction(request):
    infos="ori "
    if request.method == 'POST':
        form1 = createnewbidclass(request.POST)
        form2 =  createnewauctionclass(request.POST)
        infos+=" if1"
        if form1.is_valid() and form2.is_valid():
            # add some exception check here
            # date validation, name validation
            # form2.cleaned_data['auction_item'] = str(form1.cleaned_data['bid_item'])
            test = "bid_item " + \
                str(form1.cleaned_data['bid_item'])+" auction_item" + \
                str(form2.cleaned_data['auction_item'])
            print("outter if")
            print(str(form1.cleaned_data['bid_item']))
            print(str(form2.cleaned_data['auction_item']))
            infos = "if2 "+str(form1.cleaned_data['bid_item'])+" "+str(form2.cleaned_data['auction_item'])
            if str(form1.cleaned_data['bid_item']) != str(form2.cleaned_data['auction_item']):
                # print("if")
                # print(str(form1.cleaned_data['bid_item']))
                # print(str(form2.cleaned_data['auction_item']))

                return render(request, 'auctions/createnewbidauction.html', {'same_flag': True,
                                                                             "itms": test,
                                                                             "infos":infos})
            else:
                print("else")

                # add one if, whether this auction_item is in the auction_item list
                test = str(form2.cleaned_data['auction_item'])
                # current_bid_id = uuid.UUID(str(form1.cleaned_data['bid_id']))
                # userPk(request)
                all_auction_item = [i.auction_item.item_name for i in auction_list.objects.all(
                ).filter(auction_owner=User.objects.all().get(username=request.user).pk)]
                if test in all_auction_item:
                    return render(request, 'auctions/createnewbidauction.html', {'exist_flag': True,
                                                                                 "infos":infos})
                # form2.cleaned_data['auction_bid_count'] = 0
                st1 = form1.save()
                st1.bid_user = request.user
                # st1.bid_
                st1.save()
                st2 = form2.save()
                st2.auction_owner = request.user
                st2.auction_state = "2"
                st2.save()
                # act= [i.auction_item for i in auction_list.objects.all().filter(auction_owner=User.objects.all().get(username="redhat").pk)]
                # update current bid number
                # updateAuctionBid(auctionItem)
                curbid = uuid.UUID(str(st1.bid_id))
                # curact = uuid.UUID(str(st2.auction_id))
                current_auction_item = auction_list.objects.all().get(
                    auction_item=item_info.objects.all().get(item_name=test))
                
                tmp = auction_list.objects.get(auction_owner=User.objects.all().get(
                    username=request.user).pk, auction_item=item_info.objects.get(item_name=test))
                # tmp = auction_list.objects.filter(auction_owner=User.objects.all().get(username="redhat").pk)
                # tmp = auction_list.objects.all().get(auction_owner=request.user)
                # update bid_count
                tmp.auction_bid_count = bid_info.objects.filter(
                    bid_item=item_info.objects.all().get(item_name=test)).count()
                # update auction_bid
                tmp.auction_bid.add(st1)
                tmp.save()
                # updateAuctionBid(current_auction_item.auction_item)
                # add the base bid into the auction
                # get current bid_id and then add to current auction list
                # TODO !!!!
                # return redirect('success')
                return render(request, 'auctions/createnewbidauction.html', {'alert_flag': True,
                                                                             "infos":infos
                                                                             })
    else:
        infos+=" else1"
        form1 = createnewbidclass()
        form1.fields["bid_item"].queryset = item_info.objects.filter(item_publisher=request.user)
        
        form2 = createnewauctionclass()
        form2.fields["auction_owner"].queryset = User.objects.filter(username=request.user)
        form2.fields["auction_item"].queryset =item_info.objects.filter(item_publisher=request.user)
        # form2.fields["auction_item"].queryset = auction_list.objects.filter(auction_ownerUser.objects.filter(username=request.user)

    return render(request, 'auctions/createnewbidauction.html', {'form1': form1,
                                                                 'form2': form2,
                                                                 "infos":infos})

# TODO 1. display all the bids user owns
# TODO 2. display all the auctions user owns


def getData(request):
    # user index_id in database
    name = request.user
    retstr = "Post content here"
    upks = User.objects.all().get(username=name).pk
    # user user index_id to get his watching auctions
    b_ids = [i.watchlist_auction.auction_id for i in watchlists.objects.all(
    ).filter(watchlist_user=upks)]
    lts = [auction_list.objects.all().get(auction_id=i) for i in b_ids]
    #  get all bid id, ids is one item of lts
    # ids.auction_bid.all().values_list('bid_id',flat=True)
    return lts

# ANCHOR Nav to watchinglist, and send auctions user is watching


def watchinglist(request):
    # data_all = auction_list.objects.all().filter(auction_state=2)
    data_all = auction_list.objects.all()

    data_watching = getData(request)
    return render(request, "auctions/watchinglist.html", {
        "data_all": data_all,
        "data_watching": data_watching
    })

def addWatchinglist_inlisting(request):
    lis = []
    itemname = None
    if request.method == 'POST':
        itemname = request.POST['itemname']
    current_user = request.user    
    # process watching
    myWatching_list = [i.watchlist_auction for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    
    myWatching_list_name = [i.watchlist_auction.auction_item.item_name for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    
    watchflag = "notwatch"
    if itemname in myWatching_list_name:
        
        # delete the watching
        wl = watchlists.objects.get(watchlist_user=User.objects.all().get(
                username=request.user), watchlist_auction=auction_list.objects.get(auction_item=item_info.objects.get(item_name=itemname)))
        wl.delete()
    else:
        # add watching 
        wl = watchlists(watchlist_user=User.objects.all().get(
                username=request.user), watchlist_auction=auction_list.objects.get(auction_item=item_info.objects.get(item_name=itemname)))
        wl.save()
    myWatching_list_name = [i.watchlist_auction.auction_item.item_name for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    
    watchflag = None
    if itemname in myWatching_list_name:
        watchflag = "currentwatching" 
    else:
        watchflag = "currentnotwatching"
    a_lists = auction_list.objects.all()
    # state = auction_list.objects.only('auction_state')
    # al is a list of objects that contains all the targets
    al = auction_list.objects.all().get(Q(auction_item=item_info.objects.get(
        item_name=itemname)), Q(auction_state=str("2"))| Q(auction_state=str("1")) )
    # al = auction_list.objects.all().get(auction_item=item_info.objects.get(
        # item_name=auction_item), auction_state=str("2"))
        
    # img_add is a list contains img targets that contains all the targets
    # theoracally, they will shall the same order, but need to be check or modify
    img_add = []
    al = [al]
    for i in range(len(al)):
        img_add.append(item_info.objects.get(item_name=al[i].auction_item))

    # get current auction bids and filter the biggest one
    
    current_auction = al[0]
    
    bids = bid_info.objects.all().filter(bid_item=item_info.objects.get(item_name=itemname))
    
    current_high=0
    
    for i in bids:
        if i.bid_price>=current_high:
            current_high = i.bid_price
    
    retarr = []
    # for i in range(len(al)):
    retarr.append(al[0])
    retarr.append(img_add[0])
    retarr.append(current_high)

    # item_info.objects.all().filter()
    for i in al:
        updateAuctionBid(i.auction_item)
    # print(len(retarr))
    # print(len(retarr[0]))
    # print(len(retarr[1]))

    comment_dic = {}
    # cl = comments.objects.all().filter(comment_auction=auction_list.objects.all().get(auction_id=a_lists[0].auction_id).pk)
    for i in a_lists:
        comment_dic[i.auction_id] = comments.objects.all().filter(
            comment_auction=auction_list.objects.all().get(auction_id=i.auction_id).pk)
    tag = "fromsubmitcomments"
    # return watching state
    
    # return all info

    return render(request, "auctions/listing.html", {
        "activelist": retarr,
        "watchflag": watchflag,
        "signal": 1,
        "comments": comment_dic,
        "tag": tag,
        "itemname":itemname+" add"
    })
    
    

def addWatchinglist(request):
    lis = []
    if request.method == 'POST':
        lis = request.POST.getlist('checkbox_add')
    # auction_get = []
    # myWatching = watchlists.objects.all().filter(watchlist_user=request.user)
    # user_now_watching_item = [i.watchlist_auction.auction_item.item_name for i in watchlists.objects.all(
    # ).filter(watchlist_user=userPk(request))]
    # add check box content to my watchinglist
    # check box auction
    als = [auction_list.objects.all().get(
        auction_item=item_info.objects.all().get(item_name=i).pk) for i in lis]
    # check box auction name
    auction_name_list = [auction_list.objects.all().get(auction_item=item_info.objects.all(
    ).get(item_name=i).pk).auction_item.item_name for i in lis]
    myWatching_list = [i.watchlist_auction for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    # duplicate check
    duplicate_check = False
    duplicate_name_list = []
    for i in als:
        if i not in myWatching_list:
            wl = watchlists(watchlist_user=User.objects.all().get(
                username=request.user), watchlist_auction=i)
            wl.save()
        if i in myWatching_list:
            duplicate_check = True
            duplicate_name_list.append(i)
    # add current auction id and current user name
    # publisher = Publisher(name=p1,address=p2)
    # publisher.save()
    # current active auctions
    data_all = auction_list.objects.all().filter(Q(auction_state=2)|Q(auction_state=1))
    # current watching auctions(active and not active)
    data_watching = getData(request)
    return render(request, "auctions/watchinglist.html", {
        "data_all": data_all,
        "data_watching": data_watching,
        "msg1": str(als),
        "duplicate_alert": duplicate_check,
        "duplicate_list": watchinglistDupMsg(duplicate_name_list)
    })


def deleteWatchinglist(request):
    lis = []
    if request.method == 'POST':
        lis = request.POST.getlist('checkbox_delete')
    # content in check box
    # type auction_list
    als = [auction_list.objects.all().get(
        auction_item=item_info.objects.all().get(item_name=i).pk) for i in lis]
    # emp = Employee.objects.get(pk = id)
    # emp.delete()
    # user list to get auction list
    myWatching_list = [i.watchlist_auction for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    for i in als:
        tmp = watchlists.objects.get(
            watchlist_user=userPk(request), watchlist_auction=i)
        tmp.delete()

    data_all = auction_list.objects.all().filter()
    data_watching = getData(request)
    return render(request, "auctions/watchinglist.html", {
        "data_all": data_all,
        "data_watching": data_watching,
        "als": str(lis)
    })

# class watchingListForm(forms.Form):
#     class Meta:
#         model = watchlists
#         fields = ['watchlist_auction']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super(watchingListForm, self).__init__(*args, **kwargs)
#         self.fields['lists'].queryset = watchlists.objects.filter(
#             watchlist_user=user)

#     lists = forms.ModelChoiceField(
#         queryset=None, widget=forms.Select, required=True)


def watchinglistsub(request, itemname):
    # return item infomation and bid information over it
    bid_list = bid_info.objects.all().filter(
        bid_item=item_info.objects.get(item_name=itemname).pk)
    return render(request, "auctions/watchinglistsub.html", {
        "itemname": bid_list
    })


def bid_with_detail(request):
    # current bids
    itemname = ""
    if request.method == 'POST':
        itemname = request.POST['itemname']
    current_bid = bid_info.objects.all().filter(
        bid_item=item_info.objects.all().get(item_name=itemname).pk)
    current_bid_user = [i.bid_user.username for i in current_bid]
    item_price_name = [[i.bid_item.item_name, i.bid_price,
                        i.bid_user.username] for i in current_bid]
    duplicate_flag = False

    if request.user in current_bid_user:
        duplicate_flag = True
    sorted_item_price_name = sorted(
        item_price_name, key=lambda item_price: item_price[1])

    current_bid_max = sorted_item_price_name[-1][1]

    return render(request, "auctions/bidpage.html", {
        "itemname": itemname,
        "current_bids": current_bid,
        "current_bid_max": current_bid_max
    })



def biditem(request):
    it = ""
    front_price = 0
    not_number = False
    not_max = False
    duplicate_flag = False

    msg = ""
    if request.method == 'POST':
        it = request.POST["auction_item"]
        front_price = str(request.POST["price"])
    # number check
    current_bid_user = str(request.user)
    current_bid = bid_info.objects.all().filter(
        bid_item=item_info.objects.all().get(item_name=it))
    current_bid_user_list = [i.bid_user.username for i in current_bid]
    current_user_name = str(request.user)
    item_price_name = [[i.bid_item.item_name, i.bid_price, i.bid_user.username]
                       for i in current_bid]
    sorted_item_price_name = sorted(
        item_price_name, key=lambda item_price: item_price[1])
    current_bid_max = sorted_item_price_name[-1][1]

    if current_bid_user in current_bid_user_list:
        duplicate_flag = True
        msg = "You have bid"
        return render(request, "auctions/bidpage.html", {
            "itemname": it,
            "current_bids": current_bid,
            "current_bid_max": current_bid_max,
            "not_number": not_number,
            "msg": msg})

    if not front_price.isnumeric():
        not_number = True
        msg = "Invalid Input"
        return render(request, "auctions/bidpage.html", {
            "itemname": it,
            "current_bids": current_bid,
            "current_bid_max": current_bid_max,
            "not_number": not_number,
            "msg": msg})

    front_price = float(front_price)
    if front_price <= current_bid_max:
        not_max = True
        msg = "Input too small"
        return render(request, "auctions/bidpage.html", {
            "itemname": it,
            "current_bids": current_bid,
            "current_bid_max": current_bid_max,
            "not_max": not_max,
            "msg": msg})
    # current active bids
    # create bid
    item = item_info.objects.all().get(item_name=it)
    cur_user = User.objects.all().get(username=request.user)
    new_bid = bid_info(
        bid_item=item,
        bid_price=front_price,
        bid_user=cur_user)
    new_bid.save()
    
    current_bid = bid_info.objects.all().filter(
        bid_item=item_info.objects.all().get(item_name=it))
    current_bid_max = sorted_item_price_name[-1][1]

    return render(request, "auctions/bidpage.html", {
        "itemname": it,
        "pr": front_price,
        "current_bids": current_bid,
        "current_bid_max": current_bid_max
    })


def editbid(request):
    current_bid_user = str(request.user)
    current_bid_own = bid_info.objects.all().filter(
        bid_user=User.objects.all().get(username=current_bid_user).pk)

    return render(request, "auctions/editbid.html", {
        "current_bid_own": current_bid_own
    })


def bidprice(request):

    itemname = ""
    front_price = 0
    not_number = False
    not_max = False
    duplicate_flag = False

    msg = ""
    if request.method == 'POST':
        itemname = request.POST["biditem"]
        front_price = str(request.POST["newbidprice"])

    current_bid_user = str(request.user)

    current_bid = bid_info.objects.all().get(bid_item=item_info.objects.all().get(
        item_name=itemname).pk, bid_user=User.objects.all().get(username=current_bid_user).pk)
    current_bid_price = current_bid.bid_price

    current_bid_own = bid_info.objects.all().filter(
        bid_user=User.objects.all().get(username=current_bid_user).pk)


    if not front_price.isnumeric():
        msg = "Invalid Input"
        return render(request, "auctions/editbid.html", {
            "itemname": itemname,
            "current_bid_own": current_bid_own,
            "msg": msg})

    front_price = float(front_price)

    if front_price <= current_bid_price:
        msg = "New Price should BIGGER than previous one"
        return render(request, "auctions/editbid.html", {
            "itemname": itemname,
            "current_bid_own": current_bid_own,
            "msg": msg})

    current_bid.bid_price = front_price
    current_bid.save()

    return render(request, "auctions/editbid.html", {
        "current_bid_own": current_bid_own,
        "itemname": itemname,
    })


def biddelete(request):
    if request.method == 'POST':
        lis = request.POST.getlist('checkbox_bid_delete')
    # lst = str(type(lis))
    current_bid_user = str(request.user)
    current_bid_own = bid_info.objects.all().filter(
        bid_user=User.objects.all().get(username=current_bid_user).pk)
    
    # if current bid == 1
    #   Then do not delete
    msg = ""
    alertflag = ""
    for i in current_bid_own:
        if i.bid_item.item_name in lis:
            if i.bid_item.item_publisher==request.user:
                msg = "Cannot delete item base bid"
                alertflag = "alertflag"
            else:
                i.delete()
    current_bid_own = bid_info.objects.all().filter(
        bid_user=User.objects.all().get(username=current_bid_user).pk)
    return render(request, "auctions/editbid.html", {
        "current_bid_own": current_bid_own,
        "lis": lis,
        "alertflag":alertflag,
        "msg":msg
    })


def editauction(request):
    current_auction_user = str(request.user)
    current_auction_own = auction_list.objects.all().filter(
        auction_owner=User.objects.all().get(username=current_auction_user).pk)
    auction_max = []
    for i in current_auction_own:
        current_bid = bid_info.objects.all().filter(
            bid_item=item_info.objects.all().get(item_name=i.auction_item.item_name).pk)
        maxprice = 0
        for j in current_bid:
            if j.bid_price >= maxprice:
                maxprice = j.bid_price
        auction_max.append([i, maxprice])

    return render(request, "auctions/editauction.html", {
        "current_auction_own": current_auction_own,
        "auction_max": auction_max
    })


def executeauction(request):
    if request.method == 'POST':
        auctionname = request.POST["auction"]

    current_auction_user = str(request.user)
    current_auction_own = auction_list.objects.all().filter(
        auction_owner=User.objects.all().get(username=current_auction_user).pk)
    auction_max = []
    for i in current_auction_own:
        current_bid = bid_info.objects.all().filter(
            bid_item=item_info.objects.all().get(item_name=i.auction_item.item_name).pk)
        maxprice = 0
        for j in current_bid:
            if j.bid_price >= maxprice:
                maxprice = j.bid_price
        auction_max.append([i, maxprice])

    # find the user who give out the highest price
    # change the user
    cur_auction = auction_list.objects.all().get(
        auction_item=item_info.objects.all().get(item_name=auctionname).pk)
    cur_auction_bids = bid_info.objects.all().filter(
        bid_item=item_info.objects.all().get(item_name=auctionname).pk)
    maxprice = 0
    auctiongetter = ""
    for j in cur_auction_bids:
        if j.bid_price >= maxprice:
            maxprice = j.bid_price
            auctiongetter = j.bid_user
    tmp = item_info.objects.get(item_name=auctionname)
    tmp.item_publisher = auctiongetter
    tmp.save()

    cur_auction.auction_state = 1
    cur_auction.save()
    # for i in cur_auction_bids:
    #     i.delete()
    # bid add one data are invalid or not

    return render(request, "auctions/editauction.html", {
        "current_auction_own": current_auction_own,
        "auction_max": auction_max})


def oneacution(request, auction_item):
    # save comments
    itemname = None
    if request.method == 'POST':
        itemname = request.POST["item_name"]
        comment_words = request.POST["item_comment"]
        user = str(request.user)
        tmpcomment = comments(comment_content=comment_words,
                              comment_user=User.objects.get(username=user))
        tmpcomment.save()
        # p = Person(first_name="Bruce", last_name="Springsteen")
        # p.save(force_insert=True)
    # retrive comments and display
    a_lists = auction_list.objects.all()
    state = auction_list.objects.only('auction_state')
    # al is a list of objects that contains all the targets
    al = auction_list.objects.all().get(Q(auction_item=item_info.objects.get(
        item_name=auction_item)), Q(auction_state=str("2"))| Q(auction_state=str("1")) )
    # al = auction_list.objects.all().get(auction_item=item_info.objects.get(
        # item_name=auction_item), auction_state=str("2"))
        
    # img_add is a list contains img targets that contains all the targets
    # theoracally, they will shall the same order, but need to be check or modify
    img_add = []
    al = [al]
    for i in range(len(al)):
        img_add.append(item_info.objects.get(item_name=al[i].auction_item))

    # get current auction bids and filter the biggest one
    
    current_auction = al[0]
    
    bids = bid_info.objects.all().filter(bid_item=item_info.objects.get(item_name=auction_item))
    
    current_high=0
    
    for i in bids:
        if i.bid_price>=current_high:
            current_high = i.bid_price
    
    retarr = []
    # for i in range(len(al)):
    retarr.append(al[0])
    retarr.append(img_add[0])
    retarr.append(current_high)

    # item_info.objects.all().filter()
    for i in al:
        updateAuctionBid(i.auction_item)
    # print(len(retarr))
    # print(len(retarr[0]))
    # print(len(retarr[1]))

    comment_dic = {}
    # cl = comments.objects.all().filter(comment_auction=auction_list.objects.all().get(auction_id=a_lists[0].auction_id).pk)
    for i in a_lists:
        comment_dic[i.auction_id] = comments.objects.all().filter(
            comment_auction=auction_list.objects.all().get(auction_id=i.auction_id).pk)
    tag = "fromsubmitcomments"
    
    myWatching_list_name = [i.watchlist_auction.auction_item.item_name for i in watchlists.objects.all().filter(
        watchlist_user=userPk(request))]
    itemname = auction_item

    watchflag = None
    if str(itemname) in myWatching_list_name:
        watchflag = "currentwatching"
    else:
        watchflag = "currentnotwatching"
        
        
        
    return render(request, "auctions/listing.html", {
        "activelist": retarr,
        "watchflag": watchflag,
        "signal": 1,
        "comments": comment_dic,
        "tag": tag,
        "myWatching_list_name":myWatching_list_name,
        "itemname":itemname
    })


def submitcomments(request):
    # save comments
    if request.method == 'POST':
        auctionid = request.POST["auction_id"]

        comment_words = request.POST["item_comment"]
        user = str(request.user)
        tmpcomment = comments(comment_auction=auction_list.objects.get(auction_id=auctionid),
                              comment_content=comment_words,
                              comment_user=User.objects.get(username=user))
        tmpcomment.save()
        # p = Person(first_name="Bruce", last_name="Springsteen")
        # p.save(force_insert=True)
    # retrive comments and display
    current_auction_id = request.POST["auction_id"]

    a_lists = auction_list.objects.all()
    state = auction_list.objects.only('auction_state')
    # al is a list of objects that contains all the targets
    al = auction_list.objects.all().filter(Q(auction_state=str("2"))|Q(auction_state=str("1")),Q(auction_id=current_auction_id))
    # img_add is a list contains img targets that contains all the targets
    # theoracally, they will shall the same order, but need to be check or modify
    img_add = []
    for i in range(len(al)):
        img_add.append(item_info.objects.get(item_name=al[i].auction_item))

    # retarr = []
    # retarr.append(al[i])
    # retarr.append(img_add[i])
    # item_info.objects.all().filter()
    for i in al:
        updateAuctionBid(i.auction_item)

    comment_dic = {}
    # cl = comments.objects.all().filter(comment_auction=auction_list.objects.all().get(auction_id=a_lists[0].auction_id).pk)
    for i in a_lists:
        comment_dic[i.auction_id] = comments.objects.all().filter(
            comment_auction=auction_list.objects.all().get(auction_id=i.auction_id).pk)
    tag = "fromsubmitcomments"
    return HttpResponseRedirect(reverse('oneacution', args=[al[0].auction_item]))
    # return render(request, "auctions/listing.html", {
    #     "activelist": retarr,
    #     "len": retarr[0][0].get_num_bid_info(),
    #     "signal": 1,
    #     "comments": comment_dic,
    #     # "tag": tag
    # })


'''
If the user is signed in and is the one who created the listing, 
the user should have the ability to “close” the auction from this page, 
which makes the highest bidder the winner of the auction and makes the listing no longer active.

If a user is signed in on a closed listing page, 
and the user has won that auction, the page should say so.
'''

# find current bids and list them
# must give the price that is equal or larger than the current max bid price
# check whether current has bid, if current user has bided this item before,
# he is allowed to reset his price, but must higher than the current max

# get auction_id
# from form with hidden input
#
# 1 check whether has bid before
# 2 if not add this bid
# 2 if has bid, use the current price update the previous one
# get all su
# def createnewitem(request):
#     if request.method == 'POST':
#         form = createnewitemclass(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             # return redirect('success')
#             return render(request, 'auctions/createnewitem.html', {'alert_flag': True})
#     else:
#         form = createnewitemclass()
#     return render(request, 'auctions/createnewitem.html', {'form': form})

# class createnewbidclass(forms.ModelForm):
#     class Meta:
#         model=bid_info
#         fields=['bid_item']

# class createnewauctionclass(forms.ModelForm):
#     class Meta:
#         model=auction_list
#         fields=['']

# def auctiondetails(request, categoryname, itemname):
#     a_lists = auction_list.objects.all()
#     target = 0
#     for i in a_lists:
#         if i.auction_item.item_name == itemname and i.auction_state == "2":
#             target = i
#     # state = auction_list.objects.only('auction_state')
#     # al is a list of objects that contains all the targets
#     # al = auction_list.objects.all().filter(auction_state=str("2"))
#     # img_add is a list contains img targets that contains all the targets
#     # theoracally, they will shall the same order, but need to be check or modify
#     return render(request, "auctions/auctiondetails.html", {
#         "items": target
#     })
def myitems(request):
    uname=None
    if request.method == 'POST':
        uname = request.POST["username"]
    uname = request.user
    my_items = item_info.objects.all().filter(item_publisher=User.objects.get(username=uname))

    my_auction = auction_list.objects.all().filter(auction_state=str("2"),auction_owner=User.objects.get(username=uname))
    auction_dic = {}
    
    alitems = [i.auction_item for i in my_auction]
    maxdic = {}
    bids=[]
    
    for i in alitems:
        bids.append(bid_info.objects.filter(
            bid_item=item_info.objects.get(item_name=str(i))))
        
    for one in bids:
        for i in one:
        # print(i.bid_price)
            if i.bid_item.item_name not in maxdic:
                maxdic[i.bid_item.item_name] = [i.bid_price,i.bid_user.username]
            if maxdic[i.bid_item.item_name][0] <= i.bid_price:
                maxdic[i.bid_item.item_name] = [i.bid_price,i.bid_user.username]
    retarr = []
    for i in maxdic:
        retarr.append([i,maxdic[i][0],maxdic[i][1]])
    return render(request, "auctions/myitem.html", {
        "my_items": my_items,
        "my_auction":my_auction,
        "maxdic":retarr,
    })   

def wantit(request):
    if request.method == 'POST':
        currentitem = request.POST["itemname"]
        currentbider = request.POST["currbiduname"]
        # ! find the item
        currentitem_obj = item_info.objects.all().get(item_name=currentitem)
        currentitem_obj.item_publisher = User.objects.get(username=currentbider)
        
        currentitem_obj.save()
        
        currentauction = auction_list.objects.all().get(auction_item=item_info.objects.all().get(item_name=currentitem) ,auction_owner=User.objects.get(username=request.user))

        currentauction.auction_state = "1"
        currentauction.save()
        # uname = request.POST["username"]
        uname = request.user
        my_items = item_info.objects.all().filter(item_publisher=User.objects.get(username=uname))

        my_auction = auction_list.objects.all().filter(auction_state=str("2"),auction_owner=User.objects.get(username=uname))
        auction_dic = {}
        
        alitems = [i.auction_item for i in my_auction]
        maxdic = {}
        bids=[]
        
        for i in alitems:
            bids.append(bid_info.objects.filter(
                bid_item=item_info.objects.get(item_name=str(i))))
            
        for one in bids:
            for i in one:
            # print(i.bid_price)
                if i.bid_item.item_name not in maxdic:
                    maxdic[i.bid_item.item_name] = [i.bid_price,i.bid_user.username]
                if maxdic[i.bid_item.item_name][0] <= i.bid_price:
                    maxdic[i.bid_item.item_name] = [i.bid_price,i.bid_user.username]
        retarr = []
        
        for i in maxdic:
            retarr.append([i,maxdic[i][0],maxdic[i][1]])
        return render(request, "auctions/myitem.html", {
            "my_items": my_items,
            "my_auction":my_auction,
            "maxdic":retarr,
        })   
        '''
        1. find the auction. set as unavailable. 
        2. set the item_user to currbiduname
        3. remove all related bids
        
        '''
"""    bids = []
    alitems = [i.auction_item for i in my_auction]
    maxdic = {}
    for i in alitems:
        bids.append(bid_info.objects.filter(S
            bid_item=item_info.objects.get(item_name=str(i))))
    for one in bids:
        for i in one:
            # print(i.bid_price)
            if i.bid_item.item_name not in maxdic:
                maxdic[i.bid_item.item_name] = i.bid_price
            if maxdic[i.bid_item.item_name] <= i.bid_price:
                maxdic[i.bid_item.item_name] = i.bid_price
"""


"""
def biditem(request):
    it = ""
    front_price = 0
    not_number = False
    not_max = False
    duplicate_flag = False

    msg = ""
    if request.method == 'POST':
        it = request.POST["auction_item"]
        front_price = str(request.POST["price"])
    # number check
    current_bid_user = str(request.user)
    current_bid = bid_info.objects.all().filter(
        bid_item=item_info.objects.all().get(item_name=it))
    current_bid_user_list = [i.bid_user.username for i in current_bid]
    current_user_name = str(request.user)
    item_price_name = [[i.bid_item.item_name, i.bid_price, i.bid_user.username]
                       for i in current_bid]
    sorted_item_price_name = sorted(
        item_price_name, key=lambda item_price: item_price[1])
    current_bid_max = sorted_item_price_name[-1][1]

    if current_bid_user in current_bid_user_list:
        duplicate_flag = True
"""
