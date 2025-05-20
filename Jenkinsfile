pipeline {
    agent any
    stages {
        stage('Check OS') {
            steps {
                script {
                    def osName = System.getProperty("os.name")
                    echo "Running on OS: ${osName}"
                }
            }
        }
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/AlexandraMolina22/app-reservas-peluqueria.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\activate && pytest backend/tests'
            }
        }
    }
}