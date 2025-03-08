from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import *

"""
Get Current barber, if current user is a berber.
"""
def get_barber(request):
    try:
        return Barber.objects.get(user_id=request.user.pk)
    except Barber.DoesNotExist:
        raise ValidationError('barber does not exist!')

"""
To change, and access barber panel information.
"""
class BarberDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BarberSerializer
    model = Barber

    def get_object(self):
        return get_object_or_404(Barber, user_id=self.request.user.pk)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class WorkDayViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkDaysSerializer

    def get_queryset(self):
        return WorkDay.objects.filter(barber_id=get_barber(self.request).pk)

    def perform_create(self, serializer):
        try:
            serializer.save(barber=get_barber(self.request))
        except IntegrityError:
            raise ValidationError('This day already set for this barber!')

    def perform_update(self, serializer):
        try:
            serializer.save(barber=get_barber(self.request))
        except IntegrityError:
            raise ValidationError('This day already set for this barber!')


class UnAvailabilityViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UnAvailabilitySerializer

    def get_queryset(self):
        return UnAvailability.objects.filter(barber_id=get_barber(self.request).pk)

    def perform_create(self, serializer):
        serializer.save(barber=get_barber(self.request))



"""
For POST request, you have to specify weekday in query parameters,
< for example, http://127.0.0.1:8000/barbers/off-times/?weekday=Monday,
this will create an off time on Monday for current barber. >
"""
class OffTimeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OffTimesSerializer

    def get_queryset(self):
        barber = get_barber(self.request)
        queryset = OffTime.objects.filter(workday__barber_id=barber.pk)
        weekday = self.request.query_params.get('weekday')
        if weekday:
            try:
                workday = WorkDay.objects.get(day=weekday, barber_id=barber.pk)
                queryset = queryset.filter(workday=workday)
            except WorkDay.DoesNotExist:
                return OffTime.objects.none()
            return queryset
        return queryset

    def perform_create(self, serializer):
        barber = get_barber(self.request)
        weekday = self.request.query_params.get('weekday')
        if weekday:
            try:
                workday = WorkDay.objects.get(day=weekday, barber_id=barber.pk)
            except WorkDay.DoesNotExist:
                return OffTime.objects.none()
            serializer.save(workday=workday)

    def perform_update(self, serializer):
        serializer.save()


class ImageGalleryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageGalleySerializer

    def get_queryset(self):
        return ImageGallery.objects.filter(barber_id=get_barber(self.request).pk)

"""
The Barber can see the list of reservations.
"""
class ReservationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(barber_id=get_barber(self.request).pk)


"""
The barber can retrieve a reservation or change the reservation status.
"""
class ReservationDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(barber_id=get_barber(self.request).pk)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return BarberReservationUpdateSerializer
        return ReservationSerializer

    def perform_update(self, serializer):
        serializer.save(barber=get_barber(self.request))

