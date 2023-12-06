pipeline {
    agent any
    stages {
        stage("Setup python virtual environment"){
            steps{
                sh '''
                chmod +x crestlearn/env-setup.sh
                ./crestlearn/env-setup.sh
                '''
            }
        }
        stage("Setup Gunicorn"){
            steps {
                sh '''
                chmod +x crestlearn/gunicorn.sh
                ./crestlearn/gunicorn.sh
                '''
            }
        }
        stage("Setup Nginx"){
            steps{
                sh '''
                chmod +x crestlearn/nginx.sh
                ./crestlearn/nginx.sh
                '''
            }
        }
        stage("Email Development Team"){
            steps{
                sh'''
                    recepients="louis.eyoma@crestagile.com,mary.okafor@crestagile.com,paul.effiong@crestagile.com,sage@crestagile.com,samson.otobong@crestagile.com"
                    echo "Crestlearn Backend Deployment" | mail -s "Crestlearn Backend deployment successful" $recepients
                '''
            }
        }
    }
}