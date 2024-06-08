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
    hosts_entry = f"127.0.0.1 {common_name}\n"
    run_command(f"echo '{hosts_entry}' | sudo tee -a /etc/hosts")

    # Generate private key for the server
    run_command(f"openssl genrsa -aes256 -passout pass:{passphrase} -out server_key.pem 2048")

    # Generate Certificate Signing Request (CSR)
    csr_command = (
        f"openssl req -new -key server_key.pem -out server_csr.pem "
        f"-subj '/C=US/ST=California/L=Monterey/O=CSUMB/OU=CST311/CN={common_name}' -passin pass:{passphrase}"
    )
    run_command(csr_command)

    # Generate certificate using the CA
    run_command(f"openssl x509 -req -in server_csr.pem -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -out server_cert.pem -days 365 -sha256 -passin pass:{passphrase}")

    print("Certificate generation complete. Files generated:")
    print("  server_key.pem")
    print("  server_csr.pem")
    print("  server_cert.pem")

if __name__ == "__main__":
    main()