# Foodgram  
This is a site where you can became an author and create your own recipes as well as subscribe to others.  
Choosing your favorite recipes is also avaliable. Moreover, you can form a shopping list and download it.

## Getting Started
*Adapt .env as you need*  
The following commands should be made from
project directory.

#### Launching Docker
 ```
 docker-compose up
 ```
#### First Start
Enter to the container:
```
docker-compose exec web 
```
Make migrations:  
```
python manage.py migrate
```
Collect static and create tags:  
```
python manage.py collectstatic  
python manage.py create_tags
```
Create a superuser:
```
docker-compose exec web python manage.py createsuperuser
```
#### Built with
* [Django](https://www.djangoproject.com/) 
* [PostgreSQl](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Docker compose](https://docs.docker.com/compose/)

#### Authors
* [Alexei Zverev](https://github.com/aleksizverev)
