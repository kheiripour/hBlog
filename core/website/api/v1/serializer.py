from rest_framework import serializers
from ...models import Contact, Newsletter, Slider
class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['sender','name','subject','message','email']
        read_only_fields = ['sender']

class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = ['email']

class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = ['post','snippet','image',]

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep ['abs_url'] = instance.post.get_absolute_url()
        if not instance.snippet :
            rep['snippet'] = instance.post.active_version.snippet
        if not instance.image:
            rep['image'] = instance.post.active_version.image.url
        rep['author'] = instance.post.author.__str__()
        rep['pub_date'] = instance.post.pub_date
        return rep
        