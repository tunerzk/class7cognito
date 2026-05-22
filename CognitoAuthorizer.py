import { createPublicKey } from "crypto";

export const handler = async (event) => {
  try {
    let token = event.authorizationToken;

    if (token.startsWith("Bearer ")) {
      token = token.slice(7);
    }

    // Decode header to get kid
    const [headerB64] = token.split(".");
    const header = JSON.parse(Buffer.from(headerB64, "base64").toString());
    const kid = header.kid;

    // Fetch JWKS
    const jwksUrl = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_A5HfTWSE6/.well-known/jwks.json";
    const jwks = await fetch(jwksUrl).then(r => r.json());

    const key = jwks.keys.find(k => k.kid === kid);
    if (!key) throw new Error("Key not found");

    // Convert JWK → PEM
    const publicKey = createPublicKey({
      key: Buffer.from(
        `-----BEGIN PUBLIC KEY-----\n${Buffer.from(JSON.stringify(key)).toString("base64")}\n-----END PUBLIC KEY-----`
      ),
      format: "pem"
    });

    // Verify signature
    const verified = crypto.verify(
      "RSA-SHA256",
      Buffer.from(token.split(".").slice(0, 2).join(".")),
      publicKey,
      Buffer.from(token.split(".")[2], "base64")
    );

    if (!verified) throw new Error("Invalid signature");

    return generatePolicy("user", "Allow", event.methodArn);

  } catch (err) {
    console.error("AUTH ERROR:", err);
    return generatePolicy("unauthorized", "Deny", event.methodArn);
  }
};

function generatePolicy(principalId, effect, resource) {
  return {
    principalId,
    policyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "execute-api:Invoke",
          Effect: effect,
          Resource: resource
        }
      ]
    }
  };
}

   
