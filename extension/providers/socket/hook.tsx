import { useContext } from "react"

import { SocketContext } from "~providers/socket/context"

function useSocket() {
  const socket = useContext(SocketContext)

  return socket
}

export default useSocket
