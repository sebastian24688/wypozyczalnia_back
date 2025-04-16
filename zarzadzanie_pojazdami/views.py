from django.contrib.auth.models import User
from rest_framework import generics, status
from .models import Pojazd, Wypozyczenie
from .serializers import PojazdSerializer, ObrazekSerializer, WypozyczenieSerializer, WypozyczenieKlientaSerializer, \
    RejestracjaKlientaSerializer, EdytujStatusWypozyczeniaSerializer, WypozyczenieUsunSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters import rest_framework as filters
from rest_framework.permissions import BasePermission
from rest_framework.decorators import permission_classes


# pobranie grup
class Pracownik(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Pracownik').exists()


@permission_classes([Pracownik])
class DodajPojazd(generics.CreateAPIView):
    serializer_class = PojazdSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'obrazek' in request.FILES:
            obrazek_serializer = ObrazekSerializer(data=request.FILES)
            if obrazek_serializer.is_valid():
                obrazek_serializer.save()
                obrazek_url = obrazek_serializer.data['obrazek']
                request.data['zdjecie1'] = obrazek_url
            else:
                return Response({'status': 'error', 'errors': obrazek_serializer.errors}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class WyszukiwarkaPojazdow(generics.ListAPIView):
    queryset = Pojazd.objects.all()
    serializer_class = PojazdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['marka', 'cena', 'kategoria', 'moc', 'id', 'nr_rejestracyjny']


class WylistujMarki(APIView):
    def get(self, request):
        marki = Pojazd.objects.values_list('marka', flat=True).distinct()
        return Response(marki)


class WylistujKategorie(APIView):
    def get(self, request):
        kategoria = Pojazd.objects.values_list('kategoria', flat=True).distinct()
        return Response(kategoria)


@permission_classes([Pracownik])
class EdytujPojazd(generics.UpdateAPIView):
    queryset = Pojazd.objects.all()
    serializer_class = PojazdSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'nr_rejestracyjny'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()


@permission_classes([Pracownik])
class UsunPojazd(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pojazd.objects.all()
    serializer_class = PojazdSerializer
    lookup_field = 'nr_rejestracyjny'

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Wystąpił błąd: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Wyloguj(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            Token.objects.create(user=request.user)

            return Response({'status': 'success', 'message': 'Wylogowano pomyślnie.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'status': 'error', 'message': 'Brak tokenu do wylogowania.'},
                            status=status.HTTP_400_BAD_REQUEST)




class WypozyczPojazd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WypozyczenieSerializer

    def create(self, request, *args, **kwargs):
        try:
            wypozyczenie = Wypozyczenie.objects.create(
                klient=request.user,
                pojazd_id=request.data.get('pojazd'),
                data_wypozyczenia=request.data.get('data_wypozyczenia'),
                ilosc_dni=request.data.get('ilosc_dni'),
                status_wypozyczenia='Rezerwacja',
                czy_oplacone=False,
            )

            serializer = self.get_serializer(wypozyczenie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class WypozyczenieFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='klient__email', lookup_expr='exact')

    class Meta:
        model = Wypozyczenie
        fields = ['email']


@permission_classes([Pracownik])
class WyszukajWypozyczenia(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wypozyczenie.objects.all()
    serializer_class = WypozyczenieSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WypozyczenieFilter


class WypozyczeniaKlienta(generics.ListAPIView):
    serializer_class = WypozyczenieKlientaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wypozyczenie.objects.filter(klient=self.request.user)


class CzyZalogowany(APIView):
    def get(self, request):
        try:
            auth_header = request.headers.get('Authorization', '')
            token = auth_header.split(' ')[1]
            Token.objects.get(key=token)

            return Response({'czy_zalogowany': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'czy_zalogowany': False}, status=status.HTTP_400_BAD_REQUEST)


class RejestracjaKlienta(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RejestracjaKlientaSerializer


@permission_classes([Pracownik])
class EdytujStatusWypozyczenia(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wypozyczenie.objects.all()
    serializer_class = EdytujStatusWypozyczeniaSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
        


class UsunWypozyczenie(generics.DestroyAPIView):
    queryset = Wypozyczenie.objects.all()
    serializer_class = WypozyczenieUsunSerializer
    permission_classes = [IsAuthenticated]

    def usun(self, request, *args, **kwargs):
        instance = self.get_object()
        print("siema")
        if instance.klient == request.user:
            if instance.status_wypozyczenia == 'Rezerwacja' and not instance.czy_oplacone:
                instance.delete()
                return Response({'status': 'success', 'message': 'Wypożyczenie usunięte'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'status': 'error', 'message': 'Nie można usunąć opłaconego wypożyczenia'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Nie masz uprawnień do usunięcia tego wypożyczenia'},
                            status=status.HTTP_403_FORBIDDEN)


class JakaGrupa(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = request.user.groups.all()
        group_names = [group.name for group in user_groups]

        return Response({'grupa': group_names}, status=status.HTTP_200_OK)


class Oplac(generics.UpdateAPIView):
    queryset = Wypozyczenie.objects.all()
    serializer_class = WypozyczenieSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.instance.czy_oplacone = True
        serializer.instance.save()