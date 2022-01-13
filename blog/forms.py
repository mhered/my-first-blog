from django import forms

from .models import Post, Category, Image

cat_query = Category.objects.all().values_list('name','name')

cat_list = []

for item in cat_query:
    cat_list.append(item)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=cat_list, attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control'}),
        }


class ImageForm(forms.ModelForm):

    image = forms.ImageField(label='Image')    
    
    class Meta:
        model = Image
        fields = ('image', )


class CatForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }