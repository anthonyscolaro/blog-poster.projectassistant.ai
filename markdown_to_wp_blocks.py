"""
Markdown+Frontmatter to WordPress Blocks HTML Renderer
Converts markdown with YAML frontmatter to WordPress block HTML
"""
import re
import yaml
from typing import Dict, Any, Tuple, Optional
import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


class WordPressBlockConverter:
    """Convert Markdown to WordPress block HTML"""
    
    @staticmethod
    def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and return (metadata, content)"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return metadata or {}, body
        except yaml.YAMLError:
            pass
        
        return {}, content
    
    @staticmethod
    def wrap_paragraph(text: str) -> str:
        """Wrap text in WordPress paragraph block"""
        if not text.strip():
            return ''
        return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->\n'
    
    @staticmethod
    def wrap_heading(text: str, level: int) -> str:
        """Wrap text in WordPress heading block"""
        return f'<!-- wp:heading {{"level":{level}}} -->\n<h{level}>{text}</h{level}>\n<!-- /wp:heading -->\n'
    
    @staticmethod
    def wrap_image(src: str, alt: str = '', caption: str = '') -> str:
        """Wrap image in WordPress image block"""
        figure_class = 'wp-block-image'
        img_html = f'<img src="{src}" alt="{alt}"/>'
        
        if caption:
            return f'''<!-- wp:image -->\n<figure class="{figure_class}">{img_html}<figcaption>{caption}</figcaption></figure>\n<!-- /wp:image -->\n'''
        else:
            return f'''<!-- wp:image -->\n<figure class="{figure_class}">{img_html}</figure>\n<!-- /wp:image -->\n'''
    
    @staticmethod
    def wrap_list(items: list, ordered: bool = False) -> str:
        """Wrap list items in WordPress list block"""
        tag = 'ol' if ordered else 'ul'
        block_type = 'list' if not ordered else 'list'
        attrs = '{"ordered":true}' if ordered else ''
        
        list_html = f'<{tag}>\n'
        for item in items:
            list_html += f'<li>{item}</li>\n'
        list_html += f'</{tag}>'
        
        return f'<!-- wp:{block_type} {attrs} -->\n{list_html}\n<!-- /wp:{block_type} -->\n'
    
    @staticmethod
    def wrap_quote(text: str, citation: str = '') -> str:
        """Wrap text in WordPress quote block"""
        cite_html = f'<cite>{citation}</cite>' if citation else ''
        return f'''<!-- wp:quote -->\n<blockquote class="wp-block-quote"><p>{text}</p>{cite_html}</blockquote>\n<!-- /wp:quote -->\n'''
    
    @staticmethod
    def wrap_code(code: str, language: str = '') -> str:
        """Wrap code in WordPress code block"""
        return f'''<!-- wp:code -->\n<pre class="wp-block-code"><code>{code}</code></pre>\n<!-- /wp:code -->\n'''


class ImageShortcodePreprocessor(Preprocessor):
    """Convert [image] shortcodes to markdown images before processing"""
    
    def run(self, lines):
        text = '\n'.join(lines)
        # Pattern: [image src="url" alt="text" caption="text"]
        pattern = r'\[image\s+src="([^"]+)"(?:\s+alt="([^"]*)")?(?:\s+caption="([^"]*)")?\]'
        
        def replace_shortcode(match):
            src = match.group(1)
            alt = match.group(2) or ''
            caption = match.group(3) or ''
            # Convert to markdown image with caption stored as title
            if caption:
                return f'![{alt}]({src} "{caption}")'
            return f'![{alt}]({src})'
        
        text = re.sub(pattern, replace_shortcode, text)
        return text.split('\n')


class WordPressBlockExtension(Extension):
    """Markdown extension to output WordPress blocks"""
    
    def extendMarkdown(self, md):
        md.preprocessors.register(ImageShortcodePreprocessor(md), 'image_shortcode', 100)


