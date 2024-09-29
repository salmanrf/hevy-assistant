import React, { createContext, useEffect, useState } from "react"
import { io, type Socket } from "socket.io-client"

import { fetchSession } from "~api/auth"
import { CONFIG } from "~config"

export type SocketContextValues = {
  client: Socket
}

export type ProviderProps = {
  children: React.ReactNode
}

export const SocketContext = createContext<SocketContextValues>({
  client: null
})

function SocketContextProvider({ children }: ProviderProps) {
  const [sioClient, setSioClient] = useState<Socket>(null)

  useEffect(() => {
    init()
  }, [])

  async function init() {
    const session = await fetchSession()

    const socket = io(CONFIG.BACKEND_URL, {
      auth: { ...session }
    })

    socket.on("connect", async () => {
      setSioClient(socket)
    })
  }

  function set(s: Socket) {
    setSioClient(s)
  }

  return (
    <SocketContext.Provider value={{ client: sioClient }}>
      {children}
    </SocketContext.Provider>
  )
}

export default SocketContextProvider
