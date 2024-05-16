Mikoblocks is a minimal library to programmatically generate html. It is unopinionated and outputs pure html code and due to a small simple syntax the programming is much easier and clearer to type compared to html. It allows assembling of component "blocks" which can nest further components within, allowing complex reusable pieces to be shared across pages and projects.

``` javascript
const { Block } = import('mikoblocks');

class MikoblocksExamplePage extends Block {

    constructor() {
        super();
        this.raw('&lt;!doctype html&gt;');
        let html = this.tag('html');
        let head = html.tag('head');
        let body = html.tag('body');
        body.tag('div', { id: "content", class: "example-class" }).raw("Hello World!");
    }

}

let page = new MikoblocksExamplePage();
console.log(page.toHtml());
```

# Installation
``` javascript

npm install mikoblocks

```

# Uses
Mikoblocks can be used as a prebuild process to output static html pages and it can also be run on the server dynamically to generate html at runtime.

- Programmatically generate your entire website from one script. Define components for header, footer, menus, buttons whatever you like and combine them all to output your entire page.
- Use mikoblocks on the server to dynamically generate pages with common shared elements.

# Guide
Mikoblocks elegantly only uses 4 functions.


## Block
A block is a beginning structure of a mikoblock, on it's own it has no output but can hold a list of sub-blocks. This is what empowers it over dom programming in that a block be be an element akin to an object or a list of elements akin to a list.

## Tag
A tag is any xml tag that has a paired closing tag. You define the tag name and any attributes on the block itself.

## Void
A void is any xml block that doesn't have a closing tag. You define the tag name and any attributes on the block itself.

## Raw
Raw outputs text, it can hold text representations of further html or be the text between the opening and closing of an html block.


# Outputs
Any mikoblock can use the .toHtml() function to output text based html of itself and all nested blocks. That's it, pretty simple huh? 

### toHtml()
Outputs the block into html text including all nested blocks.


