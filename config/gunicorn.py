from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


bind = '0.0.0.0:8000'
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()

env = {
    'DJANGO_SETTINGS_MODULE': 'config.settings'
}

reload = True
name = 'blog_platform'
