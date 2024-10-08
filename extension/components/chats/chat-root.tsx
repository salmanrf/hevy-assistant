import { useEffect, useState } from "react"

import ChatInput from "~components/chats/chat-input"
import ChatMessage from "~components/chats/chat-message"
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

  function onMessageSubmit(content: string, cb?: () => void) {
    console.log("content", content)
  }

  useEffect(() => {}, [])

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
        Hevy Assistant
      </div>
      <div
        id="chat-container"
        style={{
          boxShadow: isActive
            ? "rgba(0, 0, 0, 0.19) 0px 0px 10px"
            : "rgba(0, 0, 0, 0.19) 0px 6px 10px"
        }}>
        <div id="chat-messages-container"></div>
        <ChatInput onSubmit={onMessageSubmit} />
      </div>
    </div>
  )
}

export default ChatRoot
