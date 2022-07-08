FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8501
RUN mkdir ~/.streamlit
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["azureStreamlit.py"]