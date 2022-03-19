# Model detection
pip3 uninstall keras -y
pip3 uninstall keras-nightly -y
pip3 uninstall keras-Preprocessing -y
pip3 uninstall keras-vis -y
pip3 uninstall tensorflow -y
pip3 uninstall h5py -y
pip3 install tensorflow-gpu==1.13.1
pip3 install keras==2.0.8
pip3 install h5py==2.10.0

# RPisocket
pip3 install websocket-client