FROM python:3-slim

WORKDIR /kolulu

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV prefix="!gbf "
ENV sql='002_v1'
ENV data="https://raw.githubusercontent.com/nnguyen259/KoluluData/master"

CMD [ "python", "./bot.py" ]