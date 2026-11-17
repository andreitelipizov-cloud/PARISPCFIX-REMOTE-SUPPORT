use hbb_common::{anyhow::anyhow, config, ResultType};

#[cfg(all(feature = "parispcfix-client", feature = "parispcfix-admin"))]
compile_error!("Build the PARISPCFIX client and administrator editions separately.");

pub mod security;

pub const LANGUAGES: &[&str] = &["ru", "ro", "uk", "en", "fr"];

pub fn app_name() -> &'static str {
    if cfg!(feature = "parispcfix-client") {
        "PARISPCFIX-CLIENT"
    } else if cfg!(feature = "parispcfix-admin") {
        "PARISPCFIX-ADMIN"
    } else {
        "PARISPCFIX"
    }
}

pub fn initialize() -> ResultType<()> {
    *config::APP_NAME
        .write()
        .map_err(|_| anyhow!("Unable to initialize the PARISPCFIX application identity"))? =
        app_name().to_owned();

    let mut local = config::DEFAULT_LOCAL_SETTINGS
        .write()
        .map_err(|_| anyhow!("Unable to initialize PARISPCFIX local defaults"))?;
    local.insert("theme".to_owned(), "dark".to_owned());
    local.insert("lang".to_owned(), "ru".to_owned());
    drop(local);

    let mut hard = config::HARD_SETTINGS
        .write()
        .map_err(|_| anyhow!("Unable to initialize the PARISPCFIX edition"))?;
    if cfg!(feature = "parispcfix-client") {
        hard.insert("conn-type".to_owned(), "incoming".to_owned());
    } else if cfg!(feature = "parispcfix-admin") {
        hard.insert("conn-type".to_owned(), "outgoing".to_owned());
    }
    drop(hard);

    config::BUILTIN_SETTINGS
        .write()
        .map_err(|_| anyhow!("Unable to initialize PARISPCFIX presentation defaults"))?
        .insert("hide-powered-by-me".to_owned(), "Y".to_owned());
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn edition_uses_its_own_application_identity() {
        assert!(super::app_name().starts_with("PARISPCFIX"));
        #[cfg(feature = "parispcfix-client")]
        assert_eq!(super::app_name(), "PARISPCFIX-CLIENT");
        #[cfg(feature = "parispcfix-admin")]
        assert_eq!(super::app_name(), "PARISPCFIX-ADMIN");
    }

    #[test]
    fn five_requested_languages_are_available() {
        assert_eq!(super::LANGUAGES, ["ru", "ro", "uk", "en", "fr"]);
    }
}
