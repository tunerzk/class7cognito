Cognito ClickOps Lab — User Authentication (No Federation)
We will do Federation in SEIR-II

Objective---> “We are not building a login page. We are building an identity system that issues tokens.”

Students will:

    Create a User Pool
    Enable login with:
        username
        email
        phone number
    Enforce MFA
    Create and authenticate a user
    Use the JWT to call your REST API
   <img width="1339" height="474" alt="image" src="https://github.com/user-attachments/assets/4d4cf09d-db52-468a-a35b-73eda1516bab" />
 

Updated Flow: Client → WAF → API Gateway (Cognito Authorizer) → Lambda


Task 1 — Create Cognito User Pool
  Navigation
  
    AWS Console → Cognito
    Click User Pools
    Click Create user pool


Step-by-Step Configuration


1. Sign-in Options

Select: “We allow multiple identity inputs. Real systems don’t force one.”

        ✔ Username
        ✔ Email
        ✔ Phone number

2. Password Policy

Keep default or slightly stronger:

        Min 8 characters
        Numbers + symbols

3. MFA Configuration---> “MFA is not optional in real systems.”

Set: Required MFA

        MFA Types:
        ✔ SMS
        ✔ TOTP (Authenticator app)

4. User Account Recovery

        Enable:
        ✔ Email
        ✔ Phone

5. Attributes

Set required:

        ✔ email
        ✔ phone_number

6. App Client

Create one:

Name: chewbacca-client

Disable: ----> ❌ Client secret

Why? Client secret complicates API usage. We keep it simple.

Click Create
<img width="1211" height="525" alt="image" src="https://github.com/user-attachments/assets/78e535a2-e601-4aad-8deb-e6f923d6bfb5" />


Task 2 — Create a User

Inside User Pool:

        Go to Users
        Click Create user

Fill:

        Username: lizzo1
        Email: student1@lizzo.com
        Phone: +1XXXXXXXXXX

Set password manually: --->  Permanent password
“We are skipping email verification to move faster. We will return to it later"
<img width="1397" height="317" alt="image" src="https://github.com/user-attachments/assets/66945e7f-91ed-4718-a62d-f3c4b68695b0" />


Task 3 — Enable MFA for User

Inside User:
        Click user
        Set MFA:

        ✔ Enable MFA
        ✔ Choose:

SMS OR Authenticator app
<img width="894" height="695" alt="cogmfasetup" src="https://github.com/user-attachments/assets/a3f004d3-5074-45f6-8715-af5850c142e1" />


If TOTP:
    Scan QR code with:
        Google Authenticator
        or Microsoft Authenticator
<img width="1152" height="584" alt="cogsigninapprove" src="https://github.com/user-attachments/assets/e7a2ed45-7a86-40a6-a43e-9b78f344c48b" />


 A secret hash is only used when your Cognito App Client has a client secret enabled.
You would use it only when:
--You have a confidential client (server‑side app, backend service, etc.)
--You want to prevent someone from abusing your App Client ID
--You want Cognito to require a second factor (the secret) during authentication
--You do NOT use a secret hash for browser apps, mobile apps, or anything running on the client side.
<img width="1196" height="392" alt="cognitosecretproof" src="https://github.com/user-attachments/assets/13d51d25-07de-46bf-85af-7ccb5fddd45d" />



Task 4 — Get JWT Token (CLI Method)
This isn't easy. Let's go slow.

Use AWS CLI:

        aws cognito-idp initiate-auth \
          --auth-flow USER_PASSWORD_AUTH \
          --client-id <CLIENT_ID> \
          --auth-parameters USERNAME=student1,PASSWORD=YourPassword,SECRET_HASH=
<img width="1036" height="265" alt="image" src="https://github.com/user-attachments/assets/e7ca7b81-a0ef-4fa6-b48f-8379827f33ce" />


If MFA is required → challenge returned

Then run:

        aws cognito-idp respond-to-auth-challenge \
          --client-id <CLIENT_ID> \
          --challenge-name SMS_MFA \
          --challenge-responses USERNAME=student1,SMS_MFA_CODE=123456 \
          --session <SESSION>
<img width="1538" height="387" alt="image" src="https://github.com/user-attachments/assets/e7b0d39e-c373-4074-95c6-c233a15c26e7" />


Result:

You get:

        {
          "AuthenticationResult": {
            "IdToken": "...",
            "AccessToken": "...",
            "RefreshToken": "..."
          }
        }

Use: AccessToken

Task 5 — Create API Gateway Authorizer
<img width="1407" height="300" alt="image" src="https://github.com/user-attachments/assets/956113ba-3b11-4350-8b45-fdf366fac85b" />


Go to API Gateway (REST API)--> Authorizers → Create New ---> Type: Cognito ---> 

Configure:

        Name:chewbacca-authorizer
        Cognito User Pool: → Select your pool
        Token Source: Authorization

Task 6 — Attach Authorizer to Methods
<img width="792" height="570" alt="image" src="https://github.com/user-attachments/assets/56352964-a05f-47ee-afb2-7e55bf2077ad" />


For /python and For /node:

    Method Request --> Authorization: Cognito Authorizer
<img width="1065" height="501" alt="image" src="https://github.com/user-attachments/assets/126a4785-f32d-4164-ad50-a0e426a3e909" />

 
Task 7 — Deploy API (Again!)

👉 REST API requires redeploy
Actions → Deploy API → prod

Task 8 — Test

Without Token ---> 

        curl https://<api>/prod/python 
<img width="1378" height="167" alt="image" src="https://github.com/user-attachments/assets/800f457c-da92-4c70-acf2-511853ded9e6" />


 --> 401 Unauthorized
 

With Token -->  

        curl https://<api>/prod/python \
          -H "Authorization: <ACCESS_TOKEN>" 
<img width="1508" height="178" alt="image" src="https://github.com/user-attachments/assets/32bf7ee7-41f5-4c86-b63f-ab29715ef719" />
  
        → 200 OK


Task 9 — Verify Behavior

1. Did Lambda run when no token?
2. Where was request blocked?
3. What changed in event?

Final Explanation

    What Cognito does?
    What API Gateway does?
    What MFA adds?
    Why AccessToken matters?
