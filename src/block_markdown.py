
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block : block.strip(), blocks))
    blocks = list(filter(lambda block : len(block) > 0, blocks))
    return blocks