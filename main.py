import os
from string import Template

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    os.system("echo > ./static/data.json")

    if request.method == 'POST':
        query = request.form['query']
        helper(query)
        return render_template('index.html', results=True)

    return render_template('index.html')
    
def helper(input):
    query = input.replace(' ', '+')
    request = f'https://search.scielo.org/?lang=en&&q=$query'

    bash = Template("curl -L 'https://search.scielo.org/?lang=en&&q=$query' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' | pup ':parent-of(strong.title) json{}' | yq -o json '.[] | {\"title\": .children.[].text, \"link\": .href}' | cat >> ./static/aux.json")

    os.system("echo '[' > ./static/aux.json")

    os.system(bash.safe_substitute(query=query))

    os.system("echo ']' >> ./static/aux.json")

    os.system("sed -i -e 's/amp;//g' ./static/aux.json")

    os.system("sed -i -e 's/}/},/g' ./static/aux.json")

    os.system("cat ./static/aux.json | yq -o json | cat > ./static/data.json")

    os.system("cat ./static/data.json")


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
