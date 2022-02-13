#![cfg_attr(not(feature = "std"), no_std)]
extern crate alloc;

use pink_extension as pink;

#[pink::contract(env=PinkEnvironment)]
mod fat_client {

    use super::pink;
    use alloc::format;
    use alloc::string::String;
    use alloc::vec::Vec;
    use pink::{http_get, PinkEnvironment};

    #[ink(storage)]
    pub struct FatClient {
        render_server: String,
    }

    impl FatClient {
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                render_server: Default::default(),
            }
        }

        #[ink(message)]
        pub fn set_render_server(&mut self, render_server: String) {
            self.render_server = render_server;
        }

        #[ink(message)]
        pub fn get_render_server(&self) -> String {
            self.render_server.clone()
        }

        #[ink(message)]
        pub fn render(&self, file: String) -> (u16, Vec<u8>) {
            let path = String::from("render");
            let url = format!("{}/{}?filename={}", self.render_server, path, file);
            let response = http_get!(url);
            (response.status_code, response.body)
        }
    }
}
