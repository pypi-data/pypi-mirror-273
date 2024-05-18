import json

from django.utils.safestring import mark_safe


def pretty_json(json_string):
    return mark_safe(
        "<style>div.readonly { width: 100%; overflow-wrap: break-word }</style>"
        '<div style="white-space: pre-wrap; "width: 100%; overflow-wrap: break-word">'
        + "<br>".join(json.dumps(json_string, indent=4).split("\n"))
        + "</div>"
    )
