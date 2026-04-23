"""Shared form helpers."""
from django import forms


FORM_WIDGET_CLASS = "form-control"


def _apply_form_control(widget: forms.Widget) -> None:
    """Ensure every widget gets the ``form-control`` CSS class."""
    existing = widget.attrs.get("class", "")
    classes = {c for c in existing.split() if c}
    if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
        classes.add("form-check-input")
    elif isinstance(widget, forms.Select):
        classes.add("form-select")
    else:
        classes.add(FORM_WIDGET_CLASS)
    widget.attrs["class"] = " ".join(sorted(classes))


class StyledModelForm(forms.ModelForm):
    """ModelForm base that applies consistent Bootstrap-like styling to widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            _apply_form_control(field.widget)
            if isinstance(field.widget, forms.DateInput):
                field.widget.input_type = "date"
            if isinstance(field.widget, forms.TimeInput):
                field.widget.input_type = "time"
            if isinstance(field.widget, forms.DateTimeInput):
                field.widget.input_type = "datetime-local"
