"""Helper utilities for formatting responses with media URLs"""

def convert_minio_url_for_frontend(url: str, is_docker: bool = False) -> str:
    """
    Convert MinIO internal URLs to publicly accessible URLs.
    
    Args:
        url: Original MinIO URL (e.g., http://minio:9000/media/image.jpg)
        is_docker: If True, keeps minio:9000; if False, uses localhost:9000
        
    Returns:
        Publicly accessible URL
    """
    if not url:
        return ""
    
    # For frontend access, replace internal docker hostname with localhost
    if not is_docker and 'minio:9000' in url:
        return url.replace('minio:9000', 'localhost:9000')
    
    return url


def extract_image_urls_from_text(text: str) -> list[str]:
    """
    Extract all HTTP/HTTPS URLs from text.
    
    Args:
        text: Text potentially containing URLs
        
    Returns:
        List of extracted URLs
    """
    import re
    pattern = r'https?://[^\s<>"()]+(?:\.jpg|\.jpeg|\.png|\.gif|\.webp|\.svg)'
    return re.findall(pattern, text, re.IGNORECASE)


def format_response_with_images(response_text: str, convert_urls: bool = True) -> dict:
    """
    Format a response to include both text and separate image URLs for frontend.
    
    Args:
        response_text: Raw response text with potential markdown images
        convert_urls: Whether to convert minio URLs to localhost
        
    Returns:
        Dict with 'text' and 'images' fields
    """
    import re
    
    # Extract markdown images: ![alt](url)
    markdown_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', response_text)
    
    images = []
    seen_urls = set()
    
    for alt_text, url in markdown_images:
        if convert_urls:
            url = convert_minio_url_for_frontend(url)
        if url not in seen_urls:
            images.append({
                'url': url,
                'alt': alt_text or 'Image'
            })
            seen_urls.add(url)
    
    # Also extract plain URLs that might not be in markdown (but exclude markdown syntax)
    # Remove markdown images first to avoid re-matching
    text_without_markdown = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', response_text)
    plain_urls = extract_image_urls_from_text(text_without_markdown)
    
    for url in plain_urls:
        if convert_urls:
            url = convert_minio_url_for_frontend(url)
        # Avoid duplicates
        if url not in seen_urls:
            images.append({
                'url': url,
                'alt': 'Image'
            })
            seen_urls.add(url)
    
    return {
        'text': response_text,
        'images': images,
        'has_images': len(images) > 0
    }


def create_markdown_image(url: str, alt_text: str = "Image") -> str:
    """
    Create markdown image syntax.
    
    Args:
        url: Image URL
        alt_text: Alternative text for image
        
    Returns:
        Markdown formatted image string
    """
    return f"![{alt_text}]({url})"


def format_post_with_media(post_data: dict) -> str:
    """
    Format a post object with its media for display.
    
    Args:
        post_data: Dict containing post info and media URL
        
    Returns:
        Formatted string with post details and image
    """
    post_id = post_data.get('id', 'Unknown')
    user = post_data.get('user', 'Unknown')
    caption = post_data.get('caption', '')
    media_url = post_data.get('media_url', '')
    
    result = f"**Post #{post_id}** by {user}"
    if caption:
        result += f"\n{caption}"
    if media_url:
        public_url = convert_minio_url_for_frontend(media_url)
        result += f"\n{create_markdown_image(public_url, f'Post {post_id}')}"
    
    return result
