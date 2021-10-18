sam package --template-file template.yaml --output-template-file package.yaml --s3-bucket ph-platform --s3-prefix 2020-11-11/cicd/PROJECT_NAME/samtem
sam deploy --template-file package.yaml --stack-name lmd-PROJECT_NAME-deploy-v2 --capabilities CAPABILITY_IAM
