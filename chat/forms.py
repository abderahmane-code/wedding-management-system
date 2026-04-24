from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Write a message…",
                "maxlength": 4000,
            }
        ),
        max_length=4000,
        strip=True,
        label="",
    )
