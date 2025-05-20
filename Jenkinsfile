pipeline {
    agent any

    stages {
        stage('Clonar código') {
            steps {
                echo 'Clonando código desde GitHub...'
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                echo 'Instalando dependencias con pip...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                echo 'Ejecutando pruebas unitarias con pytest...'
                sh 'pytest --junitxml=results.xml'
            }
        }
    }

    post {
        always {
            junit 'results.xml'
        }
    }
}
