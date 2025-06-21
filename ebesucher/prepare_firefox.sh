# Load Extension Firefox
# eBesucher Addon ID: {fef425dc-a60f-4484-954d-71ecf2544846}
set -e

rm -rf /etemp
mkdir /etemp
wget "https://addons.mozilla.org/firefox/downloads/latest/{fef425dc-a60f-4484-954d-71ecf2544846}/latest.xpi" -O /etemp/ebesucher.zip
cd /etemp
unzip ebesucher.zip
rm ebesucher.zip
sed -i "s/\"all_frames\": true/\"all_frames\": true, \"run_at\": \"document_start\"/g" manifest.json
sed -i "s/this.username = null/this.username = \"$USERNAME\"/g" popup/popupData.js
sed -i "s/this.acceptedCookies = false/this.acceptedCookies = true/g" popup/popupData.js
cat /patch_webgl.js >> ads/iframe.js
zip -r ebesucher.zip .
mv ebesucher.zip ebesucher.xpi
cd /

mkdir -p /etc/firefox/policies
echo '
{
  "policies": {
    "DisableAppUpdate": true,
    "RequestedLocales": "de,de-DE",
    "Preferences": {
      "xpinstall.signatures.required": {
        "Value": false
      }
    },
    "Extensions": {
      "Install": ["//etemp/ebesucher.xpi"]
    }
  }
}' > /etc/firefox/policies/policies.json

rm -rf ~/.mozilla ~/.cache
firefox-esr -headless -CreateProfile ebesucher # Generate Firefox Profiles
echo "Patch Firefox Profile"

for i in ~/.mozilla/firefox/*/; do
  # Network saving
  echo 'user_pref("network.captive-portal-service.enabled", false);' >> "$i/user.js"
  echo 'user_pref("network.connectivity-service.enabled", false);' >> "$i/user.js"
  echo 'user_pref("dom.push.enabled", false);' >> "$i/user.js"
  echo 'user_pref("extension.blocklist.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.malware.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.phishing.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.blockedURIs.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.block_dangerous", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.block_dangerous_host", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.block_potentially_unwanted", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.block_uncommon", false);' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.downloads.remote.url", "");' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.provider.mozilla.gethashURL", "");' >> "$i/user.js"
  echo 'user_pref("browser.safebrowsing.provider.mozilla.updateURL", "");' >> "$i/user.js"
  echo 'user_pref("privacy.trackingprotection.enabled", false);' >> "$i/user.js"
  echo 'user_pref("security.OCSP.enabled", 0);' >> "$i/user.js"
  echo 'user_pref("browser.search.update", false);' >> "$i/user.js"
  echo 'user_pref("app.update.auto", false);' >> "$i/user.js"
  echo 'user_pref("extensions.update.enabled", false);' >> "$i/user.js"
  echo 'user_pref("extensions.systemAddon.update.enabled", false);' >> "$i/user.js"
  echo 'user_pref("extensions.getAddons.cache.enabled", false);' >> "$i/user.js"
  echo 'user_pref("extensions.abuseReport.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.contentblocking.report.proxy.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.startup.page", 0);' >> "$i/user.js"
  echo 'user_pref("extensions.pocket.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.telemetry", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.showSponsored", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.topsites", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.snippets", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.system.topsites", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.discoverystream.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.discoverystream.endpoints", "");' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.section.topstories.options", "");' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.feeds.recommendationprovider", false);' >> "$i/user.js"
  echo 'user_pref("signon.management.page.breach-alerts.enabled", false);' >> "$i/user.js"
  echo 'user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.urlbar.addons.featureGate", false);' >> "$i/user.js"
  echo 'user_pref("browser.ping-centre.telemetry", false);' >> "$i/user.js"
  echo 'user_pref("security.certerrors.mitm.priming.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.topsites.contile.enabled", false);' >> "$i/user.js"
  echo 'user_pref("app.normandy.enabled", false);' >> "$i/user.js"
  echo 'user_pref("identity.fxaccounts.enabled", false);' >> "$i/user.js"
  echo 'user_pref("identity.fxaccounts.toolbar.enabled", false);' >> "$i/user.js"
  echo 'user_pref("identity.fxaccounts.toolbar.pxiToolbarEnabled.monitorEnabled", false);' >> "$i/user.js"
  echo 'user_pref("layout.spellcheckDefault", 0);' >> "$i/user.js"
  echo 'user_pref("iui.SpellCheckerUnderlineStyle", 0);' >> "$i/user.js"
  echo 'user_pref("media.gmp-manager.checkContentSignature", false);' >> "$i/user.js"
  echo 'user_pref("browser.urlbar.contextualSearch.enabled", false);' >> "$i/user.js"
  echo 'user_pref("browser.urlbar.quicksuggest.contextualOptIn.topPosition", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);' >> "$i/user.js"
  echo 'user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);' >> "$i/user.js"

  echo 'user_pref("devtools.console.stdout.content", true);' >> "$i/user.js"
  echo 'user_pref("devtools.debugger.remote-enabled", true);' >> "$i/user.js"
  echo 'user_pref("devtools.chrome.enabled", true);' >> "$i/user.js"
  echo 'user_pref("devtools.debugger.prompt-connection", false);' >> "$i/user.js"

  # Füge diese Zeilen zur Firefox-Profilkonfiguration hinzu
  echo 'user_pref("network.stricttransportsecurity.preloadlist", false);' >> "$i/user.js"
  echo 'user_pref("security.cert_pinning.enforcement_level", 0);' >> "$i/user.js"
  echo 'user_pref("security.enterprise_roots.enabled", true);' >> "$i/user.js"
  echo 'user_pref("security.ssl.enable_ocsp_must_staple", false);' >> "$i/user.js"
  echo 'user_pref("security.ssl.enable_ocsp_stapling", false);' >> "$i/user.js"
  echo 'user_pref("security.ssl.enable_ocsp_response_strict", false);' >> "$i/user.js"
  echo 'user_pref("security.ssl.require_safe_negotiation", false);' >> "$i/user.js"
  echo 'user_pref("security.insecure_connection_text.enabled", false);' >> "$i/user.js"
done
