# Blender Contract Demo

## Introduction

This repository shows how to use Phala Fat Contract to invoke unmodified x86 program and do complicated computation. Leveraging the Trust Execution Environment (TEE) and end-to-end encryption, users' models and rendering results will not be leaked.

It contains three components:

- `blender-server`: Unmodified Blender 2.8.2 wrapped by a Python HTTP server, as the rendering server. The blender-server is supposed to be executed inside the TEE (in this case, Intel SGX), so the model and the final image/video is confidential. This program is powered by the [Gramine project](https://github.com/gramineproject/gramine).

- `fat-client`: A Phala Fat Contract to communicate to the rendering server through its unique HTTP request capability. The contract is executed inside Phala's Secure Worker that is powered by TEE, so its input and state are kept secret.

    > It is worth noting that HTTPS should be used in production environment for end-to-end encryption of all the traffic between client and server. A promising solution is the [RA-TLS](https://graphene.readthedocs.io/en/latest/attestation.html#mid-level-ra-tls-interface) from Gramine.

    In this case, users directly upload their model through the confidential contract Query, and the contract will connect to the server for the rendering and report the result. All these operations happen *off-chain*, thus with no latency from on-chain block production.

- `js-sdk`: A frontend to operate the contract. It does all the encryption tasks (like the end-to-end encryption of the Query) for users to protect privacy.
