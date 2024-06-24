pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_REGION = 'us-east-1'  // Specify your AWS region here
    }
    stages {
        stage('Create Athena Database and Table') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        // Create Athena Database
                        bat 'aws athena start-query-execution --query-string "CREATE DATABASE IF NOT EXISTS my_athena_db;" --result-configuration OutputLocation=s3://athenajenkinstestbucket/ --region us-east-1'

                        // Create Athena Table with Schema
                        bat 'aws athena start-query-execution --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS my_athena_db.salary_data (YearsExperience FLOAT, Salary FLOAT) ROW FORMAT SERDE \'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe\' WITH SERDEPROPERTIES (\'field.delim\' = \',\') STORED AS INPUTFORMAT \'org.apache.hadoop.mapred.TextInputFormat\' OUTPUTFORMAT \'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat\' LOCATION \'s3://athenajenkinstestbucket/Salary_Data.csv\';" --result-configuration OutputLocation=s3://athenajenkinstestbucket/ --region us-east-1'
                    }
                }
            }
        }
        stage('Verify Table Exists') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        // Verify that the table exists
                        def queryExecutionResult = bat(script: 'aws athena start-query-execution --query-string "SHOW TABLES IN my_athena_db;" --result-configuration OutputLocation=s3://athenajenkinstestbucket/ --region us-east-1', returnStdout: true).trim()
                        echo "queryExecutionResult: ${queryExecutionResult}"
                        def queryExecutionId = queryExecutionResult.split('"QueryExecutionId": "')[1].split('"')[0]
                        echo "QueryExecutionId: ${queryExecutionId}"
                        
                        // Get query results
                        bat "aws athena get-query-results --query-execution-id ${queryExecutionId} --region us-east-1 > query_result.json"
                        def queryOutput = readFile('query_result.json')
                        echo "Query Output: ${queryOutput}"
                        
                        // Check if the table exists in the output
                        if (!queryOutput.contains('salary_data')) {
                            error "Table 'salary_data' does not exist in database 'my_athena_db'."
                        }
                    }
                }
            }
        }
        stage('Run Athena Query') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                                 string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        // Run Athena Query and save the output as CSV
                        def queryExecutionResult = bat(script: 'aws athena start-query-execution --query-string "SELECT * FROM my_athena_db.salary_data;" --result-configuration OutputLocation=s3://athenajenkinstestbucket/output/ --region us-east-1', returnStdout: true).trim()
                        echo "queryExecutionResult: ${queryExecutionResult}"
                        def queryExecutionId = queryExecutionResult.split('"QueryExecutionId": "')[1].split('"')[0]
                        echo "QueryExecutionId: ${queryExecutionId}"
                        
                        // Check query execution status
                        def queryExecutionStatus = bat(script: "aws athena get-query-execution --query-execution-id ${queryExecutionId} --region us-east-1", returnStdout: true).trim()
                        echo "queryExecutionStatus: ${queryExecutionStatus}"
                        
                        // Parse query execution status
                        if (queryExecutionStatus.contains('"State": "FAILED"')) {
                            error "Athena query execution failed. Please check the query and try again."
                        }
                        
                        // Get query results
                        bat "aws athena get-query-results --query-execution-id ${queryExecutionId} --region us-east-1 > query_result.json"
                        def queryOutput = readFile('query_result.json')
                        echo "Query Output: ${queryOutput}"
                    }
                }
            }
        }
    }
}