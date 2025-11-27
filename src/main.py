from textnode import TextNode, TextType

def main():
    text_node_1 = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(text_node_1)

main()