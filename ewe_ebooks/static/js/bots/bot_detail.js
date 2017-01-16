/**
 * Extra javascript for popovers
 *
 **/

$(function () {
  $('[data-toggle="popover"]').popover(
      {
          'trigger':'hover',
          'template':'<div class="popover" role="tooltip"><div class="popover-arrow"></div>' +
          '<h3 class="popover-title"></h3><div class="popover-content thumb-wrapper"></div></div>',
          'html':true


      })
})
/**

<div class="corpus-preview">
    {% for corpus in mashup.corpora.all %}
        {% if corpus %}
            <span class="thumb-wrapper">
                <div style="background-image:url({{ corpus.image_url }})"
                    class="corpus-thumb" title="{{ corpus.desc }}" id="cimage{{ corpus.id }}"
                    data-corpus_id="{{ corpus.id }}">
                   {#  include the appropriate icon #}
                    {% if corpus.type == "TW" %}
                        <i class="fa fa-twitter"></i>
                    {% elif corpus.type == "EX" %}
                        <i class="fa fa-book"></i>
                    {% endif %}
                </div>
            </span>
{% if not forloop.last %}
    {# include the plus between elements #}
    <span class="preview-plus">
        <i class="fa fa-plus" aria-hidden="true"></i>
    </span>
{% endif %} {# end inner loop #}
    {% endif %}
{% endfor %}
</div>

 */
