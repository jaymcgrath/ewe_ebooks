from django import template

register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(value, arg):
    """
    custom template filter for packing extra html attrs onto django form fields
    argument should be formatted as "key:value, key1:value1, key2:value2" etc
    example usage: user_form.username|add_attrs:'class:form-control, id:username, aria-label:Input for username'
    please note that leading and trailing whitespace will be stripped
    """
    try:
        # Split list on comma
        kv_pairs = arg.split(",")
    except ValueError:
        raise template.TemplateSyntaxError(
            "add_attrs requires as an argument a string in the format 'key:value, key1:value1, key2:value2...'"
        )


    # Create dictionary
    html_attrs = dict()

    # Clean items and add attribute pairs to dictionary
    for item in kv_pairs:
        item = item.strip()
        k, v = item.split(":")
        html_attrs.update({k.strip():v.strip()})

    return value.as_widget(attrs=html_attrs)
