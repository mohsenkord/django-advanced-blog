from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):

    snippet = serializers.CharField(read_only=True, source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True, method_name='get_abs_url')
    # category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=Category.objects.all())


    class Meta:
        model = Post
        fields = ['title', 'author','image', 'content', 'category', 'snippet', 'status', 'relative_url', 'absolute_url', 'created_date', 'published_date']
        read_only_fields = ['author', 'created_date']

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
            rep.pop('absolute_url', None)
            rep.pop('relative_url', None)
        else:
            rep.pop('content', None)

        rep['category'] = CategorySerializer(instance.category, context={'request': request}).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(user__id=self.context.get("request").user.id)
        return super().create(validated_data)

