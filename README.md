
![Logo](https://raw.githubusercontent.com/ddominet/METIS-cluster/master/85414462_pazzddezd_logo.png)


# AGH-IX

Project AGH-IX goal is to create first in Poland automatic virtual internet exchange point. It will allow it's users to establish BGP peering with themselves directly or via Route-Server. Operations of this IX will be completely automatic, with little to no interference from NOC operator.


## Authors

- [@dobrowolski_dominik](https://github.com/ddominet)
- [@wodecki_piotr](https://github.com/PiotrWodecki)


## Roadmap

- Testing arouteserver, checking it with bird and figuring out whether it can be easily implemented as a backend to check if asns, ip addresses are correct (RPKI, ROA), and if configuration is easily generated

- Creating backend integrated with arouteserver, and the ability to create and check status of vpn sessions (ping probes ?), Status of both BGP sessions and VPN sessions (bridged together )to be accessible from the frontend
- Frontend (Flask, Django, FastAPI)??? T.B.D 

- Nice clean website, integrated with a db with the ability to register and login for the IX users. The ability to enter resources ASN, IPs, ability to select session type IPv4, IPV6, IPv4+IPV6. ability to select VPN type (zerotier, gretap, vxlan) If everything checks out, establish and show parameters nessesary to establish sessiom, tunnel for the client side.

- Admin Pannel to see all users, kick them if nessesary.

- LookingGlass?

- Checking if members adhere to security rules. Netflow? PacketCapture? Detecting port scans?

- Noitify users by mail if their session is down, if they violate rules 
## Support

For support, email dobrowolski.domino@gmail.com or pwodecki@student.agh.edu.pl.


## FAQ

#### Is it ready?

NO

#### Why am i doing this?

I don't know


## Contributing

Contributions are always welcome!

Contact us to get started.

Please adhere to this project's `code of conduct`.

