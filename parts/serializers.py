from rest_framework import serializers

from .models import *

from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    ancestry = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'has_children', 'parent', 'ancestry', 'full_path']

    def get_ancestry(self, obj):
        """Returns the ancestry as a list of category names."""
        return [category.name for category in obj.get_ancestry()]

    def get_full_path(self, obj):
        """Returns the full path of the category as a string."""
        return obj.get_full_path()

class PartImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartImage
        fields = ['image']

class PartSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = serializers.SerializerMethodField()
    class Meta:
        model = Part
        fields = ['part', 'category', 'part_description','images']
    def get_images(self,obj):
        images = PartImageSerializer(instance=PartImage.objects.filter(part=obj),many=True)
        return images.data