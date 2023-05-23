from django.views.generic import TemplateView

class IndexView(TemplateView):
    """
    View to see all offers
    """

    template_name = "index.html"