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
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest backend/tests
                '''
            }
        }
    }
}
