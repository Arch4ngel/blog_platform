

def add_view_permission(user):
    user.user_permissions.add('blog.view_post')
    return user
