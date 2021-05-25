from django import template
from django.utils.safestring import mark_safe
import phonenumbers

register = template.Library()

@register.filter("legal_url", is_safe=True)
def phone_number(illegal):
    splitIllegal = illegal.split(":")
    if splitIllegal[0] == "https://" or splitIllegal[0] == "http://":
        return mark_safe(illegal)
    else:
        return "//" + illegal

@register.filter("format_phone", is_safe=True)
def phone_number(s):
    parsed = phonenumbers.parse(s, "US")
    autoFormatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    rawNoExt = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    ext = ""
    splitNumber = autoFormatted.split(" ")
    if len(splitNumber) == 4:
        ext = "x" + splitNumber[3]
    linkText = " "
    linkText = linkText.join(splitNumber[0:2])

    html = f'<a target="_blank" href="tel:{rawNoExt}">{linkText}</a> {ext}'

    return mark_safe(html)

@register.simple_tag(name="bu_options", takes_context=True)
def bu_options(context):
    site = context["site"]
    options = []
    if site["bwn"]:
        options.append("With naloxone (ex. Suboxone)")
    if site["bwon"]:
        options.append("Without naloxone")
    if site["beri"]:
        options.append("Injectable extended-release (ex. Sublocade)")
    if site["bsdm"]:
        options.append("Sub-dermal implant (Probuphine)")
    options = ";<br/>".join(options) + ";"
    return mark_safe(options)

@register.simple_tag(name="nu_options", takes_context=True)
def nu_options(context):
    site = context["site"]
    options = []
    if site["vtrl"]:
        options.append("Vivitrol (injectable)")
    if site["nxn"]:
        options.append("Oral naltrexone")
    options = ";<br/>".join(options) + ";"
    return mark_safe(options)
