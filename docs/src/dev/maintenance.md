# Maintenance

## Updates

To update the site once deployed, update the repository, then re-enter the screen, take the containers down, and re-build them.

```shell
screen -r
git pull
sudo docker compose down  
sudo docker compose build --no-cache
sudo docker compose up
```

## Deployments

On a deployed version, 
you'll need to do `sudo docker compose up web` or `sudo docker compose up web-dev` as appropriate.
 
If the reverse proxy settings need updating, you'll have to re-copy the settings file:
```shell
sudo cp /var/www/gaia-cob-pmp-dev/deploy/nginx/isolutions.conf /etc/nginx/
sudo systemctl reload nginx
```