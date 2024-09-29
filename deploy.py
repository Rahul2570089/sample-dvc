import os
import paramiko

def main():
    ec2_host = os.getenv('EC2_IP')
    ec2_user = os.getenv('EC2_USER')
    ec2_key = os.getenv('EC2_SECRET_KEY')
    private_key_path = "/tmp/ec2_key"
    with open(private_key_path, 'w') as f:
        f.write(ec2_key)
    os.chmod(private_key_path, 0o600)
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ec2_host, username=ec2_user, pkey=key)
    stdin, stdout, stderr = client.exec_command("echo -e \"#!/bin/bash\ncd sample-dvc/\nnohup python3.12 app.py > /dev/null 2>&1 &\" > deploy.sh")
    stdin, stdout, stderr = client.exec_command("sh deploy.sh")
    if stderr.read().decode().strip():
        print("Error running deployment script: " + stderr.read().decode())
        return
    print(stdout.read().decode())
    client.close()



if __name__ == "__main__":
    main()