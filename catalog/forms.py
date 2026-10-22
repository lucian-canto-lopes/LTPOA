from django import forms

from .models import Sample


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = [
            "code",
            "sample_type",
            "received_at",
            "origin",
            "requester",
            "amount",
            "unit",
            "condition",
            "status",
            "notes",
        ]
        widgets = {
            "received_at": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()
