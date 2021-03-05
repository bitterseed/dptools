import os
import random
import string
from time import sleep

# clear the screen
print("\n"*100)

# small Space
def space(lines):
        print("\n"*lines)

# password generator
def passwd():
    length = 60
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    print(password)

# Confirmation method
def confirm(message):
        while True:
                space(1)
                print(message)
                space(1)
                userInput = input("Type 'yes' to continue: ")
                if userInput == "YES" or userInput == "yes":
                        space(100)
                        break




# Change root password
confirm("Let's change the 'root' password to something more secure...ready?")
print("Here is a strong password for user 'root' - paste it in below and don't forget to save it securely!:")
space(1)
passwd()
space(1)
os.system("passwd root")
confirm("Have you backed up your password securely?")

# create dash user
space(100)
print("Great, let's set up a new user account called 'dash':")
space(1)
print("Here is a strong password for you to paste in as you did before - don't forget to save it securely!:")
space(1)
passwd()
space(1)
os.system("adduser dash")
os.system("usermod -aG sudo dash")
space(1)
confirm("Have you backed up your new password?")

# run updates
time = 10
space(100)
print(f"We're going to do some system updates in {time} seconds:")
space(1)
while time > 0:
        print(time)
        sleep(1)
        time += -1

os.system("apt update && apt upgrade -y && apt autoremove -y")
sleep(5)

# add cron job to keep the system up to date
space(100)
print("Let's add some cron job to keep the system up to date and reboot the system once a week")
sleep(5)
space(1)
os.system("(crontab -l ; echo '0 0 * * */3 sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y')| crontab -")
os.system("(crontab -l ; echo '0 0 * * */7 sudo reboot')| crontab -")

# firewall
space(100)
print("Let's open some ports and enable the firewall")
space(1)
sleep(5)
os.system("ufw allow ssh/tcp && ufw limit ssh/tcp && ufw allow 19999/tcp && ufw allow 26656/tcp")
os.system("ufw allow 3000/tcp && ufw allow 3010/tcp & ufw logging on && ufw enable")
sleep(2)


# set up swap space
space(100)
print("Let's set up some Swap space")
space(1)
sleep(5)
os.system("sudo swapoff -a")
os.system("rm /var/swapfile")
os.system("fallocate -l 4G /var/swapfile")
os.system("chmod 600 /var/swapfile")
os.system("mkswap /var/swapfile")
os.system("swapon -a")
if os.system("grep '^/var/swapfile.none.swap.sw.0.0\' /etc/fstab"):
        os.system("echo '/var/swapfile\tnone\tswap\tsw\t0\t0\' >>/etc/fstab")
sleep(2)

# install fail2ban and enable the service
space(100)
print("Let's install 'fail2ban' and enable the service")
space(1)
sleep(5)
os.system("apt install fail2ban -y")

os.system("rm /etc/fail2ban/jail.local")
my_file = open("/etc/fail2ban/jail.local","w+")
my_file.write("[sshd]\nenabled = true\nport = 22\nfilter = sshd\nlogpath = /var/log/auth.log\nmaxretry = 3")

os.system("systemctl restart fail2ban")
os.system("systemctl enable fail2ban")
sleep(2)

# Disable the root login and enable the 'dash' user login
space(100)
print("Let's disable the 'root' user login and enable the 'dash' user login")
print("From now on, you will no longer be able to log in as the 'root' user")
confirm("Do you understand?")
space(1)
sleep(5)
#open file in read mode
file = open("/etc/ssh/sshd_config", "r")
replaced_content = ""
#looping through the file
for line in file:
    #stripping line break
    line = line.strip()
    #replacing the texts
    new_line = line.replace("PermitRootLogin yes", "PermitRootLogin no\nAllowUsers dash")
    #concatenate the new string and add an end-line break
    replaced_content = replaced_content + new_line + "\n"
#close the file
file.close()
#Open file in write mode
write_file = open("/etc/ssh/sshd_config", "w")
#overwriting the old file contents with the new/replaced content
write_file.write(replaced_content)
#close the file
write_file.close()
space(10)
confirm("Step one complete, server is ready for a reboot, do you have your new login details?")
space(2)
print("Rebooting in 10 seconds - ctrl-C now if you must")
sleep(10)
os.system("sudo reboot")
