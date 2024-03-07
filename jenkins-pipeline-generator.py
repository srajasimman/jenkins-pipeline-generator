import argparse
from jinja2 import Environment, FileSystemLoader
import os

def generate_build_pipeline(repo_url, branch, language, build_tool, deploy=False):
    # Set up Jinja environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load Jinja template
    template = env.get_template('jenkins_pipeline.j2')

    # Render template with provided inputs
    pipeline_script = template.render(
        repo_url=repo_url,
        branch=branch,
        language=language,
        build_tool=build_tool,
        deploy=deploy
    )

    return pipeline_script

def main():
    options = {
        'languages': ['java', 'javascript', 'python'],
        'build_tools': ['maven', 'gradle', 'npm', 'pip'],
    }

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate Jenkins pipeline file')
    parser.add_argument('-r', '--repo-url', type=str, help='Repository URL', dest='repo_url', required=True)
    parser.add_argument('-b', '--branch', type=str, help='Branch', dest='branch')
    parser.add_argument('-l', '--language', type=str, help='Language', dest='language', required=True, choices=options['languages'])
    parser.add_argument('-t', '--build-tool', type=str, help='Build tool', dest='build_tool', required=True, choices=options['build_tools'])
    parser.add_argument('-d', '--deploy', type=bool, help='Deploy', dest='deploy', default=False)
    
    args = parser.parse_args()

    # if args.language is 'java' and args.build_tool is not 'maven' or args.build_tool or not 'gradle'
    if args.language == 'java' and args.build_tool != 'maven' and args.build_tool != 'gradle':
        parser.error( "\033[91m" + args.build_tool + '\033[0m is a Invalid build tool for Java language')
    
    if args.language == 'javascript' and args.build_tool != 'npm':
        parser.error( "\033[91m" + args.build_tool + '\033[0m is a Invalid build tool for Javascript language')
    
    if args.language == 'python' and args.build_tool != 'pip':
        parser.error( "\033[91m" + args.build_tool + '\033[0m is a Invalid build tool for Python language')

    # Generate Jenkins pipeline script
    pipeline_script = generate_build_pipeline(
        args.repo_url,
        args.branch,
        args.language,
        args.build_tool,
        args.deploy
    )

    # Print the generated pipeline script
    print(pipeline_script)

if __name__ == "__main__":
    main()