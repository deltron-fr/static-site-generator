from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_nodes = []

    delimiter_count = 0 

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)

        else:
            text_nodes.append(old_node)

    for text_node in text_nodes:
        for char in text_node.text:
            if delimiter == char:
                delimiter_count += 1
    
    if delimiter_count % 2 != 0:
        raise Exception("Invalid text, missing delimiter")
    

    for text_node in text_nodes:
        text_split = text_node.text.split(delimiter)
    
    for i in range(len(text_split)):
        if i % 2 == 0:
            text_nodes.append(TextNode(text_split[i], TextType.TEXT))
        else:
            text_nodes.append(TextNode(text_split[i], text_type))


    new_nodes.extend(text_nodes)

    return new_nodes




    

