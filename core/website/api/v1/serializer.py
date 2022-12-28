from rest_framework import serializers
from ...models import Contact, Newsletter
class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['sender','name','subject','message','email']
        read_only_fields = ['sender']

class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = ['email']
