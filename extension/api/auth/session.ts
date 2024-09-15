import { CONFIG } from "~config"
import type { HevyUser } from "~type"

async function fetchSession(): Promise<HevyUser> {
  try {
    // @ts-ignore
    const authTokenCookie = await cookieStore.get(CONFIG.AUTH_TOKEN_COOKIE_KEY)
    const authToken = authTokenCookie.value

    const res = await fetch(`${CONFIG.HEVY_API_URL}/user/account`, {
      headers: {
        accept: "application/json, text/plain, */*",
        "accept-language": "en-US,en-GB;q=0.9,en;q=0.8,id;q=0.7",
        "auth-token": authToken,
        "hevy-platform": "web",
        "sec-ch-ua":
          '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-api-key": "shelobs_hevy_web"
      },
      referrer: "https://hevy.com/",
      referrerPolicy: "strict-origin-when-cross-origin",
      body: null,
      method: "GET",
      mode: "cors",
      credentials: "omit"
    })

    const parsed = await res.json()

    const data: HevyUser = {
      hevy_user_id: parsed["id"],
      email: parsed["email"],
      username: parsed["username"],
      birthday: parsed["birthday"],
      sex: parsed["sex"]
    }

    return data
  } catch (error) {
    console.log("Error at fetch session", error)

    throw new Error("Unable to fetch session")
  }
}

export default fetchSession
