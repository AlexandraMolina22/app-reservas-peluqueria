pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        SONARQUBE_ENV = 'SonarQube' // Nombre de la instalación SonarQube en Jenkins
    }

    stages {

        stage('Checkout') {
            steps {
                echo '🔄 Clonando el repositorio...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/AlexandraMolina22/app-reservas-peluqueria.git']],
                    extensions: [[$class: 'CloneOption', shallow: false]] // ¡Clave!
                ])
            }
        }

        stage('Preparar entorno') {
            steps {
                echo '📦 Creando entorno virtual e instalando dependencias...'
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
                echo '✅ Ejecutando pruebas con Pytest...'
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest backend/tests --junitxml=report.xml --cov=backend --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo '📊 Ejecutando análisis con SonarQube...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        . $VENV_DIR/bin/activate
                        sonar-scanner \
                            -Dsonar.projectKey=app-reservas-peluqueria \
                            -Dsonar.sources=backend \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '🔁 Proceso completo.'
        }
        success {
            echo '✅ Pipeline ejecutado con éxito.'
        }
        failure {
            echo '❌ Falló la ejecución del pipeline.'
        }
    }
}
