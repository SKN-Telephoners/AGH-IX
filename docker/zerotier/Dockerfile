FROM zyclonite/zerotier:latest AS zerotier

RUN echo "{\"settings\": {\"portMappingEnabled\": true,\"softwareUpdate\": \"disable\",\"allowManagementFrom\": [\"0.0.0.0/0\"]}}" > /var/lib/zerotier-one/local.conf

EXPOSE 9993/tcp
EXPOSE 9993/udp

RUN chown -R 777 /var/lib/zerotier-one
ENTRYPOINT ["zerotier-one"]