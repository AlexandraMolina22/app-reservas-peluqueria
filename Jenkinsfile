pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        SONAR_TOKEN = credentials('sonar-token')  // usa el ID que diste en Jenkins
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo 'Creando entorno virtual e instalando dependencias...'
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                echo 'Ejecutando pytest...'
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest backend/tests
                '''
            }
        }

        stage('Análisis SonarQube') {
            steps {
                echo 'Ejecutando análisis SonarQube...'
                sh '''
                    . $VENV_DIR/bin/activate
                    sonar-scanner \
                    -Dsonar.projectKey=app-peluqueria \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=$SONAR_TOKEN
                '''
            }
        }
    }

    post {
        always {
            echo '📦 Proceso completado.'
        }
        success {
            echo '✅ Pruebas y análisis ejecutados con éxito.'
        }
        failure {
            echo '❌ Error en las pruebas o análisis.'
        }
    }
}
