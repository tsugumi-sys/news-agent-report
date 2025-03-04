import os


def generate_index_html(reports_dir="reports", output_file="index.html"):
    # Ensure the reports directory exists
    if not os.path.exists(reports_dir) or not os.path.isdir(reports_dir):
        print(f"Directory '{reports_dir}' does not exist.")
        return

    # Get all HTML files in the reports directory
    html_files = sorted([f for f in os.listdir(reports_dir) if f.endswith(".html")])

    # Generate the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report Index</title>
    </head>
    <body>
        <h1>Report Index</h1>
        <ul>
    """

    for file in html_files:
        html_content += (
            f'            <li><a href="{reports_dir}/{file}">{file}</a></li>\n'
        )

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Write to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Index file '{output_file}' has been created successfully.")


# Run the function
generate_index_html()
