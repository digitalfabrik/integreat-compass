from ...models import Report
from ..custom_model_form import CustomModelForm


class ReportForm(CustomModelForm):
    """
    Form for reporting an offer
    """

    class Meta:
        """
        This class contains the meta information
        """

        model = Report
        fields = ["comment"]
