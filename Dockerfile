FROM python:3.12

WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install uv

# Export dependencies and install them
RUN uv export --format requirements-txt > requirements.txt
RUN uv pip install --system --no-cache --upgrade -r requirements.txt

# Copy the rest of the project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
