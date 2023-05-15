from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Start page of the project
    """

    template_name = "index.html"
