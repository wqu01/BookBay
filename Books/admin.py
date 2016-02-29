from django.contrib import admin
from Books.models import *

admin.site.register(book)
admin.site.register(user)
admin.site.register(book_visit)
admin.site.register(user_visit)
admin.site.register(user_complaints)
admin.site.register(book_complaints)
admin.site.register(sale)
admin.site.register(auction)
admin.site.register(Bid)
admin.site.register(comment)
admin.site.register(book_comment)
admin.site.register(user_comment)
admin.site.register(complaint_contest)
admin.site.register(three_complaints)