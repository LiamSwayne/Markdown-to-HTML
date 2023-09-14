# Read the markdown content
with open("source.md", "r") as inputFile:
    markdownContent = inputFile.readlines()

# Initialize variables
htmlOutput = ""

# Define the CSS style
cssStyling = """
<style>
  body {
    background: black;
    color: #ffffff;
    font-family: 'Helvetica Neue', Helvetica;
    text-align: center;
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
    max-width: 100%;
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
        while line[0] == " ":
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

# Update the source with corrected markdown syntax
with open("source.md", "w") as inputFile:
    inputFile.write("".join(markdownContent))

# Close the last text block if necessary
if insideBlock:
    htmlOutput += "</div>"

# Close the body and html tags
htmlOutput += "</body>"
htmlOutput += "</html>"

# Write the HTML output to a file
with open("source.html", "w") as outputFile:
    outputFile.write(htmlOutput)
