lsblk
sudo mkfs.ext4 -E nodiscard -m0 /dev/nvme0n1   #format
sudo mkdir /home/ubuntu/spda                   #make root for mounting
sudo mount -o discard /dev/nvme0n1 /home/ubuntu/spda # mount
lsblk
