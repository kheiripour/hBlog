from rest_framework import serializers
from ...models import Contact, Newsletter, Slider
class ContactSerializer(serializers.ModelSerializer):
    """
    Provide contact message and it's sender data
    """
    class Meta:
        model = Contact
        fields = ['sender','name','subject','message','email']
        read_only_fields = ['sender']

class NewsletterSerializer(serializers.ModelSerializer):
    """
    Provide email for newsletter api view
    """
    class Meta:
        model = Newsletter
        fields = ['email']

class SliderSerializer(serializers.ModelSerializer):
    """
    Provide sliders data in index page
    """
    class Meta:
        model = Slider
        fields = ['post','snippet','image',]
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep ['abs_url'] = instance.post.get_absolute_url()

        # If slider has'nt snippet or image will user post's instead
        if not instance.snippet :
            rep['snippet'] = instance.post.active_version.snippet
        if not instance.image:
            rep['image'] = instance.post.active_version.image.url
        rep['author'] = instance.post.author.__str__()
        rep['pub_date'] = instance.post.pub_date
        return rep 