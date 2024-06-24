pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/pranavchandran/Aws_athena_python_IAAS'
            }
        }

        stage('Create Athena Table') {
            steps {
                bat 'aws cloudformation create-stack --stack-name my-stack --template-body template.yaml'
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