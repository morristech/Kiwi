# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from tcms.core.models.base import UrlMixin
from tcms.xmlrpc.serializer import XMLRPCSerializer

User._meta.ordering = ['username']


class TCMSActionModel(models.Model, UrlMixin):
    """
    TCMS action models.
    Use for global log system.
    """

    class Meta:
        abstract = True

    @classmethod
    def to_xmlrpc(cls, query=None):
        """
        Convert the query set for XMLRPC
        """
        if query is None:
            query = {}
        serializer = XMLRPCSerializer(queryset=cls.objects.filter(**query))
        return serializer.serialize_queryset()

    def serialize(self):
        """
        Convert the model for XMLPRC
        """
        serializer = XMLRPCSerializer(model=self)
        return serializer.serialize_model()

    def clean(self):
        strip_types = (models.CharField,
                       models.TextField,
                       models.URLField,
                       models.EmailField,
                       models.IPAddressField,
                       models.GenericIPAddressField,
                       models.SlugField)

        for field in self._meta.fields:
            # TODO: hardcode 'notes' here
            if not (field.name == 'notes') and isinstance(field, strip_types):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name,
                            value.replace('\t', ' ').replace('\n', ' ').replace('\r', ' '))
