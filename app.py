from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    # if request method is not POST
    if request.method != 'POST':
        return index()
    else:
        repo_url = request.form['repo_url']
        branch = request.form['branch']
        language = request.form['language']
        build_tool = request.form['build_tool']
        deploy = request.form.get('deploy') == 'on'
        port = request.form.get('port')

        # Set up Jinja environment
        pipelines_dir = os.path.join(os.path.dirname(__file__), 'pipelines')
        env = Environment(loader=FileSystemLoader(pipelines_dir))

        # Load Jinja template
        template = env.get_template('jenkins_pipeline.j2')

        pipeline_script = template.render(
            repo_url=repo_url,
            branch=branch,
            language=language,
            build_tool=build_tool,
            deploy=deploy,
            port=port
        )

        return render_template('generated.html', pipeline_script=pipeline_script)

if __name__ == '__main__':
    app.run()