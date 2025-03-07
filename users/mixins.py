from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response

"""
Ratelimit Mixin class only for ViewSets
"""
class RateLimitMixin:
    rate_limits = {
        'GET' : '10/m',
        'POST' : '5/m',
        'PUT' : '10/m',
        'PATCH' : '10/m',
        'DELETE' : '10/m',
    }

    key = 'ip'

    def dispatch(self, request, *args, **kwargs):
        method = request.method.upper()
        rate = self.rate_limits.get(method, None)
        if rate:
            @ratelimit(key=self.key, rate=rate, method=method, block=True)
            def limited_view(request, *args, **kwargs):
                return super(RateLimitMixin, self).dispatch(request, *args, **kwargs)

            was_limited = getattr(request, 'limited', False)
            if was_limited:
                return Response({'Error': 'Too many requests. you have to wait for a while.'},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            return limited_view(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)