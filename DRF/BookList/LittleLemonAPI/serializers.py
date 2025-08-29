from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    # stock = serializers.IntegerField(source='inventory', min_value=0)
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_price_after_tax')
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only = True)
    # category_id = serializers.IntegerField()
    category_id = serializers.IntegerField(write_only=True)
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'category_detail'
    # )
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    
    # def validate_price(self, value):
    #     if value < 2:
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     return value
    
    # def validate_stock(self, value):
    #     if value < 0:
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     return value
    
    def validate(self, attrs):
        attrs['title']=bleach.clean(attrs['title'])
        if (attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2')
        if (attrs['inventory']<0):
            raise serializers.ValidationError('Inventory should not be less than 0')
        return super().validate(attrs)
    
    # title = serializers.CharField(max_length=255, 
    #                               validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    
    # def validate_title(self, value):
    #     return bleach.clean(value)
    
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock', 'price_after_tax','category','category_id']
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=MenuItem.objects.all(),
        #         fields=['title', 'price']
        #     ),
        # ]
        # extra_kwargs = {
        #     'price': {'min_value': 2},
        #     'stock':{'source':'inventory', 'min_value': 0}
        # }
        
        extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(
                            queryset=MenuItem.objects.all()
                    )
                ]
            }
        }
        # depth = 1
        
    def calculate_price_after_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)