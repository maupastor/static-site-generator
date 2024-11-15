class HTMLNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        props_list = list(self.props.items())
        props = "".join(map(lambda prop : f' {prop[0]}="{prop[1]}"', props_list))
        return props
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: No value defined")
        html = self.value
        if self.tag:
            html = f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
        return html

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: No HTML Tag was defined")
        if self.children is None:
            raise ValueError("Invalid HTML: No children were defined")
        
        children_html = "".join(map(lambda child: child.to_html(), self.children))
        html = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        return html