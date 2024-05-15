from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from reversion import set_comment
from reversion.views import RevisionMixin

from huscy.subjects import pagination, models, serializers, services
from huscy.subjects.permissions import ChangeSubjectPermission, ViewSubjectPermission


class SubjectViewSet(RevisionMixin, viewsets.ModelViewSet):
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    http_method_names = 'get', 'post', 'put', 'delete', 'head', 'options', 'trace'
    ordering_fields = (
        'contact__date_of_birth',
        'contact__first_name',
        'contact__gender',
        'contact__last_name',
    )
    pagination_class = pagination.SubjectPagination
    permission_classes = (ViewSubjectPermission & DjangoModelPermissions, )
    search_fields = 'contact__display_name', 'contact__date_of_birth'
    serializer_class = serializers.SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        return services.get_subjects(
            include_children=user.has_perm('subjects.view_child'),
            include_patients=user.has_perm('subjects.view_patient')
        )

    def perform_create(self, serializer):
        subject = serializer.save()
        set_comment(f'Created subject <ID-{subject.id}>')

    def perform_destroy(self, subject):
        services.delete_subject(subject)
        set_comment(f'Deleted subject <ID-{subject.id}')

    def perform_update(self, serializer):
        subject = serializer.save()
        set_comment(f'Updated subject <ID-{subject.id}>')

    def list(self, request):
        '''
        For data protection reasons it's necessary to limit the number of returned subjects to 500.
        Unfortunately it is not possible to limit the queryset because filters cannot be applied
        to a sliced queryset. For this reason, the limiting have to be done after filtering.
        '''
        MAX_RESULT_COUNT = getattr(settings, 'HUSCY_SUBJECTS_SUBJECT_VIEWSET_MAX_RESULT_COUNT', 500)
        filtered_queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset = self.paginate_queryset(filtered_queryset[:MAX_RESULT_COUNT])
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('delete', 'post'), permission_classes=(ChangeSubjectPermission, ))
    def inactivity(self, request, pk):
        if request.method == 'DELETE':
            return self._delete_inactivity()
        elif request.method == 'POST':
            return self._create_inactivity(request)

    def _delete_inactivity(self):
        services.unset_inactivity(self.get_object())
        set_comment('Unset inactivity')
        return Response(status=HTTP_204_NO_CONTENT)

    def _create_inactivity(self, request):
        serializer = serializers.InactivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inactivity = serializer.save()
        set_comment(f'Set inactivity: {inactivity}')
        return Response(serializer.data)


class GuardianViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = 'post', 'put', 'delete', 'head', 'options', 'trace'
    permission_classes = (ChangeSubjectPermission, )
    serializer_class = serializers.GuardianSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.subject = get_object_or_404(models.Subject, pk=self.kwargs['subject_pk'])

    def get_queryset(self):
        return self.subject.guardians.all()

    def perform_create(self, serializer):
        guardian = serializer.save(subject=self.subject)
        set_comment(f'Created guardian <ID-{guardian.id}>')

    def perform_destroy(self, guardian):
        services.remove_guardian(self.subject, guardian)
        set_comment(f'Deleted guardian <ID-{guardian.id}>')

    def perform_update(self, serializer):
        guardian = serializer.save()
        set_comment(f'Updated guardian <ID-{guardian.id}>')
