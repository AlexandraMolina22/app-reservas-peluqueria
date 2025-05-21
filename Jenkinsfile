pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        SONAR_HOST_URL = 'http://host.docker.internal:9000'
        SONAR_TOKEN = credentials('sonar-token')  // Aquí usas credencial almacenada en Jenkins
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
                      -Dsonar.projectKey=mi_proyecto \
                      -Dsonar.sources=backend \
                      -Dsonar.host.url=$SONAR_HOST_URL \
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
