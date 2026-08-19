Run the following code in a javascript console to generate a public and private
encryption key.

```javascript
async function generateKey() {
  try {
    const keyPair = await window.crypto.subtle.generateKey(
      {
        name: "RSA-OAEP",
        modulusLength: 2048, // Can be 2048, 3048, or 4096
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256",
      },
      true,
      ["encrypt", "decrypt"]
    );
    return keyPair;
  } catch (error) {
    console.error("Key generation failed:", error);
  }
}

const key = await generateKey();
const pub = await window.crypto.subtle.exportKey("jwk", key.publicKey);
const priv = await window.crypto.subtle.exportKey("jwk", key.privateKey);

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

downloadJSON(pub, "public_key.json");
downloadJSON(priv, "private_key.json");
```

Copy the public key to your repository. It is loaded on the
[submission page](./submit.html) and used for encryption of arbitrary text (in
our case, email-addresses).

Safeguard the private key. It is to be used for decryption. The website offers
a [decryption page](./decrypt.html) where you can load the key and decrypt text
locally.
