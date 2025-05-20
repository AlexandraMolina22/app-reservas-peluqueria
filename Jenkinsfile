pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest backend/tests'
            }
        }
    }
}
