//! Native PARISPCFIX sessions must never fall back to an unprotected channel.

const UNPROTECTED: &str =
    "PARISPCFIX requires an encrypted connection. Check the ID server and public key settings.";
const UNVERIFIED: &str =
    "PARISPCFIX could not verify the remote identity. Check the ID server public key.";

pub fn check_outgoing(encrypted: bool, verified_identity: bool) -> Result<(), &'static str> {
    check_incoming(encrypted)?;
    if !verified_identity {
        return Err(UNVERIFIED);
    }
    Ok(())
}

pub fn check_incoming(encrypted: bool) -> Result<(), &'static str> {
    if !encrypted {
        return Err(UNPROTECTED);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn outgoing_rejects_plaintext_even_with_a_known_identity() {
        assert!(super::check_outgoing(false, false).is_err());
        assert!(super::check_outgoing(false, true).is_err());
    }

    #[test]
    fn outgoing_requires_verified_identity_even_on_an_encrypted_transport() {
        assert!(super::check_outgoing(true, false).is_err());
        assert!(super::check_outgoing(true, true).is_ok());
    }

    #[test]
    fn incoming_requires_encryption_before_login() {
        assert!(super::check_incoming(false).is_err());
        assert!(super::check_incoming(true).is_ok());
    }
}
