git clone https://github.com/yoavfreund/Public-DSC291.git
sudo pip install psutil

# run the following if the instance has an SSD that needs to be formatted and mounted.

lsblk
sudo mkfs.ext4 -E nodiscard -m0 /dev/nvme0n1   #format
sudo mkdir /home/ubuntu/spda                   #make root for mounting
sudo mount -o discard /dev/nvme0n1 /home/ubuntu/spda # mount
ln -s /home/ubuntu/spda scratch                #create local link
sudo chmod a+rwx scratch                       # make read/write-able
lsblk
