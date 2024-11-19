FROM python:3-alpine

WORKDIR /app/polls

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost,127.0.0.1}
ENV TIME_ZONE=${TIME_ZONE}

COPY . .

# Install Dependencies on Docker Container
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./entrypoint.sh

# Open Port
EXPOSE 8000

# Run application
CMD ["./entrypoint.sh"]
