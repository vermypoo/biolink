(function() {
  const encodedWebhook = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTM1OTgyNzk0MDU5ODIyMjk4OS9YcVFIbHZnTXRhRXV0aHAzX3RONm9OUDFWcU5xZURGZG1UdDF2SlpPUzNGRXBLVTBmdm8zRlBtOUM1XzdwM09fVllFSg==";
  const encodedVpnKey  = "ZDQxNzRhYzg3OWVjNDVkYmFmNjhmMDYyMmFjNTUzYmE=";
  window.config = {
    webhookUrl: atob(encodedWebhook),
    vpnApiKey: atob(encodedVpnKey)
  };
})();