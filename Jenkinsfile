pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Create Athena Table') {
            steps {
                // AWS credentials are already set in the environment
                bat 'aws cloudformation create-stack --stack-name my-stack --template-body file://template.yaml --region us-east-1'
                bat 'aws cloudformation wait stack-create-complete --stack-name my-stack --region us-east-1'
            }
        }
        stage('Run Athena Query') {
            steps {
                // AWS credentials are already set in the environment
                bat 'python athena_iaas.py'
            }
        }
    }
}