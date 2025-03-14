FROM python:3.12-alpine

WORKDIR /url-shortener

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "app.main"]