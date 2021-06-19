from django.contrib import admin
from .models import User, item_info, bid_info, comments, auction_list, category, watchlists
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# https://stackoverflow.com/questions/37539132/display-foreign-key-columns-as-link-to-detail-object-in-django-admin


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


class CustomUserAdmin(UserAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "item_category", "item_description",
                    "item_id", "item_origin_price", "item_state", "item_publisher", "item_publish_date")
    ordering = ("item_name",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=item_info.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_item", "category_description")
    ordering = ("category_item",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=category.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class BidinfoAdmin(admin.ModelAdmin):
    list_display = ("bid_id", "bid_item", "bid_user",
                    "bid_date", "bid_price")
    ordering = ("bid_id",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=bid_info.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class AuctionListAdmin(admin.ModelAdmin):
    list_display = ("auction_id", "auction_item", "auction_state", "items_start_date",
                    "items_end_date", "auction_bid_count", "auction_owner")
    filter_horizontal = ("auction_bid",)
    ordering = ("auction_id",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=auction_list.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("watchlist_user", "watchlist_auction")
    ordering = ("watchlist_user",)

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=watchlists.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"
# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#         "age",
#         linkify(field_name="country"),
#         linkify(field_name="career"),
#     ]


class CommentAdmin(admin.ModelAdmin):
    # list_display = ("bid_item", "bid_user")
    list_display = ("comment_auction", "comment_user", "comment_date",
                    "comment_content")
    ordering = ("comment_auction",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=comments.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


admin.site.register(watchlists, WatchlistAdmin)

admin.site.register(User, CustomUserAdmin)
admin.site.register(item_info, ItemAdmin)
admin.site.register(bid_info, BidinfoAdmin)
admin.site.register(comments, CommentAdmin)
admin.site.register(auction_list, AuctionListAdmin)
admin.site.register(category, CategoryAdmin)
