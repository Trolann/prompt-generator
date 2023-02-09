from flask import Flask, request, render_template

app = Flask(__name__)

def read_file(filename):
    """
    Reads a file and returns the contents in a dictionary with each line separated by a pipe ('|') as the key and value.

    :param filename: The name of the file to be read.
    :type filename: str
    :return: A dictionary with each line separated by a pipe ('|') as the key and value.
    :rtype: dict
    """
    result = {}
    with open(filename, 'r') as file:
        key = None
        value = []
        for line in file:
            line = line.strip()
            if "|" in line:
                if key is not None:
                    result[key] = "".join(value).strip()
                key, v = line.split("|")
                key = key.strip()
                value = [v.strip()]
            else:
                value.append(line)
        if key is not None:
            result[key] = "".join(value).strip()
    return result



@app.route("/", methods=["GET", "POST"])
def index():
    """
    The main page of the flask application. If the request method is POST, it will get the form data,
    write it to a file named `prompt.txt`, then return the result in a template with the appropriate
    data. If the request method is GET, it will just read the file and return the result in a template.

    :return: The template with the appropriate data.
    :rtype: flask.templating.Template
    """
    if request.method == "POST":
        language = request.form.get("lang_radio")
        output = request.form.get("output_style")
        function_name = request.form.get("name")
        function_description = request.form.get("description")
        inputs = request.form.get("inputs")
        outputs = request.form.get("outputs")
        keywords = request.form.get("keywords")

        result = f"Language| {language}\n" \
                 f"Output style| {output}\n" \
                 f"Function Name| {function_name}\n" \
                 f"Function Description| {function_description}\n" \
                 f"Inputs| {inputs}\n" \
                 f"Outputs| {outputs}\n" \
                 f"Keywords| {keywords}"
        with open('prompt.txt', 'w') as f:
            f.write(result)
        result_dict = read_file('prompt.txt')
        return render_template("index.html",
                               language=result_dict["Language"],
                               style=result_dict["Output style"],
                               inputs=result_dict["Inputs"],
                               outputs=result_dict["Outputs"],
                               name=result_dict["Function Name"],
                               description=result_dict["Function Description"],
                               keywords=result_dict["Keywords"])

    result_dict = read_file('prompt.txt')

    return render_template("index.html",
                           language=result_dict["Language"],
                           style=result_dict["Output style"],
                           inputs=result_dict["Inputs"],
                           outputs=result_dict["Outputs"],
                           name=result_dict["Function Name"],
                           description=result_dict["Function Description"],
                           keywords=result_dict["Keywords"])
if __name__ == "__main__":
    app.run(port=80)
