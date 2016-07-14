export ENCRYPTION_LABEL="33e9f3ccc52a"
export ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
export ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
export ENCRYPTED_KEY="${!ENCRYPTED_KEY_VAR}"
export ENCRYPTED_IV="${!ENCRYPTED_IV_VAR}"
#openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in nyuad-hpc-module-configs-deploy.enc -out nyuad-hpc-module-configs-deploy -d
