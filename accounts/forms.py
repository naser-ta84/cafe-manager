from django import forms

class UserForm(forms.Form):
    # اینجا دیگر به مدل وصل نیستیم، پس ارور تکراری بودن نمی‌دهد
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-gray-800/50 border border-gray-600 text-white focus:border-amber-500 focus:outline-none transition',
            'placeholder': '09123456789'
        })
    )