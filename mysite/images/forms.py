from django import forms
from urllib import request
from django.core.files.base import ContentFile
# from django.utils.text import slugify
from uuslug import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        extension = url.rsplit('.', 1)[1].lower()  # 从右边起以第1个点号分成两个组(从1开始计数)
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        # 下载图片
        res = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(res.read()), save=False)

        if commit:
            image.save()
        return image
