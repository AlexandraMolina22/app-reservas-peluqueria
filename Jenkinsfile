pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        VENV_PATH = '.venv'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🛠️ Creando entorno virtual e instalando dependencias...'
                sh """
                   python3 -m venv $VENV_PATH
                   . $VENV_PATH/bin/activate
                   pip install --upgrade pip
                   pip install -r requirements.txt
                """
            }
        }
        
        stage('Ejecutar pruebas') {
            steps {
                echo '🚀 Ejecutando pruebas con pytest...'
                sh """
                   . $VENV_PATH/bin/activate
                   pytest --maxfail=1 --disable-warnings -q
                """
            }
        }
        
        stage('Analizar con SonarQube') {
            steps {
                echo '🔎 Analizando código con SonarQube...'
                // Aquí agregarías el comando sonar-scanner
                // sh 'sonar-scanner'
            }
        }
    }
    
    post {
        always {
            echo '🏁 Pipeline terminado.'
            // Aquí podrías agregar limpieza, notificaciones, etc.
        }
        failure {
            echo '❌ Hubo un error en el pipeline.'
        }
    }
}
