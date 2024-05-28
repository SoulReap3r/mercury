Python
#!/usr/bin/env python3

import os
import pwd
import grp
import subprocess
import argparse

def main():
    # Handle help option and display usage information
    if "-h" in sys.argv or "--help" in sys.argv:
        print("""
        Network File System (NFS) Setup Tool

        Written by: Marcus Aurelius
          Roman Emperor (161-180 AD)

        A tool for configuring Network File System (NFS).

        Usage: nfs_setup [OPTION]

        Options:
          -h, --help     Show this help message.
          -s, --server   Configure server-side NFS.
          -c, --client   Configure client-side NFS mount.
        """)
        return

    # Print Network File System (NFS) title in ASCII art
    print("""
        .---.        .----.        .----.
       / _ \        |  __ \        |  __ \
      | | | |_   _  | |__) |_   _  | |__) |
      | |_| / | | | |  ___/ | | | | |  ___/
       \___/  |_| | | |     | |_| | | |
              |_____| |_|     |_____| |_|

                    Network File System (NFS)

                 Setup Tool

        Written by: Marcus Aurelius
          Roman Emperor (161-180 AD)

        A tool for configuring Network File System (NFS).
        """)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NFS Setup Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--server", action="store_true", help="Configure server-side NFS.")
    group.add_argument("-c", "--client", action="store_true", help="Configure client-side NFS mount.")
    args = parser.parse_args()

    # Get server IP (automatic or manual)
    use_auto_ip = input("Use automatic server IP detection (y/n) [default: y]: ").lower()
    if use_auto_ip not in ("y", "n"):
        use_auto_ip = "y"

    if use_auto_ip == "y":
        server_ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    else:
        server_ip = input("Enter the server's IP address: ")

    # Initialize share name and mount point
    share_name = ""
    mount_point = ""

    # Server-side setup
    if args.server:
        # Get share name (default to 'shared_data')
        share_name = input("Enter the desired share name (default: shared_data): ") or "shared_data"

        # Create shared directory if it doesn't exist
        share_path = os.path.join('/srv', share_name)
        if not os.path.exists(share_path):
            try:
                os.makedirs(share_path)
            except OSError as e:
                print(f"Error creating shared directory: {e}")
                return

        # Get current user and group information
        current_user = pwd.getpwuid(os.getuid()).pw_name
        current_group = grp.getgrgid(os.getgid()).gr_name

        # Ask for custom permissions or use defaults
        custom_permissions = input(
            f"Set custom permissions (y/n) [default: owned by {current_user}:{current_group}, 755]: "
        )
        if custom_permissions.lower() == "y":
            try:
                user_input = input("Enter desired owner (user:group): ")
                owner, group = user_input.split(":")
                uid = pwd.getpwnam(owner).pw_uid
                gid = grp.getgrnam(group).gr_gid
                permissions = input("Enter desired permissions (octal format, e.g., 755): ")
            except (ValueError, KeyError):
                print("Invalid input. Using default ownership and permissions.")
                uid = os.getuid()
                gid = os.getgid()
                permissions = "755"
        else:
            uid = os.getuid()
            gid = os.getgid()
            permissions = "755"

        # Construct and write the export line to /etc/exports
        export_line = f"{share_path} *(rw,sync,no_subtree_check,owner={uid}:{gid},mode={permissions})"
        try:
            with open("/etc/exports", "a") as f:
                f.write(export_line + "\n")
        except PermissionError:
            print("Error: Insufficient permissions. Run the script with sudo.")
            return

        # Restart NFS server
        try:
            subprocess.run(["sudo", "exportfs", "-ra"])
        except subprocess.CalledProcessError as e:
            print(f"Error exporting NFS shares: {e}")

    # Client-side setup logic (unchanged)
    # ... (client-side code using server_ip, share_name, mount_point)


if __name__ == "__main__":
    import sys
    main()