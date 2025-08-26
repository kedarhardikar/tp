pipeline {
    agent any
    environment {
        APP_DIR = '/var/www/'
        VIRTUAL_ENV = 'venv'
        SERVICE_NAME = '.service'
        PYTHON = "${APP_DIR}/venv/bin/python3"
        STREAM = "${APP_DIR}/venv/bin/streamlit"
    }
    stages {
        stage('Checkout') {
            steps {
                dir(APP_DIR) {
                    git url: 'https://github.com/kedarhardikar/tp',
                        credentialsId: 'GITID'
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    sh '''
                        #!/bin/bash
                        cd ${APP_DIR}
                        if [ ! -d "${VIRTUAL_ENV}" ]; then
                            python -m venv ${VIRTUAL_ENV}
                        fi
                        source ${VIRTUAL_ENV}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        deactivate
                    '''
                }
            }
        }
        stage('Find Free Port') {
            steps {
                script {
                    def freePort = sh(script: '''
                        for port in $(seq 8501 8600); do
                            (echo >/dev/tcp/127.0.0.1/$port) &>/dev/null || { echo $port; exit 0; }
                        done
                        exit 1
                    ''', returnStdout: true).trim()
                    echo "Found free port: ${freePort}"
                    env.APP_PORT = freePort
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    sh '''
                        SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
                        sudo bash -c "cat > $SERVICE_FILE" << EOF
                        [Unit]
                        Description=Streamlit 
                        After=network.target

                        [Service]
                        User=ubuntu
                        Group=ubuntu
                        WorkingDirectory=${APP_DIR}
                        ExecStart=${STREAM} run app.py --server.port=${APP_PORT} --server.headless true
                        Restart=always
                        RestartSec=5

                        [Install]
                        WantedBy=multi-user.target
                        EOF
                        sudo systemctl daemon-reload
                        sudo systemctl enable ${SERVICE_NAME}
                        sudo systemctl restart ${SERVICE_NAME}
                    '''
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo "Deployment succeeded on port ${env.APP_PORT}"
        }
        failure {
            echo "Deployment failed"
        }
    }
}