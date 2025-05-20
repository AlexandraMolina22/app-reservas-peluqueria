pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/AlexandraMolina22/app-reservas-peluqueria.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh './venv/Scripts/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh './venv/Scripts/activate && pytest backend/tests'
            }
        }
    }
}
