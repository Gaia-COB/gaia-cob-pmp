# Deployment

To deploy this app to a Red Hat VM using `docker compose`:

1. Install the prerequisites listed in `requirements_yum.txt` on the VM. 
   * This may involve adding the Docker repositories to the VM [as per the Docker docs](https://docs.docker.com/compose/install/linux/). 

2. **Set up the repositories**
   * Create a new directory: `/var/www/`, and `cd` into it.
   * Clone the repositories to the directory:
     ```shell
     sudo git https://github.com/Gaia-COB/gaia-cob-pmp
     sudo git clone -b dev https://github.com/Gaia-COB/gaia-cob-pmp gaia-cob-pmp-dev
     ```
   
4. **Set up the permissions**

   * Create a new user group, `gaia-staff`
     ```shell
     sudo groupadd gaia-staff 
     ```
         
   * Add the `nginx` user to that group.
     ```shell
     sudo usermod -a -G gaia-staff nginx
     ```

   * Assign the directories to that group with read and write permission.
     ```shell
     sudo chgrp -R gaia-staff /var/www/gaia-cob-pmp*
     sudo chmod -R g+rwx /var/www/gaia-cob-pmp*
     ```

   * Add the other project staff to the `gaia-staff` group.

5. **Set up the configuration files**

   * Copy the `.env` files for both:
     ```shell
     cp /var/www/gaia-cob-pmp/.env.default /var/www/gaia-cob-pmp/.env
     cp /var/www/gaia-cob-pmp-dev/.env.default /var/www/gaia-cob-pmp-dev/.env 
     ```
     
   * Fill in the `.env` files as [./env-files.html]. Make sure to set the `URL` for the `dev` environment file!

6. Copy the reverse-proxy configuration, and restart it.

   ```shell
   sudo cp /var/www/gaia-cob-pmp-dev/deploy/isolutions.conf /etc/nginx/sites-available/.
   sudo systemctl reload nginx
   ```    
   * You *may* have to edit this, if the SSL certificates are in a different location than I assumed.

7. **Start the servers**

   * Start the production server in a screen session:
     ```shell
     cd /var/www/gaia-cob-pmp
     screen
     sudo docker compose up web
     [ctrl-a, ctrl-d] 
     ```
     
   * Enter the container, and import the fixtures:
     ```shell
     sudo docker exec -it gaia-cob-pmp-web /bin/bash
     uv run manage.py loaddata app/fixtures/*.json
     exit
     ```
     
   * Start the development server in a screen session. 
     The command is *slightly* different, as it uses a different port:
     ```shell
     cd /var/www/gaia-cob-pmp-dev
     screen
     sudo docker compose up web-dev
     [ctrl-a, ctrl-d]
     ```
     
   * Enter the development container, and import the fixtures:
     ```shell
     sudo docker exec -it gaia-cob-pmp-web-dev /bin/bash
     uv run manage.py loaddata app/fixtures/*.json
     exit
     ```
