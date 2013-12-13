from rest_framework import status
from rest_framework.response import Response


class CreateModelMixin(object):
    """
    Create a model instance. This is almost identical to the mixin provided by
    django-rest-framework. The only two changes have notes above them. These
    two changes allow for more control over which serializer is used after
    creating an object.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA,
                                         files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            # Note: Create a new serialiser instance with object. Gives
            # subclasses a chance to change serializer.
            serializer = self.get_serializer(instance=self.object)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_success_headers(self, data):
        try:
            return {'Location': data['url']}
        except (TypeError, KeyError):
            return {}

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        # NOTE: Modified to pass instance to get_serializer_class.
        serializer_class = self.get_serializer_class(instance=instance)
        context = self.get_serializer_context()
        return serializer_class(instance, data=data, files=files,
                                many=many, partial=partial, context=context)
