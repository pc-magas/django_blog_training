import bleach

def xss_sanitize_html(dirty:str)->str
    return bleach.clean(
            dirty,
            tags=[
                "p", "br", "strong", "em",
                "ul", "ol", "li",
                "a", "blockquote",
            ],
            attributes={
                "a": ["href", "title", "target", "rel"],
            },
            protocols=["http", "https", "mailto"],
            strip=True,
        )