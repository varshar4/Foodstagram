# Description

This folder serves the purpose of containing all screenshot files from our AWS Instance configuration and explanation of how we deployed it!

## Screenshots:

***Instance Summary***
![Instance Summary](https://user-images.githubusercontent.com/63990614/130074561-d60a879b-c0e5-4289-958b-4cd18ad7dd36.jpg)

***Instance Details***
![Instance Details](https://user-images.githubusercontent.com/63990614/130074577-f3bdff45-e0f4-4191-a602-b350a80c90e6.jpg)

***Host and Placement Group***
![Host and Placement Group](https://user-images.githubusercontent.com/63990614/130074579-ae5904a7-d274-47aa-86ac-3b94657ef114.jpg)

***Security***
![Security Details](https://user-images.githubusercontent.com/63990614/130074582-bc73714e-e434-4403-ae11-117e171ba1f9.jpg)

***Networking Details***
![Networking Details](https://user-images.githubusercontent.com/63990614/130074584-c3dc42fb-a73a-44ab-bc75-04989e036d0b.jpg)

***Storage***
![Storage](https://user-images.githubusercontent.com/63990614/130074588-97d83905-c0af-42ff-83c4-070c4e0dccf1.jpg)

***Tags***
![Tags](https://user-images.githubusercontent.com/63990614/130074590-04532786-f349-41d8-91c0-6176decd3046.jpg)


## Explanation of how we deployed the AWS Instance:

The configuration details for our AWS EC2 instance are shown in the screenshots above, but here are the steps for creating an instance with our configurations: 
1. Press the "Launch Instances" button on the AWS EC2 console. You should choose a CentOS Stream 8 x86_64 AMI. As we deployed in the us-east-2 region, we chose the corresponding Community AMI `ami-0d97ef13c06b05a19`. 
2. After selecting an AMI, you have to select an instance type. Choose t2.small.
3. The default settings should be correct for Configuring Instance Details. Storage size should be set at 10 GiB. 
4. As shown in the screenshot, we tagged our instance with a key-value pair of `Name: foodstagram`. This is not a required configuration for the instance to work, but it is good to have a clear `Name` tag so you know what each instance is for. 
5. For the security group, choose the type "All traffic" and the source as `0.0.0.0/0`. Adding a description may be helpful but is not necessary. 
6. Review your instance settings to ensure they are correct, and then go ahead and launch the instance. 

For deployment of the site, we use our Deploy action. However, in order for this to work, some setup is required on the AWS instance. SSH into the instance and do the following: 
1. Use the command `sudo dnf install git` to install git. 
2. Run the following commands to install Docker: 

        $ curl -sSL https://get.docker.com/ | sudo sh
        $ sudo systemctl start docker
        $ sudo systemctl enable docker
        $ sudo systemctl enable containerd
        $ sudo groupadd docker
        $ sudo usermod -aG docker $USER

3. Use `exit` to exit the instance. SSH into the instance again, and then install Docker-Compose with the following commands: 

        $ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        $ sudo chmod +x /usr/local/bin/docker-compose

4. Run the command `git clone <Github repository HTTPS link>` to create a copy of the repository on your instance. 

Note: in order for the Deploy action to work, make sure your Github repository secrets (accessible in the 'Settings' tab) are updated with the correct values.

Our site uses an Nginx-Certbot container with Let's Encrypt certificates. For this, you must have Nginx installed on the instance (`sudo dnf install nginx`). In order to install Let's Encrypt certificates, follow the instructions [here](https://certbot.eff.org/lets-encrypt/centosrhel8-nginx) (for installing snapd, make sure you are following the instructions for CentOS 8 specifically), and replace the certificate files in `user_conf.d/nginx_conf.conf` with the files created by Certbot on your instance. Make sure your domain is linked to your AWS EC2 instance's public IP address. 


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
