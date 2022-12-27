from rest_framework import serializers
from ...models import Post, PostVersion, Comment, Category
from accounts.models import Profile

class ProfileBlogSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='__str__')
    class Meta:
        model = Profile
        fields = ['id','name','image','about']

    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        request = self.context.get('request')
        rep.pop('image',None)
        rep.pop('about',None)
        if request.parser_context.get('kwargs').get('pk'):
            if instance.image: rep['image'] = request.build_absolute_uri(instance.image.url)
            rep['about'] = instance.about
            
        return rep

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['post','id','commenter','name','replied_to','message']
        read_only_fields = ['commenter','post']
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if instance.commenter is not None:
            commmenter = ProfileBlogSerializer(instance.commenter,context={'request':request}).data
            commmenter.pop('about',None)
            rep['commenter'] = commmenter    
        else: 
            rep['commenter'] = {'name':instance.name}
        replies = CommentSerializer(Comment.objects.filter(replied_to=instance),many=True,context={'request':request}).data
        if replies: rep['replies'] = replies
        rep.pop('replied_to',None)
        rep.pop('name',None)
        rep.pop('post',None)
        return rep


class BlogModelSerializer(serializers.ModelSerializer):
   
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['absolute_url','id','author','pub_date','counted_view','active_version','status']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['title'] = instance.active_version.title
        rep['category'] = CategorySerializer(instance.active_version.category.all(),many=True).data
        image = instance.active_version.image
        if image:
            rep['image'] = request.build_absolute_uri(image.url)

        if request.parser_context.get('kwargs').get('pk'):
            if request.method == "GET":
                instance.counted_view += 1
                instance.save()
            rep['content'] = instance.active_version.content.replace("\"", "\'")   
            rep.pop('absolute_url', None)
            rep['comments'] = CommentSerializer(Comment.objects.filter(post=instance,replied_to=None),many=True,context={'request':request}).data
        else:
            rep['author'] = ProfileBlogSerializer(instance.author,context={'request':request}).data
            rep['snippet'] = instance.active_version.snippet 
            rep['comments'] = Comment.objects.filter(post=instance).count()
            if request.user.is_authenticated:
                if request.user.profile == instance.author:
                    last_version = PostVersion.objects.filter(post=instance).order_by('-number').first()
                    rep['active_version_number'] = instance.active_version.number
                    rep['last_version_number'] = last_version.number
                    if last_version != instance.active_version and last_version.admin_note: rep['admin_checked'] = ('V:%i not approved'%(last_version.number))
        
        return rep

class PostVersionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = PostVersion
        fields = ['post','number','title','content','snippet','category','image','author_note','admin_note']
        read_only_fields = ['post','number','admin_note']


    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category.all(),many=True).data
        rep['content'] = instance.content.replace("\"", "\'")
        if instance.image:
            rep['image'] = request.build_absolute_uri(instance.image.url)

        return rep
