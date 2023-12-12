from rest_framework import serializers

from taqqos.account.serializers.user import UserSerializer
from taqqos.document.serializers import FileSerializer
from taqqos.product.models import Review, ReviewFile


class ReviewFileSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields['file'] = FileSerializer()
        return super().to_representation(instance)

    class Meta:
        model = ReviewFile
        fields = (
            'id',
            "file"
        )


class ReviewSerializer(serializers.ModelSerializer):
    review_files = ReviewFileSerializer(many=True)

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super().to_representation(instance)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "product",
            "rate",
            "created_at",
            "text",
            "review_files"
        )
        read_only_fields = (
            "user",
            "created_at"
        )

    def create(self, validated_data):
        review_files = validated_data.pop('review_files', [])
        review = Review.objects.create(**validated_data)
        for review_file in review_files:
            ReviewFile.objects.create(review=review, **review_file)
        return review
