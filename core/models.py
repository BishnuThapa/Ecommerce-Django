from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User
from taggit.managers import TaggableManager
# Create your models here.


STATUS_CHOICE = (
    ("process", "Pocessing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered")
)
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published")
)
RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐")
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=15,
                         prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category')

    class Meta:

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    # tags = TaggableManager()
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=user_directory_path)
    cover_image = models.ImageField(upload_to=user_directory_path)
    description = RichTextUploadingField(null=True, blank=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, default="+977-0000000000")
    chat_resp_time = models.CharField(max_length=255, default="100")
    shipping_on_time = models.CharField(max_length=255, default="100")
    authentic_rating = models.CharField(max_length=255, default="100")
    days_return = models.CharField(max_length=255, default="100")
    warranty_period = models.CharField(max_length=255, default="100")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    class Meta:

        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=15,
                         alphabet="abcdefgh12345")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, default="1")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=user_directory_path)
    description = RichTextUploadingField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(max_digits=6, decimal_places=2)
    specification = RichTextUploadingField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    stock_count = models.CharField(max_length=255, null=True, blank=True)
    life = models.CharField(max_length=255, null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)
    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix="sku",
                         alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price-self.price)*100)/self.old_price
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:

        verbose_name = 'Cart Order'
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Cart Order Items'
        verbose_name_plural = 'Cart Order Items'

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlist'

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Address'
        verbose_name_plural = 'Address'
