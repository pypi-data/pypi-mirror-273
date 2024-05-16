from django.forms import Form
from django.forms.fields import CharField


from django_apis.views import get_apiview
from django_apis.views import get_json_payload
from django_apis.exceptions import ValidationError


apiview = get_apiview()


@apiview(methods="GET")
def ping(request):
    return "pong"


class EchoInput(Form):
    msg = CharField(max_length=16, required=True)


@apiview(methods="POST")
def echo(request):
    payload = get_json_payload(request)
    form = EchoInput(payload)
    if form.is_valid():
        return form.cleaned_data["msg"]
    else:
        raise ValidationError(form)


@apiview(methods="GET")
def getRequestInfo(request):
    result = {}
    for key, value in request.META.items():
        if isinstance(value, str):
            result[key] = value
    return result
