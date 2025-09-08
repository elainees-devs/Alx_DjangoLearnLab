# bookshelf/forms.py
from django import forms
from django.core.validators import RegexValidator

class SearchForm(forms.Form):
    """
    Validates search input to prevent overly long or malicious input.
    Use the cleaned data in views to perform ORM-filtered searches.
    """
    q = forms.CharField(
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Search books"}),
        validators=[
            # only allow letters, numbers, spaces, and basic punctuation. Adjust pattern as needed.
            RegexValidator(r"^[\w\s\-\.,:;!?']*$", "Invalid characters in search query.")
        ],
    )

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        # Additional sanitization if needed
        return q
