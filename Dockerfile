# Step 1: Use the official AWS Lambda image for Python
FROM public.ecr.aws/lambda/python:3.10

# Step 2: Copy only the requirements first (optimizes Docker caching)
COPY app/requirements.txt ${LAMBDA_TASK_ROOT}

# Step 3: Install dependencies
RUN pip install -r requirements.txt

# Step 4: Copy code into the task root
COPY app/monitor.py ${LAMBDA_TASK_ROOT}

# Step 5: The command that AWS Lambda calls
CMD [ "monitor.lambda_handler" ]