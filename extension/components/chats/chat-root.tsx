import { useEffect, useState } from "react"

import { useSocket } from "~providers"

function ChatRoot() {
  const { client: socket } = useSocket()

  const [isActive, setIsActive] = useState(false)

  useEffect(() => {
    if (socket) {
    }

    return () => {
      if (socket) {
      }
    }
  }, [socket])

  function toggleIsActive() {
    setIsActive((ia) => !ia)
  }

  return (
    <div
      id="hevy-assistant-chat-root"
      style={{
        transform: `translateY(${isActive ? "-100%" : "-38px"})`
      }}>
      <div
        id="chat-toggler"
        onClick={toggleIsActive}
        style={{
          boxShadow: isActive
            ? "rgba(0, 0, 0, 0.19) 0px 0px 10px 2px"
            : "rgba(0, 0, 0, 0.19) 0px 6px 10px",
          borderRadius: isActive ? "6px 6px 0 0 " : "6px"
        }}>
        Assistant Chat
      </div>
      <div
        id="chat-container"
        style={{
          boxShadow: isActive
            ? "rgba(0, 0, 0, 0.19) 0px 0px 10px"
            : "rgba(0, 0, 0, 0.19) 0px 6px 10px"
        }}></div>
    </div>
  )
}

export default ChatRoot
