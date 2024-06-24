pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id_secret_text')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key_secret_text')
    }
    stages {
        stage('Create Glue Database and Table') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id_secret_text', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key_secret_text', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        def stackExists = bat(script: 'aws cloudformation describe-stacks --stack-name my-glue-database-table-stack --region us-east-1', returnStatus: true) == 0
                        if (stackExists) {
                            bat 'aws cloudformation delete-stack --stack-name my-glue-database-table-stack --region us-east-1'
                            bat 'aws cloudformation wait stack-delete-complete --stack-name my-glue-database-table-stack --region us-east-1'
                        }
                        bat 'aws cloudformation create-stack --stack-name my-glue-database-table-stack --template-body file://template.yaml --region us-east-1'
                        bat 'aws cloudformation wait stack-create-complete --stack-name my-glue-database-table-stack --region us-east-1'
                    }
                }
            }
        }
        stage('Run Athena Query') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id_secret_text', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key_secret_text', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    bat 'python athena_iaas.py'
                }
            }
        }
    }
}