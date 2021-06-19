from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

ITEM_STATE = (("1", "Not Available"), ("2", "For Sale"))
AUCTION_STATE = (("1", "Not Available"), ("2", "Available"))


class User(AbstractUser):
    pass


class category(models.Model):
    category_item = models.CharField(max_length=200, verbose_name="Category")
    category_description = models.CharField(
        max_length=1000, verbose_name="Description")

    class Meta:
        verbose_name = "Item Category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category_item


class item_info(models.Model):
    item_name = models.CharField(max_length=200, verbose_name="Name")
    item_description = models.TextField(
        max_length=1000, verbose_name="Description")
    item_category = models.ForeignKey(
        category, null=True, on_delete=models.SET_NULL, verbose_name="Category")
    item_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Item ID")
    item_origin_price = models.FloatField(
        max_length=64, verbose_name="Origin Price")
    # active or not / on auction or off auction
    item_state = models.CharField(
        max_length=50, choices=ITEM_STATE, default="1", verbose_name="Item State")
    item_publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="owener",
                                       verbose_name="Publisher")
    item_publish_date = models.DateTimeField(
        null=True, auto_now_add=True, verbose_name="Publish date")
    item_img = models.ImageField(
        upload_to='pictures/', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Item Info"
        verbose_name_plural = verbose_name

class bid_info(models.Model):
    bid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Bid ID")
    bid_item = models.ForeignKey(item_info, null=True, on_delete=models.    SET_NULL, related_name="bid_item",
                                 verbose_name="Item")
    bid_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="bid_user",
                                 verbose_name="Bider")
    bid_date = models.DateTimeField(auto_now_add=True, verbose_name="Bid date")
    bid_price = models.FloatField(max_length=64, verbose_name="Bid Price")

    def get_num_bid_info(self):
        num = bid_info.object.all().count  # NOT WORKING
        return num

    def __str__(self):
        retinfo = str(self.bid_item.item_name+" "+self.bid_user.username)
        return retinfo

    class Meta:
        verbose_name = "Bid Info"
        verbose_name_plural = verbose_name

    # flights = models.ManyToManyField(flight, blank=True, related_name="passengers")


class auction_list(models.Model):
    auction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Auction ID")
    # auction_bid = models.ForeignKey(bid_info, null=True, on_delete=models.SET_NULL, related_name="auction_bid",
    #                                 verbose_name="Auction")
    auction_item = models.ForeignKey(item_info, null=True, on_delete=models.SET_NULL, related_name="auction_item_name", verbose_name="Auction item")
    # auction_item_id = models.ForeignKey(item_info, null=True, on_delete=models.SET_NULL, related_name="auction_item_id",
    #                                  verbose_name="Auction Item ID")
    auction_owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="auction_owner",verbose_name="Auction Owner")

    auction_bid = models.ManyToManyField(
        bid_info, blank=True, related_name="Auction")
    
    auction_state = models.CharField(
        max_length=50, choices=AUCTION_STATE, default="1", verbose_name="Auction State")
    
    items_start_date = models.DateTimeField(
        auto_created=True, verbose_name="Start Date")
    
    items_end_date = models.DateTimeField(
        auto_created=True, verbose_name="End Date")
    
    auction_bid_count = models.IntegerField(
        null=True, blank=True, verbose_name="Bid Count")
    # auction_woner

    def __str__(self):
        retinfo = str(self.auction_id)
        return retinfo

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = verbose_name

    def get_num_bid_info(self):
        return bid_info.objects.filter(bid_item=self.auction_item).count()


class comments(models.Model):
    comment_date = models.DateTimeField(
        null=True, auto_now_add=True,  verbose_name="Comment Date")
    comment_content = models.CharField(
        max_length=200, verbose_name="Comment")
    comment_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="comment_user",
                                     verbose_name="User")
    comment_auction = models.ForeignKey(auction_list, null=True, on_delete=models.SET_NULL, related_name="comment_bid",
                                        verbose_name="Auction")

    def __str__(self):
        retinfo = str(self.comment_user)
        return retinfo

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = verbose_name


class watchlists(models.Model):
    watchlist_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="watchlist_user",
                                       verbose_name="User")
    watchlist_auction = models.ForeignKey(auction_list,  null=True, on_delete=models.SET_NULL, related_name="watchlists_auction",
                                          verbose_name="Auction")

    class Meta:
        verbose_name = "Watchlist"
        verbose_name_plural = verbose_name

    def __str__(self):
        retinfo = str(self.watchlist_user)
        return retinfo
