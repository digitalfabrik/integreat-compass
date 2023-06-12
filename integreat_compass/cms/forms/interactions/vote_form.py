from ...models import Vote
from ..custom_model_form import CustomModelForm


class VoteForm(CustomModelForm):
    """
    Form for creating and editing votes
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        mode = Vote
        fields = ["approval", "comment"]
