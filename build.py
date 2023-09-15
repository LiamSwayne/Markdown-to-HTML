# SETTINGS
sourceFolder = "source" # Process all markdown files in the source folder and subfolders
outputFolder = "docs" # Output html files with same directory structure
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

# imports
import os
import shutil

# Function to process a markdown file and generate HTML
def markdownToHTML(inputFilePath, outputFolderPath):
    # Read the markdown content
    with open(inputFilePath, "r") as inputFile:
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
            htmlOutput += "<img class='image' src='" + image_url + "'/>"
            insideImageBlock = True
            insideBlock = False
        elif line.startswith("######"):  # Caption
            # Slice to caption
            line = line[len("######"):]
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

            markdownContent[i] = "###### " + line + "\n"
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
    with open(inputFilePath, "w") as inputFile:
        inputFile.write("".join(updatedMarkdownContent))

    # Close the last text block if necessary
    if insideBlock:
        htmlOutput += "</div>"

    # Close the body and html tags
    htmlOutput += "</body>"
    htmlOutput += "</html>"

    # Determine the output HTML file path
    output_file_name = os.path.basename(inputFilePath).replace(".md", ".html")
    output_file_path = os.path.join(outputFolderPath, output_file_name)

    # Write the HTML output to a file
    with open(output_file_path, "w") as outputFile:
        outputFile.write(htmlOutput)

# Build every markdown file to html
for root, _, files in os.walk(sourceFolder):
    for fileName in files:
        srcFilePath = os.path.join(root, fileName)
        relativePath = os.path.relpath(srcFilePath, sourceFolder)
        dstFolder = os.path.join(outputFolder, os.path.dirname(relativePath))
        os.makedirs(dstFolder, exist_ok=True)

        if fileName.endswith(".md"):
            # Process markdown files to HTML
            markdownToHTML(srcFilePath, dstFolder)
        else:
            # Copy non-markdown files
            dstFilePath = os.path.join(dstFolder, fileName)
            shutil.copy2(srcFilePath, dstFilePath)