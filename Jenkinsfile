pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        SONAR_SCANNER_HOME = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
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

        stage('Análisis SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        $SONAR_SCANNER_HOME/bin/sonar-scanner
                    '''
                }
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
