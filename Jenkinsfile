pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id_secret_text')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key_secret_text')
    }
    stages {
        stage('Create Athena Database and Table') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id_secret_text', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key_secret_text', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        // Create Athena Database
                        bat 'aws athena start-query-execution --query-string "CREATE DATABASE my_athena_db;" --result-configuration OutputLocation=s3://athenajenkinstestbucket/'

                        // Create Athena Table with Schema
                        bat 'aws athena start-query-execution --query-string "CREATE EXTERNAL TABLE my_athena_db.salary_data (YearsExperience FLOAT, Salary FLOAT) ROW FORMAT SERDE \'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe\' WITH SERDEPROPERTIES (\'field.delim\' = \',\') STORED AS INPUTFORMAT \'org.apache.hadoop.mapred.TextInputFormat\' OUTPUTFORMAT \'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat\' LOCATION \'s3://athenajenkinstestbucket/Salary_Data.csv\';" --result-configuration OutputLocation=s3://s3://athenajenkinstestbucket/'
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