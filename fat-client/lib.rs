#![cfg_attr(not(feature = "std"), no_std)]
extern crate alloc;

use pink_extension as pink;

#[pink::contract(env=PinkEnvironment)]
mod fat_client {

    use super::pink;
    use alloc::format;
    use alloc::string::String;
    use alloc::vec::Vec;
    use pink::chain_extension::HttpRequest;
    use pink::PinkEnvironment;

    #[ink(storage)]
    pub struct FatClient {
        render_server: String,
    }

    impl FatClient {
        #[ink(constructor)]
        pub fn new(render_server: String) -> Self {
            Self { render_server }
        }

        #[ink(message)]
        pub fn upload_blend_model(&self, data: Vec<u8>) -> (u16, Vec<u8>) {
            let tmp_filename = String::from("input.blend");
            let url = format!("{}/{}", self.render_server, tmp_filename);
            let request = HttpRequest {
                url,
                method: "PUT".into(),
                headers: Default::default(),
                body: data,
            };

            let response = self.env().extension().http_request(request);
            (response.status_code, response.body)
        }
    }
}
