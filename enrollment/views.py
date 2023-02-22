from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError, ModelSerializer
from .models import Application, Participant


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email']


class ApplicationSerializer(ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Application
        fields = ['contact_phone', 'ticket_type', 'participants']


@api_view(['POST'])
def enroll(request):
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    participants = request.data.get('participants', [])
    # if not isinstance(participants, list):
    #     raise ValidationError('Excepts participants field be a list')
    #
    # for fields in participants:
    #     serializer = ParticipantSerializer(data=fields)
    #     serializer.is_valid(raise_exception=True)

    application = Application.objects.create(
        contact_phone=str(serializer.validated_data['contact_phone']),
        ticket_type=str(serializer.validated_data['ticket_type']),
    )
    participants_fields = serializer.validated_data['participants']
    participants = [Participant(application=application, **fields) for fields in participants_fields]
    Participant.objects.bulk_create(participants)

    return Response({
        'application_id': application.id,
    })
