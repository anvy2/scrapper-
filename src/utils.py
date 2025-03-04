def format_proxy(proxy_string):
    """Format a proxy string for use with HTTP clients."""
    if not proxy_string:
        return None

    # If protocol is not specified, default to http
    if not (
        proxy_string.startswith("http://")
        or proxy_string.startswith("https://")
        or proxy_string.startswith("socks5://")
    ):
        proxy_string = f"http://{proxy_string}"

    return proxy_string
