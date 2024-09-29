import os
import paramiko

def main():
    try:
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
        stdin, stdout, stderr = client.exec_command("nohup python3.12 sample-dvc/app.py > /dev/null 2>&1 &")
        if stderr:
            print("Error running deployment script: " + stderr.read().decode())
            return
        print(stdout.read().decode())
        client.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()