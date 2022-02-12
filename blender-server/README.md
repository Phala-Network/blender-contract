# Environment Setup

## SGX Driver and Gramine Installation

Ubuntu 20.04 is recommended.

Refer to Gramine's [tutorial](https://graphene.readthedocs.io/en/latest/quickstart.html) for SGX driver and Gramine installation.

> We strongly recommend to use Linux kernel >=5.11 for the in-kernel SGX driver. `/dev/sgx_enclave` should be presented for DCAP-compatible devices if you successfully install the driver (`/dev/isgx` for legacy EPID devices).

## Dependencies Installation

Install the Blender dependencies with

```bash
sudo apt install -y libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1
```

## Build

Build the SGX version with

```bash
make SGX=1 SGX_SIGNER_KEY=/path/to/your/enclave-key.pem
```

or a normal non-SGX version with

```bash
make SGX=0
```

## Run

Run the SGX version with

```bash
gramine-sgx ./python scripts/blender-server.py server_port
```

or a non-SGX version with

```bash
gramine-direct ./python scripts/blender-server.py server_port
```

## Quick Test

Get a .blend model for testing (like https://github.com/gramineproject/gramine/blob/master/CI-Examples/blender/data/scenes/simple_scene.blend).

```bash
curl -X PUT --upload-file /path/to/your.blend http://localhost:[server_port]
```

You should see the rendering logs from Blender.
