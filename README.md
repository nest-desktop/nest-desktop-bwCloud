## Deploy image on bwCloud


### Preparation

Build apptainer container for Ansible and packer
```
sudo apptainer build bwCloud-packer.sif ./apptainer/bwCloud-packer.def
```

Modify image_name, source_image and networks in nest-desktop.json

Generate user with password
```
htpasswd -c ./ansible-roles/setup-nest-desktop/templates/apache2/.htpasswd <user>
```

### Build an image

Start apptainer for ansible and packer
```
apptainer shell bwCloud-packer.sif
```

Download OpenStack RC File (top right of bwCloud dashboard)
```
source *-openrc.sh
 -> enter password
```

Change configuration file in ``nest-desktop.json``.
Values for ``source_image`` and ``networks`` are taken from bwCloud dashboard.

Start build an image for NEST Desktop
```
packer build nest-desktop.json
```
