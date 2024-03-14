# Jenkins Pipeline Generator
Simple command-line tool generates Jenkins pipeline files based on the provided parameters.

![Contributors](https://img.shields.io/github/contributors/srajasimman/jenkins-pipeline-generator?color=dark-green) ![Forks](https://img.shields.io/github/forks/srajasimman/jenkins-pipeline-generator?style=social) ![Stargazers](https://img.shields.io/github/stars/srajasimman/jenkins-pipeline-generator?style=social) ![Issues](https://img.shields.io/github/issues/srajasimman/jenkins-pipeline-generator) ![License](https://img.shields.io/github/license/srajasimman/jenkins-pipeline-generator) 

## Usage
```
usage: jenkins-pipeline-generator.py [-h] -r REPO_URL -b BRANCH -l {java,javascript} -t {maven,gradle,npm}

Generate Jenkins pipeline file

options:
  -h, --help                 show this help message and exit
  -r, --repo-url REPO_URL    Repository URL
  -b, --branch BRANCH        Branch
  -l, --language             Language
  -t, --build-tool           Build tool
```
## Description
This tool creates a Jenkins pipeline file tailored to your project's needs. It automates the process of setting up Jenkins pipelines for Java and JavaScript projects using either Maven or Gradle as the build tool.

## Options
- `-h, --help`: Displays help message and exits.
- `-r, --repo-url REPO_URL`: Specifies the repository URL.
- `-b, --branch BRANCH`: Specifies the branch name.
- `-l, --language {java,javascript}`: Specifies the programming language (either Java or JavaScript).
- `-t, --build-tool {maven,gradle,npm}`: Specifies the build tool (either Maven or Gradle).
- `-d, --deploy {true,false}`: Specifies the deployment step required or not.

## Example
```sh
jenkins-pipeline-generator.py \
  --repo "https://github.com/example/project.git" \
  --branch "main" \
  --language "java" \
  --build-tool "maven" \
  --deploy true
```
This command generates a Jenkins pipeline file for a Java project using Maven as the build tool, based on the repository located at https://github.com/example/project with the branch main.

```groovy
pipeline {
    agent any
    parameters {
        string(name: 'GIT_REPO', defaultValue: 'https://github.com/example/project.git', description: 'Git Repository URL')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Branch to build')
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        githubProjectProperty(
            displayName: '',
            projectUrlStr: '${params.GIT_REPO}'
        )
    }
    def job_name = "${env.JOB_NAME.split('/')[-1]}"
    def commit_hash = "${env.GIT_COMMIT.substring(0, 7)}"
    def build_number = "${env.BUILD_NUMBER}"
    def docker_image = "${job_name}:${commit_hash}-${build_number}"
    stages {
        stage('Checkout') {
            steps {
                script {
                    git (url: "${params.GIT_REPO}", branch: "${params.GIT_BRANCH}")
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    
                    sh 'mvn clean package -DskipTests'
                    artifact 'target/*.jar'
                    
                }
            }
        }
        stage('Create Docker Image') {
            steps {
                script {
                    if (!fileExists('Dockerfile')) {
                        
                        writeFile(file: 'Dockerfile', text: '''
                        FROM openjdk:17-jdk-slim
                        WORKDIR /app
                        COPY target/*.jar app.jar
                        ENTRYPOINT ["java", "-jar", "app.jar"]
                        ''')
                        
                    else {
                        print('Dockerfile already exists')
                    }
                }
            }
        }
        stage('Docker Build') {
            steps {
                script {
                    sh 'docker build -t ${docker_image} .'
                }
            }
        }
        stage('Docker Push') {
            steps {
                script {
                    sh 'docker push ${docker_image}'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh 'kubectl create deployment $job_name --image=${docker_image}'
                    sh 'kubectl expose deployment $job_name --type=ClusterIP --port=8080'
                }
            }
        }
        
    }
}

```

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
