from . import utils

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("mikoblocks")
except PackageNotFoundError:
    __version__ = "unknown"

def slot_to_html(slot):
    """Generate HTML string from the block's contents."""
    html = ""
    for child in slot:
        if hasattr(child, 'to_html'):
            html += child.to_html()
        else:
            html += str(child)  # Convert non-html components to string
    return html
    
def attribute_string(attributes):
    attributes_str = ' '.join(f'{key}="{value}"' for key, value in attributes.items())
    attributes_str = f" {attributes_str}" if attributes_str else ""
    return attributes_str

class Block(list):

    def __init__(self,type_id=None,block_id=None):
        super().__init__()
        self.type_id = type_id
        self.block_id = block_id
        
    def add(self,obj):
        self.append(obj)
        return obj
    
    def __truediv__(self, other):
        self.append(other)
        return other

    def __iadd__(self, other): 
        self.append(other)
        return self
    
    def tag(self,tag,attr={}):
        return self.add(Tag(tag,attr))

    def raw(self,content):
        return self.add(Raw(content))
    
    def void(self,tag,attr={}):
        return self.add(Void(tag,attr))

    def block(self):
        return self.add(Block())

    #def clear(self):
        #self.clear()

    def to_html(self):
        return self.slot_html

    @property
    def slot_html(self):
        return slot_to_html(self)
      
class Tag(Block):

    def __init__(self,tag,attr={}):
        super().__init__()
        self.tag_name = tag
        self.attributes = attr

    def add_class(self, class_name):
        if 'class' in self.attributes:
            self.attributes['class'] += f" {class_name}"
        else:
            self.attributes['class'] = class_name
            
    def to_html(self):
        return f"<{self.tag_name}{attribute_string(self.attributes)}>{self.slot_html}</{self.tag_name}>"

class Void():

    def __init__(self,tag,attr={}):
        self.tag = tag
        self.attributes = attr

    def to_html(self):
        return f"<{self.tag}{attribute_string(self.attributes)}/>"
    
class Raw():

    def __init__(self,content):
        self.content = str(content)

    def to_html(self):
        return self.content
