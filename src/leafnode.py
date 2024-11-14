from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError()
        html = self.value
        if self.tag:
            html = f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
        return html