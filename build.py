# Read the markdown content from source.md
with open("source.md", "r") as markdown_file:
    markdown_content = markdown_file.readlines()

# Initialize variables
html_output = ""

# Define the CSS style
css_style = """
<style>
  body {
    background: black;
    color: white;
  }
  div {
    max-width: 500px;
    margin-bottom: 20px;
  }
  div.title {
    font-weight: bold;
  }
  img {
    max-width: 500px;
  }
  div.caption {
    color: grey;
  }
</style>
"""

# Add the HTML structure and style to the output
html_output += "<html>"
html_output += "<head>"
html_output += css_style
html_output += "</head>"
html_output += "<body>"

# Initialize variables
in_block = False

# Process the markdown content
for line in markdown_content:
    line = line.strip()
    if line.startswith("# "):  # Title
        html_output += "<div class='title'>"
        html_output += line[2:]  # Remove the "#" symbol
        html_output += "</div>"
    elif line.startswith("![]("):  # Image
        # Extract the image URL
        image_url = line[line.find("(") + 1:line.find(")")]
        html_output += "<div>"
        html_output += "<img src='" + image_url + "' />"
        html_output += "<div class='caption'>[caption] This is a dog.</div>"
        html_output += "</div>"
    elif line.startswith("[caption] "):  # Caption
        html_output += "<div class='caption'>"
        html_output += line[len("[caption] "):]
        html_output += "</div>"
    elif line:  # Text block
        if not in_block:
            html_output += "<div>"
            in_block = True
        html_output += line
    else:  # Empty line
        if in_block:
            html_output += "</div>"
            in_block = False
        html_output += "<div style='height:20px;'></div>"

# Close the last text block if necessary
if in_block:
    html_output += "</div>"

# Close the body and html tags
html_output += "</body>"
html_output += "</html>"

# Write the HTML output to a file
with open("source.html", "w") as html_file:
    html_file.write(html_output)
