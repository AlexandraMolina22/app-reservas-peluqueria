pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🛠️ Creando entorno virtual e instalando dependencias...'
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Ejecutar pruebas con cobertura') {
            steps {
                echo '🧪 Ejecutando pytest con cobertura...'
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest backend/tests --cov=backend --cov-report=xml --cov-report=term
                '''
            }
        }
    }

    post {
        always {
            echo '📦 Proceso completado.'
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        }
        success {
            echo '✅ Pruebas ejecutadas con éxito.'
        }
        failure {
            echo '❌ Error en las pruebas.'
        }
    }
}
