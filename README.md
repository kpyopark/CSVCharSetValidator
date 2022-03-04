# CSVCharSetValidator

해당 프로젝트는, CSV 파일안에 있는 UTF-8 Character Set이외의 Invalid Character Set을 제거하고, 이 결과를 Target쪽에 복사해주는 Lambda Function입니다. 

기본적으로 동일 Bucket안에 /refined라는 타겟 디렉토리를 생성하고, 여기에 원본 자료를 복사합니다. 

복사 도중에 Invalid Character가 나오는 경우, 가능한 Invalid Character만 제거하고 지속적으로 Copy를 수행합니다. 
하지만, Invalid Character Skipping 역시, 오류가 발생할 수 있기 때문에, 해당 Line전체를 Drop하는 기능도 추가로 구현해야 합니다. (TODO #1)

추가적으로, 문제가 많이 발생하는 Date Format에 대한 부분도 확인하고 진행하는 부분이 필요합니다. (TODO #2)

현재, Stream Read/Write를 통하여 메모리 사용율과 Temporary File 사용을 최소화 하였지만 테스트를 진행하지 않았습니다. (TODO #3)

## Prerequiste

먼저, IAM Permission을 추가합니다. 

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucketMultipartUploads",
                "s3:AbortMultipartUpload",
                "s3:PutObjectVersionAcl",
                "s3:DeleteObject",
                "s3:PutObjectAcl",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::<<bucket_name>>",
                "arn:aws:s3:::<<bucket_name>>/*"
            ]
        }
    ]
}

```

이후, Lambda Function을 생성하고, S3 Trigger 조건을 생성해 주십시요. (All creation event)

## installation

이 부분은, AWS 공식문서를 참조하여 만들었습니다. 

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

1. git clone https://github.com/kpyopark/CSVCharSetValidator.git
2. cd CSVCharSetValidator
3. pip install --target ./package smart-open
4. cd package
5. zip -r ../my-deployment-package.zip .
6. cd ..
7. zip -g ./my-deployment-package.zip lambda_function.py
8. aws lambda update-function-code --function-name <<위에서만든Function Name> --zip-file fileb://my-deployment-package.zip


## Test

해당 test_resources 폴더로 들어가서 utf-8 하고 utf-16be 가 복합적으로 들어가 있는 파일이 있습니다. (testdoc.csv)

AWS s3 cli 를 이용하여 Trigger가 설정되어 있는 bucket에 파일을 복사합니다. 

이후 해당 bucket 안에 있는 /refined 폴더에 validated된 자료가 생성됩니다. 

