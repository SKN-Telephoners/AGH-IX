FROM zyclonite/zerotier:latest AS zerotier

RUN echo "{\"settings\": {\"portMappingEnabled\": true,\"softwareUpdate\": \"disable\",\"allowManagementFrom\": [\"0.0.0.0/0\"]}}" > /var/lib/zerotier-one/local.conf
RUN apk add --no-cache python3 py3-pip && apk add --no-cache iproute2 && apk add --no-cache openrc && apk add --no-cache openvswitch
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
COPY ./namespace.sh /app
COPY ./.env /app
RUN chmod +x namespace.sh
COPY ./zerotier_restartd.py /app
RUN chmod +x zerotier_restartd.py
COPY ./setup_openvswitch.py /app
RUN chmod +x setup_openvswitch.py
EXPOSE 9993/tcp
EXPOSE 9993/udp
EXPOSE 5000/tcp
RUN chown -R 777 /var/lib/zerotier-one
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]