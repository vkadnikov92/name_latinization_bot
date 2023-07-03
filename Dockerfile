FROM python:3.10-slim 
ENV TOKEN=6356805916:AAEX1SfnpjxC3mZNABt69n6dO2DI4qLUR9o
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]