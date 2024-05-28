import os
import pwd
import grp
import subprocess


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

    # Print Network F S title in ASCII art
    print("""
        .---.        .----.        .----.
       / _ \        |  __ \        |  __ \
      | | | |_   _  | |__) |_   _  | |__) |
      | |_| / | | | |  ___/ | | | | |  ___/
       \___/  |_| | | |     | |_| | | |
              |_____| |_|     |_____| |_|

                    Network F S

                 Setup Tool

        Written by: Marcus Aurelius
          Roman Emperor (161-180 AD)

        A tool for configuring Network File System (NFS).
        """)

    # Server or client setup choice (using argparse for cleaner input handling)
    import argparse

    parser = argparse.ArgumentParser(description="NFS Setup Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--server", action="store_true", help="Configure server-side NFS.")
    group.add_argument("-c", "--client", action="store_true", help="Configure client-side NFS mount.")

    args = parser.parse_args()

    # Server IP (automatic or manual)
    use_auto_ip = input("Use automatic server IP detection (y/n) [default: y]: ").lower()
    if use_auto_ip not in ("y", "n"):
        use_auto_ip = "y"  # Default to automatic

    if use_auto_ip == "y":
        server_ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    else:
        server_ip = input("Enter the server's IP address: ")

    # Common variables (initialize with empty values)
    share_name = ""
    mount_point = ""

    # Server-side setup logic
    if args.server:
        # Prompt user for share name, accepting default on enter
        share_name = input("Enter the desired share name (default: tester_share): ") or "tester_share"

        # Ask for additional options (optional)
        custom_permissions = input("Set custom permissions (y/n) [default: 755]: ")
        if custom_permissions.lower() == "y":
            try:
                permissions = int(input("Enter desired permissions (octal format): "))
            except ValueError:
                print("Invalid permission format. Using default (755).")
                permissions = 0o755
        else:
            permissions = 0o755  # Default permissions

        # Server-side configuration steps
        # ... (rest of your server-side code using server_ip, share_name, permissions)

    # Client-side setup logic
    else:
        # Get user input for share name (optional, default to server name)
        share_name = input("Enter the desired share name (default: {}): ".format(server_ip)) or server_ip

        # Ask for mount point (optional, default to specific directory)
        custom_mount_point = input("Set custom mount point (y/n) [default: /path/to/mount/point]: ")
        if custom_mount_point.lower() == "y":
            mount_point = input("Enter desired mount point directory: ")
        else:
            mount_point = "/path/to/mount/point"

        # Client-side configuration steps
        # ... (rest of your client-side code using server_ip, share_name, mount_point)


if __name__ == "__main__":
    import sys

    main()