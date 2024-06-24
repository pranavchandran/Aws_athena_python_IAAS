pipeline {
    agent any

    stages {
        stage('Create Athena Table') {
            steps {
                bat 'aws cloudformation create-stack --stack-name my-stack --template-body template.yaml --region us-east-1'
                bat 'aws cloudformation wait stack-create-complete --stack-name my-stack'
            }
        }

        stage('Run Athena Query') {
            steps {
                bat 'python athena_iaas.py'
            }
        }
    }
}