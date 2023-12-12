from rest_framework import serializers

from taqqos.account.models import User
from taqqos.document.serializers import FileSerializer


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["profile_image"] = FileSerializer()
        return super(UserSerializer, self).to_representation(instance)

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "full_name",
            "profile_image",
            "date_joined",
        )
        read_only_fields = ("phone_number", "user_type", "date_joined")