def markdown_to_wp_blocks(content: str, parse_frontmatter: bool = True) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Convert Markdown+frontmatter to WordPress block HTML
    
    Args:
        content: Markdown content with optional YAML frontmatter
        parse_frontmatter: Whether to extract frontmatter
    
    Returns:
        Tuple of (metadata dict or None, WordPress block HTML)
    """
    converter = WordPressBlockConverter()
    
    # Parse frontmatter if requested
    metadata = None
    if parse_frontmatter:
        metadata, content = converter.parse_frontmatter(content)
    
    # Split content into blocks for manual processing
    lines = content.split('\n')
    wp_blocks = []
    current_paragraph = []
    in_code_block = False
    code_lines = []
    code_language = ''
    list_items = []
    list_type = None
    
    for i, line in enumerate(lines):
        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                # Flush current paragraph
                if current_paragraph:
                    wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                # Start code block
                in_code_block = True
                code_language = line[3:].strip()
                code_lines = []
            else:
                # End code block
                wp_blocks.append(converter.wrap_code('\n'.join(code_lines), code_language))
                in_code_block = False
                code_lines = []
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # Headings
        if line.startswith('#'):
            # Flush current paragraph
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            wp_blocks.append(converter.wrap_heading(text, min(level, 6)))
            continue
        
        # Lists
        if re.match(r'^(\*|-|\+|\d+\.)\s+', line):
            # Flush current paragraph
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            
            # Determine list type
            is_ordered = bool(re.match(r'^\d+\.', line))
            item_text = re.sub(r'^(\*|-|\+|\d+\.)\s+', '', line)
            
            if list_type is None:
                list_type = 'ordered' if is_ordered else 'unordered'
                list_items = [item_text]
            elif (list_type == 'ordered') == is_ordered:
                list_items.append(item_text)
            else:
                # Different list type, flush current list
                wp_blocks.append(converter.wrap_list(list_items, list_type == 'ordered'))
                list_type = 'ordered' if is_ordered else 'unordered'
                list_items = [item_text]
            continue
        
        # Flush list if we're out of list items
        if list_items and not re.match(r'^(\*|-|\+|\d+\.)\s+', line):
            wp_blocks.append(converter.wrap_list(list_items, list_type == 'ordered'))
            list_items = []
            list_type = None
        
        # Blockquotes
        if line.startswith('>'):
            # Flush current paragraph
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            
            quote_text = line.lstrip('>').strip()
            wp_blocks.append(converter.wrap_quote(quote_text))
            continue
        
        # Images (markdown style or shortcode)
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)(?:\s+"([^"]+)")?\)'
        img_match = re.match(img_pattern, line)
        if img_match:
            # Flush current paragraph
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            
            alt = img_match.group(1)
            src = img_match.group(2)
            caption = img_match.group(3) or ''
            wp_blocks.append(converter.wrap_image(src, alt, caption))
            continue
        
        # Image shortcode
        shortcode_pattern = r'\[image\s+src="([^"]+)"(?:\s+alt="([^"]*)")?(?:\s+caption="([^"]*)")?\]'
        shortcode_match = re.match(shortcode_pattern, line)
        if shortcode_match:
            # Flush current paragraph
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            
            src = shortcode_match.group(1)
            alt = shortcode_match.group(2) or ''
            caption = shortcode_match.group(3) or ''
            wp_blocks.append(converter.wrap_image(src, alt, caption))
            continue
        
        # Empty line - flush paragraph
        if not line.strip():
            if current_paragraph:
                wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            continue
        
        # Regular text - add to current paragraph
        current_paragraph.append(line)
    
    # Flush any remaining content
    if current_paragraph:
        wp_blocks.append(converter.wrap_paragraph(' '.join(current_paragraph)))
    if list_items:
        wp_blocks.append(converter.wrap_list(list_items, list_type == 'ordered'))
    
    # Join all blocks
    html = '\n'.join(filter(None, wp_blocks))
    
    return metadata, html


# Example usage and tests
if __name__ == "__main__":
    test_content = """---
title: Understanding Service Dogs
author: AI Agent
tags: [service-dogs, ADA, training]
category: Education
---

# What Are Service Dogs?

Service dogs are specially trained animals that assist people with disabilities. They perform specific tasks related to their handler's disability.

## Types of Service Dogs

* Guide dogs for the blind
* Hearing dogs for the deaf
* Mobility assistance dogs
* Medical alert dogs

[image src="/wp-content/uploads/service-dog.jpg" alt="Service dog in vest" caption="A trained service dog wearing an official vest"]

### Training Requirements

1. Basic obedience training
2. Task-specific training
3. Public access training
4. Handler bonding period

> Important: Service dogs are not pets. They are working animals protected under the ADA.

```python
def is_service_dog(dog):
    return dog.trained and dog.task_specific
```

Regular paragraph text continues here with more information about service dogs and their important role in society.
"""
    
    metadata, html = markdown_to_wp_blocks(test_content)
    
    print("=== METADATA ===")
    print(yaml.dump(metadata, default_flow_style=False))
    print("\n=== WORDPRESS BLOCKS HTML ===")
    print(html)