from django.db import models

# Import to handle images and resizing
from io import BytesIO
from PIL import Image

# Import to help with thumbnails
from django.core.files import File

class Category(models.Model):

    # Name of categories
    name = models.CharField(max_length=255)

    # Address version of the name
    slug = models.SlugField()

    # Order the categories by name. Trailing comma creates a tuple that allows for iteration of the objects.
    class Meta:
        ordering = ("name",)

    # Display. By default the display on screen will be "{object 0x12345}". Add this def to make it display the product name instead. 
    def __str__(self):
        return self.name

    # Function to get the url of the category. 
    def get_absolute_url(self):
        return f"/{self.slug}/"

class Product(models.Model):

    # Refer to the category. Use the foreign key of the category. If you delete the category, delete all the related products.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    # Set description to null incase a description is not necessary/ 
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Where to store product images. Not required and its okay to be empty.
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    # Where to store the thumbnails. Not required and its okay to be empty.
    thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)

    # Date field to show the newest products first. When product is created, datetime is automatically added to the product.
    date_added = models.DateTimeField(auto_now_add=True)

    # Order by newest. "-" beforehand means descending order. Trailing comma creates a tuple that allows for iteration of the objects.
    class Meta:
        ordering = ("-date_added",)

    # Display. By default the display on screen will be "{object 0x12345}". Add this def to make it display the product name instead. 
    def __str__(self):
        return self.name

    # Function to get the url of the product in the category.
    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/"

    # Get the product image.
    def get_image(self):

        # Check if there is an image in the field, and return the address (easier to use in the front end). 
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return ""

    # Thumbnail
    def get_thumbnail(self):

        # If a thumbnail already exists, return it with the url address.
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url

        # If the thumbnail does not exist. Go grab the product image, run it through a function to make the thumbnail, and save it in the database
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return "http://127.0.0.1:8000" + self.thumbnail.url
            
            # If there is no image. Return nothing.
            else:
                return ""

    # Function to make thumbnail. Take in an image and set the default size to 300x200
    def make_thumbnail(self, image, size=(300, 200)):

        # Create a new object based on the image passed in.
        img = Image.open(image)

        # Convert to a RGB just in case
        img.convert("RGB")

        # Use the built-in thumbnail function to resize the picture.
        img.thumbnail(size)

        # Import function from top
        thumb_io = BytesIO()

        # Save the image
        img.save(thumb_io, "JPEG", quality=85)

        # Create the thumbnail and return it
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
