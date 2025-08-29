from rest_framework.throttling import UserRateThrottle


class TenMinutesThrottle(UserRateThrottle):
    scope = 'ten'