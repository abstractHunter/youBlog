
def custom_tag_splitter(tags):
    # custom tag splitter according to tagify.js
    return [tag.lstrip('[{"value":').rstrip('"}]') for tag in tags.split(',')]
