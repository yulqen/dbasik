from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    ButtonHolder,
    Div,
    Field,
    Fieldset,
    Layout,
    Submit,
)
from dbasik.register.models import ProjectStage, ProjectType, Tier
from django import forms
from django.forms import BooleanField, CharField, ModelChoiceField
from django.urls import reverse

from . import models


class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = models.ProjectStage
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("register:projectstage_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit Project Stage",
                "name",
                "description",
            ),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )


class TierForm(forms.ModelForm):
    class Meta:
        model = models.Tier
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("register:tier_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit Tier",
                "name",
                "description",
            ),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )


class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = models.ProjectType
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("register:projecttype_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit Project Type",
                "name",
                "description",
            ),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )


class StrategicAlignmentForm(forms.ModelForm):
    class Meta:
        model = models.StrategicAlignment
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("register:strategicalignment_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit Strategic Alignment",
                "name",
                "description",
            ),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )


class ProjectForm(forms.ModelForm):
    tier = ModelChoiceField(
        queryset=Tier.objects.all(),
        help_text="Please select an existing Tier. <a href='/register/tier/create' target='_blank'> Create new Tier </a>",
    )

    project_type = ModelChoiceField(
        queryset=ProjectType.objects.all(),
        help_text="Please select an existing Project Type. <a href='/register/projecttype/create' target='_blank'> Create new Project Type </a>",
    )

    stage = ModelChoiceField(
        queryset=ProjectStage.objects.all(),
        help_text="Please select an existing Project Stage. <a href='/register/projectstage/create' target='_blank'> Create new Project Stage </a>",
    )

    class Meta:
        model = models.Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("register:project_list")

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Create/Edit a Project",
                Field("name", css_class="basicfield"),
                "tier",
                "project_type",
                "stage",
                Field("abbreviation", css_class="basicfield"),
                "dft_group",
                "gmpp",
            ),
            ButtonHolder(
                Submit("submit", "Submit"),
                Button(
                    "cancel",
                    "Cancel",
                    onclick=f"location.href='{cancel_redirect}';",
                    css_class="btn btn-danger",
                ),
            ),
        )
