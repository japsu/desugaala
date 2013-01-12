import json
from functools import wraps

from django.http import HttpResponse
from django.core.cache import cache
from django.http import HttpResponseForbidden

def json_rest(func):
  @wraps(func)
  def inner(request, *args, **kwargs):
    try:
      data = json.loads(request.body)
    except ValueError:
      return HttpResponse('bad request', status=400)

    result = func(request, data, *args, **kwargs)
    return HttpResponse(json.dumps(result), content_type='application/json')

  return inner

# http://djangosnippets.org/snippets/2017/
def throttle_post(func, duration=5):
  def inner(request, *args, **kwargs):
    if request.method == 'POST':
      remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
        request.META.get('REMOTE_ADDR')
      key = '%s.%s' % (remote_addr, request.get_full_path())
      if cache.get(key):
        return HttpResponseForbidden('Try slowing down a little.')
      else:
        cache.set(key, 1, duration)
    return func(request, *args, **kwargs)
  return inner