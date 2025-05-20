pipeline {
    agent any

    stages {
        stage('Clonar repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/AlexandraMolina22/app-reservas-peluqueria.git'
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/Scripts/activate && pip install -r requirements.txt'
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '. venv/Scripts/activate && pytest backend/tests'
            }
        }
    }
}
