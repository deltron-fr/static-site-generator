
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        formatted_string = ""
        for name, value in self.props.items():
            formatted_string += f' {name}="{value}"'

        return formatted_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("leaf node must contain a value")
        
        if not self.tag:
            return self.value
        
        props = self.props_to_html()
        if not props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node must have a tag")
        
        if not self.children:
            raise ValueError("pare node must have child elements")

        merged_html = ""
        for child in self.children:
            merged_html += child.to_html()

        return f"<{self.tag}>{merged_html}</{self.tag}>"