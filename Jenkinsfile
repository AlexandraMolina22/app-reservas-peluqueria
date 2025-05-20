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
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install --upgrade pip'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Prepare Reports Directory') {
            steps {
                bat 'if not exist reports mkdir reports'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\activate && pytest backend/tests --junitxml=reports/results.xml'
            }
        }
    }

    post {
        always {
            junit 'reports/results.xml'
        }
    }
}
