# django
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

# installed
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel, TreeManyToManyField
from ckeditor_uploader.fields import RichTextUploadingField

from taqqos.account.models import User
# business app
from taqqos.core.models import BaseDateModel
from taqqos.document.models import File


class Brand(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("родитель")
    )
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)

    class Meta:
        verbose_name = _("бренд")
        verbose_name_plural = _("бренды")

    def __str__(self):
        return self.name_ru


class Category(MPTTModel):
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("родитель")
    )
    icon = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    brands = TreeManyToManyField(Brand, related_name="categories", verbose_name=_("бренды"), blank=True)
    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

    def __str__(self):
        return self.name_uz

    def get_all_child(self):
        child_category = Category.objects.filter(parent=self)
        queue = list(child_category)
        while len(queue):
            next_children = Category.objects.filter(parent=queue[0])
            child_category = child_category.union(next_children)
            queue.pop(0)
            queue = queue + list(next_children)
        return child_category


class Attribute(models.Model):
    TEXT = "text"
    TOGGLE = "toggle"
    OPTION = "option"
    MULTI_OPTION = "multi_option"

    TYPES = (
        (TEXT, TEXT),
        (TOGGLE, TOGGLE),
        (OPTION, OPTION),
        (MULTI_OPTION, MULTI_OPTION),
    )
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    code = models.CharField(_("код"), max_length=64, unique=True)
    type = models.CharField(_("тип"), max_length=64, choices=TYPES)
    is_required = models.BooleanField(_("требуется"), default=False)
    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)
    categories = TreeManyToManyField(Category, verbose_name=_("категории"), related_name="attributes", blank=True)

    class Meta:
        verbose_name = _("атрибут")
        verbose_name_plural = _("атрибуты")

    def __str__(self):
        return self.name_ru


class Option(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("атрибут"),
    )
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    code = models.CharField(_("код"), max_length=64)
    value = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=18)

    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)

    class Meta:
        verbose_name = _("параметр")
        verbose_name_plural = _("параметры")
        unique_together = ("attribute", "code")

    def __str__(self):
        return self.name_ru


class Product(BaseDateModel):
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    slug = models.SlugField(db_index=True, unique=True)
    short_name = models.CharField(_("название короткое"), max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
        verbose_name=_("категория"),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
        verbose_name=_("бренд"),
    )
    photo = models.ForeignKey(
        File, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("фото")
    )
    is_popular = models.BooleanField(_("популярен"), default=False)
    views = models.PositiveIntegerField(_("Просмотры"), default=0)
    description_uz = RichTextUploadingField(_("описание uzb"))
    description_ru = RichTextUploadingField(_("описание rus"))

    class Meta:
        verbose_name = _("продукт")
        verbose_name_plural = _("продукты")

    def __str__(self):
        return self.name_ru

    @property
    def rate(self):
        reviews = self.reviews.filter(rate__gt=0)
        count = reviews.count()
        if count > 0:
            return round(sum([review.rate for review in reviews]) / count, 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.filter(rate__gt=0).count()

    @property
    def min_price(self):
        return min(
            self.product_prices.all().values_list(
                "price_amount", flat=True
            ), default=None
        )

    @property
    def price_count(self):
        return self.product_prices.all().count()

    @property
    def has_credit(self):
        return self.product_prices.filter(has_credit=True).exists()

    @property
    def has_delivery(self):
        return self.product_prices.filter(has_delivery=True).exists()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("продукт")
    )
    photo = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("фото")
    )

    class Meta:
        verbose_name = _("фото продукта")
        verbose_name_plural = _("фотографии продукта")


class ProductAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=_("атрибут"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes", verbose_name=_("продукт")
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="product_attributes",
        verbose_name=_("параметр")
    )

    class Meta:
        verbose_name = _("продукт атрибут")
        verbose_name_plural = _("продукт атрибуты")


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name=_("продукт")
    )
    name_uz = models.CharField(_("название uzb"), max_length=200)
    name_ru = models.CharField(_("название rus"), max_length=200)
    value = models.CharField(_("ценить"), max_length=512)

    class Meta:
        verbose_name = _("продукт характеристика")
        verbose_name_plural = _("продукт характеристики")


class ProductVideoReview(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="video_reviews",
        verbose_name=_("продукт")
    )
    link = models.URLField(_("URL-адрес"))

    class Meta:
        verbose_name = _("видеообзор")
        verbose_name_plural = _("видеообзоры")


class ProductPrice(BaseDateModel):
    products = models.ManyToManyField(
        Product,
        related_name="product_prices",
        verbose_name=_("продукты"),
        blank=True
    )

    name = models.CharField(_("название"), max_length=512)
    price_amount = models.DecimalField(_("сумма цены"), decimal_places=2, max_digits=18)
    description = models.TextField(_("описание"), null=True, blank=True)
    features = models.JSONField(_("характеристика"), null=True, blank=True)
    photo = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("фото")
    )

    has_credit = models.BooleanField(_("есть кредит"), default=False)
    credit_monthly_amount = models.CharField(_("ежемесячная сумма кредита"), null=True, blank=True)

    has_delivery = models.BooleanField(_("есть доставка"), default=False)
    delivery_info = models.TextField(_("информация о доставке"), null=True, blank=True)

    address = models.TextField(_("адрес"), null=True, blank=True)
    phone_number = models.CharField(_("номер телефона"), null=True, blank=True)

    website = models.CharField(_("Веб-сайт"), max_length=256)
    website_link = models.URLField(_("ссылка на сайт"), null=True, blank=True)

    class Meta:
        verbose_name = _("цены на продукцию")
        verbose_name_plural = _("цены на продукцию")
        unique_together = ("name", "website")


class Review(BaseDateModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("пользователь"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("продукт"))
    rate = models.PositiveIntegerField(
        _("ставка"),
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    text = models.TextField(_("текст"), null=True, blank=True)

    class Meta:
        verbose_name = _("отзыв")
        verbose_name_plural = _("отзывы")


class ReviewFile(BaseDateModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_files", verbose_name=_("отзыв"))
    file = models.ForeignKey(File, on_delete=models.CASCADE, verbose_name=_("файл"))

    class Meta:
        verbose_name = _("отзыв файл")
        verbose_name_plural = _("отзыв файлы")


class Favourite(BaseDateModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites", verbose_name=_("пользователь"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites", verbose_name=_("продукт"))

    class Meta:
        unique_together = (
            "user", "product"
        )
        verbose_name = _("Избранной")
        verbose_name_plural = _("Избранное")

    def __str__(self):
        return _(f"{self.user.full_name} избранное {self.product.name_ru}")


class Slider(models.Model):
    image = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="фото"
    )
    image_mobile = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="sliders_mobile",
        verbose_name="фото для мобиль"
    )
    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)

    class Meta:
        verbose_name = _("Слидер")
        verbose_name_plural = _("Слидеры")


class Seller(models.Model):
    image = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="фото"
    )
    order_number = models.PositiveIntegerField(_("порядковый номер"), null=True, blank=True)

    class Meta:
        verbose_name = _("Продавц")
        verbose_name_plural = _("Продавцы")

