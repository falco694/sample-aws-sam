STACK_NAME=sample-aws-sam

ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text`
FUNCTIONNAME=DefaultFunction
BUCKET_NAME=$(STACK_NAME)-$(ACCOUNT_ID)

init:
	pipenv install --dev --python 3.7

bucket:
	aws s3 mb s3://$(BUCKET_NAME)
	aws s3api put-bucket-lifecycle-configuration \
		--bucket $(BUCKET_NAME) \
		--lifecycle-configuration file://lifecycle.json

validate:
	sam validate --template template.yaml

build:
	pipenv lock -r > src/requirements.txt
	sed -i -e "s@https://pypi.org/simple@https://pypi.org/simple/@g" src/requirements.txt
	sam build

debug: build
	sam local invoke $(FUNCTIONNAME) --event event.json

package: build
	sam package \
		--output-template-file packaged.yaml \
		--s3-bucket $(BUCKET_NAME)

deploy: package
	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM

describe:
	aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--output table

logs:
	sam logs -n DefaultFunction --stack-name $(STACK_NAME) --tail

clean:
	-pipenv --rm
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	aws s3 rb s3://$(BUCKET_NAME) --force
