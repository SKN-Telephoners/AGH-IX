FROM zyclonite/zerotier:latest AS zerotier

RUN echo "{\"settings\": {\"portMappingEnabled\": true,\"softwareUpdate\": \"disable\",\"allowManagementFrom\": [\"0.0.0.0/0\"]}}" > /var/lib/zerotier-one/local.conf

RUN apk add --no-cache python3 py3-pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY app.py requirements.txt ./
RUN pip3 install -r requirements.txt

EXPOSE 9993/tcp
EXPOSE 9993/udp
EXPOSE 5000/tcp

RUN chown -R 777 /var/lib/zerotier-one
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
