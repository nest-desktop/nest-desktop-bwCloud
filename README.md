## Deploy image on bwCloud


### Preparation

Build singularity container for Ansible and packer
```
sudo singularity build bwCloud-packer.sif ./singularity/bwCloud-packer.def
```

Modify image_name, source_image and networks in nest-desktop.json

Generate user with password
```
htpasswd -c ./ansible-roles/setup-nest-desktop/templates/apache2/.htpasswd <user>
```

### Build an image

Start singularity container for ansible and packer
```
singularity shell bwCloud-packer.sif
```

Download OpenStack RC File (top right of bwCloud dashboard)
```
source Project_<username>-openrc.sh
 -> enter password
```

Change configuration file in ``nest-desktop.json``.
``source_image`` and ``networks`` are taken from bwCloud dashboard.

Start build an image for NEST Desktop
```
packer build nest-desktop.json
```
