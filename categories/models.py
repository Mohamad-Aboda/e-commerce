from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        
        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Category with this name already exists.")

        instance.name = name
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    