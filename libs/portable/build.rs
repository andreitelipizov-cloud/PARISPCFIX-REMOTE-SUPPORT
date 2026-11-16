fn main() {
    println!("cargo:rerun-if-env-changed=PARISPCFIX_EDITION");
    #[cfg(windows)]
    {
        use std::io::Write;
        let mut res = winres::WindowsResource::new();
        res.set_icon("../../res/icon.ico")
            .set_language(winapi::um::winnt::MAKELANGID(
                winapi::um::winnt::LANG_ENGLISH,
                winapi::um::winnt::SUBLANG_ENGLISH_US,
            ))
            .set_manifest_file("../../res/manifest.xml");
        if let Ok(edition) = std::env::var("PARISPCFIX_EDITION") {
            if edition == "client" || edition == "admin" {
                res.set_icon("../../flutter/windows/runner/resources/parispcfix.ico");
                res.set("CompanyName", "PARISPCFIX")
                    .set("ProductName", "PARISPCFIX Remote Support")
                    .set("FileDescription", "PARISPCFIX Remote Support installer")
                    .set("OriginalFilename", &format!("PARISPCFIX-{}-install.exe", edition.to_uppercase()));
            }
        }
        match res.compile() {
            Err(e) => {
                write!(std::io::stderr(), "{}", e).unwrap();
                std::process::exit(1);
            }
            Ok(_) => {}
        }
    }
}
