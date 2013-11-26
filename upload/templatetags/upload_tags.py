from django import template

register = template.Library()

@register.simple_tag
def upload_js():
    return """
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <div class="template-upload fade photo-upload">
        <span class="preview"></span>
        <p class="name">{%=file.name%}</p>
        {% if (file.error) { %}
            <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
        {% } %}

        <p class="size">{%=o.formatFileSize(file.size)%}</p>
        {% if (!o.files.error) { %}
            <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>
        {% } %}
        {% if (!o.files.error && !i && !o.options.autoUpload) { %}
            <button class="btn btn-primary start">
                <i class="glyphicon glyphicon-upload"></i>
                <span>{%=locale.fileupload.start%}</span>
            </button>
        {% } %}
        {% if (!i) { %}
            <button class="btn btn-warning cancel">
                <i class="glyphicon glyphicon-ban-circle"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}
    </div>
{% } %}
</script>
<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <div class="template-download fade photo-upload">
            <span class="preview">
                {% if (file.thumbnailUrl) { %}
                    <a href="{%=file.thumbnailUrl%}" title="{%=file.name%}" download="{%=file.name%}" data-gallery><img src="{%=file.thumbnailUrl%}"></a>
                {% } %}
            </span>
            <p class="name">
                <a href="{%=file.url%}" title="{%=file.name%}" download="{%=file.name%}" {%=file.thumbnailUrl?'data-gallery':''%}>{%=file.name%}</a>
            </p>
            {% if (file.error) { %}
                <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
            {% } %}
            <span class="size">{%=o.formatFileSize(file.size)%}</span>
            <button class="btn btn-danger delete" data-type="{%=file.deleteType%}" data-url="{%=file.deleteUrl%}"{% if (file.deleteWithCredentials) { %} data-xhr-fields='{"withCredentials":true}'{% } %}>
                <i class="glyphicon glyphicon-trash"></i>
                <span>{%=locale.fileupload.destroy%}</span>
            </button>

            <span class="make-primary" {% if (!file.isPrimary) { %} style="display:none" {% } %} >
                Primary
            </span>

            <button class="btn btn-primary make" data-url="{%=file.makePrimaryUrl%}"
                {% if (file.isPrimary) { %} style="display:none" {% } %}>
                <span>{%=locale.fileupload.makePrimary%}</span>
            </button>
    </div>
{% } %}
</script>
"""






