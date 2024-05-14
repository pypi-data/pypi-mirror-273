
import os
import subprocess

def uninstall():
    ''' This function will uninstall both deepnccl and deepncclplugin package,
        which installed by rpm/deb.
    '''

    # already installed by setup.py
    import distro
    os_version = distro.id()

    # if deepnccl installation overwrote previous installed libraries
    def restore():
        dst_path = "/usr/local/lib"
        if os.path.isfile(f'{dst_path}/libnccl.bak'):
            os.system(f'mv {dst_path}/libnccl.bak {dst_path}/libnccl.so')
            os.system(f'ln -s {dst_path}/libnccl.so {dst_path}/libnccl.so.2')
        if os.path.isfile(f'{dst_path}/libnccl-net.bak'):
            os.system(f'mv {dst_path}/libnccl-net.bak {dst_path}/libnccl-net.so.0.0.0')
            os.system(f'ln -s {dst_path}/libnccl-net.so.0.0.0 {dst_path}/libnccl-net.so.0')
            os.system(f'ln -s {dst_path}/libnccl-net.so.0.0.0 {dst_path}/libnccl-net.so')

    # uninstall rpm/deb packages
    if os_version.lower() == "ubuntu":
        subprocess.run(["dpkg", "--purge", "aiacc-nccl-plugin"])
        subprocess.run(["dpkg", "--purge", "deep-nccl"])
        restore()
    elif os_version.lower() == "centos":
        subprocess.run(["rpm", "--erase", "aiacc-nccl-plugin"])
        subprocess.run(["rpm", "--erase", "deep-nccl"])
        restore()
    else:
        pass
