import os

# Function to process a markdown file and generate HTML
def process_markdown_file(input_file_path, output_folder_path):
    # Read the markdown content
    with open(input_file_path, "r") as inputFile:
        markdownContent = inputFile.readlines()

    # Remove leading and trailing empty lines
    while markdownContent and markdownContent[0].strip() == "":
        markdownContent = markdownContent[1:]
    while markdownContent and markdownContent[-1].strip() == "":
        markdownContent = markdownContent[:-1]
    if markdownContent and markdownContent[-1][-1] == "\n":
        markdownContent[-1] = markdownContent[-1][:-1]

    # Initialize variables
    htmlOutput = ""

    # Define the CSS style
    cssStyling = """
    <style>
      body {
        background: black;
        color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica;
      }
      .markdown {
        max-width: 500px;
        margin: 15px auto;
        text-align: left;
        line-height: 1.6;
        font-size: 16px;
      }
      .title {
        font-weight: 700;
        font-size: 40px;
        line-height: 0.95;
      }
      .image {
        width: 500px;
      }
      .caption {
        margin-top: 3px;
        color: #757575;
        line-height: 1.1;
        font-weight: 500;
        font-size: 14px;
      }
    </style>
    """

    # Add the HTML structure and style to the output
    htmlOutput += "<html>"
    htmlOutput += "<head>"
    htmlOutput += "<meta charset='UTF-8'>"
    htmlOutput += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    htmlOutput += cssStyling
    htmlOutput += "</head>"
    htmlOutput += "<body>"

    # Initialize variables
    insideBlock = False
    insideImageBlock = False
    captionText = ""

    # Process the markdown content
    for i in range(len(markdownContent)):
        line = markdownContent[i].strip()
        if line.startswith("# "):  # Title
            htmlOutput += "<div class='markdown title'>"
            htmlOutput += line[2:]  # Remove the "#" symbol
            htmlOutput += "</div>"
            insideBlock = False
        elif line.startswith("![]("):  # Image
            # Extract the image URL
            image_url = line[line.find("(") + 1:line.find(")")]
            htmlOutput += "<div class='markdown'>"
            htmlOutput += "<img class='image' src='" + image_url + "' />"
            insideImageBlock = True
            insideBlock = False
        elif line.startswith("[caption]"):  # Caption
            # Slice to caption
            line = line[len("[caption]"):]
            while line and line[0] == " ":
                line = line[1:]

            if insideImageBlock:
                captionText = line
            else:
                if insideBlock:
                    htmlOutput += "</div>"
                    insideBlock = False
                htmlOutput += "<div class='markdown caption'>"
                htmlOutput += line
                htmlOutput += "</div>"

            markdownContent[i] = "[caption] " + line + "\n"
        elif line:  # Text block
            if not insideBlock:
                htmlOutput += "<div class='markdown'>"
                insideBlock = True
            if insideBlock:
                htmlOutput += " "  # Add a space between lines in the same block
            htmlOutput += line
        else:  # Empty line
            if insideBlock:
                htmlOutput += "</div>"
                insideBlock = False
            elif insideImageBlock:
                htmlOutput += "<div class='caption'>" + captionText + "</div>"
                insideImageBlock = False
                captionText = ""

    # Remove writespace longer than 2 lines in markdown
    updatedMarkdownContent = []
    consecutiveNewlines = 0
    for line in markdownContent:
        if line.strip() == "":
            consecutiveNewlines += 1
            if consecutiveNewlines <= 2:
                updatedMarkdownContent.append(line)
        else:
            consecutiveNewlines = 0
            updatedMarkdownContent.append(line)

    # Update the source with corrected markdown syntax
    with open(input_file_path, "w") as inputFile:
        inputFile.write("".join(updatedMarkdownContent))

    # Close the last text block if necessary
    if insideBlock:
        htmlOutput += "</div>"

    # Close the body and html tags
    htmlOutput += "</body>"
    htmlOutput += "</html>"

    # Determine the output HTML file path
    output_file_name = os.path.basename(input_file_path).replace(".md", ".html")
    output_file_path = os.path.join(output_folder_path, output_file_name)

    # Write the HTML output to a file
    with open(output_file_path, "w") as outputFile:
        outputFile.write(htmlOutput)

# Process all markdown files in the source folder and subfolders
source_folder = "source"
docs_folder = "docs"

for root, _, files in os.walk(source_folder):
    for file_name in files:
        if file_name.endswith(".md"):
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, source_folder)
            output_folder = os.path.join(docs_folder, os.path.dirname(relative_path))
            os.makedirs(output_folder, exist_ok=True)
            process_markdown_file(file_path, output_folder)
