pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    tools {
        // Asegúrate de que 'SonarQube Scanner' esté configurado en Jenkins Global Tool Configuration
        // y que el nombre coincida con el que pongas aquí, por ejemplo: "SonarQubeScanner"
        sonarScanner = 'SonarQubeScanner'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🔧 Creando entorno virtual e instalando dependencias...'
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
                echo '🧪 Ejecutando pytest...'
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest backend/tests --junitxml=report.xml
                '''
            }
        }

        stage('Análisis SonarQube') {
            steps {
                echo '📊 Ejecutando análisis con SonarQube...'
                withSonarQubeEnv('SonarQube Local') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=app-reservas-peluqueria \
                          -Dsonar.sources=backend \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.junit.reportPaths=report.xml \
                          -Dsonar.host.url=http://localhost:9000
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '📦 Proceso completado.'
        }
        success {
            echo '✅ Pruebas ejecutadas con éxito.'
        }
        failure {
            echo '❌ Error en las pruebas.'
        }
    }
}
