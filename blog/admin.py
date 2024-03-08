from django.contrib import admin

from blog.models import Post, Payment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class Paymentdmin(admin.ModelAdmin):
    pass
