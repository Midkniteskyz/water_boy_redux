from django.db.models import Q
from django.shortcuts import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer

# View for getting the latest product. Use APIView to handle API rendering
class LatestProductsList(APIView):

    # Set some customization with the APIView with get()
    def get(self, request, format=None):
        
        # Grab all the products and show the latest 4
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# Viewset for the product details
class ProductDetail(APIView):

    # Check if the object exists
    def get_object(self, category_slug, product_slug):
        try:
            # Filter every product in the category and get the slug. Based on the slug, a pair of category and product should be returned
            return Product.objects.filter(category_slug=category_slug).get(slug=product_slug)
        # Return an http404 if the product doesnt exist
        except Product.DoesNotExist:
            raise Http404

    # Get the details of the product
    def get(self, request, category_slug, product_slug, format=None):
            product = self.get_object(category_slug, product_slug)
            serializer = ProductSerializer
            return Response(serializer.data)

# Viewset for the category. Used for when clicking on domestic and import up top. Will look very similar to the product view.
class CategoryDetail(APIView):

    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

# Accept only post data from anything with api_view
@api_view(["POST"])
def search(request):
    # take in the request data from the search entry
    query = request.data.get("query", "")

    # if There is something in the query request
    if query:
        # check products and look to see if the name or description matches the query. Q is a function from django
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        # if the query is empty. return an empty products list
        return Response({"products": []})       