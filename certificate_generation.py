import subprocess

def run_command(command):
    """Run a shell command and check for errors."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
    return result

def main():
    # Prompt for common name
    common_name = input("Enter the common name for the chat server (default: tpa4.chat.test): ") or "tpa4.chat.test"
    passphrase = "CST311"
    
    # Write the common name to a txt file
    with open("common_name.txt", "w") as file:
        file.write(common_name)
    
    # Add IP addresses and common name to /etc/hosts
    hosts_entry = f"10.0.2.2/24 {common_name}\n"
    run_command(f"echo '{hosts_entry}' | sudo tee -a /etc/hosts")

    # Generate private key for the server
    run_command(f"openssl genrsa -aes256 -passout pass:{passphrase} -out server_key.pem 2048")

    # Generate Certificate Signing Request (CSR)
    csr_command = (
        f"openssl req -new -key server_key.pem -out server_csr.pem "
        f"-subj '/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}' -passin pass:{passphrase}"
    )
    run_command(csr_command)

    # Check if CA certificate and key exist, generate if they don't
    try:
        with open("ca_cert.pem", "r") as f:
            #print("CA certificate exists.")
            print()
    except FileNotFoundError:
        #print("CA certificate not found, generating new one.")
        # Generate CA private key
        run_command(f"openssl genrsa -aes256 -passout pass:{passphrase} -out ca_key.pem 2048")
        # Generate CA certificate
        run_command(f"openssl req -x509 -new -nodes -key ca_key.pem -sha256 -days 365 -out ca_cert.pem -subj '/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN=ca' -passin pass:{passphrase}")

    # Generate certificate using the CA
    run_command(f"openssl x509 -req -in server_csr.pem -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -out chatserver-cert.pem -days 365 -sha256 -passin pass:{passphrase}")


if __name__ == "__main__":
    main()
