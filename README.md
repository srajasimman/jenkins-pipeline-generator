# Jenkins Pipeline Generator
This command-line tool generates Jenkins pipeline files based on the provided parameters.

## Usage
```sh
jenkins-pipeline-generator.py [-h] -r REPO_URL -b BRANCH -l {java,javascript} -t {maven,gradle}
```
## Description
This tool creates a Jenkins pipeline file tailored to your project's needs. It automates the process of setting up Jenkins pipelines for Java and JavaScript projects using either Maven or Gradle as the build tool.

## Options
- `-h, --help`: Displays help message and exits.
- `-r REPO_URL, --repo-url REPO_URL`: Specifies the repository URL.
- `-b BRANCH, --branch BRANCH`: Specifies the branch name.
- `-l {java,javascript}, --language {java,javascript}`: Specifies the programming language (either Java or JavaScript).
- `-t {maven,gradle}, --build-tool {maven,gradle}`: Specifies the build tool (either Maven or Gradle).

## Example
```sh
jenkins-pipeline-generator.py -r https://github.com/example/project -b main -l java -t maven
```
This command generates a Jenkins pipeline file for a Java project using Maven as the build tool, based on the repository located at https://github.com/example/project with the branch main.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.