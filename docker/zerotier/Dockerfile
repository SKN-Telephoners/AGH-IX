FROM zyclonite/zerotier:latest AS zerotier

RUN echo "{\"settings\": {\"portMappingEnabled\": true,\"softwareUpdate\": \"disable\",\"allowManagementFrom\": [\"0.0.0.0/0\"]}}" > /var/lib/zerotier-one/local.conf
RUN apk add --no-cache python3 py3-pip openrc openvswitch iproute2
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
COPY app.py namespace.sh .env setup_openvswitch.py zerotier_restartd.py ./
RUN chmod +x app.py namespace.sh setup_openvswitch.py namespace.sh zerotier_restartd.py
EXPOSE 9993/tcp 5000/tcp 9993/udp
RUN chown -R 777 /var/lib/zerotier-one
CMD [ "python3", "app.py" ]