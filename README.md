# airflow-starter

Get started with few sample airflow DAG's

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Virtual Machine or EC2 or Mac/Windows machine
Docker installed on VM
```
If trying this on AWS, then use this community AMI: *ami-0055d58addfe009d0* from AWS marketplace.

### Installing

Please follow the steps below in order to have it up and running on your machine.

* make sue git is installed on your EC2/VM

```
sudo yum -y install git

```

* Change directory

```
cd /opt/

```

* Clone the repo


```
sudo git clone https://github.com/ranjay-POC/airflow-starter.git 
```

* Change Permission and change folder


``` 
sudo chmod -R 777 airflow-starter/
cd  airflow-starter/
```

* run the following script to install dependencies


``` 
sudo chmod a+x ./install-dependencies.sh
sudo ./install-dependencies.sh 

```


## Validate it is running
```
sudo docker ps
```

<!-- This is commented out. 
### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
-->