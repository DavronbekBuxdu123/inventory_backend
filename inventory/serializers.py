from .models import Category,Product,StockMovement
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='category.name',read_only=True)

    class Meta:
        model=Product
        fields=['id','category','category_name','name','sku','price','current_stock']
        read_only_fields=['current_stock']

class CategorySerializer(serializers.ModelSerializer):
    products_count=serializers.IntegerField(source='products.count',read_only=True)

    class Meta:
        model=Category        
        fields=['id','name','products_count']

class StockMovementSerializer(serializers.ModelSerializer):
     product_name=serializers.CharField(source='product.name',read_only=True) 
     product_sku=serializers.CharField(source='product.sku',read_only=True)
     formatted_date=serializers.DateTimeField(source='created_at',format='%Y-%m-%d %H:%M',read_only=True) 

     class Meta:
          model=StockMovement
          fields=['id','product','product_name','product_sku','quantity','movement_type','created_at','formatted_date']

     def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        movement_type = validated_data['movement_type']

        if movement_type == 'IN':
            product.current_stock += quantity
        elif movement_type == 'OUT':
            if product.current_stock >= quantity:
                product.current_stock -= quantity
            else:
                raise serializers.ValidationError(
                    {"quantity": f"Omborda yetarli mahsulot yo'q! Hozirgi qoldiq: {product.current_stock} dona."}
                )
        product.save()

        return super().create(validated_data)     