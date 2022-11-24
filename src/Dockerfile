FROM public.ecr.aws/lambda/python:3.9

# Copy code
COPY . ${LAMBDA_TASK_ROOT}/src

# Install the function's dependencies using file requirements.txt
# from our project folder.
RUN  pip3 install -r src/requirements.txt --target "${LAMBDA_TASK_ROOT}"
